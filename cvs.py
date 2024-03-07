import requests
import re
import json

def extractCVSData(item_name, data):
    item_dict = {}
    item_dict["item"] = item_name
    categories = [breadcrumb["title"] for breadcrumb in data.get("breadcrumbs", [])]

    item_dict["categories"] = categories
    item_dict["name"] = data.get("handle", "")
    item_dict["price"] = data.get("price", {}).get("value", "")
    
    sizes = []
    if "options" in data and data["options"] and "values" in data["options"][0]:
        sizes = [option.get("value", "") for option in data["options"][0].get("values", [])]
    item_dict["sizes"] = sizes

    item_dict["images"] = [img.get("uri", "") for img in data.get("images", [])]

    return item_dict

def scrape_cvs(items):
    all_products = []  # List to aggregate products from all items

    for item_name in items:
        url = f"https://www.cvs.com/search?searchTerm={item_name}"
        response = requests.get(url)
        
        if response.status_code == 200:
            match = re.search(r'var productSearchData = (.*?);', response.text, re.DOTALL)
            
            if match:
                data_str = match.group(1)
                data = json.loads(data_str)

                if 'products' in data:
                    for product in data['products']:
                        processed_product = extractCVSData(item_name, product)
                        all_products.append(processed_product)
            else:
                print(f'productSearchData variable not found in the page for item "{item_name}".')
        else:
            print(f"Failed to retrieve data for item \"{item_name}\", status code: {response.status_code}")
    
    # Save aggregated products data to a JSON file
    with open("aggregated_cvs_products.json", 'w', encoding='utf-8') as json_file:
        json.dump(all_products, json_file, indent=4, ensure_ascii=False)

    return all_products

# Example usage for multiple items
items = ["Chips", "Apples", "Cheese", "Milk"]
aggregated_data = scrape_cvs(items)
print(aggregated_data)