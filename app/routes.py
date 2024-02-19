from flask import Flask, Blueprint, jsonify, request
import json

from scraper import scrape_cvs

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

    # loop through items and then scrape the data
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