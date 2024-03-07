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
    json_file_path = "aggregated_products.json"
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_products, json_file, indent=4, ensure_ascii=False)

    return all_products

# Example usage
items = ["Chips", "Apples", "Cheese", "Milk"]
scraped_products = scrape_hannaford(items)
print("done")