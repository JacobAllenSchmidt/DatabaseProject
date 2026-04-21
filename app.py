from flask import Flask, render_template, flash, session, redirect, jsonify, request
from mysql_utilities import execute_modify_query, execute_read_query
import smtplib
import random
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
load_dotenv("secrets.env")
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
app.secret_key = SECRET_KEY

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        phone_number = request.form.get("phonenum")
        account_type = request.form.get("account_type")
        execute_modify_query(f"INSERT INTO {account_type} (Name, Email, PhoneNum) VALUES (\"{name}\", \"{email}\", \"{phone_number}\")")
        return redirect("/")
    return render_template("create_account.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(f"DEBUG: Data received: {request.form}")
        global code
        global user_email
        form_id = request.form.get('form_id')
        
        if form_id == "email_customer":
            user_email = request.form.get("email_customer")
            if execute_read_query(f"SELECT * FROM CUSTOMER WHERE EMAIL=\"{user_email}\"") != []:
                code = random.randint(1000, 9999)
            
                msg = MIMEMultipart()
                msg['Subject'] = "2FA Code"
                msg['From'] = EMAIL
                msg['To'] = user_email
                msg.attach(MIMEText(f"This is your two-factor authentication code: {code}", "plain"))

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls() # This is mandatory for Gmail
                server.login(EMAIL, EMAIL_PASSWORD)
                server.send_message(msg)
                print("Login successful!")
                
            else:
                return jsonify({"status": "error", "message": "Email not found"})
        
        if form_id == "two_factor_customer":
            if int(request.form.get("two_factor_customer")) == code:
                print(f"Logged in successfully with code {code}")
                result = execute_read_query(f"SELECT CustomerID FROM Customer WHERE EMAIL=\"{user_email}\"")
                session["user_id"] = int(result[0][0])
                return redirect("/customer_home")
            else:
                print("Errors logging in")
        
        if form_id == "email_contractor":
            code = random.randint(1000, 9999)
            
            msg = MIMEMultipart()
            msg['Subject'] = "2FA Code"
            msg['From'] = EMAIL
            msg['To'] = request.form.get("email_contractor")
            msg.attach(MIMEText(f"This is your two-factor authentication code: {code}", "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls() # This is mandatory for Gmail
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Login successful!")
        
        if form_id == "two_factor_contractor":
            if int(request.form.get("two_factor_contractor")) == code:
                print(f"Logged in successfully with code {code}")
            else:
                print("Errors logging in")

    return render_template("login.html")

@app.route("/customer_home")
def customer_home():
    user_id = session.get("user_id")
    print(user_id)
    
    if not user_id:
        return redirect("/login")
    
    jobs_list = execute_read_query(f"SELECT * FROM servicerequest WHERE CustomerID = {user_id}")
    if jobs_list is None:
        jobs_list = []
    
    return render_template("customer_home.html", jobs=jobs_list)

@app.route("/contractor_home")
def contractor_home():
    return render_template("contractor_home.html")

@app.route("/create_service_request")
def create_service_request():
    return render_template("create_service_request.html")


if __name__ == "__main__":
    app.run()