# Rushy Panchal
# HackPrinceton 2015
# app/config.py

import os

ENVIRONMENT = os.environ.get("PYTHONENV", "dev")

DEV_MODE = (ENVIRONMENT == "dev")

class FlaskSettings(object):
	'''Settings for Flask server'''
	DEBUG = DEV_MODE

	SECRET_KEY = "NtaTRKcZKw256RNMwp25Xqvw"
	SESSION_COOKIE_NAME = "jellifish"

	SERVER_NAME = "localhost:8080" if DEV_MODE else "app.jelli.fish"
	PREFERRED_URL_SCHEME = "http://"

RECIPES = ["Baked Potato", "Cook Pasta"]

VIEW_GLOBALS = {
	"name": "Jellifish"
	}
