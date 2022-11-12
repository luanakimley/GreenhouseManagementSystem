from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_mysqldb import MySQL

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'GMS'

print(os.getenv('MYSQL_USER'))

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

mysql = MySQL(app)


@app.route("/")
def index():
    return render_template("entry.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # TODO: fix login functionality
    if request.method == "POST":
        name = request.form.get("name")
        session["name"] = name
        return redirect("/")
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    # TODO: encrypt password
    # TODO: ensure no duplicate email and username
    cursor = mysql.connection.cursor()
    cursor.execute('''insert into Users(username, email, password) values (%s, %s, %s)''', (username, email, password))
    mysql.connection.commit()
    cursor.close()

    return redirect("/landing")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


@app.route("/landing")
def landing():
    return render_template("landing.html")


if __name__ == '__main__':
    app.run()
