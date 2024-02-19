from flask import Blueprint, jsonify, request
import requests

database = Blueprint('database', __name__)

@database.route('/put-data', methods=['POST'])
def databasedata():
    # process_data_response = requests.get("http://127.0.0.1:3000/process-data")
    # if process_data_response.status_code != 200:
    #     return jsonify({"error": "Failed to fetch processed data"}), 500

    # process_data = process_data_response.json()

    # # returns list of stores and true if the data was sucessfully inserted
    # result = {}
    # for store, store_data in process_data["Parsed Data"].items():
    #     if store_data["success"]:
    #         print(f"{store}: Success")
    #         result[store] = "Success"
    #     else:
    #         print(f"{store}: Failed")
    #         result[store] = "Failed"

    return jsonify({"Database Insertion Results": "good"})
