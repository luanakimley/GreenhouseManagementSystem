import MySQLdb
from flask import Flask, redirect, render_template, request, session, flash, abort
from flask_session import Session
from flask_mysqldb import MySQL
import bcrypt
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import os
import pathlib
import requests

load_dotenv()

app = Flask(__name__)

# PubNub configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.getenv('PUBNUB_SUBSCRIBE_KEY')
pnconfig.publish_key = os.getenv('PUBNUB_PUBLISH_KEY')
pnconfig.user_id = os.getenv('PUBNUB_USERID')
pnconfig.auth_key = os.getenv('PUBNUB_AUTHKEY')
pnconfig.cipher_key = os.getenv('PUBNUB_CIPHERKEY')
pnconfig.ssl = True  # Encrypt the data when sent to PubNub
pubnub = PubNub(pnconfig)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

GOOGLE_CLIENT_ID = "896287247574-lt02c3oqmrv42hii5eeiafdi7l90u4hu.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://greenhousemanagementsystem.tk/callback"
)

Session(app)

mysql = MySQL(app)

myChannel = "greenhouse"


def login_required(function):
    def wrapper(*args, **kwargs):
        if "users_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500) #States do not match, Don't trust

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token = credentials._id_token,
        request=token_request,
        audience = GOOGLE_CLIENT_ID
    )

    cursor = mysql.connection.cursor()
    cursor.execute("select * from user where email=%s", [id_info.get("sub")])
    user_data = cursor.fetchall()

    if len(user_data) == 0:
        cursor.execute('''insert into user(username, email) values (%s, %s)''',
                       (id_info.get("name"), id_info.get("sub")))
        mysql.connection.commit()

        cursor.execute("select users_id from user where email=%s", [id_info.get("sub")])
        users_id = cursor.fetchall()[0][0]

        session["email"] = id_info.get("sub")
        session["username"] = id_info.get("name")
        session["users_id"] = users_id
        session["google_token"] = credentials._id_token

        return redirect("/landing")

    session["users_id"] = user_data[0][0]
    session["username"] = user_data[0][1]
    session["email"] = user_data[0][2]

    cursor.execute("select * from ucl where users_id=%s", [user_data[0][0]])
    user_culture_lifecycle = cursor.fetchall()

    session["UCL"] = user_culture_lifecycle
    publish(myChannel, {'ucl': session["UCL"][0][0]})

    return redirect("/")


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
        publish(myChannel, {'ucl': session["UCL"][0][0]})
        return redirect("/monitoring")


@app.route("/google_login", methods=["GET", "POST"])
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


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
            publish(myChannel, {'ucl': user_culture_lifecycle[0][0]})
            return redirect("/")
        else:
            flash("Wrong email address or password")
            return redirect("/login")
    except Exception:
        flash("Wrong email address or password")
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

        cursor = mysql.connection.cursor()
        cursor.execute('''insert into user(username, email, password) values (%s, %s, %s)''',
                       (username, email, hashed))
        mysql.connection.commit()

        cursor.execute("select users_id from user where email=%s", [email])
        users_id = cursor.fetchall()[0][0]

        session["username"] = username
        session["email"] = email
        session["users_id"] = users_id

        cursor.close()
        return redirect("/landing")
    except MySQLdb.IntegrityError:
        flash("A user with that email address already exists")
        return redirect("/signup")


@app.route("/logout")
def logout():
    session.clear()
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
    publish(myChannel, {'ucl': user_culture_lifecycle[0][0]})

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
@login_required
def monitoring():
    cursor = mysql.connection.cursor()
    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    mysql.connection.commit()
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select * from lifecycle")
    all_lifecycle = cursor.fetchall()

    cursor.execute("select * from data_range where ucl_id=%s", [session["UCL"][0][0]])
    preset_data = cursor.fetchall()

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    cur_lifecycle = cursor.fetchall()

    cursor.execute("select count(users_id) from user_notification where users_id=%s", [session["users_id"]])
    notifications_count = cursor.fetchall()[0][0]

    cursor.close()

    return render_template("monitoring.html", culture_name=culture_name, lifecycles=all_lifecycle,
                           preset_data=preset_data, cur_lifecycle=cur_lifecycle, notifications_count=notifications_count)


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

    return render_template("edit_temp.html", culture_name=culture_name, lifecycle_name=lifecycle_name,
                           tempRange=tempRange)


