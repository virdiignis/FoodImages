import requests
from json import loads
from urllib.request import urlretrieve
from urllib.error import HTTPError
import os
from time import sleep


def down_batch(data: str, dir: str):
    json = loads(data)
    page_nr = int(json["pagination"]["current_page"])
    reviews = json["data"]["sightings"]
    i = 1
    for r in reviews:
        try:
            urlretrieve(r["current_review"]["thumb_590"], dir + "/" + str(40 * (page_nr - 1) + i) + ".jpg")
            print("Downloading " + str(40 * (page_nr - 1) + i) + " image.")
            i += 1
        except HTTPError:
            print("Image can't be found.")
        except ConnectionResetError:
            sleep(100)
            i += 1
        except TypeError:
            i += 1


with open("food_names.txt") as F:
    foods = tuple(map(str.strip, F.readlines()))

for food in foods:
    directory = food.replace(' ', '_')
    if not os.path.exists(directory):
        os.makedirs(directory)
    r = requests.get(
        "http://www.foodspotting.com/api/v1/sightings.json?api_key=88jrlU7j4HsTnnVNciqhfZbXd6vgPmVU9gbu46Mh"
        "&per_page=40&page=1&query={}".format(food))
    pages = int(loads(r.text)["pagination"]["total_pages"]) + 1
    down_batch(r.text, directory)
    for i in range(2, pages):
        r = requests.get(
            "http://www.foodspotting.com/api/v1/sightings.json?api_key=88jrlU7j4HsTnnVNciqhfZbXd6vgPmVU9gbu46Mh"
            "&per_page=40&page={}&query={}".format(i, food))
        down_batch(r.text, directory)
