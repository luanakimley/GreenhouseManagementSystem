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
app.config['MYSQL_DB'] = 'gms'

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
    cursor.execute("select * from ucl where users_id=%s", (users_id,))
    user_culture_lifecycle = cursor.fetchall()

    if len(user_culture_lifecycle) == 0:
        return redirect("/landing")

    else:
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

        cursor.execute("select * from user where email =%s", [email])
        user_data = cursor.fetchall()
        password = user_data[0][3]

        salt = os.getenv('SALT').encode()
        if email.lower() == user_data[0][2] and bcrypt.hashpw(user_password.encode('utf-8'), salt) == password.encode('utf-8'):
            session["users_id"] = user_data[0][0]
            session["username"] = user_data[0][1]
            session["email"] = user_data[0][2]

            cursor = mysql.connection.cursor()
            cursor.execute("select * from ucl where users_id=%s", (user_data[0][0],))
            user_culture_lifecycle = cursor.fetchall()

            session["UCL"] = user_culture_lifecycle
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
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        salt = os.getenv('SALT').encode()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

        session["username"] = username
        session["email"] = email

        cursor = mysql.connection.cursor()
        cursor.execute('''insert into user(username, email, password) values (%s, %s, %s)''',
                       (username, email, hashed))
        mysql.connection.commit()

        cursor.execute("select users_id from user where email=%s", [email])
        users_id = cursor.fetchall()[0][0]

        session["users_id"] = users_id

        cursor.close()
        return redirect("/landing")


@app.route("/logout")
def logout():
    session["username"] = None
    session["email"] = None
    session["users_id"] = None
    session["UCL"] = None
    return redirect("/")


@app.route("/landing")
def landing():
    if not session.get("username") and not session.get("email"):
        return redirect("/")
    cursor = mysql.connection.cursor()
    cursor.execute("select * from culture")
    cultures = cursor.fetchall()
    return render_template("landing.html", cultures=cultures)


@app.route("/culture_submit", methods=["POST"])
def culture_submit():
    culture = request.form.get("culture")
    cursor = mysql.connection.cursor()
    cursor.execute('''insert into ucl(users_id, culture_id, lifecycle_id) values (%s, %s, %s)''',
                   (session["users_id"], culture, 1))
    mysql.connection.commit()

    users_id = session["users_id"]
    cursor = mysql.connection.cursor()
    cursor.execute("select * from ucl where users_id=%s", (users_id,))
    user_culture_lifecycle = cursor.fetchall()

    session["UCL"] = user_culture_lifecycle

    cursor.execute("select * from preset_data where culture_id=%s and lifecycle_id=%s",
                   [session["UCL"][0][2], session["UCL"][0][3]])
    preset_data = cursor.fetchall()

    cursor.execute('''insert into data_range(ucl_id, creation_dateTime, tempMin, tempMax, humidityMin, humidityMax, 
    pHMin, phMax) values (%s, curdate(), %s, %s, %s, %s, %s, %s)''',
                   (session["UCL"][0][0], preset_data[0][3], preset_data[0][4], preset_data[0][5],
                   preset_data[0][6], preset_data[0][7], preset_data[0][8])
                   )
    mysql.connection.commit()
    return redirect("/")


@app.route("/monitoring")
def monitoring():
    cursor = mysql.connection.cursor()
    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)", [session["users_id"]])
    mysql.connection.commit()
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select * from lifecycle")
    all_lifecycle = cursor.fetchall()

    cursor.execute("select * from data_range where ucl_id=%s", [session["UCL"][0][0]])
    preset_data = cursor.fetchall()

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    cur_lifecycle = cursor.fetchall()

    cursor.close()

    return render_template("monitoring.html", culture_name=culture_name, lifecycles=all_lifecycle, preset_data=preset_data, cur_lifecycle=cur_lifecycle)


@app.route("/edit_temp")
def edit_temp():
    cursor = mysql.connection.cursor()
    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    mysql.connection.commit()
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    lifecycle_name = cursor.fetchall()[0][0]

    cursor.execute("select tempMin, tempMax from data_range where ucl_id=%s", [session["UCL"][0][0]])
    tempRange = cursor.fetchall()

    return render_template("edit_temp.html", culture_name=culture_name, lifecycle_name=lifecycle_name, tempRange=tempRange)


