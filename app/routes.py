from flask import Blueprint, jsonify
import requests

main = Blueprint('main', __name__)

@main.route('/CVS')
def CVS():
    # fetching logic for CVS
    return jsonify({"data": "CVS data will be scraped here"})

@main.route('/Shoprite')
def Shoprite():
    # fetching logic for Shoprite
    return jsonify({"data": "Shoprite data will be scraped here"})

@main.route('/Target')
def Target():
    # fetching logic for Shoprite
    return jsonify({"data": "Target data will be scraped here"})

@main.route('/scrape')
def getData():
    # Dictionary that holds the status and data for each store
    results = {
        "CVS": {"success": False, "data": None},
        "Shoprite": {"success": False, "data": None},
        "Target": {"success": False, "data": None}
    }
    
    # URLs for each store scrape endpoint
    urls = {
        "CVS": "http://127.0.0.1:3000/CVS",
        "Shoprite": "http://127.0.0.1:3000/Shoprite",
        "Target": "http://127.0.0.1:3000/Target",
    }

    # Iterate over the URLs and make requests
    for store, url in urls.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Store was successfully scraped
                results[store]["success"] = True
                results[store]["data"] = response.json()
            else:
                # Store scraping failed
                print(f"Failed to scrape {store}, status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"RequestException for {store}: {e}")
    
    # Return the results together
    return jsonify(results)