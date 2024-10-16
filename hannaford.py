from selenium import webdriver
from bs4 import BeautifulSoup
import json

# Set up the WebDriver
driver = webdriver.Chrome()

item = "cookies"

# URL you want to load
url = f"https://www.hannaford.com/search/product?form_state=searchForm&keyword={item}&ieDummyTextField=&productTypeId=P"

# Load the webpage
driver.get(url)

all_products = []

# Get the HTML content of the loaded page
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
thumbnail_container = soup.find('div', class_='entity-thumbnail-container row', id='thumbnail-container')
product_divs = thumbnail_container.find_all('div', class_='plp_thumb_wrap product-impressions')

# parses the HTML code
for product_div in product_divs:
    product_data = {
        "root_category": product_div.get('data-root-category'),
        "categories": product_div.get('data-category'),
        "name": product_div.get('data-name'),
        "price": product_div.get('data-price'),
        "size": product_div.find('span', class_='overline text-truncate').text.strip() if product_div.find('span', class_='overline text-truncate') else 'No size information',
        "image_links": [product_div.find('img')['src']] if product_div.find('img') else [],
        "product_url": "https://www.hannaford.com" + product_div.find('div', class_='catalog-product')['data-url'] if product_div.find('div', class_='catalog-product') else 'No URL'
    }

# add all products
all_products.append(product_data)

# save all the data that is scraped to a json file
json_file_path = "hannaford.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_products, json_file, indent=4, ensure_ascii=False)

# Close the WebDriver
driver.quit()