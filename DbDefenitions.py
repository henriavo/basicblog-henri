from google.appengine.ext import db

class BlogEntry(db.Model):
	subject = db.StringProperty(required=True)
	blog = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)