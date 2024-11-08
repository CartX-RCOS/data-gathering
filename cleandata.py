import json
import re

def read_json(file_path):
    """
    function to read each line from the JSON file
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                yield json.loads(line)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")

# Basic cleaning function for product data
def basic_cleaning(product_data):
    """
    This function performs basic cleaning on product data
    """
    if 'name' in product_data:
        product_data['name'] = re.sub(r'\s+', ' ', product_data['name']).strip().lower()
    
    if 'size' in product_data:
        product_data['size'] = re.sub(r'\s+', ' ', product_data['size']).strip()
    
    if 'rating' in product_data:
        product_data['rating'] = product_data['rating'].strip()
    
    if 'review_count' in product_data:
        product_data['review_count'] = re.sub(r'[^\d]', '', product_data['review_count']).strip()
    
    if 'price_info' in product_data:
        product_data['price_info'] = product_data['price_info'].strip()
    
    return product_data

# Example usage function
def process_and_clean(file_path):
    """
    Reads data from a JSON file, processes each entry with basic cleaning
    """
    cleaned_products = []
    
    for product_data in read_json(file_path):
        print(f"Processing product: {product_data.get('name', 'Unnamed Product')}")
        
        cleaned_data = basic_cleaning(product_data)
        
        cleaned_products.append(cleaned_data)
    
    return cleaned_products

file_path = "products.json"

processed_data = process_and_clean(file_path)

for product in processed_data:
    print(json.dumps(product, indent=2))