import json
file_path = './json/cvs/apple.json'

def parseCVS(data):
  if '-' in data[0]:
    elem1 = (data[0].split(' - '))
    name = elem1[0]
    for i in range(1, len(elem1)):
      if elem1[i][0].isdigit():
        quantity = elem1[i]
    print("Name: ", name)
    print("Quantity: ", quantity)
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
