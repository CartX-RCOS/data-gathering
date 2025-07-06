from flask import Flask, request, jsonify
from target_scraper import scrape_target_website, deduplicate_data
import os
import json

# Initialize Flask application
app = Flask(__name__)

# Route for scraping Target's website
@app.route('/scrape', methods=['PUT'])
def scrape():
    try:
        # Extract item name from the request body
        item = request.json.get('item')
        if not item:
            return jsonify({'error': 'Item name is required'}), 400

        # Call the scraping function
        data = scrape_target_website(item)

        # Define storage folder and file path
        storage_folder = os.path.join(os.getcwd(), 'storage', 'target')
        os.makedirs(storage_folder, exist_ok=True)
        file_path = os.path.join(storage_folder, f"{item}.json")

        # Check if the file already exists and deduplicate data if needed
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
    # Start the Flask application
    app.run(debug=True)
