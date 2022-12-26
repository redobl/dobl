#!/usr/bin/env python3

import random
import sys
import json
import sqlite3
import math
import base64
from os import path
from enum import IntEnum

ITEM_TYPES = ("weapon", "armor", "tool", "consumable", "drone")
ATTRIBUTES_ALWAYS_KNOWN = ("двуручн", "дальн", "материал")

class Index(IntEnum):
    NAME = 0
    LOOK = 1
    TYPE = 2
    ATTRIBUTES = 3
    DURABILITY = 4
    WEIGHT = 5

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
        if items[i][Index.DURABILITY] is None:
            items[i][Index.DURABILITY] = 20
        if items[i][Index.WEIGHT] is None:
            items[i][Index.WEIGHT] = 1
    weights = [i[Index.WEIGHT] for i in items]
    item = random.choices(items, weights=weights, k=1)[0]
    if item[Index.LOOK] == item[Index.NAME]:
        name = item[Index.NAME]
    else:
        name = item[Index.LOOK] + " (" + item[Index.NAME] + ")"
    attrList = []
    for i in json.loads(item[Index.ATTRIBUTES]):
        if i in ATTRIBUTES_ALWAYS_KNOWN:
            attrList.append(i)
        else:
            attrList.append("???"+i)
    attributes = "{" + ", ".join(attrList) + "}"
    return f"{name} {attributes} ({item[Index.DURABILITY]}/{item[Index.DURABILITY]})"

# Calculate HP or MP based on starting value and spent SP
def gen_hp_mp(start, sp):
    result = start
    for i in range(sp):
        newres = math.floor(result*1.05)
        if newres > result:
            result = newres
        else:
            result += 1
    return result

# Calculate property strength based on starting value and spent SP
def gen_property(start, sp):
    result = start
    for i in range(sp):
        newres = math.floor(result*1.2)
        if newres > result:
            result = newres
        else:
            result += 1
    return result

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
        elif sys.argv[1] in ("hp", "mp", "skill", "trait"):
            if len(sys.argv) < 3:
                print("Usage: generate.py hp|mp|skill|trait [start] <sp>")
            else:
                if len(sys.argv) == 3:
                    start = 100
                    sp = int(sys.argv[2])
                else:
                    start = int(sys.argv[2])
                    sp = int(sys.argv[3])
                print(gen_hp_mp(start, sp))
        elif sys.argv[1] in ["property", "prop"]:
            if len(sys.argv) < 4:
                print("Usage: generate.py property <start> <sp>")
            else:
                start = int(sys.argv[2])
                sp = int(sys.argv[3])
                print(gen_property(start, sp))


if __name__ == "__main__":
    main()