@app.route("/edit_temp_action", methods=["POST"])
def edit_temp_action():
    temp_min = request.form.get("tempMin")
    temp_max = request.form.get("tempMax")

    cursor = mysql.connection.cursor()
    cursor.execute('''update data_range set tempMin=%s, tempMax=%s where ucl_id=%s''',
                   (temp_min, temp_max, session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/monitoring")


@app.route("/reset_default_temp")
def reset_default_temp():
    cursor = mysql.connection.cursor()
    cursor.execute("select tempMin, tempMax from preset_data where culture_id=%s and lifecycle_id=%s",
                   [session["UCL"][0][2], session["UCL"][0][3]])
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
    cursor.execute('''update data_range set humidityMin=%s, humidityMax=%s where ucl_id=%s''',
                   (humidity_min, humidity_max, session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/monitoring")


@app.route("/reset_default_humidity")
def reset_default_humidity():
    cursor = mysql.connection.cursor()
    cursor.execute("select humidityMin, humidityMax from preset_data where culture_id=%s and lifecycle_id=%s",
                   [session["UCL"][0][2], session["UCL"][0][3]])
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
    cursor.execute('''update data_range set pHMin=%s, pHMax=%s where ucl_id=%s''',
                   (ph_min, ph_max, session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/monitoring")


@app.route("/reset_default_ph")
def reset_default_ph():
    cursor = mysql.connection.cursor()
    cursor.execute("select pHMin, pHMax from preset_data where culture_id=%s and lifecycle_id=%s",
                   [session["UCL"][0][2], session["UCL"][0][3]])
    default_ph = cursor.fetchall()
    cursor.execute('''update data_range set pHMin=%s, pHMax=%s where ucl_id=%s''',
                   (default_ph[0][0], default_ph[0][1], session["UCL"][0][0]))
    mysql.connection.commit()

    return redirect("/edit_ph")


@app.route("/lifecycle/<int:lifecycle_id>")
def lifecycle(lifecycle_id):
    cursor = mysql.connection.cursor()
    cursor.execute("select * from ucl where users_id=%s and culture_id=%s and lifecycle_id=%s",
                   [session["UCL"][0][1], session["UCL"][0][2], lifecycle_id])
    ucl = cursor.fetchall()

    if len(ucl) == 0:
        cursor.execute('''insert into ucl(users_id, culture_id, lifecycle_id) values (%s, %s, %s)''',
                       (session["UCL"][0][1], session["UCL"][0][2], lifecycle_id))
        mysql.connection.commit()
        cursor.execute("select * from ucl where users_id=%s and culture_id=%s and lifecycle_id=%s",
                       [session["UCL"][0][1], session["UCL"][0][2], lifecycle_id])
        session["UCL"] = cursor.fetchall()
        publish(myChannel, {'ucl': session["UCL"][0][0]})

        cursor.execute("select * from preset_data where culture_id=%s and lifecycle_id=%s",
                       [session["UCL"][0][2], session["UCL"][0][3]])
        preset_data = cursor.fetchall()

        print(preset_data)
        cursor.execute('''insert into data_range(ucl_id, creation_dateTime, tempMin, tempMax, humidityMin, humidityMax,
            pHMin, phMax) values (%s, curdate(), %s, %s, %s, %s, %s, %s)''',
                       (session["UCL"][0][0], preset_data[0][3], preset_data[0][4], preset_data[0][5],
                        preset_data[0][6], preset_data[0][7], preset_data[0][8])
                       )
        mysql.connection.commit()

        return redirect("/monitoring")

    session["UCL"] = ucl
    publish(myChannel, {'ucl': ucl[0][0]})
    return redirect("/monitoring")


@app.route("/notifications")
def notifications():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select user_notification_id, description, icon, notification_dateTime from notification n, user_notification un where n.notifications_id = un.notifications_id and users_id=%s order by user_notification_id desc",
        [session["users_id"]])
    notifications_list = cursor.fetchall()

    return render_template("notifications.html", notifications=notifications_list)


@app.route("/delete_notification/<int:user_notification_id>")
def delete_notification(user_notification_id):
    cursor = mysql.connection.cursor()
    cursor.execute("delete from user_notification where user_notification_id=%s", [user_notification_id])
    mysql.connection.commit()

    return redirect("/notifications")


@app.route("/temp_graph")
def temp_graph():
    cursor = mysql.connection.cursor()
    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    lifecycle_name = cursor.fetchall()[0][0]

    cursor.execute("select distinct date(creation_dateTime) from crop_data where ucl_id=%s group by date(creation_dateTime) order by date(creation_dateTime) desc limit 5",
                   [session["UCL"][0][0]])
    dates = cursor.fetchall()

    if len(dates) == 0:
        flash("No data available")
        return redirect("/monitoring")

    cursor.execute("select t.temp, t.creation_dateTime from crop_data t join (select min(t2.creation_dateTime) as min_timestamp from crop_data t2 group by day(t2.creation_dateTime), hour(t2.creation_dateTime)) t2 on t.creation_dateTime = t2.min_timestamp where date(creation_dateTime)=%s and ucl_id=%s order by creation_dateTime desc",
                   [dates[0][0], session["UCL"][0][0]])
    temp_graph_data = cursor.fetchall()

    cursor.execute("select temp from crop_data where date(creation_dateTime)=%s and ucl_id=%s", [dates[0][0], session["UCL"][0][0]])
    temp_statistics_data = cursor.fetchall()

    cursor.execute("select tempMin, tempMax from data_range where ucl_id=%s", [session["UCL"][0][0]])
    range = cursor.fetchall()

    return render_template("temp_graph.html", culture_name=culture_name, lifecycle_name=lifecycle_name, temp_statistics_data=temp_statistics_data,
                           temp_graph_data=temp_graph_data, range=range, dates=dates, cur_date=dates[0][0].strftime('%y-%m-%d'))


@app.route("/temp_graph/<string:creation_date>")
def temp_graph_day(creation_date):
    cursor = mysql.connection.cursor()

    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    lifecycle_name = cursor.fetchall()[0][0]

    cursor.execute(
        "select distinct date(creation_dateTime) from crop_data where ucl_id=%s group by date(creation_dateTime) order by date(creation_dateTime) desc limit 5",
        [session["UCL"][0][0]])
    dates = cursor.fetchall()

    cursor.execute(
        "select t.temp, t.creation_dateTime from crop_data t join (select min(t2.creation_dateTime) as min_timestamp from crop_data t2 group by day(t2.creation_dateTime), hour(t2.creation_dateTime)) t2 on t.creation_dateTime = t2.min_timestamp where date(creation_dateTime)=%s and ucl_id=%s order by creation_dateTime desc",
        [creation_date, session["UCL"][0][0]])
    temp_graph_data = cursor.fetchall()

    cursor.execute("select temp from crop_data where date(creation_dateTime)=%s and ucl_id=%s",
                   [creation_date, session["UCL"][0][0]])
    temp_statistics_data = cursor.fetchall()

    cursor.execute("select tempMin, tempMax from data_range where ucl_id=%s", [session["UCL"][0][0]])
    range = cursor.fetchall()

    return render_template("temp_graph.html", culture_name=culture_name, lifecycle_name=lifecycle_name, temp_statistics_data=temp_statistics_data,
                           temp_graph_data=temp_graph_data, range=range, dates=dates, cur_date=creation_date)


@app.route("/humidity_graph")
def humidity_graph():
    cursor = mysql.connection.cursor()
    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    lifecycle_name = cursor.fetchall()[0][0]

    cursor.execute(
        "select distinct date(creation_dateTime) from crop_data where ucl_id=%s group by date(creation_dateTime) order by date(creation_dateTime) desc limit 5",
        [session["UCL"][0][0]])
    dates = cursor.fetchall()

    if len(dates) == 0:
        flash("No data available")
        return redirect("/monitoring")

    cursor.execute(
        "select t.humidity, t.creation_dateTime from crop_data t join (select min(t2.creation_dateTime) as min_timestamp from crop_data t2 group by day(t2.creation_dateTime), hour(t2.creation_dateTime)) t2 on t.creation_dateTime = t2.min_timestamp where date(creation_dateTime)=%s and ucl_id=%s order by creation_dateTime desc",
        [dates[0][0], session["UCL"][0][0]])
    humidity_graph_data = cursor.fetchall()

    cursor.execute("select humidity from crop_data where date(creation_dateTime)=%s and ucl_id=%s", [dates[0][0], session["UCL"][0][0]])
    humidity_statistics_data = cursor.fetchall()

    cursor.execute("select humidityMin, humidityMax from data_range where ucl_id=%s", [session["UCL"][0][0]])
    range = cursor.fetchall()

    return render_template("humidity_graph.html", culture_name=culture_name, lifecycle_name=lifecycle_name, dates=dates,
                           humidity_statistics_data=humidity_statistics_data,
                           humidity_graph_data=humidity_graph_data, range=range, cur_date=dates[0][0].strftime('%y-%m-%d'))


@app.route("/humidity_graph/<string:creation_date>")
def humidity_graph_day(creation_date):
    cursor = mysql.connection.cursor()

    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    lifecycle_name = cursor.fetchall()[0][0]

    cursor.execute(
        "select distinct date(creation_dateTime) from crop_data where ucl_id=%s group by date(creation_dateTime) order by date(creation_dateTime) desc limit 5",
        [session["UCL"][0][0]])
    dates = cursor.fetchall()

    cursor.execute(
        "select t.humidity, t.creation_dateTime from crop_data t join (select min(t2.creation_dateTime) as min_timestamp from crop_data t2 group by day(t2.creation_dateTime), hour(t2.creation_dateTime)) t2 on t.creation_dateTime = t2.min_timestamp where date(creation_dateTime)=%s and ucl_id=%s order by creation_dateTime desc",
        [creation_date, session["UCL"][0][0]])
    humidity_graph_data = cursor.fetchall()

    cursor.execute("select humidity from crop_data where date(creation_dateTime)=%s and ucl_id=%s", [creation_date, session["UCL"][0][0]])
    humidity_statistics_data = cursor.fetchall()

    cursor.execute("select humidityMin, humidityMax from data_range where ucl_id=%s", [session["UCL"][0][0]])
    range = cursor.fetchall()

    return render_template("humidity_graph.html", culture_name=culture_name, lifecycle_name=lifecycle_name,
                           humidity_statistics_data=humidity_statistics_data,
                           humidity_graph_data=humidity_graph_data, range=range, dates=dates, cur_date=creation_date)


@app.route("/ph_graph")
def ph_graph():
    cursor = mysql.connection.cursor()
    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    lifecycle_name = cursor.fetchall()[0][0]

    cursor.execute(
        "select distinct date(creation_dateTime) from crop_data where ucl_id=%s group by date(creation_dateTime) order by date(creation_dateTime) desc limit 5",
        [session["UCL"][0][0]])
    dates = cursor.fetchall()

    if len(dates) == 0:
        flash("No data available")
        return redirect("/monitoring")

    cursor.execute(
        "select t.pH, t.creation_dateTime from crop_data t join (select min(t2.creation_dateTime) as min_timestamp from crop_data t2 group by day(t2.creation_dateTime), hour(t2.creation_dateTime)) t2 on t.creation_dateTime = t2.min_timestamp where date(creation_dateTime)=%s and ucl_id=%s order by creation_dateTime desc",
        [dates[0][0], session["UCL"][0][0]])
    ph_graph_data = cursor.fetchall()

    cursor.execute("select pH from crop_data where date(creation_dateTime)=%s and ucl_id=%s", [dates[0][0], session["UCL"][0][0]])
    ph_statistics_data = cursor.fetchall()

    cursor.execute("select pHMin, pHMax from data_range where ucl_id=%s", [session["UCL"][0][0]])
    range = cursor.fetchall()

    return render_template("ph_graph.html", culture_name=culture_name, lifecycle_name=lifecycle_name, ph_statistics_data=ph_statistics_data,
                           ph_graph_data=ph_graph_data, range=range, dates=dates, cur_date=dates[0][0].strftime('%y-%m-%d'))


@app.route("/ph_graph/<string:creation_date>")
def ph_graph_day(creation_date):
    cursor = mysql.connection.cursor()

    cursor.execute("select name from culture where culture_id=(select culture_id from ucl where users_id=%s limit 1)",
                   [session["users_id"]])
    culture_name = cursor.fetchall()[0][0]

    cursor.execute("select name from lifecycle where lifecycle_id=%s", [session["UCL"][0][3]])
    lifecycle_name = cursor.fetchall()[0][0]

    cursor.execute(
        "select distinct date(creation_dateTime) from crop_data where ucl_id=%s group by date(creation_dateTime) order by date(creation_dateTime) desc limit 5",
        [session["UCL"][0][0]])
    dates = cursor.fetchall()

    cursor.execute(
        "select t.pH, t.creation_dateTime from crop_data t join (select min(t2.creation_dateTime) as min_timestamp from crop_data t2 group by day(t2.creation_dateTime), hour(t2.creation_dateTime)) t2 on t.creation_dateTime = t2.min_timestamp where date(creation_dateTime)=%s and ucl_id=%s order by creation_dateTime desc",
        [creation_date, session["UCL"][0][0]])
    ph_graph_data = cursor.fetchall()

    cursor.execute("select pH from crop_data where date(creation_dateTime)=%s and ucl_id=%s", [creation_date, session["UCL"][0][0]])
    ph_statistics_data = cursor.fetchall()

    cursor.execute("select pHMin, pHMax from data_range where ucl_id=%s", [session["UCL"][0][0]])
    range = cursor.fetchall()

    return render_template("ph_graph.html", culture_name=culture_name, lifecycle_name=lifecycle_name, ph_statistics_data=ph_statistics_data,
                           ph_graph_data=ph_graph_data, range=range, dates=dates, cur_date=creation_date)


def publish(custom_channel, msg):
    pubnub.publish().channel(custom_channel).message(msg).pn_async(my_publish_callback)


def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


if __name__ == '__main__':
    app.run()
