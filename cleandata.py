import json
import re
import openai

openai.api_key = "YOUR_API_KEY"

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

def enrich_data_with_openai(product_data):
    """
    Uses the OpenAI API to generate summaries based on product data.
    """
    try:
        # write a prompt
        prompt = (f"Provide a summary and key insights for a product in a retail setting.\n\n"
                  f"Product Name: {product_data.get('name', 'Unknown Product')}\n"
                  f"Size: {product_data.get('size', 'N/A')}\n"
                  f"Rating: {product_data.get('rating', 'No rating available')}\n"
                  f"Review Count: {product_data.get('review_count', 0)}\n"
                  f"Price Info: {product_data.get('price_info', 'Price not available')}\n"
                  f"Product Image URL: {product_data.get('image_url', '')}\n\n"
                  f"Create a helpful summary that includes:\n"
                  f"1. A brief product description.\n"
                  f"2. Key highlights based on rating and reviews.\n"
                  f"3. Any notable considerations or unique attributes.\n\n"
                  f"Summary:")

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        
        summary = response.choices[0].text.strip()
        product_data['openai_summary'] = summary if summary else "No summary available"
    
    except openai.error.OpenAIError as e:
        print(f"Error with OpenAI API: {e}")
        product_data['openai_summary'] = "Error generating summary"
    
    return product_data

# Example usage function
def process_and_clean(file_path):
    """
    Reads data from a JSON file, processes each entry
    """
    cleanupproducts = []
    
    # Read, clean, and enrich each product entry
    for product_data in read_json(file_path):
        print(f"Processing product: {product_data.get('name', 'Unnamed Product')}")
        
        cleaned_data = enhanced_cleaning(product_data)
        
        enriched_data = enrich_data_with_openai(cleaned_data)
        
        cleanupproducts.append(enriched_data)
    
    return cleanupproducts

file_path = "walgreens.json"

processed_data = process_and_clean(file_path)

for product in processed_data:
    print(json.dumps(product, indent=2))