DROP DATABASE IF EXISTS gms;
CREATE DATABASE gms;
USE gms;
drop table if exists user, crop_data, notification, user_notification, preset_data, lifecycle, culture, ucl, data_range;

/*Creating tables*/
create table culture (culture_id int NOT NULL AUTO_INCREMENT,
name varchar(30),
PRIMARY KEY (culture_id));

create table lifecycle (lifecycle_id int NOT NULL AUTO_INCREMENT,
name varchar(30),
PRIMARY KEY (lifecycle_id));

create table preset_data (presetData_id int NOT NULL AUTO_INCREMENT,
culture_id int NOT NULL,
lifecycle_id int NOT NULL,
tempMin double,
tempMax double,
humidityMin int,
humidityMax int,
pHMin double,
pHMax double,
PRIMARY KEY (presetData_id),
FOREIGN KEY (culture_id) REFERENCES culture(culture_id),
FOREIGN KEY (lifecycle_id) REFERENCES lifecycle(lifecycle_id));

create table user (users_id int NOT NULL AUTO_INCREMENT,
username varchar(30),
email varchar(125),
password varchar(100),
UNIQUE(email),
PRIMARY KEY (users_id));

create table ucl (ucl_id int NOT NULL AUTO_INCREMENT,
users_id int NOT NULL,
culture_id int NOT NULL,
lifecycle_id int NOT NULL,
PRIMARY KEY (ucl_id),
FOREIGN KEY (culture_id) REFERENCES culture(culture_id),
FOREIGN KEY (lifecycle_id) REFERENCES lifecycle(lifecycle_id),
FOREIGN KEY (users_id) REFERENCES user(users_id)); 

create table crop_data (crops_id int NOT NULL AUTO_INCREMENT,
ucl_id int NOT NULL,
creation_dateTime DATETIME,
temp double,
humidity int,
pH double,
moisture varchar(20),
PRIMARY KEY (crops_id),
FOREIGN KEY (ucl_id) REFERENCES ucl(ucl_id)); 

create table data_range (dataRanges_id int NOT NULL AUTO_INCREMENT,
ucl_id int NOT NULL,
creation_dateTime DATETIME,
tempMin double,
tempMax double,
humidityMin int,
humidityMax int,
pHMin double,
pHMax double,
PRIMARY KEY (dataRanges_id),
FOREIGN KEY (ucl_id) REFERENCES ucl(ucl_id));

create table notification (notifications_id int NOT NULL AUTO_INCREMENT,
description varchar(125),
icon varchar(100),
PRIMARY KEY (notifications_id));

create table user_notification (user_notification_id int NOT NULL AUTO_INCREMENT,
notifications_id int NOT NULL,
users_id int NOT NULL,
notification_dateTime DATETIME,
PRIMARY KEY (user_notification_id),
FOREIGN KEY (notifications_id) REFERENCES notification(notifications_id),
FOREIGN KEY (users_id) REFERENCES user(users_id));

/*Adding data into the tables*/
INSERT INTO culture VALUES (1, "Strawberry");
INSERT INTO culture VALUES (2, "Lettuce");
INSERT INTO culture VALUES (3, "Potato");
INSERT INTO culture VALUES (4, "Tomato");
INSERT INTO culture VALUES (5, "Spinach");

INSERT INTO lifecycle VALUES (1, "Sprout");
INSERT INTO lifecycle VALUES (2, "Seedling");
INSERT INTO lifecycle VALUES (3, "Vegetative");
INSERT INTO lifecycle VALUES (4, "Budding");
INSERT INTO lifecycle VALUES (5, "Flowering");
INSERT INTO lifecycle VALUES (6, "Ripening");

INSERT INTO preset_data VALUES (1, 1, 1, 10, 26, 65, 75, 5.8, 6.2);
INSERT INTO preset_data VALUES (2, 1, 2, 10, 26, 65, 75, 5.8, 6.2);
INSERT INTO preset_data VALUES (3, 1, 3, 10, 26, 65, 75, 5.8, 6.2);
INSERT INTO preset_data VALUES (4, 1, 4, 15, 26, 65, 75, 5.8, 6.2);
INSERT INTO preset_data VALUES (5, 1, 5, 15, 26, 65, 75, 5.8, 6.2);
INSERT INTO preset_data VALUES (6, 1, 6, 15, 26, 65, 75, 5.8, 6.2);

