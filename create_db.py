import pymysql
import getpass

db_user = input("Enter your MySQL username: ")
db_password = getpass.getpass("Enter your MySQL password: ")

mydb = pymysql.connect(
    host="localhost",
    user=db_user,
    passwd=db_password,
)

my_cursor = mydb.cursor()


my_cursor.execute("SHOW DATABASES LIKE 'animal_shelter'")
result = my_cursor.fetchone()
if result:
    print("Database 'animal_shelter' already exists")
else:
    my_cursor.execute("CREATE DATABASE animal_shelter")
    print("Created database 'animal_shelter'")