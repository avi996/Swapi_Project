import pymongo
import requests
import bson
from pprint import pprint
client = pymongo.MongoClient()
db = client["starwars"]

def swapi(url):
    # Creating a list of starships
    list= []

    response = requests.get(url)
    data = response.json()

    # Storing the first page of results
    list += data["results"]

    while data["next"] is not None:
        response = requests.get(data["next"])
        data = response.json()
        # Storing the current page of results
        list += data["results"]
    return list

# Returns all starships from each page as a list
starship_list = swapi('https://swapi.dev/api/starships/')

# Drops the previous starships collection
db.starships.drop()

# Looping over starship_list for starships that have pilots
for i in starship_list:
    if len(i["pilots"]) > 0:
        # Replacing API urls with ObjectIds from characters collection in mongodb
        for index, pilot in enumerate(i["pilots"]):
            pilot_info = requests.get(pilot).json()
            pilot_name = pilot_info["name"]
            pilot_id = db.characters.find_one({"name":pilot_name})["_id"]
            i["pilots"][index] = bson.ObjectId(pilot_id)

# Inserting updated documents into starships collection in mongodb
for document in starship_list:
    db.starships.insert_one(document)