@app.route("/edit_temp_action", methods=["POST"])
def edit_temp_action():
    temp_min = request.form.get("tempMin")
    temp_max = request.form.get("tempMax")

    cursor = mysql.connection.cursor()
    cursor.execute('''update data_range set tempMin=%s, tempMax=%s where ucl_id=%s''', (temp_min, temp_max, session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/monitoring")


@app.route("/reset_default_temp")
def reset_default_temp():
    cursor = mysql.connection.cursor()
    cursor.execute("select tempMin, tempMax from preset_data where culture_id=%s and lifecycle_id=%s", [session["UCL"][0][2], session["UCL"][0][3]])
    default_temp = cursor.fetchall()
    cursor.execute('''update data_range set tempMin=%s, tempMax=%s where ucl_id=%s''',
                   (default_temp[0][0], default_temp[0][1], session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/edit_temp")


@app.route("/edit_humidity")
def edit_humidity():
    cursor = mysql.connection.cursor()
    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    mysql.connection.commit()
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    lifecycle_name = cursor.fetchall()[0][0]

    cursor.execute("select humidityMin, humidityMax from data_range where ucl_id=%s", [session["UCL"][0][0]])
    humidity_range = cursor.fetchall()

    return render_template("edit_humidity.html", culture_name=culture_name, lifecycle_name=lifecycle_name,
                           humidity_range=humidity_range)


@app.route("/edit_humidity_action", methods=["POST"])
def edit_humidity_action():
    humidity_min = request.form.get("humidityMin")
    humidity_max = request.form.get("humidityMax")

    cursor = mysql.connection.cursor()
    cursor.execute('''update data_range set humidityMin=%s, humidityMax=%s where ucl_id=%s''', (humidity_min, humidity_max, session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/monitoring")


@app.route("/reset_default_humidity")
def reset_default_humidity():
    cursor = mysql.connection.cursor()
    cursor.execute("select humidityMin, humidityMax from preset_data where culture_id=%s and lifecycle_id=%s", [session["UCL"][0][2], session["UCL"][0][3]])
    default_humidity = cursor.fetchall()
    cursor.execute('''update data_range set humidityMin=%s, humidityMax=%s where ucl_id=%s''',
                   (default_humidity[0][0], default_humidity[0][1], session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/edit_humidity")


@app.route("/edit_ph")
def edit_ph():
    cursor = mysql.connection.cursor()
    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    mysql.connection.commit()
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    lifecycle_name = cursor.fetchall()[0][0]

    cursor.execute("select pHMin, pHMax from data_range where ucl_id=%s", [session["UCL"][0][0]])
    ph_range = cursor.fetchall()

    return render_template("edit_ph.html", culture_name=culture_name, lifecycle_name=lifecycle_name,
                           ph_range=ph_range)


@app.route("/edit_ph_action", methods=["POST"])
def edit_ph_action():
    ph_min = request.form.get("pHMin")
    ph_max = request.form.get("pHMax")

    cursor = mysql.connection.cursor()
    cursor.execute('''update data_range set pHMin=%s, pHMax=%s where ucl_id=%s''', (ph_min, ph_max, session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/monitoring")


@app.route("/reset_default_ph")
def reset_default_ph():
    cursor = mysql.connection.cursor()
    cursor.execute("select pHMin, pHMax from preset_data where culture_id=%s and lifecycle_id=%s", [session["UCL"][0][2], session["UCL"][0][3]])
    default_ph = cursor.fetchall()
    cursor.execute('''update data_range set pHMin=%s, pHMax=%s where ucl_id=%s''',
                   (default_ph[0][0], default_ph[0][1], session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/edit_ph")


@app.route("/lifecycle/<int:lifecycle_id>")
def lifecycle(lifecycle_id):
    cursor = mysql.connection.cursor()
    cursor.execute("select * from ucl where users_id=%s and culture_id=%s and lifecycle_id=%s", [session["UCL"][0][1], session["UCL"][0][2], lifecycle_id])
    ucl = cursor.fetchall()

    if len(ucl) == 0:
        cursor.execute('''insert into ucl(users_id, culture_id, lifecycle_id) values (%s, %s, %s)''',
                       (session["UCL"][0][1], session["UCL"][0][2], lifecycle_id))
        mysql.connection.commit()
        cursor.execute("select * from ucl where users_id=%s and culture_id=%s and lifecycle_id=%s", [session["UCL"][0][1], session["UCL"][0][2], lifecycle_id])
        session["UCL"] = cursor.fetchall()

        cursor.execute("select * from preset_data where culture_id=%s and lifecycle_id=%s", [session["UCL"][0][2], session["UCL"][0][3]])
        preset_data = cursor.fetchall()

        cursor.execute('''insert into data_range(ucl_id, creation_dateTime, tempMin, tempMax, humidityMin, humidityMax,
            pHMin, phMax) values (%s, curdate(), %s, %s, %s, %s, %s, %s)''',
                       (session["UCL"][0][0], preset_data[0][3], preset_data[0][4], preset_data[0][5],
                        preset_data[0][6], preset_data[0][7], preset_data[0][8])
                       )
        mysql.connection.commit()

        return redirect("/monitoring")

    session["UCL"] = ucl
    return redirect("/monitoring")


if __name__ == '__main__':
    app.run()
