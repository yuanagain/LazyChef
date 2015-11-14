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
			return render_template("timer.html", recipe_data = {"active": [{"start_time": 0.0, "description": "Put water in pot. Put pot on stove", "name": "Put water on stove", "end_time": 5.0, "time_delta": 5}, {"start_time": 5.0, "description": "Add salt to water", "name": "Add salt", "end_time": 15, "time_delta": 10}, {"start_time": 15.0, "description": "Add pasta to boiling water", "name": "Put pasta in water", "end_time": 25.0, "time_delta": 10}, {"start_time": 25.0, "description": "Dice Tomatoes into small cubes", "name": "Dice Tomatoes", "end_time": 35.0, "time_delta": 10}, {"start_time": 35.0, "description": "Drain pasta using a strainer", "name": "Drain pasta", "end_time": 50.0, "time_delta": 15}, {"start_time": 50.0, "description": "Cover the pasta with Tomatoes", "name": "Put Tomatoes in pasta", "end_time": 55.0, "time_delta": 5}], "passive": [{"name":"Boiling Water\n","end_time":7.0,"start_time":0.0,"descripton":"Bring cold water to a boil\n","time_delta":7.0},{"name":"Pasta\n","end_time":120.0,"start_time":120.0,"descripton":"Ingredient\n","time_delta":0.0},{"name":"Water\n","end_time":120.0,"start_time":120.0,"descripton":"Ingredient\n","time_delta":0.0}, {"start_time": 2.0, "end_time": 30.0, "time_delta": 28.0, "name": "Sautee onions", "description": "none"},{"name":"Boiling Water\n","end_time":9.0,"start_time":0.0,"descripton":"Bring cold water to a boil\n","time_delta":9.0},{"name":"Boiling Water\n","end_time":10.0,"start_time":0.0,"descripton":"Bring cold water to a boil\n","time_delta":10.0}]}, recipes = ["Pasta", "Hot Water"])

if __name__ == '__main__':
	main()
