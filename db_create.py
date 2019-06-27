from app import db
from app import Url

db.create_all()

#
db.session.add(Url("www.atomicgrowth.co/blog",clicks=0))

db.session.commit()