import json
import os

from game import constants


items = {}


def save():
    global items
    with open(constants.ITEMS_PATH, "w") as writefile:
        json.dump(items, writefile)

def load():
    global items
    if not os.path.exists(constants.ITEMS_PATH):
        # If file doesn't exist, return
        return
    with open(constants.ITEMS_PATH, "r") as readfile:
        return json.load(readfile)

def clear():
    global items
    items = {}
    if os.path.exists(constants.PLAYER_DATA_PATH):
        os.remove(constants.PLAYER_DATA_PATH)


def generate():
    return {
        "stone": _item(0)
    }

def _item(texture_id):
    return {
        "texture_id": texture_id
    }


# Load or generate items
if not items:
    items = load()
    if not items:
        items = generate()
        save()