from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_table import Table, Col
from flask import Markup
from flask_heroku import Heroku



app = Flask(__name__)
# app.config["SECRET_KEY"] = "goblicon"
app.config.['SSQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Daylight99!@localhost/teensypy'
heroku = Heroku(app)
db = SQLAlchemy(app)

# TODO: User system to save shorten urls
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self,username,email):
#             self.username=username
#             self.email=email
#
#     def __repr__(self):
#         return "<User %r>" % self.username

# Model for DB
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fattyurl = db.Column(db.String, nullable=False)
    clicks = db.Column(db.Integer, nullable=False)

    def __init__(self,fattyurl, clicks):
            self.fattyurl = fattyurl
            self.clicks=clicks

    def __repr__(self):
        return "<Url %r>" % self.id

# Form class
class UrlForm(FlaskForm):
    longurl = StringField('Fatty Url', validators=[DataRequired()])

# Table Class
class Results(Table):
    id = Col('Id', show=True)
    fattyurl = Col('Fatty Url')
    clicks = Col('Clicks')

# Last 5 entries
def lastfive():
    query = Url.query

# Routing
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()
    tabledata = Url.query.all()
    tabledata = reversed(tabledata)
    table = Results(tabledata)
    table.border =True
    table.classes =".table"
    if form.validate_on_submit():
        newurl=Url(form.longurl.data, 0)

        db.session.add(newurl)
        db.session.commit()
        newid=Url.query.order_by(Url.id.desc()).first()
        tnzyurl= "https://tnzy.io/"+str(newid.id)

        flash(Markup('Your Tnzy.io url is <a href="'+ tnzyurl +'">'+tnzyurl+'</a>'))
        return redirect('/')
    return render_template('index.html', form=form, table=table)

@app.route('/<int:url_id>')
def forward_url(url_id):
    furl = Url.query.get(url_id)
    furl.clicks += 1
    db.session.commit()
    return redirect("http://"+furl.fattyurl, code=302)

if __name__== "__main__":
    app.run()


