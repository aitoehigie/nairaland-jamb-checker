import cherrypy
import os, time
from cherrypy import expose
from configuration import settings
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('views'))

class Jamb(object):
	@expose
	def index(self):
		tmpl = env.get_template("index.html")
		return tmpl.render()
	@expose
	def check_result(self, registration_number=None, exam_year=None, pin=None):
		tmpl = env.get_template("result.html")
		return tmpl.render(reg=registration_number)

cherrypy.config.update(settings)
root = Jamb()

if __name__ == "__main__":
    cherrypy.tree.mount(root, "/", config=settings)
    cherrypy.engine.start() 
    cherrypy.engine.block()