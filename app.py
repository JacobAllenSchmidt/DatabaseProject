from flask import Flask, render_template, request
import mysql_utilities
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
code = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_account")
def create_account():
    return render_template("create_account.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(f"DEBUG: Data received: {request.form}")
        global code
        form_id = request.form.get('form_id')
        
        if form_id == "email_customer":
            code = random.randint(1000, 9999)
            
            msg = MIMEMultipart()
            msg['Subject'] = "2FA Code"
            msg['From'] = EMAIL
            msg['To'] = request.form.get("email_customer")
            msg.attach(MIMEText(f"This is your two-factor authentication code: {code}", "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls() # This is mandatory for Gmail
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Login successful!")
        
        if form_id == "two_factor_customer":
            if int(request.form.get("two_factor_customer")) == code:
                print(f"Logged in successfully with code {code}")
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
    return render_template("cutomer_home.html")

@app.route("/contractor_home")
def contractor_home():
    return render_template("contractor_home.html")


if __name__ == "__main__":
    app.run()