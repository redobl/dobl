#!/usr/bin/env python3

import sys
import re
import base64

equippedPattern = r"^(\d+)э\. "
unequippedPattern = r"(^\d+)\. "
subslotsPattern = r"^-(\d+)\. "

class Item:
    def __init__(self, number, value, equipped):
        self.number = number
        self.value = value
        self.equipped = equipped

def sort_inventory(inventory):
    def sort_key(item):
        return int(not item.equipped)*1000+(item.number if item.number is not None else 0)

    inventory = inventory.split("\n")
    i = 0
    while i < len(inventory):
        item = inventory[i]
        
        if re.match(equippedPattern, item):
            for match in re.finditer(equippedPattern, item):
                number = int(match.group(1))
                value = item[match.end():]
                equipped = True
                inventory[i] = Item(number, value, equipped)
                i+=1
        elif re.match(unequippedPattern, item):
            for match in re.finditer(unequippedPattern, item):
                number = int(match.group(1))
                value = item[match.end():]
                equipped = False
                inventory[i] = Item(number, value, equipped)
                i+=1
        elif re.match(subslotsPattern, item):
            for match in re.finditer(subslotsPattern, item):
                inventory[i-1].value += "\n"+item
                inventory.pop(i)
        else:
            inventory[i] = Item(None, item, False)
            i+=1

    inventory.sort(key=sort_key)
    result = ""
    nextNum = 1
    for item in inventory:
        if item.number is not None:
            item.number = nextNum
            nextNum += 1
            if item.equipped:
                result += str(item.number)+"э. "+item.value+"\n"
            else:
                result += str(item.number)+". "+item.value+"\n"
        else:
            result += item.value+"\n"
    return result

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(sort_inventory(sys.argv[1]))
    elif len(sys.argv) == 3 and sys.argv[1] == "base64":
        import base64
        print(str(base64.b64encode(sort_inventory(sys.argv[2]).encode("utf-8")), "utf-8"))
    else:
        print("Usage: sort.py [base64] <inventory>")