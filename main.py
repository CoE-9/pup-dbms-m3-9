import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Thesis(ndb.Model):
	year = ndb.StringProperty(indexed=True)
	thesis_title = ndb.StringProperty(indexed=True)
	abstract = ndb.StringProperty(indexed=True)
	adviser = ndb.StringProperty(indexed=True)
	section = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render())

    def post(self):
		thesis = Thesis()
		thesis.year = self.request.get('year')
		thesis.thesis_title = self.request.get('thesis_title')
		thesis.abstract = self.request.get('abstract')
		thesis.adviser = self.request.get('adviser')
		thesis.section = self.request.get('section')
		thesis.put()

class ThesisCpE(webapp2.RequestHandler):
	 
	def get(self):
        #get all student
		thesis = Thesis.query().order(-Thesis.date).fetch()
		thesis_list = []

		for thesis in thesis:
			thesis_list.append({
                    'id' : thesis.key.id(),
                    'Year' : thesis.year,
                    'Title' : thesis.thesis_title,
                    'Abstract' : thesis.abstract,
                    'Adviser' : thesis.adviser,
                    'Section' : thesis.section
                })
        #return list to client
		response = {
		'result' : 'OK',
		'data' : thesis_list
        }
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

	def post(self):

		thesis = Thesis()
		thesis.year = self.request.get('year')
		thesis.thesis_title = self.request.get('thesis_title')
		thesis.abstract = self.request.get('abstract')
		thesis.adviser = self.request.get('adviser')
		thesis.section = self.request.get('section')
		thesis.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
		    'result' : 'OK',
		    'data': {
		        'id' : thesis.key.id(),
		            'year' : thesis.year,
		            'thesis_title' : thesis.thesis_title,
		            'abstract' : thesis.abstract,
		            'adviser' : thesis.adviser,
		            'section' : thesis.section
		    }
		}
		self.response.out.write(json.dumps(response))

class DeleteInfo(webapp2.RequestHandler):
    def get(self, studentId):
        d = Thesis.get_by_id(int(studentId))
        d.key.delete()
        self.redirect('/')

app = webapp2.WSGIApplication([
('/api/thesis', ThesisCpE),
('/thesis/delete/(.*)', DeleteInfo),
('/home', MainPageHandler),
('/', MainPageHandler)
], debug=True)