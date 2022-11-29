import MySQLdb
import pytest

#TODO change connection to AWS database

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="gms")

@pytest.mark.parametrize(
    "humidity,valid",
    [
        (50, True),
        (51, False),
        (49, False)
    ]
)
def test_humidity(humidity, valid):
    data = {
        'temp': 17,
        'humidity': humidity,
        'pH': 6.5,
        'moisture': 'Wet'
    }

    try:
        cur = db.cursor()
        cur.execute("select * from crop_data where humidity=%s", [humidity])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == data["temp"]
        assert user[0][4] == humidity
        assert user[0][5] == data["pH"]
        assert user[0][6] == data["moisture"]
    except:
        assert not valid


@pytest.mark.parametrize(
    "temp,valid",
    [
        (20, True),
        (19, False),
        (21, False)
    ]
)
def test_temperature(temp, valid):
    data = {
        'temp': temp,
        'humidity': 68,
        'pH': 7.0,
        'moisture': 'Wet'
    }

    try:
        cur = db.cursor()
        cur.execute("select * from crop_data where temp=%s", [temp])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == temp
        assert user[0][4] == data["humidity"]
        assert user[0][5] == data["pH"]
        assert user[0][6] == data["moisture"]
    except:
        assert not valid


@pytest.mark.parametrize(
    "pH,valid",
    [
        (6.0, True),
        (6.1, False),
        (5.9, False)
    ]
)
def test_pH(pH, valid):
    data = {
        'temp': 15,
        'humidity': 79,
        'pH': pH,
        'moisture': 'Wet'
    }

    try:
        cur = db.cursor()
        cur.execute("select * from crop_data where pH=%s", [pH])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == data["temp"]
        assert user[0][4] == data["humidity"]
        assert user[0][5] == pH
        assert user[0][6] == data["moisture"]
    except:
        assert not valid

@pytest.mark.parametrize(
    "moisture,valid",
    [
        ("Dry", True),
        ("Wet", False),
        ("ASDWqwesa", False)

    ]
)
def test_moisture(moisture, valid):
    data = {
        'temp': 18,
        'humidity': 75,
        'pH': 7.0,
        'moisture': moisture
    }

    try:
        cur = db.cursor()
        cur.execute("select * from crop_data where moisture=%s", [moisture])
        user = cur.fetchall()
        assert valid
        assert user is not None
        assert user[0][3] == data["temp"]
        assert user[0][4] == data["humidity"]
        assert user[0][5] == data["pH"]
        assert user[0][6] == moisture
    except:
        assert not valid
