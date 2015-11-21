# Rushy Panchal
# HackPrinceton 2015
# app/config.py

class FlaskSettings(object):
	'''Settings for Flask server'''
	DEBUG = True

	SECRET_KEY = "NtaTRKcZKw256RNMwp25Xqvw"
	SESSION_COOKIE_NAME = "lazychef"

	SERVER_NAME = "localhost:8080"
	PREFERRED_URL_SCHEME = "http://"

RECIPES = ["Baked Potato", "Cook Pasta"]

VIEW_GLOBALS = {
	"name": "Lazy Chef"
	}
