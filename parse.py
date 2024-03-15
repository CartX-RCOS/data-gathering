import json
import re
file_path = './json/cvs/apple.json'

all_possible_endings = ["ct", "CT", "oz", "OZ", "mg", "MG"]

def getCountSizeAndSizeType(string, all_possible_endings):
  ret = dict()
  strings = re.split(r',|-', string)
  strings = strings[::-1]
  count = 0
  size = 0
  size_type = ""
  for index in range(0, len(strings)):
    for suffix in all_possible_endings:
      if suffix in strings[index]:
        if suffix.lower() == "ct":
          count = string[index]
          count = count.replace(suffix, "")
        else:
          size = string[index]
          size = size.replace(suffix, "")
          size_type = suffix
  ret["Count"] = count
  ret["Size"] = size
  ret["Size Type"] = size_type
  return ret

def parseCVS(data):
  if ',' in data[0]:
    elem1 = (data[0].split(', '))
    name = elem1[0]

    for i in range(1, len(elem1)):
      if elem1[i][0].isdigit():
        quantity = elem1[i]

        for i in range(len(quantity)):
          if quantity[i].isalpha():
            quantity_type = quantity[i:]

    print("Name: ", name)
    print("Quantity: ", quantity)
    print("Quantity Type: ", quantity_type)

  elif "-" in data[0]:
    elem1 = (data[0].split(' = '))
    name = elem1[0]

    for i in range(1, len(elem1)):
      if elem1[i][0].isdigit():
        quantity = elem1[i]

        for i in range(len(quantity)):
          if quantity[i].isalpha():
            quantity_type = quantity[i:]


    print("Name: ", name)
    print("Quantity: ", quantity)
    print("Quantity Type: ", quantity_type)

  else:
    elem1 = data[0]
    name = elem1
    quantity = "N/A"
    print("Name: ", name)
    print("Quantity: ", quantity)
  
  brand = data[1]
  price = data[2]
  print("Brand: ", brand)
  print("Price: ", price)
    

with open(file_path, 'r') as file:
  data = json.load(file)

for item in data:
  # print(f"Starting to parse: \n{item}")
  # print("Result: ")
  print(item[0])
  # parseCVS(item[0])
  ret = getCountSizeAndSizeType(item[0], all_possible_endings)
  print(ret)