INSERT INTO preset_data VALUES (7, 2, 1, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO preset_data VALUES (8, 2, 2, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO preset_data VALUES (9, 2, 3, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO preset_data VALUES (10, 2, 4, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO preset_data VALUES (11, 2, 5, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO preset_data VALUES (12, 2, 6, 10, 21, 50, 75, 6.0, 7.0);

INSERT INTO preset_data VALUES (13, 3, 1, 7, 10, 50, 85, 5.8, 6.5);
INSERT INTO preset_data VALUES (14, 3, 2, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO preset_data VALUES (15, 3, 3, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO preset_data VALUES (16, 3, 4, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO preset_data VALUES (17, 3, 5, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO preset_data VALUES (18, 3, 6, 16, 21, 50, 85, 5.8, 6.5);

INSERT INTO preset_data VALUES (19, 4, 1, 21, 27, 65, 85, 5.5, 7.5);
INSERT INTO preset_data VALUES (20, 4, 2, 14, 18, 65, 85, 5.5, 7.5);
INSERT INTO preset_data VALUES (21, 4, 3, 14, 29, 65, 85, 5.5, 7.5);
INSERT INTO preset_data VALUES (22, 4, 4, 14, 29, 65, 85, 5.5, 7.5);
INSERT INTO preset_data VALUES (23, 4, 5, 14, 29, 65, 85, 5.5, 7.5);
INSERT INTO preset_data VALUES (24, 4, 6, 14, 29, 65, 85, 5.5, 7.5);

INSERT INTO preset_data VALUES (25, 5, 1, -6, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO preset_data VALUES (26, 5, 2, -6, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO preset_data VALUES (27, 5, 3, 10, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO preset_data VALUES (28, 5, 4, 10, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO preset_data VALUES (29, 5, 5, 10, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO preset_data VALUES (30, 5, 6, 10, 15.5, 40, 70, 6.0, 7.5);

INSERT INTO user VALUES (1, "admin", "admin@admin.com", "$2b$12$T9sRNpwI2.sMPmz/OtI1pe8Yi5hu0iYsIoXwpEiP1MKq5Y9ZKmfN.");
INSERT INTO user VALUES (2, "teomeo", "teomeo@gmail.com", "$2b$12$T9sRNpwI2.sMPmz/OtI1pe8Yi5hu0iYsIoXwpEiP1MKq5Y9ZKmfN.");
INSERT INTO user VALUES (3, "shakira", "shakira@gmail.com", "$2b$12$T9sRNpwI2.sMPmz/OtI1pe8Yi5hu0iYsIoXwpEiP1MKq5Y9ZKmfN.");
INSERT INTO user VALUES (4, "vincent", "vincent@gmail.com", "$2b$12$T9sRNpwI2.sMPmz/OtI1pe8Yi5hu0iYsIoXwpEiP1MKq5Y9ZKmfN.");
INSERT INTO user VALUES (5, "luana", "luana@gmail.com", "$2b$12$T9sRNpwI2.sMPmz/OtI1pe8Yi5hu0iYsIoXwpEiP1MKq5Y9ZKmfN.");

INSERT INTO ucl VALUES (1, 1, 1, 1);
INSERT INTO ucl VALUES (2, 2, 3, 2);
INSERT INTO ucl VALUES (3, 3, 1, 5);
INSERT INTO ucl VALUES (4, 4, 4, 2);

INSERT INTO crop_data VALUES (1, 1, "2022-11-08 15:00:00", 17, 50, 6.5, "Wet");
INSERT INTO crop_data VALUES (2, 1, "2022-11-09 15:00:00", 18, 75, 7.0, "Dry");
INSERT INTO crop_data VALUES (3, 1, "2022-11-10 15:00:00", 20, 68, 7.0, "Wet");
INSERT INTO crop_data VALUES (4, 1, "2022-11-11 15:00:00", 15, 79, 6.0, "Wet");
INSERT INTO crop_data VALUES (5, 1, "2022-11-11 15:00:00", 16, 60, 6.2, "Wet");
INSERT INTO crop_data VALUES (6, 1, "2022-11-12 15:00:00", 17, 72, 6.8, "Wet");
INSERT INTO crop_data VALUES (7, 1, "2022-11-13 15:00:00", 20, 66, 7.0, "Wet");

INSERT INTO data_range VALUES (1, 1, "2022-11-12 15:00:00", 15, 20, 70, 80, 6.0, 7.0);

INSERT INTO notification VALUES (1, "Your crop needs watering", "water");
INSERT INTO notification VALUES (2, "Your crop is too warm", "device_thermostat");
INSERT INTO notification VALUES (3, "Your crop needs more pH solution", "water_ph");
INSERT INTO notification VALUES (4, "Your crop is too cold", "device_thermostat");
INSERT INTO notification VALUES (5, "Motion detected near crops", "directions_run");

INSERT INTO user_notification VALUES (1, 1, 1, "2022-10-08 10:45:00");
INSERT INTO user_notification VALUES (2, 2, 1, "2022-11-09 12:45:56");
INSERT INTO user_notification VALUES (3, 3, 1, "2022-11-10 12:25:12");
INSERT INTO user_notification VALUES (4, 4, 1, "2022-12-11 11:45:16");
INSERT INTO user_notification VALUES (5, 5, 1, "2022-12-12 12:16:09");

/*Creating a view to find out which are under or over their min/max*/
Create view Crops_Over_Under_Min_Max as Select p.crops_id, p.temp, pd.tempMin, pd.tempMax, p.humidity, pd.humidityMin, pd.humidityMax, p.pH, pd.pHMin, pd.pHMax 
from crop_data p join ucl using (ucl_id) join preset_data pd using(culture_id)
where p.temp > pd.tempMax or p.temp < pd.tempMin or p.humidity> pd.humidityMax or p.humidity < pd.humidityMin or p.pH > pd.pHMax or p.pH < pd.pHMin; 

/*Creating a view to find out which are equal their min/max*/
Create view Crops_Equal_Min_Max as Select p.crops_id, p.temp, pd.tempMin, pd.tempMax, p.humidity, pd.humidityMin, pd.humidityMax, p.pH, pd.pHMin, pd.pHMax 
from crop_data p join ucl using (ucl_id) join preset_data pd using(culture_id)
where p.temp = pd.tempMax or p.temp = pd.tempMin or p.humidity = pd.humidityMax or p.humidity = pd.humidityMin or p.pH = pd.pHMax or p.pH = pd.pHMin; 
