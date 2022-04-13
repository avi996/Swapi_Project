import pymongo
import requests
import bson
from pprint import pprint
client = pymongo.MongoClient()
db = client["starwars"]

def swapi(url):
    list= []

    response = requests.get(url)
    data = response.json()
    # pprint(data)

    list += data["results"]

    while data["next"] is not None:

        response = requests.get(data["next"])
        data = response.json()

        list += data["results"]
    return list

starship_list = swapi('https://swapi.dev/api/starships/')

db.starships.drop()

for i in starship_list:
    if len(i["pilots"]) > 0:
        for index, pilot in enumerate(i["pilots"]):
            pilot_info = requests.get(pilot).json()
            pilot_name = pilot_info["name"]
            pilot_id = db.characters.find_one({"name":pilot_name})["_id"]
            i["pilots"][index] = bson.ObjectId(pilot_id)

for document in starship_list:
    db.starships.insert_one(document)