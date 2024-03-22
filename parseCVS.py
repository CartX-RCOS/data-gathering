import json

all_possible_endings = ["ct", "CT", "oz", "OZ", "mg", "MG", "pack"]

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

# parses the function
def parseCVS(data):
    print(data)
    ret = {}
    name_list = data["name"].split("-")
    answer = (get_size_info(name_list));

    if (answer[0] != 0):

        display = True

        # there is still something wrong
        for j in range(0,len(answer[1])):
            if (contains_substring(answer[1][j], all_possible_endings) == True):
                display = False
                break

        if (display == True): 
            data["name"] = join_with_apostrophe(answer[1])
            data["size"] = answer[2]
            data["quantity"] = answer[3]
            data["count"] = 1
    return data

with open('cvs.json', 'r') as file:
    data = json.load(file)

results = []

for item in data:
    ret = parseCVS(item)

    if (len(ret) != 0):
        print(ret)
        print("\n")
        results.append(ret)

with open('parsed_cvs.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)