# python -m pipreqs.pipreqs

import mysql.connector as mysql

db = mysql.connect(
    host = "db",
    user = "root",
    passwd = "",
    database = "iotdashboard"
)

cursor = db.cursor()

## getting all the tables which are present in 'iotdatabase' database
cursor.execute("SHOW TABLES")

tables = cursor.fetchall() ## it returns list of tables present in the database

## showing all the tables one by one
for table in tables:
    print(table)