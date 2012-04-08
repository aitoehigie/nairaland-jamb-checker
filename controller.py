import cherrypy
from random import choice
import dummy
import os, time, string
import mysql.connector
from cherrypy import expose
from configuration import dbsettings
from configuration import settings
from configuration import admin_login
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('views'))
current_dir = os.path.dirname(os.path.abspath(__file__))

db = mysql.connector.Connect(user=dbsettings["user"], password=dbsettings["password"], host=dbsettings["host"], port=dbsettings["port"], database=dbsettings["database"])


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
	def datagen(self):
		cursor = db.cursor()
		for item in dummy.names:
			cursor.execute("INSERT INTO students studentname=%s, age=%d, sex=%s, registrationnumber=%d, pin=%d", (choice(dummy.names), choice(dummy.age), choice(dummy.sex), dummy.registrationnumber, dummy.pin))

	@expose
	def buycard(self):
		cur = db.cursor()
		cur.execute("select name from person")
		rows = cur.fetchall()
		tmpl = env.get_template("buycard.html")
		return tmpl.render(target=rows)

	@expose
	@cherrypy.tools.allow(methods=['POST'])
	def admin_login(self, password=None):
		if password == admin_login["password"]:
			cherrypy.session["username"] = "Admininstrator"
			cherrypy.session["logged_in"] = True
			tmpl = env.get_template("admin_loggedin.html")
			return tmpl.render(target=cherrypy.session.get("username"), time=time.ctime())
		else:	
			raise cherrypy.HTTPRedirect("admin")
	

cherrypy.config.update(settings)
root = Jamb()

if __name__ == "__main__":
    cherrypy.tree.mount(root, "/", config=settings)
    cherrypy.engine.start()
    cherrypy.engine.block()