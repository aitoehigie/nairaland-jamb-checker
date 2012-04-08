import cherrypy
import random
import os, time, string
import mysql.connector
from cherrypy import expose
from configuration import dbsettings
from configuration import settings
from configuration import admin_login
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('views'))
current_dir = os.path.dirname(os.path.abspath(__file__))

def dbconnection(self):
	db = mysql.connector.Connect(user=dbsettings["user"], password=dbsettings["password"], host=dbsettings["host"], 
	port=dbsettings["port"], database=dbsettings["database"])

cherrypy.engine.subscribe('start_thread',dbconnection)

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
	def buycard(self):
		cur = db.cursor()
		cur.execute("select name from person")
		rows = cur.fetchall()
		tmpl = env.get_template("buycard.html")
		return tmpl.render(target=rows)
		#names = ["ehigie", "aito", "pascal", "edeoghon", "aitokhuehi", "thedon"]
		#for item in names:			
			#cur.execute("insert into person set name='%s'" %(item))

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