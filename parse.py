def parse(data):
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
    

  
item1 = [
    "Clorox Original Clean-Up All Purpose Cleaner with Bleach Spray Bottle - 32oz",
    "Clorox",
    "$4.59 ($0.14/fluid ounce)"
  ]

item2 = [
    "Clorox Splash-Less Liquid Bleach - Regular - 77oz",
    "Clorox",
    "$5.79 ($0.08/fluid ounce)"
  ]

item3 = [
    "Clorox Disinfecting Bleach - Regular - 121oz",
    "Clorox",
    "$8.39 ($0.07/fluid ounce)"
  ]

item4 =  [
    "Clorox Fresh Disinfecting Wipes Bleach Free Cleaning Wipes - 9ct",
    "Clorox",
    "$0.99 ($0.11/count)"
  ]

item5 =  [
    "Clorox Disinfecting Wipes - Fresh Scent - 75ct",
    "Clorox",
    "$5.59"
  ]

item6 = [
    "Clorox Rain Clean Scent Clean-Up All Purpose Cleaner with Bleach Spray Bottle - 32 fl oz",
    "Clorox",
    "$4.59 ($0.14/fluid ounce)",
  ]

item7 = [
    "Clorox Disinfecting Wipes Value Pack Bleach Free Cleaning Wipes - 75ct/3pk",
    "Clorox",
    "$12.99 ($0.06/count)",
  ]

item8 = [
    "Clorox Disinfecting Wipes - Crisp Lemon - 75ct",
    "Clorox",
    "$5.59"
  ]

item9 = [
    "Clorox To Go Citrus Disinfecting Wipes - 9ct",
    "Clorox",
    "$0.99 ($0.11/count)",
  ]

item10 = [
    "Clorox Fresh Scent Bleach Free Disinfecting Wipes",
    "Clorox",
    "$3.39 - $5.59",
  ]

parse(item1)
print("\n")
parse(item2)
print("\n")
parse(item3)
print("\n")
parse(item4)
print("\n")
parse(item5)
print("\n")
parse(item6)
print("\n")
parse(item7)
print("\n")
parse(item8)
print("\n")
parse(item9)
print("\n")
parse(item10)