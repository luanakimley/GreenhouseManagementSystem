import MySQLdb
import pytest
from werkzeug.routing import ValidationError
from webserver.application import mysql, app
from flask_mysqldb import MySQL
import os

mysql = MySQL(app)
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="gms")

@pytest.mark.parametrize(
    "password,valid",
    [
        ("$2b$12$T9sRNpwI2.sMPmz/OtI1peRbpO0A4k3tfQW8NoAmRYv7ptJyXSTGy", True)
    ]
)
def test_validate_password(password, valid):
    data = {
        'username': 'teomeo',
        'password': password,
        'email': 'teomeo@gmail.com'
    }

    try:
        cur = db.cursor()
        cur.execute("select * from user where password=%s", [password])
        user = cur.fetchall()
        assert user is not None
        assert user[0][1] == data["username"]
        assert user[0][3] == password
        assert user[0][2] == data["email"]
    except ValidationError:
        assert not valid


@pytest.mark.parametrize(
    "email,valid",
    [
        ("teomeo@gmail.com", True)
    ]
)
def test_validate_email(email, valid):
    # given
    data = {
        "username": "teomeo",
        "password": "$2b$12$T9sRNpwI2.sMPmz/OtI1peRbpO0A4k3tfQW8NoAmRYv7ptJyXSTGy",
        "email": email
    }

    # when
    try:
        cur = db.cursor()
        cur.execute("select * from user where email=%s", [email])
        user = cur.fetchall()
        # then
        assert user is not None
        assert user[0][1] == data["username"]
        assert user[0][3] == data["password"]
        assert user[0][2] == email
    except ValidationError:
        assert not valid


@pytest.mark.parametrize(
    "username,valid",
    [
        ("teomeo", True)
    ]
)
def test_validate_username(username, valid):
    # given
    data = {
        "username": username,
        "password": "$2b$12$T9sRNpwI2.sMPmz/OtI1peRbpO0A4k3tfQW8NoAmRYv7ptJyXSTGy",
        "email": "teomeo@gmail.com"
    }

    # when
    try:
        cur = db.cursor()
        cur.execute("select * from user where username=%s", [username])
        user = cur.fetchall()
        # then
        assert user is not None
        assert user[0][1] == username
        assert user[0][3] == data["password"]
        assert user[0][2] == data["email"]
    except ValidationError:
        assert not valid
