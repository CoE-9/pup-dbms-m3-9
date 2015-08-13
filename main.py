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
	title = ndb.StringProperty(indexed=True)
	abstract = ndb.StringProperty(indexed=True)
	adviser = ndb.StringProperty(indexed=True)
	section = ndb.StringProperty(indexed=True)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render())

class POSTapiThesis(webapp2.RequestHandler):
	def post(self):
		thesis = Thesis()
		thesis.year = self.request.get('year')
		thesis.title = self.request.get('title')
		thesis.abstract = self.request.get('abstract')
		thesis.adviser = self.request.get('adviser')
		thesis.section = self.request.get('section')

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result': 'OK',
			'data': {
			'id': student.key.urlsafe(),
			'year': student.year,
			'title': student.title,
			'abstract': student.abstract,
			'adviser': student.adviser,
			'section': student.section,
			}
		}
		self.response.out.write(json.dumps(response))

class GETapiThesis(webapp2.RequestHandler):
	def get(self):
		thesis = Thesis.query().order(-Thesis.data).fetch()

		response = {
		'result': 'OK'
		'data': 
		}

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))


app = webapp2.WSGIApplication([
    ('/POST/api/thesis', POSTapiThesis),
    ('/GET/api/thesis', GETapiThesis),
    ('/home', MainPageHandler),
    ('/', MainPageHandler)
], debug=True)