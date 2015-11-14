# Rushy Panchal
# HackPrinceton 2015
# app/app.py

from flask import Flask, render_template

import config

def main():
	'''Create the server and start it'''
	server = Server("config.FlaskSettings", template_folder = "views", static_folder = "static", static_url_path = "/static")
	server.configureRoutes()
	server.run()

class Server(Flask):
	'''Creates a basic Flask Web Server'''
	def __init__(self, configPath, *args, **kwargs):
		super(Server, self).__init__("HackPrinceton", *args, **kwargs)
		self.config.from_object(configPath)
		self.jinja_env.globals["site"] = config.VIEW_GLOBALS

	def shutdown(self): # not used as of now, need OS signal handling to do this
		'''Shuts down the Flask server'''
		with self.test_request_context():
			shutdownFunc = flask.request.environ.get("werkzeug.server.shutdown")
			if not shutdownFunc:
				raise ValueError("Not running a Werkzeug server")
			return shutdownFunc()

	def configureRoutes(self):
		'''Configure the routes for the server'''
		@self.route("/index/")
		@self.route("/")
		def index():
			'''GET index page'''
			return render_template("index.html")

		@self.route("/contact/")
		def contact():
			'''GET the contact page'''
			return render_template("contact.html")

		@self.route("/demo/")
		def demo():
			'''GET demo page'''
			return render_template("demo.html")

if __name__ == '__main__':
	main()
