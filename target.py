from flask import Flask, request, jsonify
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# Helper function to check if XPath is valid
def is_xpath_valid(xpath, driver):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except Exception:
        return False

# Function to deduplicate data based on a unique identifier (index 0)
def deduplicate_data(existing_data, new_data):
    unique_identifiers = set(item[0] for item in existing_data)
    deduplicated_data = existing_data[:]

    for new_item in new_data:
        if new_item[0] not in unique_identifiers:
            deduplicated_data.append(new_item)
            unique_identifiers.add(new_item[0])

    return deduplicated_data


@app.route('/scrape', methods=['PUT'])
def scrape():
    try:
        item = request.json.get('item')
        if not item:
            return jsonify({'error': 'Item name is required'}), 400

        # data = scrape_target_website(item)

        storage_folder = os.path.join(os.getcwd(), 'storage', 'target')
        os.makedirs(storage_folder, exist_ok=True)
        file_path = os.path.join(storage_folder, f"{item}.json")

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                existing_data = json.load(f)

            merged_data = deduplicate_data(existing_data, data)

            with open(file_path, 'w') as f:
                json.dump(merged_data, f, indent=2)
        else:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

        return jsonify(data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch data from Target'}), 500

if __name__ == '__main__':
    app.run(debug=True)
