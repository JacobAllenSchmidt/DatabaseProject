import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv("secrets.env")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

def create_connection():
  try:
    connection = mysql.connector.connect(
      host='localhost',
      user=USER,
      password=PASSWORD,
      database="databaseproject"
    )
    
    if connection.is_connected():
      return connection
  except Error as e:
      print(f"Error while connecting to MySQL: {e}")
      return None 
  
    
def execute_modify_query(query):
  connection = create_connection()
  cursor = None
  if connection:
    try:
      cursor = connection.cursor()
      cursor.execute(query)
      connection.commit()
      print("Successful query")
    except Error as e:
      print(f"Unsuccessful query: {e}")
    finally:
      cursor.close()
      connection.close()
  
def execute_read_query(query):
  connection = create_connection()
  cursor = None
  result = None
  if connection:
    try:
      cursor = connection.cursor()
      cursor.execute(query)
      result = cursor.fetchall()
      print("Successful query")
    except Error as e:
      print(f"Unsuccessful query: {e}")
    finally:
      cursor.close()
      connection.close()
      return result
    
email = "schmidtjacob920@gmail.com"
name = "jacob"
phone_number = "9127591863"
account_type = "Customer"
execute_modify_query(f"INSERT INTO {account_type} (Name, Email, PhoneNum) VALUES (\"{name}\", \"{email}\", \"{phone_number}\")")