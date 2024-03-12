import json
file_path = './json/cvs/apple.json'

def getCountAndSize(string):
  ret = dict()
  for i in reversed(range(len(string))):
    if string[i].lower() == "t":
      i += 1
      if string[i:i+2].lower() == "c":
        count = ""
        i -= 2
        while string[i].isdigit() or string[i] == " ":
          count += string[i]
          i -= 1
        ret['Count'] = count

        # modify this function so that it uses .find instead of for loops


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
  print(f"Starting to parse: \n{item}")
  print("Result: ")
  parseCVS(item)
