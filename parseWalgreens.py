import json

def parseWalgreens(data):
    ret = dict()
    price_info = data["price_info"]
    quantity = data["quantity"]
    count = data["count"]
    if "/" in price_info:
        price_infoList = price_info.split("/")
        if price_infoList[-1].strip() == "oz":
            quantity += " oz"
            ret["Price Info"] = price_infoList[0][:5]
            ret["Quantity"] = quantity
            ret["Count"] = count
            return ret
        else:
            price_info = price_infoList[-1]
            ret["Price Info"] = price_info
            ret["Quantity"] = quantity
            ret["Count"] = count
            return ret
    else:
        ret["Price Info"] = price_info
        ret["Quantity"] = quantity
        ret["Count"] = count
        return ret


with open("inventory.walgreens.json", 'r') as file:
  data = json.load(file)

for item in data:
  ret = parseWalgreens(item)
  print(ret)