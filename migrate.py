#!/usr/bin/env python3

import sqlite3
import json

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Migration from items.json to database
def main():
    with open("items.json", "r") as f:
        items = json.load(f)
    for item in items:
        if "weight" not in item:
            item["weight"] = 1
        if "durability" not in item:
            item["durability"] = 20
        c.execute(
            "INSERT INTO items (id, name, look, type, attributes, durability, weight) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                item["id"],
                item["name"],
                item["look"],
                item["type"],
                json.dumps(item["attributes"], ensure_ascii=False),
                item["durability"],
                item["weight"],
            ),
        )
    conn.commit()


if __name__ == "__main__":
    main()
