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

class MainPageHandler(Handler):
	def get(self):
		self.renderIt("mainpage.html")

app = webapp2.WSGIApplication([
	('/blog/newpost', NewPostHandler),
	('/blog', MainPageHandler)
], debug=True)
