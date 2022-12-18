import MySQLdb
import pytest
import os


# MYSQL Database connection to AWS instance
db = MySQLdb.connect(host=os.getenv('MYSQL_HOST'), port=os.getenv('MYSQL_PORT'), user=os.getenv('MYSQL_USER'), passwd=os.getenv('MYSQL_PASSWORD'), db=os.getenv('MYSQL_DB'))

@pytest.mark.parametrize(
    "password,valid",
    [
        ("$2b$12$T9sRNpwI2.sMPmz/OtI1pe8Yi5hu0iYsIoXwpEiP1MKq5Y9ZKmfN.", True),
        ("$2b$12$T9sRNpwI2.sMPmz/OtI1dsadsadasdasdasdsadasdasdasddasad", False),
        ("abcdefg", False)
    ]
)
def test_validate_password(password, valid):
    data = {
        'username': 'admin',
        'password': password,
        'email': 'admin@admin.com'
    }

    try:
        cur = db.cursor()
        cur.execute("select * from user where password=%s", [password])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][1] == data["username"]
        assert user[0][3] == password
        assert user[0][2] == data["email"]
    except:
        assert not valid


@pytest.mark.parametrize(
    "email,valid",
    [
        ("teomeo@gmail.com", True),
        ("teemeo@gmail.com", False),
        ("teomeo@mai.co", False)
    ]
)
def test_validate_email(email, valid):
    # given
    data = {
        "username": "teomeo",
        "password": "$2b$12$T9sRNpwI2.sMPmz/OtI1pe8Yi5hu0iYsIoXwpEiP1MKq5Y9ZKmfN.",
        "email": email
    }

    # when
    try:
        cur = db.cursor()
        cur.execute("select * from user where email=%s", [email])
        user = cur.fetchall()
        # then
        assert valid
        assert user is not None
        assert user[0][1] == data["username"]
        assert user[0][3] == data["password"]
        assert user[0][2] == email
    except:
        assert not valid


@pytest.mark.parametrize(
    "username,valid",
    [
        ("teomeo", True),
        ("teomee", False),
        ("feomeo", False)
    ]
)
def test_validate_username(username, valid):
    # given
    data = {
        "username": username,
        "password": "$2b$12$T9sRNpwI2.sMPmz/OtI1pe8Yi5hu0iYsIoXwpEiP1MKq5Y9ZKmfN.",
        "email": "teomeo@gmail.com"
    }

    # when
    try:
        cur = db.cursor()
        cur.execute("select * from user where username=%s", [username])
        user = cur.fetchall()
        # then
        assert valid
        assert user is not None
        assert user[0][1] == username
        assert user[0][3] == data["password"]
        assert user[0][2] == data["email"]
    except:
        assert not valid
