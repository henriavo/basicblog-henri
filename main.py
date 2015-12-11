#!/usr/bin/env python
#
#
import webapp2
import os
import jinja2
import DbDefenitions
import Helper

from google.appengine.ext import db

class NewPostHandler(Helper.Handler):
	def get(self):
		self.renderIt("newpost.html")

	def post(self):
		theSubject = self.request.get("subject")
		thePost = self.request.get("content")

		if (not theSubject.strip() or not thePost.strip()):
			error = "subject and content, please!"
			self.renderIt("newpost.html", error=error, subject=theSubject, content=thePost)
		else:
			post = DbDefenitions.BlogEntry(subject=theSubject, blog=thePost)

			post.put()
			
			print "THE ID: " + str(post.key().id())
			theBlogId = str(post.key().id())

			self.redirect("/blog/%s" % theBlogId)

class PostFetchHandler(Helper.Handler):
	def get(self, post_id):
		p = DbDefenitions.BlogEntry.get_by_id(long(post_id))
		if p:
			posts =[p]
			self.renderIt("mainpage.html", posts=posts)



class MainPageHandler(Helper.Handler):
	def get(self):
		posts = db.GqlQuery("SELECT * FROM BlogEntry" 
							" ORDER BY created DESC")
		
		self.renderIt("mainpage.html", posts=posts)


app = webapp2.WSGIApplication([
	('/blog/newpost', NewPostHandler),
	('/blog', MainPageHandler),
	('/blog/([0-9]+)', PostFetchHandler)
], debug=True)
