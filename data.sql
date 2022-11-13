DROP DATABASE IF EXISTS GMS;
CREATE DATABASE GMS;
USE GMS;
drop table if exists Users, PlantData, Notifications, Users_Notifications, PresetData, Lifecycle, Culture;

/*Creating tables*/
create table Culture (culture_id int NOT NULL AUTO_INCREMENT,
name varchar(30),
PRIMARY KEY (culture_id));

create table Lifecycle (lifecycle_id int NOT NULL AUTO_INCREMENT,
name varchar(30),
PRIMARY KEY (lifecycle_id));

create table PresetData (presetData_id int NOT NULL AUTO_INCREMENT,
culture_id int NOT NULL,
lifecycle_id int NOT NULL,
tempMin double,
tempMax double,
humidityMin int,
humidityMax int,
pHMin double,
pHMax double,
PRIMARY KEY (presetData_id),
FOREIGN KEY (culture_id) REFERENCES Culture(culture_id),
FOREIGN KEY (lifecycle_id) REFERENCES Lifecycle(lifecycle_id)); 

create table Users (users_id int NOT NULL AUTO_INCREMENT,
username varchar(30),
email varchar(125),
password varchar(300),
UNIQUE(username),
UNIQUE(email),
PRIMARY KEY (users_id));

create table PlantData (plants_id int NOT NULL AUTO_INCREMENT,
users_id int NOT NULL,
presetData_id int NOT NULL,
/*Not sure if code below this is needed*/
culture_id int NOT NULL,
lifecycle_id int NOT NULL,
/*Not sure if code above this is needed*/
creation_dateTime DATETIME,
temp double,
tempMin double,
tempMax double,
humidity int,
humidityMin int,
humidityMax int,
pH double,
pHMin double,
pHMax double,
moisture varchar(20),
PRIMARY KEY (plants_id),
FOREIGN KEY (culture_id) REFERENCES Culture(culture_id),
FOREIGN KEY (lifecycle_id) REFERENCES Lifecycle(lifecycle_id),
FOREIGN KEY (presetData_id) REFERENCES PresetData(presetData_id),
FOREIGN KEY (users_id) REFERENCES Users(users_id)); 

create table Notifications (notifications_id int NOT NULL AUTO_INCREMENT,
description varchar(125),
image BLOB,
PRIMARY KEY (notifications_id));

create table Users_Notifications (notifications_id int NOT NULL AUTO_INCREMENT,
users_id int NOT NULL,
notification_dateTime DATETIME,
PRIMARY KEY (notifications_id, users_id),
FOREIGN KEY (notifications_id) REFERENCES Notifications(notifications_id),
FOREIGN KEY (users_id) REFERENCES Users(users_id)); 

/*Adding data into the tables*/
INSERT INTO Culture VALUES ("C1", "Strawberry");
INSERT INTO Culture VALUES ("C2", "Lettuce");
INSERT INTO Culture VALUES ("C3", "Potato");
INSERT INTO Culture VALUES ("C4", "Tomato");

INSERT INTO Lifecycle VALUES ("L1", "Sprout");
INSERT INTO Lifecycle VALUES ("L2", "Seeding");
INSERT INTO Lifecycle VALUES ("L3", "Vegetative");
INSERT INTO Lifecycle VALUES ("L4", "Blooming");
INSERT INTO Lifecycle VALUES ("L5", "Flowering");
INSERT INTO Lifecycle VALUES ("L6", "Mature");

INSERT INTO PresetData VALUES ("PD1", "C1", "L1", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD2", "C1", "L2", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD3", "C1", "L3", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD4", "C1", "L4", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD5", "C1", "L5", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD6", "C1", "L6", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD7", "C2", "L1", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD8", "C2", "L2", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD9", "C2", "L3", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD10", "C2", "L4", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD11", "C2", "L5", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD12", "C2", "L6", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD13", "C3", "L1", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD14", "C3", "L2", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD15", "C3", "L3", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD16", "C3", "L4", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD17", "C3", "L5", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD18", "C3", "L6", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD19", "C4", "L1", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD20", "C4", "L2", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD21", "C4", "L3", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD22", "C4", "L4", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD23", "C4", "L5", 15, 20, 45, 60, 6.0, 7.0);
INSERT INTO PresetData VALUES ("PD24", "C4", "L6", 15, 20, 45, 60, 6.0, 7.0);

