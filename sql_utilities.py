import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("secrets.env")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

db = mysql.connector.connect(
  host="localhost",
  user=USER,
  password=PASSWORD,
  database="databaseproject"
)

cursor = db.cursor()
cursor.execute("SELECT * FROM Customer")
for row in cursor.fetchall():
    print(row)
cursor.close()
db.close()