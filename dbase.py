'''
Validação de campos (ex stock / pontos)
Apresentar compras com base num_cartao - tabela compras
Correçao do stock pesquisando por nome do artigo
how to generic function sequel statments - google
'''



class dbase:
    
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def init_db(self):
        create_client = """
            CREATE TABLE `client` (
            `client_num` int(11) NOT NULL AUTO_INCREMENT,
            `name` varchar(100) COLLATE utf8_swedish_ci NOT NULL,
            `personal_id` varchar(22) COLLATE utf8_swedish_ci NOT NULL,
            `vat_number` varchar(22) COLLATE utf8_swedish_ci NOT NULL,
            `address` varchar(120) COLLATE utf8_swedish_ci NOT NULL,
            `phone_number` varchar(22) COLLATE utf8_swedish_ci NOT NULL,
            `email` varchar(50) COLLATE utf8_swedish_ci NOT NULL,
            PRIMARY KEY(client_num)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;
        """
        create_products = """
            CREATE TABLE `product` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `product_name` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
            `price` float NOT NULL,
            `stock` int(11) NOT NULL,
            PRIMARY KEY(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;
        """
        create_client_card = """
            CREATE TABLE `client_card` (
            `card_number` int(11) NOT NULL AUTO_INCREMENT,
            `name` varchar(100) COLLATE utf8_swedish_ci NOT NULL,
            `personal_id` varchar(22) COLLATE utf8_swedish_ci NOT NULL,
            `vat_number` varchar(22) COLLATE utf8_swedish_ci NOT NULL,
            `address` varchar(120) COLLATE utf8_swedish_ci NOT NULL,
            `phone_number` varchar(22) COLLATE utf8_swedish_ci NOT NULL,
            `email` varchar(50) COLLATE utf8_swedish_ci NOT NULL,
            `client_num` int(11) NOT NULL,
            `points` int(11) NOT NULL,
            PRIMARY KEY(card_number),
            FOREIGN KEY (`client_num`) REFERENCES `client` (`client_num`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;
        """
        create_sells="""
            CREATE TABLE `purchases` (
            `card_number` int(11) NOT NULL,
            `product_id` int(11) NOT NULL,
            `price` float NOT NULL,
            `quantity` int(11) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;
        """
        self.cursor.execute(create_client)
        self.cursor.execute(create_products)
        self.cursor.execute(create_client_card)
        self.cursor.execute(create_sells)
        self.connection.commit()

    # CLIENTS:
    # -----------------------------------------------------
    # Create Client
    def insert_client(self, client):
        insertClient = "INSERT INTO client(name, personal_id, vat_number, address, phone_number, email) VALUES('"+client.name+"','"+client.personal_id+"','"+client.vat_number+"','"+client.address+"','"+client.phone_number+"','"+client.email+"')"
        self.cursor.execute(insertClient)
        self.connection.commit()
    
    # Delete Cliente
    def delete_client(self):
        self.search_clients()
        client = input('Insert client ID to delete: ')
        remove_client = "DELETE FROM client WHERE client_num = '"+client+"'; "
        remove_card = "DELETE FROM client_card WHERE client_num = '"+client+"'; "
        self.cursor.execute(remove_card)
        self.cursor.execute(remove_client)
        self.connection.commit()
    
    # Update Cliente
    def update_client(self):
        self.search_clients()
        client = input('Insert client number to update: ')
        name = input('Name:')
        personal_id = input('Personal ID Number:')
        vat_number = input('VAT Number:')
        address = input('Address:')
        phone_number = input('Phone Number:')
        email = input('Email:')

        updateClient = "UPDATE client SET name= '"+name+"', personal_id= '"+personal_id+"', vat_number= '"+vat_number+"', address= '"+address+"', phone_number= '"+phone_number+"', email= '"+email+"' WHERE client_num = '"+client+"';"
        updateClientCard = "UPDATE client_card SET name= '"+name+"', personal_id= '"+personal_id+"', vat_number= '"+vat_number+"', address= '"+address+"', phone_number= '"+phone_number+"', email= '"+email+"' WHERE client_num = '"+client+"';"
        self.cursor.execute(updateClientCard)
        self.cursor.execute(updateClient)
        self.connection.commit()

    # Display Clients List
    def search_clients(self):
        client = input('Who are you looking for? ')
        retrive = "SELECT * FROM client WHERE name LIKE '"+client+"%';"
        self.cursor.execute(retrive)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        self.connection.commit()

    # Create Client Card
    def insert_client_card(self, card):
        insertCard = "INSERT INTO client_card(name, personal_id, vat_number, address, phone_number, email, client_num, points) VALUES('"+card.name+"','"+card.personal_id+"','"+card.vat_number+"','"+card.address+"','"+card.phone_number+"','"+card.email+"',"+card.client_num+","+card.points+")"
        self.cursor.execute(insertCard)
        self.connection.commit()
    
    # Get Client Number from client table (last generated number)
    def get_client_num(self):
        sql = "SELECT MAX(client_num) FROM client;"
        self.cursor.execute(sql)
        clientNum = self.cursor.fetchone()[0]
        return clientNum

    # PRODUCTS:
    # ------------------------------------------------------
    # Create Product
    def insert_product(self, product):
        insertProduct = "INSERT INTO product(product_name, price, stock) VALUES('"+product.product_name+"',"+product.price+","+product.stock+")"
        self.cursor.execute(insertProduct)
        self.connection.commit()
    
    # Delete Product
    def delete_product(self):
        self.search_products()
        product = input('Insert product ID to delete: ')
        remove_product = "DELETE FROM product WHERE id = '"+product+"'; "
        self.cursor.execute(remove_product)
        self.connection.commit()
    
    # Update Product
    def update_product(self):
        self.search_products()
        product = input('Insert product ID to update: ')
        price = input('Price: ')
        stock = input('Quantity(replace existing): ')

        updateProduct = "UPDATE product SET price= "+price+", stock= "+stock+" WHERE id = '"+product+"';"
        self.cursor.execute(updateProduct)
        self.connection.commit()

    # Display Product List
    def search_products(self):
        product = input('What product are you looking for? ')
        retrive = "SELECT * FROM product WHERE product_name LIKE '"+product+"%';"
        self.cursor.execute(retrive)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        self.connection.commit()

    # Purchases
    # -----------------------------

    # Display Client Card
    def search_client_card(self):
        card = input('Who are you looking for?')
        retrive = "SELECT * FROM client_card WHERE name LIKE '"+card+"%';"
        self.cursor.execute(retrive)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        self.connection.commit()

    # Register Purchases
    def register_purchases(self, shopping_list, card_number):
        for purchase in shopping_list:
            sql = "SELECT price FROM product WHERE id = '"+purchase.product_id+"';"
            self.cursor.execute(sql)
            price = self.cursor.fetchone()[0]     
            insertPurchase = "INSERT INTO purchases(card_number, product_id, price, quantity) VALUES('"+str(card_number)+"',"+str(purchase.product_id)+","+str(price)+","+str(purchase.qtt)+")"
            self.cursor.execute(insertPurchase)
            self.connection.commit()
    
    # Calculate Points based on Price of Purchase
    def calculate_points(self, shopping_list, card_number):
        shoppingValue = 0
        for purchase in shopping_list:
            # Calculate the Price Spent from User
            sql = "SELECT price FROM product WHERE id = '"+purchase.product_id+"';"
            self.cursor.execute(sql)
            getPrice = self.cursor.fetchone()[0]
            value = int(getPrice) * int(purchase.qtt)
            shoppingValue = shoppingValue + value

            # Update Product Stock
            sqlStock = "SELECT stock FROM product WHERE id = '"+purchase.product_id+"';"          
            self.cursor.execute(sqlStock)
            getStock = self.cursor.fetchone()[0]
            stock = int(getStock) - int(purchase.qtt)
            update_stock = "UPDATE product SET stock= '"+str(stock)+"' WHERE id = '"+purchase.product_id+"';"
            self.cursor.execute(update_stock)
            self.connection.commit()
        
        # Update Client Points
        getPoints = "SELECT points FROM client_card WHERE card_number = "+card_number+";"
        self.cursor.execute(getPoints)
        currentPoints = self.cursor.fetchone()[0]        
        points = currentPoints + (round(shoppingValue/50)*3)
        insertPoints = "UPDATE client_card SET points= '"+str(points)+"' WHERE card_number = "+card_number+";"
        self.cursor.execute(insertPoints)
        self.connection.commit()

    # Display Purchases
    def display_purchases(self):
        self.search_client_card()
        card_id = input('Insert Client Card Number: ')
        consulta = "SELECT product.product_name, purchases.price, purchases.quantity FROM purchases JOIN product ON purchases.product_id = product.id WHERE purchases.card_number = "+str(card_id)+";"
        self.cursor.execute(consulta)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        self.connection.commit()