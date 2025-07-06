import subprocess
import json
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# Function to get embeddings for a single product
def get_embedding_for_product(product_data):
    temp_file = "temp_product.json"
    with open(temp_file, 'w', encoding='utf-8') as temp_json_file:
        json.dump(product_data, temp_json_file)
    result = subprocess.run(["node", "../../vectorize.js", temp_file], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running JavaScript code:", result.stderr)
        return None
    embedded_product = json.loads(result.stdout)
    return embedded_product

# Set up the WebDriver
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)
url = f"https://www.hannaford.com/search/product?form_state=searchForm&keyword=cookies&ieDummyTextField=&productTypeId=P"
driver.get(url)

all_products = []

with open("../../itemsToScrape.txt", "r", encoding="utf-8") as f:
    itemsToScrape = [line.strip() for line in f if line.strip()]

for item in itemsToScrape:
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

    search_bar = driver.find_element(By.ID, 'search-input')
    search_bar.click()
    search_bar.clear()
    search_bar.send_keys(item)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(5)

    def close_feedback_popup():
        try:
            no_thanks_button = driver.find_element(By.CLASS_NAME, 'fsrDeclineButton')
            no_thanks_button.click()
            time.sleep(1)
            return True
        except NoSuchElementException:
            try:
                close_button = driver.find_element(By.CLASS_NAME, 'fsrInvite__closeWrapper')
                close_button.click()
                time.sleep(1)
                return True
            except NoSuchElementException:
                return False

    while True:
        try:
            if close_feedback_popup():
                print("Popup closed.")
            see_more_button = driver.find_element(By.ID, 'see-more-btn')
            driver.execute_script("arguments[0].scrollIntoView(true);", see_more_button)
            time.sleep(1)
            see_more_button.click()
            time.sleep(2)
        except NoSuchElementException:
            break

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    thumbnail_container = soup.find('div', class_='entity-thumbnail-container row', id='thumbnail-container')
    product_divs = thumbnail_container.find_all('div', class_='plp_thumb_wrap product-impressions')

    for product_div in product_divs:
        product_data = {
            "root_category": product_div.get('data-root-category'),
            "categories": product_div.get('data-category'),
            "name": product_div.get('data-name'),
            "price": product_div.get('data-price'),
            "size": product_div.find('span', class_='overline text-truncate').text.strip() if product_div.find('span', class_='overline text-truncate') else 'No size information',
            "image_links": [],
            "product_url": "https://www.hannaford.com" + product_div.find('div', class_='catalog-product')['data-url'] if product_div.find('div', class_='catalog-product') else 'No URL'
        }

        if product_div.find('img'):
            img_src = product_div.find('img')['src']
            if img_src == '/assets/hf/assets/images/common/noimage.gif':
                product_data['image_links'].append('https://eagle-sensors.com/wp-content/uploads/unavailable-image.jpg')
            else:
                product_data['image_links'].append(img_src)

        # Perform real-time vectorization
        embedded_product_data = get_embedding_for_product(product_data)
        if embedded_product_data:
            all_products.append(embedded_product_data)
        else:
            print("Failed to embed product data for:", product_data["name"])

json_file_path = "hannaford.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_products, json_file, indent=4, ensure_ascii=False)

print("Added data to the database!")

# Close the WebDriver
driver.quit()
