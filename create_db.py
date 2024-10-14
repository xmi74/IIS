# This file creates new database needed in app.py

import pymysql

mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="password123",
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE animal_shelter")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
