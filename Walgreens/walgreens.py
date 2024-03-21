from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json

def scroll_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in background
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
                    product_data['name'] = product.find("strong", class_="description").text.strip() if product.find("strong", class_="description") else "Name not available"
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

items = ["Cheese", "Apples", "Eggs"]
scraped_products = scape_walgreens(items)

# Save the data to a JSON file
with open('products.json', 'w') as f:
    json.dump(scraped_products, f, indent=4)

print("done")