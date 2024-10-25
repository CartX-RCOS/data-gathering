from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import json
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

all_products = []
items = ["Chips"]

for item_name in items:
    url = f"https://www.cvs.com/search?searchTerm={item_name}"

    driver.get(url)

    time.sleep(5)

    html_content = driver.page_source

    match = re.search(r'var productSearchData = (.*?);', html_content, re.DOTALL)
    
    if match:
        data_str = match.group(1)
        data = json.loads(data_str)

        if 'products' in data:
            for product in data['products']:
                item_dict = {}
                item_dict["item"] = item_name
                categories = [breadcrumb["title"] for breadcrumb in product.get("breadcrumbs", [])]

                item_dict["categories"] = categories
                item_dict["name"] = product.get("handle", "")
                item_dict["price"] = product.get("price", {}).get("value", "")
                
                sizes = []
                if "options" in product and product["options"] and "values" in product["options"][0]:
                    sizes = [option.get("value", "") for option in product["options"][0].get("values", [])]
                item_dict["sizes"] = sizes

                item_dict["images"] = [img.get("uri", "") for img in product.get("images", [])]

                all_products.append(item_dict)
                print(item_dict)
        else:
            print(f"No products found for item '{item_name}'.")
    else:
        print(f'productSearchData variable not found in the page for item "{item_name}".')

with open("aggregated_cvs_products.json", 'w', encoding='utf-8') as json_file:
    json.dump(all_products, json_file, indent=4, ensure_ascii=False)

driver.quit()

print(all_products)