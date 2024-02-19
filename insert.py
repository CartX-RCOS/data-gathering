# import mysql.connector
# import json

# # Function to establish a connection to the MySQL database
# def connect_to_database():
#     return mysql.connector.connect(
#         host="cartx.cfkeigas058z.us-east-2.rds.amazonaws.com",  # e.g., "localhost"
#         user="admin",  # e.g., "root"
#         passwd="cartx#rcos",  
#         database="CVS"  # Your database name
#     )

# # Function to insert data into tables
# def insert_data(products):
#     db_conn = connect_to_database()
#     cursor = db_conn.cursor()

#     for product in products:
#         # Insert product
#         cursor.execute("INSERT INTO Products (Name, Price) VALUES (%s, %s)", (product['name'], product['price']))
#         product_id = cursor.lastrowid
        
#         # Insert categories and link to product
#         for category in product['categories']:
#             cursor.execute("SELECT CategoryID FROM Categories WHERE CategoryName = %s", (category,))
#             category_id = cursor.fetchone()
#             if not category_id:
#                 cursor.execute("INSERT INTO Categories (CategoryName) VALUES (%s)", (category,))
#                 category_id = cursor.lastrowid
#             else:
#                 category_id = category_id[0]
#             cursor.execute("INSERT INTO ProductCategories (ProductID, CategoryID) VALUES (%s, %s)", (product_id, category_id))
        
#         # Insert sizes and link to product
#         for size in product['sizes']:
#             cursor.execute("SELECT SizeID FROM Sizes WHERE SizeName = %s", (size,))
#             size_id = cursor.fetchone()
#             if not size_id:
#                 cursor.execute("INSERT INTO Sizes (SizeName) VALUES (%s)", (size,))
#                 size_id = cursor.lastrowid
#             else:
#                 size_id = size_id[0]
#             cursor.execute("INSERT INTO ProductSizes (ProductID, SizeID) VALUES (%s, %s)", (product_id, size_id))
        
#         # Insert images
#         for image_url in product['images']:
#             cursor.execute("INSERT INTO Images (ProductID, ImageURL) VALUES (%s, %s)", (product_id, image_url))

#     db_conn.commit()
#     cursor.close()
#     db_conn.close()

# # Load the products data from JSON
# with open('products.json', 'r') as file:
#     products_data = json.load(file)

# # Flatten the list if it's nested
# if isinstance(products_data, list) and len(products_data) == 1 and isinstance(products_data[0], list):
#     products_data = products_data[0]

# # Insert the data into the database
# insert_data(products_data)

import mysql.connector

# def connect_to_database():
#         return mysql.connector.connect(
#         host="cartx.cfkeigas058z.us-east-2.rds.amazonaws.com",  # e.g., "localhost"
#         user="admin",  # e.g., "root"
#         passwd="cartx#rcos",  
#         database="CVS"  # Your database name
#     )

# def fetch_and_print_products():
#     db_conn = connect_to_database()
#     cursor = db_conn.cursor()

#     cursor.execute("SELECT ProductID, Name, Price FROM Products")

#     print("ProductID, Name, Price")
#     for (product_id, name, price) in cursor:
#         print(f"{product_id}, {name}, {price}")

#     cursor.close()
#     db_conn.close()

# fetch_and_print_products()

import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="cartx.cfkeigas058z.us-east-2.rds.amazonaws.com",  # e.g., "localhost"
        user="admin",  # e.g., "root"
        passwd="cartx#rcos",  
        database="CVS"  # Your database name
    )

def fetch_and_print_product_details():
    db_conn = connect_to_database()
    cursor = db_conn.cursor()

    # A complex query that joins multiple tables to fetch product details along with categories, sizes, and images
    query = """
    SELECT p.ProductID, p.Name, p.Price, c.CategoryName, s.SizeName, i.ImageURL
    FROM Products p
    LEFT JOIN ProductCategories pc ON p.ProductID = pc.ProductID
    LEFT JOIN Categories c ON pc.CategoryID = c.CategoryID
    LEFT JOIN ProductSizes ps ON p.ProductID = ps.ProductID
    LEFT JOIN Sizes s ON ps.SizeID = s.SizeID
    LEFT JOIN Images i ON p.ProductID = i.ProductID
    ORDER BY p.ProductID, c.CategoryName, s.SizeName, i.ImageURL
    """

    cursor.execute(query)

    current_product_id = None
    for (product_id, name, price, category_name, size_name, image_url) in cursor:
        if product_id != current_product_id:
            print(f"\nProductID: {product_id}, Name: {name}, Price: {price}")
            current_product_id = product_id
        if category_name:
            print(f"    Category: {category_name}")
        if size_name:
            print(f"    Size: {size_name}")
        if image_url:
            print(f"    Image URL: {image_url}")

    cursor.close()
    db_conn.close()

fetch_and_print_product_details()
