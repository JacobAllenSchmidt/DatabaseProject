from flask import Flask, render_template
import mysql_utilities

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_account")
def create_account():
    return render_template("create_account")

@app.route("/login")
def login():
    return render_template("login")


if __name__ == "__main__":
    app.run()