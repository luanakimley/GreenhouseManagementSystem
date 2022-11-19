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

    users_id = session["users_id"]
    cursor = mysql.connection.cursor()
    cursor.execute("select * from UCL where users_id=%s", (users_id,))
    user_culture_lifecycle = cursor.fetchall()

    session["UCL"] = user_culture_lifecycle[0][0]

    if len(user_culture_lifecycle) == 0:
        return redirect("/landing")

    return redirect("/monitoring")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/login_action", methods=["POST"])
def login_action():
    try:
        cursor = mysql.connection.cursor()
        email = request.form.get("email")
        user_password = request.form.get("password")

        cursor.execute("select * from Users where email =%s", [email])
        user_data = cursor.fetchall()
        password = user_data[0][3]

        salt = os.getenv('SALT').encode()
        if bcrypt.hashpw(user_password.encode('utf-8'), salt) == password.encode('utf-8'):
            session["users_id"] = user_data[0][0]
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

        salt = os.getenv('SALT').encode()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

        session["username"] = username
        session["email"] = email

        cursor = mysql.connection.cursor()
        cursor.execute('''insert into Users(username, email, password) values (%s, %s, %s)''',
                       (username, email, hashed))
        mysql.connection.commit()

        cursor.execute("select users_id from Users where email=%s", [email])
        users_id = cursor.fetchall()[0][0]

        session["users_id"] = users_id

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
    cursor = mysql.connection.cursor()
    cursor.execute("select * from Culture")
    cultures = cursor.fetchall()
    return render_template("landing.html", cultures=cultures)


@app.route("/culture_submit", methods=["POST"])
def culture_submit():
    culture = request.form.get("culture")
    cursor = mysql.connection.cursor()
    cursor.execute('''insert into UCL(users_id, culture_id, lifecycle_id) values (%s, %s, %s)''',
                   (session["users_id"], culture, 1))
    mysql.connection.commit()
    return redirect("/")


@app.route("/monitoring")
def monitoring():

    cursor = mysql.connection.cursor()
    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s)", [session["users_id"]])
    mysql.connection.commit()
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select * from Lifecycle")
    lifecycle = cursor.fetchall()

    users_id = session["users_id"]
    cursor = mysql.connection.cursor()
    cursor.execute("select * from UCL where users_id=%s", (users_id,))
    user_culture_lifecycle = cursor.fetchall()

    session["UCL"] = user_culture_lifecycle

    cursor.execute("select * from PresetData where culture_id=%s and lifecycle_id=%s", [session["UCL"][0][2], session["UCL"][0][3]])
    preset_data = cursor.fetchall()

    return render_template("monitoring.html", culture_name=culture_name, lifecycles=lifecycle, preset_data=preset_data)


if __name__ == '__main__':
    app.run()
