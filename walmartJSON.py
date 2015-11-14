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
"""

import http.client
import json

# Access key for walmart api
my_walmart_api_key = "krf8tpvtt6rsek3xx9zxe776"

# Helper function for connecting to the walmart api
def establishConnection():
    connection = http.client.HTTPSConnection('api.walmartlabs.com')
    connection.connect()
    return connection


# Use Store Locator API to find nearest walmart with Latitude and Longitude returns dictionary
def getStoreData(latitude, longitude):
    connection = establishConnection()
    connection.request('GET', '/v1/stores?format=json&lat=' + latitude + '&lon=' + longitude + '&apiKey=' + my_walmart_api_key)
    response = connection.getresponse()
    store_json = json.loads(response.read().decode())
    # Creates a dictionary with store information
    store_data = {}
    store_data['no'] = store_json[0]['no']
    store_data['name'] = store_json[0]['name']
    store_data['streetAddress'] = store_json[0]['streetAddress']
    return store_data

# Get the information of the ingredients returns list of dictionaries(one dict per item)
def getIngredientInformation(ingredients):
    connection = establishConnection()
    # Create list of id's
    id_list = []
    # Do some array stuff like append for the first item of every Search API
    for ingredient in ingredients:
        connection.request('GET', '/v1/search?query=' + ingredient + '&format=json&apiKey=' + my_walmart_api_key)
        requested_search_string = connection.getresponse()
        ingredient_json = json.loads(requested_search_string.read().decode())
        tear = ingredient_json['items'][0]
        id_list.append(tear['itemId'])
    # Create list of dictionary objects for ingredient info
    info_list = []
    # Get the information for each ingredient using Lookup API with itemId
    for identity in id_list:
        connection.request('GET', '/v1/items/' + str(identity) + '?format=json&apiKey=' + my_walmart_api_key)
        requested_lookup_string = connection.getresponse()
        info_json = json.loads(requested_lookup_string.read().decode())
        info_data = {}
        info_data['name'] = info_json['name']
        info_data['stock'] = info_json['stock']
        info_data['salePrice'] = info_json['salePrice']
        info_data['categoryPath'] = info_json['categoryPath']
        info_data['productUrl'] = info_json['productUrl']
        info_list.append(info_data)
    return info_list
