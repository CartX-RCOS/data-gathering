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

# Scrape Target website for item data
def scrape_target_website(item_name):
    zipcode = "10954"
    products = []

    # Set Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    div_index = 0

    try:
        url = f"https://www.target.com/s?searchTerm={item_name}&tref=typeahead%7Cterm%7C{item_name}%7C%7C%7Chistory"
        driver.get(url)

        scroll_height = 800
        curr_height = 0
        max_scroll_height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )

        driver.execute_script("window.scrollBy(0, 400);")
        curr_height += 400
        time.sleep(4)

        for check_index in range(1, 10):
            xpath_to_check = f'//*[@id="pageBodyContainer"]/div[1]/div[1]/div[1]/div[{check_index}]/div[1]/div[1]/section[1]/div[1]'
            if is_xpath_valid(xpath_to_check, driver):
                div_index = check_index
                break

        if div_index == 9:
            driver.quit()
            return []

        for item_number in range(1, 26):
            try:
                xpath_type = f'//*[@id="pageBodyContainer"]/div[1]/div[1]/div[1]/div[{div_index}]/div[1]/div[1]/section[1]/div[1]/div[{item_number}]'
                element_type = driver.find_element(By.XPATH, xpath_type).text.strip()

                if element_type == "Sponsored":
                    continue

                element_type_array = element_type.split('\n')

                image_xpath = f'//*[@id="pageBodyContainer"]/div[1]/div[1]/div[1]/div[{div_index}]/div[1]/div[1]/section[1]/div[1]/div[{item_number}]/div[1]/div[1]/div[1]/div[1]/h3[1]/div[1]/div[1]/a[1]/div[1]/picture[1]/img[1]'
                image_source = driver.find_element(By.XPATH, image_xpath).get_attribute("src")

                element_type_array.append(image_source)
                products.append(element_type_array)

                if max_scroll_height > curr_height:
                    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
                    time.sleep(0.5)
                    curr_height += scroll_height

            except Exception as error:
                print(f"Error: {error}")

    finally:
        driver.quit()

    return products


@app.route('/scrape', methods=['PUT'])
def scrape():
    try:
        item = request.json.get('item')
        if not item:
            return jsonify({'error': 'Item name is required'}), 400

        data = scrape_target_website(item)

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
