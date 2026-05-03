from flask import Flask, render_template, flash, session, redirect, jsonify, request, url_for
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
    if session.get("logged_in"):
        return redirect(f"/{session.get("account_type")}_home")
    
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
                server.starttls()
                server.login(EMAIL, EMAIL_PASSWORD)
                server.send_message(msg)
                return jsonify({"status": "success", "message": "A 2FA code has been sent to your email!"})
                
            else:
                return jsonify({"status": "error", "message": "Email not found"})
        
        if form_id == "two_factor_customer":
            if int(request.form.get("two_factor_customer")) == code:
                print(f"Logged in successfully with code {code}")
                result = execute_read_query(f"SELECT CustomerID FROM Customer WHERE EMAIL=\"{user_email}\"")
                session["customer_id"] = int(result[0][0])
                session["account_type"] = "customer"
                session["logged_in"] = True
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
                server.starttls()
                server.login(EMAIL, EMAIL_PASSWORD)
                server.send_message(msg)
                return jsonify({"status": "success", "message": "A 2FA code has been sent to your email!"})
                
            else:
                return jsonify({"status": "error", "message": "Email not found"})
        
        if form_id == "two_factor_contractor":
            if int(request.form.get("two_factor_contractor")) == code:
                print(f"Logged in successfully with code {code}")
                result = execute_read_query(f"SELECT ContractorID FROM Contractor WHERE EMAIL=\"{user_email}\"")
                session["contractor_id"] = int(result[0][0])
                session["account_type"] = "contractor"
                session["logged_in"] = True
                return redirect("/contractor_home")
            else:
                print("Errors logging in")
    return render_template("login.html")

@app.route("/customer_home", methods=["GET", "POST"])
def customer_home():
    customer_id = session.get("customer_id")
    print(customer_id)
    
    if not customer_id:
        return redirect("/login")
    
    if request.method == "POST":
        form_id = request.form.get("form_id")
        
        if (form_id == "review_contractor"):
            job_id = request.form.get("job_id")
            review = request.form.get("review")
            rating = request.form.get("rating")
            execute_modify_query(f"INSERT INTO review (JobID, ReviewComment, ReviewRating, ReviewDate) VALUES ({job_id}, \"{review}\", {rating}, CURDATE())")
        
        if (form_id == "accept_application"):  
            application_id_accepted = request.form.get("application_id")
            request_id = request.form.get("request_id")
            contractor_id = execute_read_query(f"SELECT ContractorID FROM application WHERE ApplicationID = {application_id_accepted}")[0][0]
            end_date = request.form.get("end_date")
            execute_modify_query(f"DELETE FROM application WHERE RequestID = {request_id} AND ApplicationID != {application_id_accepted}")
            execute_modify_query(f"INSERT INTO job (RequestID, ContractorID, ApplicationID, StartDate, FinishDate, Status) VALUES ({request_id}, {contractor_id}, {application_id_accepted}, CURDATE(), \"{end_date}\", \"in progress\")")
            
    
    curr_service_request_list = execute_read_query(f"SELECT * FROM servicerequest a WHERE CustomerID = {customer_id} AND NOT EXISTS (SELECT * FROM Job b WHERE b.RequestID = a.RequestID)")
    if curr_service_request_list is None:
        curr_service_request_list = []
        
    finished_jobs_list = execute_read_query(f"SELECT a.*, b.Description, b.ClothingType, c.Name, d.ReviewRating, d.ReviewComment FROM job a LEFT JOIN servicerequest b ON a.RequestID = b.RequestID LEFT JOIN contractor c ON a.ContractorID = c.ContractorID LEFT JOIN review d ON a.JobID = d.JobID WHERE a.status = \"finished\" AND EXISTS (SELECT * FROM servicerequest b WHERE a.RequestID = b.RequestID AND b.CustomerID = {customer_id})")
    if finished_jobs_list is None:
        finished_jobs_list = []
    
    curr_jobs_list = execute_read_query(f"SELECT a.*, b.Description, b.ClothingType, c.Name FROM job a LEFT JOIN servicerequest b ON a.RequestID = b.RequestID LEFT JOIN contractor c ON a.ContractorID = c.ContractorID WHERE a.status != \"finished\" AND EXISTS (SELECT * FROM servicerequest b WHERE a.RequestID = b.RequestID AND b.CustomerID = {customer_id})")
    if curr_jobs_list is None:
        curr_jobs_list = []

    
    application_query = f"""WITH ContractorStats AS (
        SELECT 
            c.ContractorID,
            c.Name,
            AVG(r.ReviewRating) AS avg_rating,
            COUNT(r.ReviewRating) AS review_count
        FROM Contractor c
        LEFT JOIN Job j ON j.ContractorID = c.ContractorID
        LEFT JOIN Review r ON r.JobID = j.JobID
        GROUP BY c.ContractorID, c.Name
    )
    SELECT 
        s.Name,
        s.avg_rating,
        s.review_count,
        a.ProposedPrice,
        a.Comment,
        a.ApplicationDate,
        a.ApplicationID,
        a.RequestID,
        sr.Description,
        sr.ClothingType,
        -- Step 2: Calculate the weighted rank
        ROUND (
            (COALESCE(s.avg_rating, 0) * 0.5) +            -- 50% Weight on Rating
            (LOG(s.review_count + 1) * 0.2) +              -- 20% Weight on Review Volume
            ((1.0 / NULLIF(a.ProposedPrice, 0)) * 100),    -- 30% Weight on Low Price
            2                                              -- Round to 2 decimal places
        ) AS final_score
    FROM Application a
    JOIN ContractorStats s ON a.ContractorID = s.ContractorID
    LEFT JOIN ServiceRequest sr ON sr.RequestID = a.RequestID
    WHERE EXISTS (SELECT * FROM servicerequest b WHERE b.RequestID = a.RequestID AND b.CustomerID = {customer_id})
    AND NOT EXISTS (SELECT * FROM job c WHERE a.ApplicationID = c.ApplicationID)
    ORDER BY final_score DESC;"""
    
    applications_list = execute_read_query(application_query)
    
    if applications_list is None:
        applications_list = []       
    
    return render_template("customer_home.html", curr_service_req=curr_service_request_list, finished_jobs=finished_jobs_list, curr_jobs=curr_jobs_list, applications=applications_list)

