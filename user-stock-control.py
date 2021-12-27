# import dbase, connection and cursor to connect to DB.
from dbase import *
from connection import connection, cursor

# initialize object from dbase
db = dbase(cursor, connection)

# Client Object
class client:
    def __init__(self, name, personal_id, vat_number, address, phone_number, email):
        self.name = name
        self.personal_id = personal_id
        self.vat_number = vat_number
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def new_client():
        name = input('Name:')
        personal_id = input('Personal ID Number:')
        vat_number = input('VAT Number:')
        address = input('Address:')
        phone_number = input('Phone Number:')
        email = input('Email:')
        newClient = client(name, personal_id, vat_number, address, phone_number, email)
        db.insert_client(newClient)
        client_num = db.get_client_num()
        newClientCard = client_card(name, personal_id, vat_number, address, phone_number, email, str(client_num), "0")
        db.insert_client_card(newClientCard)

    def remove_client():
        db.delete_client()

    def update_client():
        db.update_client()

    def search_client():
        db.search_clients()

# Card Object
class client_card:
    def __init__(self, name, personal_id, vat_number, address, phone_number, email, client_num, points):
        self.name = name
        self.personal_id = personal_id
        self.vat_number = vat_number
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.client_num = client_num
        self.points = points
        self.purchases = []

# Product Object
class product:
    def __init__(self, product_name, price, stock):
        self.product_name = product_name
        self.price = price
        self.stock = stock

    def new_product():
        product_name = input('Product Name:')
        price = input('Price:')
        stock = input('Quantity:')
        newProduct = product(product_name, price, stock)
        db.insert_product(newProduct)
    
    def remove_product():
        db.delete_product()

    def update_product():
        db.update_product()

    def search_product():
        db.search_products()

# Purchases Object
class purchases:
    def __init__(self, product_id, qtt):
        self.product_id = product_id
        self.qtt = qtt

# Main Menu
def menu():
    while True:
        print("\nMenu:\n1.Clients\n2.Products\n3.Register Purchase\n4.Exit")
        select = int(input("\nOption: "))

        if select > 0 and select < 5:
            return select

# Clients Menu   
def clients_menu():
    while True:
        print("\nClient Menu:\n1.Insert Client\n2.Delete Client\n3.Update Client\n4.Search Client\n5.Exit")
        select = int(input("\nOption: "))

        if select > 0 and select < 6:
            return select

# Products Menu  
def products_menu():
    while True:
        print("\nProduct Menu:\n1.Insert Product\n2.Delete Product\n3.Update Product\n4.Product Search\n5.Exit")
        select = int(input("\nOption: "))

        if select > 0 and select < 6:
            return select

# Sales Menu 
def sales_menu():
    while True:
        print("\nSales Menu:\n1.Register Purchase\n2.Consult Sells\n3.Exit")
        select = int(input("\nOption: "))

        if select > 0 and select < 4:
            return select

# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------
cont = 1

while cont != 0:

    sel = menu()

    if sel == 1:

        clients_option = clients_menu()

        if clients_option == 1:
            client.new_client()
        elif clients_option == 2:
            client.remove_client()
        elif clients_option == 3:
            client.update_client()
        elif clients_option == 4:
            client.search_client()
        else:
            cont = 0

    elif sel == 2:

        products_option = products_menu()

        if products_option == 1:
            product.new_product()
        elif products_option == 2:
            product.remove_product()
        elif products_option == 3:
            product.update_product()
        elif products_option == 4:
            product.search_product()
        else:
            cont = 0

    elif sel == 3:
        select = sales_menu()
        
        if select == 1:
            c = 1
            shopping_list=[]
            while c != 0:
                print('1. Register\n2. Completed')
                option = int(input('Option: '))
                if option == 1:
                    id = input('Insert product ID: ')
                    qtt = input('Insert quantity: ')
                    shopping_list.append(purchases(id, qtt)) 

                else:
                    card_number = input('Insert Client Card Number? ')
                    db.register_purchases(shopping_list, card_number)
                    db.calculate_points(shopping_list, card_number)
                    c = 0
            
        elif select == 2:
            db.display_purchases()
        else:
            cont = 0

    else:
        cont = 0
        
connection.close()
