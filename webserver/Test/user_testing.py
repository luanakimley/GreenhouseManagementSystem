import MySQLdb
import pytest

#TODO change connection to AWS database

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="gms")

@pytest.mark.parametrize(
    "password,valid",
    [
        ("$2b$12$T9sRNpwI2.sMPmz/OtI1peRbpO0A4k3tfQW8NoAmRYv7ptJyXSTGy", True),
        ("12345678@", False),
        ("$2b$12$T9sRNpwI2.sMPmz/OtI1peRbpO0A4k3tfQW8NoAmRYv7ptJyXST12", False)
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
        ("luana@gmail.com", True),
        ("luana@mail.com", False),
        ("luana@gmailcom", False)
    ]
)
def test_validate_email(email, valid):
    # given
    data = {
        "username": "luana",
        "password": "$2b$12$T9sRNpwI2.sMPmz/OtI1peRbpO0A4k3tfQW8NoAmRYv7ptJyXSTGy",
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
        ("shakira", True),
        ("shakiraa", False),
        ("sakira", False)
    ]
)
def test_validate_username(username, valid):
    # given
    data = {
        "username": username,
        "password": "$2b$12$T9sRNpwI2.sMPmz/OtI1peRbpO0A4k3tfQW8NoAmRYv7ptJyXSTGy",
        "email": "shakira@gmail.com"
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