@app.route("/contractor_home", methods=["GET", "POST"])
def contractor_home():
    contractor_id = session.get("contractor_id")
    
    curr_jobs_list = execute_read_query(f"SELECT a.*, b.Description, b.ClothingType, c.Name FROM job a LEFT JOIN servicerequest b ON a.RequestID = b.RequestID LEFT JOIN customer c ON b.CustomerID = c.CustomerID WHERE ContractorID = {contractor_id} AND a.status != \"finished\";")
    if curr_jobs_list is None:
        curr_jobs_list = []
    
    applications_list = execute_read_query(f"SELECT * FROM application a LEFT JOIN servicerequest b ON a.RequestID = b.RequestID LEFT JOIN customer c ON b.CustomerID = c.CustomerID WHERE ContractorID = {contractor_id} AND NOT EXISTS (SELECT * FROM job b WHERE a.RequestID = b.RequestID)")
        
    finished_jobs_list = execute_read_query(f'''SELECT a.*, b.Description, b.ClothingType, c.Name, d.ReviewRating, d.ReviewComment, d.ReviewDate
    FROM job a LEFT JOIN
    servicerequest b
    ON a.RequestID = b.RequestID
    LEFT JOIN customer c
    ON b.CustomerID = c.CustomerID
    LEFT JOIN review d
    ON a.JobID = d.jobID
    WHERE ContractorID = 1
    AND a.status = "finished";''')
    print(finished_jobs_list)
    
    if finished_jobs_list is None:
        finished_jobs_list = []
        
    available_service_requests_list = execute_read_query(f"SELECT a.*, b.name FROM servicerequest a LEFT JOIN customer b ON a.CustomerID = b.CustomerID WHERE NOT EXISTS (SELECT * FROM job b WHERE a.RequestID = b.RequestID) AND NOT EXISTS (SELECT * FROM Application b WHERE a.RequestID = b.RequestID AND b.ContractorID = {contractor_id})")
    if available_service_requests_list is None:
        available_service_requests_list = []
    
    if request.method == "POST":
        form_id = request.form.get("form_id")
        
        if (form_id == "finish_job_form"):
            finished_job = request.form.get("finish_job")
            execute_modify_query(f"UPDATE Job SET status = \"finished\" WHERE JobID = {finished_job}")
            return redirect("contractor_home")
            
        if (form_id == "apply_for_job_form"):
            applied_job = request.form.get("apply_for_job")
            return redirect(url_for('application', request_id=applied_job))
    
    return render_template("contractor_home.html", curr_jobs=curr_jobs_list, available_service_requests=available_service_requests_list, finished_jobs=finished_jobs_list, applications=applications_list)

@app.route("/create_service_request", methods=["GET", "POST"])
def create_service_request():
    customer_id = session.get("customer_id")
    if request.method == "POST":
        status = request.form.get("status")
        clothing_type = request.form.get("clothing_type")
        description = request.form.get("description")
        
        execute_modify_query(f"INSERT INTO servicerequest (CustomerID, Status, Description, ClothingType) VALUES ({customer_id}, \"{status}\", \"{description}\", \"{clothing_type}\")")
        return redirect("customer_home")
    return render_template("create_service_request.html")

@app.route("/application/<request_id>", methods=["GET", "POST"])
def application(request_id):
    contractor_id = session.get("contractor_id")
    if request.method == "POST":
        proposed_price = request.form.get("proposed_price")
        comment = request.form.get("comment")
        
        execute_modify_query(f"INSERT INTO application (RequestID, ContractorID, ProposedPrice, Comment, ApplicationDate) VALUES ({request_id}, {contractor_id}, {int(proposed_price)}, \"{comment}\", NOW())")
        return redirect(url_for("contractor_home"))    
    return render_template("/application.html")

@app.route("/logout")
def lougut():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()