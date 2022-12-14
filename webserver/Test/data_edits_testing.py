import MySQLdb
import pytest
import os

# MYSQL Database connection to AWS instance
db = MySQLdb.connect(host=os.getenv('MYSQL_HOST'), port=os.getenv('MYSQL_PORT'), user=os.getenv('MYSQL_USER'), passwd=os.getenv('MYSQL_PASSWORD'), db=os.getenv('MYSQL_DB'))



@pytest.mark.parametrize(
    "tempMin,valid",
    [
        (15, True),
        (14, False),
        (16, False),
        (15.1, False),
        (14.9, False)
    ]
)
def test_temperature_min(tempMin, valid):
    data = {
        'tempMin': tempMin,
        'tempMax': 20,
        'humidityMin': 70,
        'humidityMax': 80,
        'pHMin': 6.0,
        'pHMax': 7.0
    }

    try:
        cur = db.cursor()
        cur.execute("select * from data_range where tempMin=%s", [tempMin])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == tempMin
        assert user[0][4] == data["tempMax"]
        assert user[0][5] == data["humidityMin"]
        assert user[0][6] == data["humidityMax"]
        assert user[0][7] == data["pHMin"]
        assert user[0][8] == data["pHMax"]
    except:
        assert not valid

@pytest.mark.parametrize(
    "tempMax,valid",
    [
        (20, True),
        (19, False),
        (21, False),
        (20.1, False),
        (19.9, False)
    ]
)
def test_temperature_max(tempMax, valid):
    data = {
        'tempMin': 15,
        'tempMax': tempMax,
        'humidityMin': 70,
        'humidityMax': 80,
        'pHMin': 6.0,
        'pHMax': 7.0
    }

    try:
        cur = db.cursor()
        cur.execute("select * from data_range where tempMax=%s", [tempMax])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == data["tempMin"]
        assert user[0][4] == tempMax
        assert user[0][5] == data["humidityMin"]
        assert user[0][6] == data["humidityMax"]
        assert user[0][7] == data["pHMin"]
        assert user[0][8] == data["pHMax"]
    except:
        assert not valid


@pytest.mark.parametrize(
    "humidityMin,valid",
    [
        (70, True),
        (14, False),
        (16, False),
        (15.1, False),
        (14.9, False)
    ]
)
def test_humidity_min(humidityMin, valid):
    data = {
        'tempMin': 15,
        'tempMax': 20,
        'humidityMin': humidityMin,
        'humidityMax': 80,
        'pHMin': 6.0,
        'pHMax': 7.0
    }

    try:
        cur = db.cursor()
        cur.execute("select * from data_range where humidityMin=%s", [humidityMin])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == data["tempMin"]
        assert user[0][4] == data["tempMax"]
        assert user[0][5] == humidityMin
        assert user[0][6] == data["humidityMax"]
        assert user[0][7] == data["pHMin"]
        assert user[0][8] == data["pHMax"]
    except:
        assert not valid

@pytest.mark.parametrize(
    "humidityMax,valid",
    [
        (80, True),
        (19, False),
        (21, False),
        (20.1, False),
        (19.9, False)
    ]
)
def test_humidity_max(humidityMax, valid):
    data = {
        'tempMin': 15,
        'tempMax': 20,
        'humidityMin': 70,
        'humidityMax': humidityMax,
        'pHMin': 6.0,
        'pHMax': 7.0
    }

    try:
        cur = db.cursor()
        cur.execute("select * from data_range where humidityMax=%s", [humidityMax])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == data["tempMin"]
        assert user[0][4] == data["tempMax"]
        assert user[0][5] == data["humidityMin"]
        assert user[0][6] == humidityMax
        assert user[0][7] == data["pHMin"]
        assert user[0][8] == data["pHMax"]
    except:
        assert not valid


@pytest.mark.parametrize(
    "pHMin,valid",
    [
        (6.0, True),
        (14, False),
        (16, False),
        (15.1, False),
        (14.9, False)
    ]
)
def test_ph_min(pHMin, valid):
    data = {
        'tempMin': 15,
        'tempMax': 20,
        'humidityMin': 70,
        'humidityMax': 80,
        'pHMin': pHMin,
        'pHMax': 7.0
    }

    try:
        cur = db.cursor()
        cur.execute("select * from data_range where pHMin=%s", [pHMin])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == data["tempMin"]
        assert user[0][4] == data["tempMax"]
        assert user[0][5] == data["humidityMin"]
        assert user[0][6] == data["humidityMax"]
        assert user[0][7] == pHMin
        assert user[0][8] == data["pHMax"]
    except:
        assert not valid

@pytest.mark.parametrize(
    "pHMax,valid",
    [
        (7.0, True),
        (19, False),
        (21, False),
        (20.1, False),
        (19.9, False)
    ]
)
def test_ph_max(pHMax, valid):
    data = {
        'tempMin': 15,
        'tempMax': 20,
        'humidityMin': 70,
        'humidityMax': 80,
        'pHMin': 6.0,
        'pHMax': pHMax
    }

    try:
        cur = db.cursor()
        cur.execute("select * from data_range where pHMax=%s", [pHMax])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == data["tempMin"]
        assert user[0][4] == data["tempMax"]
        assert user[0][5] == data["humidityMin"]
        assert user[0][6] == data["humidityMax"]
        assert user[0][7] == data["pHMin"]
        assert user[0][8] == pHMax
    except:
        assert not valid
