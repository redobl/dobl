#!/usr/bin/env python3

import random
import sys
import json
import sqlite3
import math
import base64
from os import path
from enum import Enum, IntEnum

ITEM_TYPES = ("weapon", "armor", "tool", "consumable", "drone")
ATTRIBUTES_ALWAYS_KNOWN = ("двуручн", "дальн", "материал")
BEHAVIOR_TYPES = ("aggressive", "stealthy", "neutral", "tactical", "frugal", "wandering")
NPC_SP_CHOICES_LOWLVL = (
    "получить случайный предмет",
    "улучшить предмет",
    "увеличить макс. ОЗ"
)
NPC_SP_CHOICES = (
    "получить случайный предмет",
    "улучшить предмет",
    "увеличить макс. ОЗ",
    "получить случайный навык",
    "улучшить навык"
)

class ItemsIndex(IntEnum):
    NAME = 0
    LOOK = 1
    TYPE = 2
    ATTRIBUTES = 3
    DURABILITY = 4
    WEIGHT = 5
class AbilsIndex(IntEnum):
    TYPE = 0
    TEXT = 1

scriptDir = path.dirname(path.abspath(__file__))

# Pick one of items in database.db depending on weight
def gen_item(c, type=None):
    if type is not None:
        c.execute("SELECT name, look, type, attributes, durability, weight FROM items WHERE type = ?", (type,))
    else:
        c.execute("SELECT name, look, type, attributes, durability, weight FROM items")
    items = c.fetchall()
    for i in range(len(items)):
        items[i] = list(items[i])
        if items[i][ItemsIndex.DURABILITY] is None:
            items[i][ItemsIndex.DURABILITY] = 20
        if items[i][ItemsIndex.WEIGHT] is None:
            items[i][ItemsIndex.WEIGHT] = 1
    weights = [i[ItemsIndex.WEIGHT] for i in items]
    item = random.choices(items, weights=weights, k=1)[0]
    if item[ItemsIndex.LOOK] == item[ItemsIndex.NAME]:
        name = item[ItemsIndex.NAME]
    else:
        name = item[ItemsIndex.LOOK] + " (" + item[ItemsIndex.NAME] + ")"
    attrList = []
    for i in json.loads(item[ItemsIndex.ATTRIBUTES]):
        if i in ATTRIBUTES_ALWAYS_KNOWN:
            attrList.append(i)
        else:
            attrList.append("???"+i)
    attributes = "{" + ", ".join(attrList) + "}"
    return f"{name} {attributes} ({item[ItemsIndex.DURABILITY]}/{item[ItemsIndex.DURABILITY]})"

# Calculate HP or MP based on starting value and spent SP
def gen_hp_mp(start, sp):
    result = start
    for i in range(sp):
        newres = math.floor(result*1.15)
        if newres > result:
            result = newres
        else:
            result += 1
    return result

def gen_abil_lvl(start, sp):
    result = start
    for i in range(sp):
        newres = math.floor(result*1.3)
        if newres > result:
            result = newres
        else:
            result += 1
    return result

# Calculate property strength based on starting value and spent SP
def gen_property(start, sp):
    result = start
    for i in range(sp):
        newres = math.floor(result*1.6)
        if newres > result:
            result = newres
        else:
            result += 1
    return result

# Generate ability
def gen_abil(c):
    c.execute("SELECT type, text FROM abilities")
    abils = c.fetchall()
    abil = random.choice(abils)
    return f"{abil[AbilsIndex.TYPE][0]}{abil[AbilsIndex.TEXT]}"

# Roll many dice and display results, categorized by value
def roll_dice(dice, sides):
    results = [0]*sides
    for i in range(dice):
        results[random.randint(0, sides-1)] += 1
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: generate.py <type> [count]")
    else:
        if sys.argv[1] == "item":
            conn = sqlite3.connect(path.join(scriptDir, "database.db"))
            c = conn.cursor()
            if len(sys.argv) == 3:
                count = int(sys.argv[2])
                for i in range(count):
                    print(str(i+1)+". "+gen_item(c))
            else:
                print(gen_item(c))
        elif sys.argv[1] in ITEM_TYPES:
            conn = sqlite3.connect(path.join(scriptDir, "database.db"))
            c = conn.cursor()
            if len(sys.argv) == 3:
                count = int(sys.argv[2])
                for i in range(count):
                    print(gen_item(c, sys.argv[1]))
            else:
                print(gen_item(c, sys.argv[1]))
        elif sys.argv[1] == "item_base64":
            conn = sqlite3.connect(path.join(scriptDir, "database.db"))
            c = conn.cursor()
            if len(sys.argv) == 3:
                count = int(sys.argv[2])
                res = "1. "+gen_item(c)
                for i in range(1,count):
                    res += "\n"+str(i+1)+". "+gen_item(c)
            else:
                res = gen_item(c)
            # encode string to base64
            encodedBytes = base64.b64encode(res.encode("utf-8"))
            encodedStr = str(encodedBytes, "utf-8")
            print(encodedStr)
        elif sys.argv[1] in ("hp", "mp"):
            if len(sys.argv) < 3:
                print("Usage: generate.py hp|mp [start] <sp>")
            else:
                if len(sys.argv) == 3:
                    start = 100
                    sp = int(sys.argv[2])
                else:
                    start = int(sys.argv[2])
                    sp = int(sys.argv[3])
                print(gen_hp_mp(start, sp))
        elif sys.argv[1] in ("abil", "skill", "trait"):
            if len(sys.argv) < 3:
                print("Usage: generate.py abil|skill|trait <start> <sp>")
            else:
                if len(sys.argv) == 3:
                    start = 100
                    sp = int(sys.argv[2])
                else:
                    start = int(sys.argv[2])
                    sp = int(sys.argv[3])
                print(gen_abil_lvl(start, sp))
        elif sys.argv[1] in ["property", "prop"]:
            if len(sys.argv) < 4:
                print("Usage: generate.py property <start> <sp>")
            else:
                start = int(sys.argv[2])
                sp = int(sys.argv[3])
                print(gen_property(start, sp))
        elif sys.argv[1] == "dice":
            if len(sys.argv) < 3:
                print("Usage: generate.py dice <dice>d<sides>")
            else:
                dice = int(sys.argv[2].split("d")[0])
                sides = int(sys.argv[2].split("d")[1])
                res = roll_dice(dice, sides)
                for i in range(sides):
                    print(str(i+1)+": "+str(res[i]))
        elif sys.argv[1] == "behavior":
            print(random.choice(BEHAVIOR_TYPES))
        elif sys.argv[1] == "npc":
            lvl = int(sys.argv[2])
            if lvl < 3:
                availableChoices = NPC_SP_CHOICES_LOWLVL
            else:
                availableChoices = NPC_SP_CHOICES
            results = roll_dice(lvl*3, len(availableChoices))
            for i in range(len(availableChoices)):
                print(str(results[i])+": "+availableChoices[i])
        elif sys.argv[1] == "ability_base64":
            conn = sqlite3.connect(path.join(scriptDir, "database.db"))
            c = conn.cursor()
            res = gen_abil(c)
            encodedBytes = base64.b64encode(res.encode("utf-8"))
            encodedStr = str(encodedBytes, "utf-8")
            print(encodedStr)


if __name__ == "__main__":
    main()
