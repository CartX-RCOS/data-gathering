from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import subprocess

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

def scroll_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in background
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        page_source = driver.page_source
    finally:
        driver.quit()

    return page_source

def scape_walgreens(items):
    all_products = []

    for item_name in items:
        url = f"https://www.walgreens.com/search/results.jsp?Ntt={item_name}"
        page_source = scroll_page(url)
        soup = BeautifulSoup(page_source, 'html.parser')
        product_card_container = soup.find('div', class_='product-card-container')

        if product_card_container:
            ul_tag = product_card_container.find('ul')
            if ul_tag:
                products = ul_tag.findAll('li')

                for product in products:
                    product_data = {}

                    title_tag = product.find("h3", class_="description")
                    if title_tag:
                        full_text = title_tag.get_text(strip=True)
                        name = full_text.split(" - ")[0].replace('\u00a0', ' ').strip('- ')
                    else:
                        name = "Name not available"
                        continue

                    product_data["name"] = name
                    product_data['image_url'] = product.find("img")['src'] if product.find("img") else "Image URL not available"
                    
                    # Extract size and clean it
                    size_tag = product.find("span", class_="amount")
                    if size_tag:
                        raw_size = size_tag.text.strip()
                        # Remove unwanted characters and normalize the string
                        cleaned_size = raw_size.replace("-\u00a0", "").strip()
                        product_data['size'] = cleaned_size
                    else:
                        product_data['size'] = "Size not available"
                    
                    rating_tag = product.find("img", alt=True)
                    product_data['rating'] = rating_tag['alt'] if rating_tag else "Rating not available"
                    product_data['review_count'] = product.find("figcaption").text if product.find("figcaption") else "Review count not available"
                    price_info_tag = product.find("div", class_="product__price-contain")
                    product_data['price_info'] = price_info_tag.text.strip() if price_info_tag else "Price information not available"
                    all_products.append(product_data)
            else:
                print(f"No product list found for {item_name}")
        else:
            print(f"No product card container found for {item_name}")

    return all_products

with open("../../itemsToScrape.txt", "r", encoding="utf-8") as f:
    itemsToScrape = [line.strip() for line in f if line.strip()]

allProducts = []

for item in itemsToScrape:
    scraped_product = scape_walgreens(item)
    embedded_product_data = get_embedding_for_product(scraped_product)
    if embedded_product_data:
        allProducts.append(embedded_product_data)
    else:
        print("Failed to embed product data for:", scraped_product["name"])

json_file_path = "walgreens.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(allProducts, json_file, indent=4, ensure_ascii=False)

print("done")