#!/usr/bin/env python3

import random
import sys
import json
import sqlite3
import math
from enum import IntEnum

ITEM_TYPES = ("weapon", "armor", "tool", "consumable", "drone")
ATTRIBUTES_ALWAYS_KNOWN = ("двуручн", "дальн")

class Index(IntEnum):
    NAME = 0
    LOOK = 1
    TYPE = 2
    ATTRIBUTES = 3
    DURABILITY = 4
    WEIGHT = 5

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
    print(f"{name} {attributes} ({item[Index.DURABILITY]}/{item[Index.DURABILITY]})")

# Calculate HP or MP based on starting value and spent SP
def gen_hp_mp(start, sp):
    result = start
    for i in range(sp):
        newres = math.floor(result*1.05)
        if newres > result:
            result = newres
        else:
            result += 1
    print(result)

# Calculate property strength based on starting value and spent SP
def gen_property(start, sp):
    result = start
    for i in range(sp):
        newres = math.floor(result*1.2)
        if newres > result:
            result = newres
        else:
            result += 1
    print(result)

def main():
    if len(sys.argv) < 2:
        print("Usage: generate.py <type> [count]")
    else:
        if sys.argv[1] == "item":
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            if len(sys.argv) == 3:
                count = int(sys.argv[2])
                for i in range(count):
                    print(i+1, end=". ")
                    gen_item(c)
            else:
                gen_item(c)
        elif sys.argv[1] in ITEM_TYPES:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            if len(sys.argv) == 3:
                count = int(sys.argv[2])
                for i in range(count):
                    gen_item(c, sys.argv[1])
            else:
                gen_item(c, sys.argv[1])
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
                gen_hp_mp(start, sp)
        elif sys.argv[1] == "property":
            if len(sys.argv) < 4:
                print("Usage: generate.py property <start> <sp>")
            else:
                start = int(sys.argv[2])
                sp = int(sys.argv[3])
                gen_property(start, sp)


if __name__ == "__main__":
    main()
