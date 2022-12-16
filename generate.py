#!/usr/bin/env python3

import random
import sys
import json
import sqlite3

item_types = ["weapon", "armor", "tool", "consumable", "drone"]

# Pick one of items in database.db depending on weight
def gen_item(c, type=None):
    if type is not None:
        c.execute("SELECT * FROM items WHERE type = ?", (type,))
    else:
        c.execute("SELECT * FROM items")
    items = c.fetchall()
    for i in range(len(items)):
        items[i] = list(items[i])
        if items[i][5] is None:
            items[i][5] = 20
        if items[i][6] is None:
            items[i][6] = 1
    weights = [i[6] for i in items]
    item = random.choices(items, weights=weights, k=1)[0]
    if item[2] == item[1]:
        name = item[1]
    else:
        name = item[2] + " (" + item[1] + ")"
    attributes = "{" + ", ".join(['???'+i for i in json.loads(item[4])]) + "}"
    print(f"{name} {attributes} ({item[5]}/{item[5]})")


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
                    gen_item(c)
            else:
                gen_item(c)
        elif sys.argv[1] in item_types:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            if len(sys.argv) == 3:
                count = int(sys.argv[2])
                for i in range(count):
                    gen_item(c, sys.argv[1])
            else:
                gen_item(c, sys.argv[1])


if __name__ == "__main__":
    main()
