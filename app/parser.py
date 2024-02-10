from flask import Blueprint, jsonify
import requests

parser = Blueprint('parser', __name__)

@parser.route('/process-data')
def process_scraped_data():
    # fetch data from your /scrape endpoint
    scraped_data_response = requests.get("http://127.0.0.1:3000/scrape")
    if scraped_data_response.status_code != 200:
        return jsonify({"error": "Failed to fetch scraped data"}), 500

    scraped_data = scraped_data_response.json()

    # Here we will process scraped_data with our parser model
    processed_data = {"processed_data": scraped_data}

    return jsonify(processed_data)