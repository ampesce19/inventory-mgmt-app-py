#ampesce19
#CRUD_app

import csv
import os

def menu(username="ampesce19", products_count=100):
    menu = f"""
-----------------------------------
INVENTORY MANAGEMENT APPLICATION
-----------------------------------
Welcome {username}!
There are {products_count} products in the database.
    operation | description
    --------- | ------------------
    'List'    | Display a list of product identifiers and names.
    'Show'    | Show information about a product.
    'Create'  | Add a new product.
    'Update'  | Edit an existing product.
    'Destroy' | Delete an existing product.
Please select an operation: """
    return menu

def product_not_found():
    print("Error! Couldn't find a product with that identifier.")

def product_price_not_valid():
    print(f"Error! That product price is not valid. Please try again.")

csv_headers = ["id", "name", "aisle", "department", "price"]

def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    products = []
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for ordered_dict in reader:
            products.append(dict(ordered_dict))
    return products

def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("Resetting Defaults")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)

def find_product(product_id, all_products):
    matching_products = [p for p in all_products if int(p["id"]) == int(product_id)]
    matching_product = matching_products[0]
    return matching_product

def auto_incremented_product_id(products):
    if len(products) == 0:
        return 1
    else:
        product_ids = [int(p["id"]) for p in products]
        return max(product_ids) + 1

def editable_product_attributes():
    attribute_names = [attr_name for attr_name in csv_headers if attr_name != "id"]
    return attribute_names

def is_valid_price(my_price):
    try:
        float(my_price)
        return True
    except Exception as e:
        return False

def user_selected_product(all_products):
    try:
        product_id = input("Please enter the product's identifier: ")
        product = find_product(product_id, all_products)
        return product
    except ValueError as e: return None
    except IndexError as e: return None

def list_products(products):
    print(f"LISTING {len(products)} PRODUCTS:")
    for product in products:
        print(" #" + str(product["id"]) + ". " + product["name"])

def show_product(product):
    print("SHOWING A PRODUCT:")
    print(product)

def create_product(new_product, all_products):
    print("CREATING A NEW PRODUCT:")
    print(new_product)
    all_products.append(new_product)

def update_product(product):
    print("UPDATED A PRODUCT:")
    print(product)

def destroy_product(product, all_products):
    print("DESTROYING A PRODUCT:")
    print(product)
    del all_products[all_products.index(product)]

def run():
    products = read_products_from_file()

    my_menu = menu(username="ampesce19", products_count=len(products))
    operation = input(my_menu)

    operation = operation.title() #this will transform "show" to "Show" and accept either one
    if operation == "List":
        list_products(products)

    elif operation == "Show":
        product = user_selected_product(products)
        if product == None: product_not_found()
        else: show_product(product)

    elif operation == "Create":
        new_product = {}
        new_product["id"] = auto_incremented_product_id(products)
        for attribute_name in editable_product_attributes():
            new_val = input(f"Please input the product's '{attribute_name}': ")
            if attribute_name == "price" and is_valid_price(new_val) == False:
                product_price_not_valid()
                return
            new_product[attribute_name] = new_val
        create_product(new_product, products)

    elif operation == "Update":
        product = user_selected_product(products)
        if product == None: product_not_found()
        else:
            for attribute_name in editable_product_attributes():
                new_val = input(f"What is the product's new '{attribute_name}' (from '{product[attribute_name]}'): ")
                if attribute_name == "price" and is_valid_price(new_val) == False:
                    product_price_not_valid()
                    return
                product[attribute_name] = new_val
            update_product(product)

    elif operation == "Destroy":
        product = user_selected_product(products)
        if product == None: product_not_found()
        else: destroy_product(product, products)

    elif operation == "Reset":
        reset_products_file()

    else:
        print("Error! didn't recognize that operation. Please try again.")

    write_products_to_file(products=products)

if __name__ == "__main__":
    run()
