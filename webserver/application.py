from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_mysqldb import MySQL
import bcrypt

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
    if not session.get("username") and not session.get("email"):
        return render_template("entry.html")
    return render_template("monitoring.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/login_action", methods=["POST"])
def login_action():
    try:
        cursor = mysql.connection.cursor()
        email = request.form.get("email")
        user_password = request.form.get("password")

        cursor.execute("SELECT * FROM Users WHERE email =%s", [email])
        user_data = cursor.fetchall()
        password = user_data[0][3]

        salt = b'$2b$12$T9sRNpwI2.sMPmz/OtI1peh'
        if bcrypt.hashpw(user_password.encode('utf-8'), salt) == password.encode('utf-8'):
            session["username"] = user_data[0][1]
            session["email"] = user_data[0][2]
            return redirect("/")
        else:
            return redirect("/login")
    except:
        return redirect("/login")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup_action", methods=["POST"])
def register():
    try:
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        salt = b'$2b$12$T9sRNpwI2.sMPmz/OtI1peh'
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

        session["username"] = username
        session["email"] = email

        cursor = mysql.connection.cursor()
        cursor.execute('''insert into Users(username, email, password) values (%s, %s, %s)''',
                       (username, email, hashed))
        mysql.connection.commit()
        cursor.close()

        return redirect("/landing")
    except:
        return redirect("/signup")


@app.route("/logout")
def logout():
    session["username"] = None
    session["email"] = None
    return redirect("/")


@app.route("/landing")
def landing():
    if not session.get("username") and not session.get("email"):
        return redirect("/")
    return render_template("landing.html")


if __name__ == '__main__':
    app.run()
