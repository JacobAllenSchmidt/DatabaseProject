import mysql.connector
import os
from dotenv import load_dotenv

class MySQLUitilities:
  def __init__():
    load_dotenv("secrets.env")
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    
  def connect():
    db = mysql.connector.connect(
    host="localhost",
    user=USER,
    password=PASSWORD,
    database="databaseproject"
  )
    
  def selectEverythingFromCustomers():
    cursor = db.cursor()
    return cursor.execute("SELECT * FROM Customer")
    cursor.close()
    db.close()
  

