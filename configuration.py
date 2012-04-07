import os
admin_login = {"password": "nairaland"}
settings = { 
         'global': {
            'server.socket_port' : 7077,
            'server.socket_host': "127.0.0.1",
            'server.socket_file': "",
            'server.socket_queue_size': 5,
            'server.protocol_version': "HTTP/1.0",
            'server.log_to_screen': True,
            'server.log_file': "",
            'server.reverse_dns': False,
            'server.thread_pool': 10,
            'server.environment': "development",
	    'request.show_tracebacks': False,
	    'tools.sessions.on': True,
	    'tools.sessions.storage_type': "file",
	    'tools.sessions.storage_path': "sessions/",
	    'tools.sessions.timeout': 60
         },
	'/': {
	'tools.caching.on': True,
	'tools.caching.delay': 3600,
	'tools.staticdir.root': os.path.abspath(os.path.curdir)
	},
	"/pin": {
	"tools.caching.on": False
	},
	'/static': {
	  'tools.staticdir.on': True,
          'tools.staticdir.dir': 'static'
         }	
}