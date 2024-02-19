import requests
import re
import json
from flask import Blueprint, jsonify, request

scraper = Blueprint('scraper',__name__)

# this function takes in the raw HTML and structures it as a json
def extractCVSData(data):

    # store the product data as a dictionary
    item_dict = {}
    
    # Categories for the item
    categories = [breadcrumb["title"] for breadcrumb in data.get("breadcrumbs", [])]
    item_dict["categories"] = categories

    # Name
    item_dict["name"] = data.get("handle", "")

    # Price
    item_dict["price"] = data.get("price", {}).get("value", "")

    # Sizes (Quantity)
    sizes = []
    if "options" in data and len(data["options"]) > 0 and "values" in data["options"][0]:
        for k in range(len(data["options"][0]["values"])):
            sizes.append(data["options"][0]["values"][k].get("value", ""))
    item_dict["sizes"] = sizes

    # Images
    item_dict["images"] = [img.get("uri", "") for img in data.get("images", [])]

    return item_dict;

# this function takes in a item name and scrapes data
def scrape_cvs(item_name):
    # name of the item to be scraped
    url = f"https://www.cvs.com/search?searchTerm={item_name}"

    # Fetch the page content
    response = requests.get(url)

    result = []  # Initialize result as a list

    if response.status_code == 200:
        # Use a regular expression to find the productSearchData variable
        match = re.search(r'var productSearchData = (.*?);', response.text, re.DOTALL)
        
        if match:
            # Extract the matched group, which should be the JSON string
            data_str = match.group(1)
            data = json.loads(data_str)

            if 'products' in data:
                products = data['products']

                for product in products:
                    processed_product = extractCVSData(product)
                    result.append(processed_product)  # Correct use of append on a list

                return result
        else:
            print('productSearchData variable not found in the page.')
            return False
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        return False