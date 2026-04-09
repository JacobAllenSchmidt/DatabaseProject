import mysql.connector
import os
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

load_dotenv("secrets.env")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

# @app.route("/")
# def show_users():
#     db = mysql.connector.connect(
#       host="localhost",
#       user=USER,
#       password=PASSWORD,
#       database="DatabaseProject"
#     )

#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM Customer")
#     message = ""
#     for row in cursor.fetchall():
#         message += str(row)
#     cursor.close()
#     db.close()
#     return f"<p>{row}</p>"

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