INSERT INTO Users VALUES ("U1", "admin", "admin@admin.com", "123");
INSERT INTO Users VALUES ("U2", "teomeo", "teomeo@gmail.com", "456");
INSERT INTO Users VALUES ("U3", "shakira", "shakira@gmail.com", "abc");
INSERT INTO Users VALUES ("U4", "vincent", "vincent@gmail.com", "def");
INSERT INTO Users VALUES ("U5", "luana", "luana@gmail.com", "123abc");

INSERT INTO PlantData VALUES ("P1", "U1", "PD1", "C1", "L1",  "2022-11-08 15:00:00", 17, 62.6, 15, 20, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P2", "U1", "PD1", "C1", "L1",  "2022-11-09 15:00:00", 18, 64.4, 15, 20, 50, 45, 60, 6.5, 6.0, 7.0, "Dry");
INSERT INTO PlantData VALUES ("P3", "U1", "PD1", "C1", "L1",  "2022-11-10 15:00:00", 20, 68, 15, 20, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P4", "U2", "PD4", "C1", "L4",  "2022-11-11 15:00:00", 15, 59, 15, 20, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P5", "U1", "PD1", "C1", "L1",  "2022-11-11 15:00:00", 16, 60.8, 15, 20, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P6", "U1", "PD1", "C1", "L1",  "2022-11-12 15:00:00", 17, 62.6, 15, 20, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P7", "U1", "PD1", "C1", "L1",  "2022-11-13 15:00:00", 19, 66.2, 15, 20, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P8", "U2", "PD4", "C1", "L4",  "2022-11-14 15:00:00", 15, 59, 15, 20, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P9", "U1", "PD1", "C1", "L1",  "2022-11-14 15:00:00", 15, 59, 15, 20, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");

INSERT INTO Notifications VALUES ("N1", "Your plants needs watering", "warning1.png");
INSERT INTO Notifications VALUES ("N2", "Your plant is too warm", "warning2.png");
INSERT INTO Notifications VALUES ("N3", "Your plant needs more pH solution", "warning3.png");
INSERT INTO Notifications VALUES ("N3", "Your plant is too cold", "warning4.png");

INSERT INTO Users_Notifications VALUES ("N1", "U1", "2022-11-09 12:45:56");
INSERT INTO Users_Notifications VALUES ("N1", "U2", "2022-11-09 12:45:56");
INSERT INTO Users_Notifications VALUES ("N3", "U1", "2022-11-09 12:45:56");
INSERT INTO Users_Notifications VALUES ("N1", "U4", "2022-11-09 12:45:56");

/*Deleting data older than 7 days*/
SET GLOBAL event_scheduler = ON;

Create Event del_plants_data on SCHEDULE every 1 Day do Delete from PlantData 
where datediff(Now(), creation_dateTime) > 7; 

/*Creating indexes for each data gathered*/
Create index Plant_pH_index On PlantData (pH, pHMin, pHMax);
Create index Plant_humidity_index On PlantData (humidity, humidityMin, humidityMax); 
Create index Plant_temp_index On PlantData (temp, tempMin, tempMax); 
Create index Plant_moisture_index On PlantData (moisture); 

/*Creating a view to find out which are under or over their min/max*/
Create view Plants_Over_Under_Min_Max as Select u.users_id, u.username, p.plants_id, p.temp, p.tempMin, p.tempMax, p.humidity, p.humidityMin, p.humidityMax, p.pH, p.pHMin, p.pHMax 
from PlantData p join Users u using (users_id) 
where p.temp > p.tempMax or p.temp < p.tempMin or p.humidity> p. humidityMax or p. humidity < p. humidityMin or p. pH > p. pHMax or p. pH < p. pHMin; 

/*Creating a view to find out which are equal their min/max*/
Create view Plants_Equal_Min_Max as Select u.users_id, u.username, p.plants_id, p.temp, p.tempMin, p.tempMax, p.humidity, p.humidityMin, p.humidityMax, p.pH, p.pHMin, p.pHMax 
from PlantData p join Users u using (users_id) 
where p.temp = p.tempMax or p.temp = p.tempMin or p.humidity= p. humidityMax or p. humidity = p. humidityMin or p. pH = p. pHMax or p. pH = p. pHMin; 
