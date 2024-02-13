from flask import Flask, Blueprint, jsonify, request
import requests
import re, json

def extractData(data):

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
                    processed_product = extractData(product)
                    result.append(processed_product)  # Correct use of append on a list

                return result
        else:
            print('productSearchData variable not found in the page.')
            return False
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        return False


main = Blueprint('main', __name__)

# fetching logic for CVS
@main.route('/CVS', methods=['POST'])
async def CVS():

    # Ensure the request has JSON content
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Get JSON data from the request body
    data = request.get_json()

    items = data.get('items')

    if not items or not isinstance(items, list):
        return jsonify({"error": "The 'items' field is required and must be a list"}), 400

    response_data = []

    for i in range(0,len(items)):
        response = scrape_cvs(items[i])
        response_data.append(response)

    with open('response_data.json', 'w') as json_file:
        json.dump(response_data, json_file, ensure_ascii=False, indent=4)

    return jsonify(response_data)

@main.route('/Shoprite')
def Shoprite():
    # fetching logic for Shoprite
    return jsonify({"data": "Shoprite data will be scraped here"})

@main.route('/Target')
def Target():
    # fetching logic for Shoprite
    return jsonify({"data": "Target data will be scraped here"})

# @main.route('/scrape')
# def getData():
#     # Dictionary that holds the status and data for each store
#     results = {
#         "CVS": {"success": False, "data": None},
#         "Shoprite": {"success": False, "data": None},
#         "Target": {"success": False, "data": None}
#     }
    
#     # URLs for each store scrape endpoint
#     urls = {
#         "CVS": "http://127.0.0.1:3000/CVS",
#         "Shoprite": "http://127.0.0.1:3000/Shoprite",
#         "Target": "http://127.0.0.1:3000/Target",
#     }

#     # Iterate over the URLs and make requests
#     for store, url in urls.items():
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 # Store was successfully scraped
#                 results[store]["success"] = True
#                 results[store]["data"] = response.json()
#             else:
#                 # Store scraping failed
#                 print(f"Failed to scrape {store}, status code: {response.status_code}")
#         except requests.RequestException as e:
#             print(f"RequestException for {store}: {e}")
    
#     # Return the results together
#     return jsonify(results)