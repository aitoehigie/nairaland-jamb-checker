import os
admin_login = {"password": "nairaland"}
settings = { 
         'global': {
            'server.socket_port' : 8007,
            'server.socket_host': "127.0.0.1",
            'server.socket_file': "",
            'server.socket_queue_size': 5,
            'server.protocol_version': "HTTP/1.0",
            'server.log_to_screen': True,
            'server.log_file': "",
            'server.reverse_dns': False,
            'server.thread_pool': 10,
            'server.environment': "development",
	    'request.show_tracebacks': False
         },
	'/': {
	'tools.staticdir.root': os.path.abspath(os.path.curdir)
	},
	'/static': {
	  'tools.staticdir.on': True,
          'tools.staticdir.dir': 'static/'
         },
	'/static/images/': {
	 'tools.staticdir.on': True,
	 'tools.staticdir.root': os.path.abspath(os.path.curdir),
         'tools.staticdir.dir': 'static/images/'
         },
	'/static/js/': {
	 'tools.staticdir.on': True,
	 'tools.staticdir.root': os.path.abspath(os.path.curdir),
         'tools.staticdir.dir': 'static/js/'
         },
	
}