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

# cleaning function for product data
def enhanced_cleaning(product_data):
    """
    this function performs cleaning on product data
    """
    # Remove extra spaces, ensure it’s a string
    if 'name' in product_data:
        product_data['name'] = re.sub(r'\s+', ' ', product_data['name']).strip().lower()
    else:
        product_data['name'] = "Unknown Product"

    # handle empty sizes
    if 'size' in product_data:
        product_data['size'] = re.sub(r'\s+', ' ', product_data['size']).strip()
    else:
        product_data['size'] = "N/A" 

    # validate 'rating' 
    if 'rating' in product_data:
        product_data['rating'] = product_data['rating'].strip()
        if not product_data['rating']:  # Handle cases where rating may be empty
            product_data['rating'] = "No rating available"
    else:
        product_data['rating'] = "No rating available"

    # Extract number of reviews or set default
    if 'review_count' in product_data:
        review_count = re.sub(r'[^\d]', '', product_data['review_count']).strip()
        product_data['review_count'] = int(review_count) if review_count.isdigit() else 0
    else:
        product_data['review_count'] = 0

    # Remove placeholder or undefined text
    if 'price_info' in product_data:
        product_data['price_info'] = product_data['price_info'].strip()
        if "Price available" in product_data['price_info']:  # Handle non-specific price text
            product_data['price_info'] = "Check in store for price"
    else:
        product_data['price_info'] = "Price not available"

    # Validate 'image_url' field
    if 'image_url' in product_data:
        if not re.match(r'https?://', product_data['image_url']):
            product_data['image_url'] = f"https:{product_data['image_url']}" 
    else:
        product_data['image_url'] = "https://example.com/placeholder.jpg"

    return product_data


# Example usage function
def process_and_clean(file_path):
    """
    Reads data from a JSON file, processes each entry with basic cleaning
    """
    cleaned_products = []
    
    for product_data in read_json(file_path):
        print(f"Processing product: {product_data.get('name', 'Unnamed Product')}")
        
        cleaned_data = enhanced_cleaning(product_data)
        
        cleaned_products.append(cleaned_data)
    
    return cleaned_products

file_path = "products.json"

processed_data = process_and_clean(file_path)

for product in processed_data:
    print(json.dumps(product, indent=2))