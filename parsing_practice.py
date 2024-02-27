import json

def isValueValid(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        for entry in data:
            country_name = entry["Country Name"]
            value = float(entry["Value"])
            if value > 120000000.0:
                print("{} is valid".format(country_name))
            else:
                print("{} is invalid".format(country_name))
    
json_file = "population_data.json"
isValueValid(json_file)