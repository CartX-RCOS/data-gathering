import requests
import re
import json

def returnJSON(data):
    item_dict = {}
    
    # Categories
    categories = [breadcrumb["title"] for breadcrumb in data.get("breadcrumbs", [])]
    item_dict["categories"] = categories

    # Name
    item_dict["name"] = data.get("handle", "")

    # Price
    item_dict["price"] = data.get("price", {}).get("value", "")

    # Sizes
    sizes = []
    if "options" in data and len(data["options"]) > 0 and "values" in data["options"][0]:
        for k in range(len(data["options"][0]["values"])):
            sizes.append(data["options"][0]["values"][k].get("value", ""))
    item_dict["sizes"] = sizes

    # Images
    item_dict["images"] = [img.get("uri", "") for img in data.get("images", [])]

    return item_dict;

# The URL of the page
url = "https://www.cvs.com/search?searchTerm=advil"

def getData(url):
    # Fetch the page content
    response = requests.get(url)

    if response.status_code == 200:

        # Use a regular expression to find the productSearchData variable
        match = re.search(r'var productSearchData = (.*?);', response.text, re.DOTALL)
        
        if match:
            # Extract the matched group, which should be the JSON string
            data_str = match.group(1)
            data = json.loads(data_str)

            if 'products' in data:
                products = data['products']

                for i in range(len(products)):
                    processed_product = returnJSON(products[i])
                    print(processed_product)
        else:
            print('productSearchData variable not found in the page.')
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')