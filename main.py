#!/usr/bin/env python
#
#
import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
																autoescape=True)


class BlogEntry(db.Model):
	subject = db.StringProperty(required=True)
	blog = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kwArgs):
		self.response.write(*a, **kwArgs)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def renderIt(self, template, **kwArgs):
		self.write(self.render_str(template, **kwArgs))

class NewPostHandler(Handler):
	def get(self):
		self.renderIt("newpost.html")

	def post(self):
		theSubject = self.request.get("subject")
		thePost = self.request.get("content")

		if (not theSubject.strip() or not thePost.strip()):
			error = "subject and content, please!"
			self.renderIt("newpost.html", error=error, subject=theSubject, content=thePost)
		else:
			post = BlogEntry(subject=theSubject, blog=thePost)

			post.put()
			
			print "THE ID: " + str(post.key().id())
			theBlogId = str(post.key().id())

			self.redirect("/blog/%s" % theBlogId)

class PostHandler(Handler):
	def get(self, post_id):
		p = BlogEntry.get_by_id(long(post_id))
		if p:
			posts =[p]
			self.renderIt("mainpage.html", posts=posts)



class MainPageHandler(Handler):
	def get(self):
		posts = db.GqlQuery("SELECT * FROM BlogEntry" 
							" ORDER BY created DESC")
		
		self.renderIt("mainpage.html", posts=posts)


app = webapp2.WSGIApplication([
	('/blog/newpost', NewPostHandler),
	('/blog', MainPageHandler),
	('/blog/([0-9]+)', PostHandler)
], debug=True)
