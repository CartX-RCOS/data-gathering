from bs4 import BeautifulSoup
import requests
import json

def scrape_hannaford(items):
    all_products = []  # List to aggregate all products from different searches

    for item_name in items:
        url = f"https://www.hannaford.com/search/product?form_state=searchForm&keyword={item_name}&ieDummyTextField=&productTypeId=P"
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch data for {item_name}")
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        thumbnail_container = soup.find('div', class_='entity-thumbnail-container row', id='thumbnail-container')

        if thumbnail_container:
            product_divs = thumbnail_container.find_all('div', class_='plp_thumb_wrap product-impressions')

            for product_div in product_divs:
                product_data = {
                    "item": item_name,  # Adding item name to each product data
                    "categories": product_div.get('data-category'),
                    "name": product_div.get('data-name'),
                    "brand": product_div.get('data-brand').strip(),
                    "price": product_div.get('data-price'),
                    "size": product_div.find('span', class_='overline text-truncate').text.strip().replace("\n", " ").replace("  ", " ") if product_div.find('span', class_='overline text-truncate') else 'No pricing unit',
                    "average_weight": product_div.find('p', class_='unitPriceDisplay').text.strip() if product_div.find('p', class_='unitPriceDisplay') else 'No average weight',
                    "images_links": [{
                        "product_url": "https://www.hannaford.com" + product_div.find('div', class_='catalog-product')['data-url'] if product_div.find('div', class_='catalog-product') else 'No URL',
                        "product_image_url": product_div.find('img')['src'] if product_div.find('img') else 'No image URL',
                        "product_image_alt_text": product_div.find('img')['alt'] if product_div.find('img') else 'No alt text',
                    }]
                }

                all_products.append(product_data)
        else:
            print(f"Product container not found for {item_name}")

    # Save aggregated products data to a JSON file
    json_file_path = "test.json"
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_products, json_file, indent=4, ensure_ascii=False)

    return all_products

# Example usage
# items = ["Chips", "Apples", "Cheese", "Milk"]
# scraped_products = scrape_hannaford(items)
# print("done")

import json

def split_size(size):
    size = size.strip()
    quantity, *size_parts = size.split()
    size_type = ' '.join(size_parts)
    return quantity, size_type.lower()

def process_items_from_file(json_file,output_file):
    with open(json_file, 'r') as f:
        items = json.load(f)

    modified_items = []  # Store modified items here
    for item in items:
        original_size = item.get('size', None)
        if original_size:
            quantity, size_type = split_size(original_size)
            item['quantity'] = quantity
            
            if ('.' in size_type):
                size_type = size_type.replace('.','');

            item['count'] = "1"
            del item['size']
            item['size'] = size_type
            modified_items.append(item)  

    # Print the modified items
    with open(output_file, 'w') as f:
        json.dump(modified_items, f, indent=4)

# Example usage
json_file = 'inventory.hannaford.json' 
output_file = 'modified_items.json' 
process_items_from_file(json_file, output_file)