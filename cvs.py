import requests
import re
import json

from pymongo import MongoClient 
client = MongoClient("") 
mydatabase = client['inventory']
cvs_collection = mydatabase['cvs'] 

# possible endings
all_possible_endings = ["ct", "CT", "oz", "OZ", "mg", "MG", "pack"]

# extracts CVS data
def extractCVSData(item_name, data):
    item_dict = {}
    
    name_list = data.get("handle", "").split("-")
    answer = (get_size_info(name_list));

    if (answer[0] != 0):
        display = True

        # there is still something wrong
        for j in range(0,len(answer[1])):
            if (contains_substring(answer[1][j], all_possible_endings) == True):
                display = False
                break

        if (display == True): 
            item_dict["item"] = item_name
            item_dict["name"] = join_with_apostrophe(answer[1])
            categories = [breadcrumb["title"] for breadcrumb in data.get("breadcrumbs", [])]
            item_dict["categories"] = categories
            item_dict["price"] = data.get("price", {}).get("value", "")
            item_dict["size"] = answer[2]
            item_dict["quantity"] = answer[3]
            item_dict["count"] = 1
            item_dict["images"] = [img.get("uri", "") for img in data.get("images", [])]

    return item_dict

# checks if there is something wrong
def contains_substring(main_str, substrings):
    main_str = main_str.lower()  # Convert to lowercase for case-insensitive comparison
    for substring in substrings:
        sub = substring.lower()
        # Check if the main string starts or ends with the substring
        if main_str.startswith(sub) or main_str.endswith(sub):
            return True
    return False

# gets the size
def get_size_info(elements):
    # Initialize default values
    index = -1
    size = None
    size_type = None

    # Check if the last two elements are numbers (considering a decimal size)
    if len(elements) >= 3 and elements[-3].replace('.', '', 1).isdigit() and elements[-2].isdigit():
        size = f"{elements[-3]}.{elements[-2]}"  # Format as "X.Y ounces"
        size_type = elements[-1]
        index = -3  # Update index if a decimal size is identified
    elif elements[-2].isdigit():
        size = f"{elements[-2]}"  # Format as "X ounces" if only one number is present
        size_type = elements[-1]
        index = -2  # Update index for a whole number size
    else:
        return 0,0,0,0
    
    return index, elements[0:(len(elements)+index)], size, size_type

# joins the name of the products
def join_with_apostrophe(words):
    # Initialize an empty string to hold the result
    result = ''
    # Iterate over the list of words
    for i in range(len(words)):
        # If the current word is 's' (and it's not the first word), prepend it with an apostrophe
        if words[i] == 's' and i > 0:
            result += "'" + words[i]
        else:
            # If it's not a special case, just append the word
            # Add a space before the word if it's not the first word
            if i > 0:
                result += ' '
            result += words[i]
    return result.capitalize()

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
                        if (len(processed_product) != 0):
                            all_products.append(processed_product)
                    
            else:
                print(f'productSearchData variable not found in the page for item "{item_name}".')
        else:
            print(f"Failed to retrieve data for item \"{item_name}\", status code: {response.status_code}")
    
    # Save aggregated products data to a JSON file
    with open("aggregated_cvs_products.json", 'w', encoding='utf-8') as json_file:
        json.dump(all_products, json_file, indent=4, ensure_ascii=False)

        # add data to the mongo db database
        cvs_collection.insert_many(all_products)
    return all_products

# Bread
# Milk
# Eggs
# Apples
# Bananas
# Pasta
# Cheese
# Butter

items = ["Butter"]
aggregated_data = scrape_cvs(items)