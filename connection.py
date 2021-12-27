# file to save connection settings

import mysql.connector

connection = mysql.connector.connect(host="localhost",user="root",password="",database="trial")
cursor = connection.cursor()