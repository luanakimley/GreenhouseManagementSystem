import MySQLdb
import pytest

#TODO change connection to AWS database

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="gms")

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
    "phMax,valid",
    [
        (6.0, True),
        (10.0, False),
        (8.0, False),
        (20.1, False),
        (19.9, False)
    ]
)
def test_temperature_max(tempMax, valid):
    data = {

        'pHMin': 6.0,
        'pHMax': 7.0
    }

    try:
        cur = db.cursor()
        cur.execute("select * from data_range where pHMax=%s", [pHMax])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == data["pHMax"]
        assert user[0][4] == data["pHMin"]
    except:
        assert not valid

