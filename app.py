from flask import Flask

app = Flask(__name__)

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