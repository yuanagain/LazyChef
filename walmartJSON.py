"""
walmartJSON.py
By: Hector Solis
for - Princeton Fall 2015 Hackathon

func - establishConnection: helper function no need to be called

func - getStoreData: returns a dictionary with the nearest store's number('no'), name('name'), and address('streetAddress')
	examples:
		latitude = "40.350414"
		longitude = "-74.652762"
		dictionary = getStoreData(latitude,longitude)
		print('name') -> Wal-Mart - GM
		print('streetAddress') -> 101 NASSAU PARK BLVD

func - getIngredientInformation: returns a list of dictionaries where each dictionary has information on one ingredient
			name('name'), in_stock('stock'), price('salePrice'), categoryPath('categoryPath'), URL('productUrl')
		examples:
			i = {"Tomato", "Pasta", "Water"}
			list_of_info = getIngredientInformation(i)
			print(list_of_info[0]['name']) -> Hunt's Petite Diced Tomatoes, 14.5 oz, 6 ct
			print(list_of_info[0]['salePrice']) -> 5.48
			print(list_of_info[2]['name']) -> Ozarka 100% Natural Spring Water, 0.5 l, 24 ct
			print(list_of_info[2]['stock']) -> Available
func - generateIngredientJSONFile: writes the ingredient information in JSON to the shopping cart JSON file
		examples:
			i = {"Tomatoes", "Pasta", "Water", "Salt"}
			generateIngredientJSONFile(i) -> shoppingCart.json is now populated
"""

import requests

from simplejson.scanner import JSONDecodeError

# Access key for walmart api
my_walmart_api_key = "krf8tpvtt6rsek3xx9zxe776"

# get JSON from a given url from the Walmart API
def getJSON(url):
	response = requests.get("https://api.walmartlabs.com/v1/{url}".format(url = url))
	try:
		return response.json()
	except JSONDecodeError:
		return {}

# Use Store Locator API to find nearest walmart with Latitude and Longitude returns dictionary
def getStoreData(latitude, longitude):
	store_json = getJSON("stores?lat={lat}&lon={lon}&format=json&apiKey={key}".format(lat = latitude, lon = longitude, key = my_walmart_api_key))
	# Creates a dictionary with store information
	store_data = {}
	store_data['no'] = store_json[0]['no']
	store_data['name'] = store_json[0]['name']
	store_data['streetAddress'] = store_json[0]['streetAddress']
	return store_data

# Get the information of the ingredients returns list of dictionaries(one dict per item)
def getIngredientInformation(ingredients):
	# Create list of id's
	id_list = []
	# Do some array stuff like append for the first item of every Search API
	for ingredient in ingredients:
		ingredient_json = getJSON("search?query={q}&format=json&apiKey={key}".format(q = ingredient, key = my_walmart_api_key))
		tear = ingredient_json.get('items', [{}])[0]
		id_list.append(tear.get('itemId', ""))
	# Create list of dictionary objects for ingredient info
	info_list = []
	# Get the information for each ingredient using Lookup API with itemId
	info_all = getJSON("items?ids={ids}&format=json&apiKey={key}".format(ids = ",".join(map(str, id_list)), key = my_walmart_api_key))
	for info_json in info_all.get("items", []):
		info_data = {}
		info_data['name'] = info_json.get('name', "")
		info_data['stock'] = (info_json.get('stock', "") == "Available")
		info_data['salePrice'] = info_json.get('salePrice', "")
		info_data['categoryPath'] = "->".join(info_json.get('categoryPath', "").split("/")[1:])
		info_data['productUrl'] = info_json.get('productUrl', "")
		info_list.append(info_data)
	return info_list

def generateIngredientJSONFile(ingredients):
	list_of_info = getIngredientInformation(ingredients)
	with open('shoppingCart.json', 'w') as f:
		json.dump(list_of_info, f)


def generateIngredientJSONFile(ingredients, file_name):
	list_of_info = getIngredientInformation(ingredients)
	with open(file_name, 'w') as f:
		json.dump(list_of_info, f)
