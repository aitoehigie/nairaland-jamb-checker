import cherrypy
import random
import os, time, string
from cherrypy import expose
from configuration import settings
from configuration import admin_login
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
		return tmpl.render()

	@expose
	def admin(self):
		tmpl = env.get_template("admin.html")
		return tmpl.render()

	@expose
	@cherrypy.tools.allow(methods=['POST'])
	def admin_login(self, password=None):
		if password == admin_login["password"]:
			tmpl = env.get_template("admin_loggedin.html")
			return tmpl.render(target="Nairaland-Jamb-Checker Admininstrator", time=time.ctime())
		else:	
			raise cherrypy.HTTPError(401, "You are not allowed to view this resource!")
	@expose
	def pin(self):
		pin = []
		times = 4
		while times >= 1:
			pin.append(random.randrange(0, 9))
			times = times - 1
		tmpl = env.get_template("pin.html")
		pin = str(pin[0])+str(pin[1])+str(pin[2])+str(pin[3])
		return tmpl.render(pin= pin)
	

cherrypy.config.update(settings)
root = Jamb()

if __name__ == "__main__":
    cherrypy.tree.mount(root, "/", config=settings)
    cherrypy.engine.start() 
    cherrypy.engine.block()