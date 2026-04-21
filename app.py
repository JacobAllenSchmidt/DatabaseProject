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
                session["customer_id"] = int(result[0][0])
                return redirect("/customer_home")
            else:
                print("Errors logging in")
        
        if form_id == "email_contractor":
            user_email = request.form.get("email_contractor")
            if execute_read_query(f"SELECT * FROM CONTRACTOR WHERE EMAIL=\"{user_email}\"") != []:
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
        
        if form_id == "two_factor_contractor":
            if int(request.form.get("two_factor_contractor")) == code:
                print(f"Logged in successfully with code {code}")
                result = execute_read_query(f"SELECT ContractorID FROM Contractor WHERE EMAIL=\"{user_email}\"")
                session["contractor_id"] = int(result[0][0])
                return redirect("/contractor_home")
            else:
                print("Errors logging in")
    return render_template("login.html")

@app.route("/customer_home")
def customer_home():
    customer_id = session.get("customer_id")
    print(customer_id)
    
    if not customer_id:
        return redirect("/login")
    
    curr_service_request_list = execute_read_query(f"SELECT * FROM servicerequest a WHERE CustomerID = {customer_id} AND NOT EXISTS (SELECT * FROM Job b WHERE b.RequestID = a.RequestID)")
    if curr_service_request_list is None:
        curr_service_request_list = []
        
    finished_jobs_list = execute_read_query(f"SELECT * FROM job WHERE Status = finished")
    if finished_jobs_list is None:
        finished_jobs_list = []
    
    reviews_list = execute_read_query(f"SELECT * FROM review a WHERE EXISTS (SELECT * FROM job b WHERE b.JobID = a.JobID AND EXISTS (SELECT * FROM servicerequest c WHERE c.RequestID = b.RequestID AND c.CustomerID = {customer_id}))")
    if reviews_list is None:
        reviews_list = []
        
    applications_list = execute_read_query(f"SELECT * FROM Application WHERE EXISTS (SELECT * FROM servicerequest a WHERE a.CustomerID = {customer_id});")
    if applications_list is None:
        applications_list = []
    
    return render_template("customer_home.html", curr_service_req=curr_service_request_list, finished_jobs=finished_jobs_list, review=reviews_list, applications=applications_list)

@app.route("/contractor_home", methods=["GET", "POST"])
def contractor_home():
    contractor_id = session.get("contractor_id")
    
    curr_jobs_list = execute_read_query(f"SELECT * FROM job WHERE ContractorID = {contractor_id} AND status != \"finished\"")
    if curr_jobs_list is None:
        curr_jobs_list = []
        
    finished_jobs_list = execute_read_query(f"SELECT * FROM job WHERE ContractorID = {contractor_id} AND status = \"finished\"")
    if finished_jobs_list is None:
        finished_jobs_list = []
        
    available_service_requests_list = execute_read_query(f"SELECT * FROM servicerequest WHERE status != \"taken\"")
    if available_service_requests_list is None:
        available_service_requests_list = []
    
    job_ID_list = execute_read_query(f"SELECT JobID FROM job WHERE ContractorID = {contractor_id}")
    if job_ID_list is None:
        job_ID_list = []
    
    reviews_dict = {}
    
    for job_ID in job_ID_list:
        print(job_ID[0])
        
        reviews_dict[f"{job_ID[0]}"] = execute_read_query(f"SELECT * FROM review WHERE JobID = {job_ID[0]}")
        print(reviews_dict.get(f"{job_ID[0]}"))
        print(reviews_dict.get("1")[0][2])
    
    if request.method == "POST":
        finished_job = request.form.get("finish_job")
        
        execute_modify_query(f"UPDATE Job SET status = \"finished\" WHERE JobID = {finished_job}")
        return redirect("contractor_home")
    
    return render_template("contractor_home.html", curr_jobs=curr_jobs_list, available_service_requests=available_service_requests_list, finished_jobs=finished_jobs_list, reviews=reviews_dict)

@app.route("/create_service_request", methods=["GET", "POST"])
def create_service_request():
    customer_id = session.get("customer_id")
    if request.method == "POST":
        status = request.form.get("status")
        clothing_type = request.form.get("clothing_type")
        description = request.form.get("description")
        
        execute_modify_query(f"INSERT INTO servicerequest (CustomerID, Status, Description, ClothingType) VALUES ({customer_id}, \"{status}\", \'{description}\', \"{clothing_type}\")")
    return render_template("create_service_request.html")


if __name__ == "__main__":
    app.run()