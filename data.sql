DROP DATABASE IF EXISTS GMS;
CREATE DATABASE GMS;
USE GMS;
drop table if exists Users, PlantData, Notifications, Users_Notifications, PresetData, Lifecycle, Culture;

/*Creating tables*/

create table Culture (culture_id varchar(20) NOT NULL,
name varchar(20),
PRIMARY KEY (culture_id));

create table Lifecycle (lifecycle_id varchar(20) NOT NULL,
name varchar(20),
PRIMARY KEY (lifecycle_id));

create table PresetData (presetData_id varchar(20) NOT NULL,
culture_id varchar(20) NOT NULL,
lifecycle_id varchar(20) NOT NULL,
tempCMin double,
tempCMax double,
tempFMin double,
tempFMax double,
humidityMin int,
humidityMax int,
pHMin double,
pHMax double,
PRIMARY KEY (presetData_id),
FOREIGN KEY (culture_id) REFERENCES Culture(culture_id),
FOREIGN KEY (lifecycle_id) REFERENCES Lifecycle(lifecycle_id)); 

create table Users (users_id varchar(20) NOT NULL,
username varchar(20),
email varchar(20),
password varchar(20),
PRIMARY KEY (users_id));

create table PlantData (plants_id varchar(20) NOT NULL,
users_id varchar(20) NOT NULL,
presetData_id varchar(20) NOT NULL,
culture_id varchar(20) NOT NULL,
lifecycle_id varchar(20) NOT NULL,
creation_date date,
tempC double,
tempF double,
tempCMin double,
tempCMax double,
tempFMin double,
tempFMax double,
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

create table Notifications (notifications_id varchar(20) NOT NULL,
description varchar(50),
image BLOB,
PRIMARY KEY (notifications_id));

create table Users_Notifications (notifications_id varchar(20) NOT NULL,
users_id varchar(20) NOT NULL,
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

INSERT INTO PresetData VALUES ("PD1", "C1", "L1", 15, 20, 59, 68, 45, 60, 6.0, 7.0);

INSERT INTO Users VALUES ("U1", "admin", "admin@admin.com", "123");

INSERT INTO PlantData VALUES ("P1", "U1", "PD1", "C1", "L1",  "2022-11-08", 17, 62.6, 15, 20, 59, 68, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P2", "U1", "PD1", "C1", "L1",  "2022-11-09", 18, 64.4, 15, 20, 59, 68, 50, 45, 60, 6.5, 6.0, 7.0, "Dry");
INSERT INTO PlantData VALUES ("P3", "U1", "PD1", "C1", "L1",  "2022-11-10", 20, 68, 15, 20, 59, 68, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P4", "U1", "PD1", "C1", "L1",  "2022-11-11", 16, 60.8, 15, 20, 59, 68, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P5", "U1", "PD1", "C1", "L1",  "2022-11-12", 17, 62.6, 15, 20, 59, 68, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P6", "U1", "PD1", "C1", "L1",  "2022-11-13", 19, 66.2, 15, 20, 59, 68, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");
INSERT INTO PlantData VALUES ("P7", "U1", "PD1", "C1", "L1",  "2022-11-14", 15, 59, 15, 20, 59, 68, 50, 45, 60, 6.5, 6.0, 7.0, "Wet");

INSERT INTO Notifications VALUES ("N1", "Your plants need watering", "warning1.png");

INSERT INTO Users_Notifications VALUES ("N1", "U1", "2022-11-09 12:45:56");

/*Deleting data older than 7 days*/
SET GLOBAL event_scheduler = ON;

Create Event del_plants_data on SCHEDULE every 1 Day do Delete from PlantData 
where datediff(Now(), creation_date) > 7; 

/*Creating indexes for each data gathered*/
Create index Plant_pH_index On PlantData (pH, pHMin, pHMax);
Create index Plant_humidity_index On PlantData (humidity, humidityMin, humidityMax); 
Create index Plant_temp_index On PlantData (tempC, tempF, tempCMin, tempCMax, tempFMin, tempFMax); 
Create index Plant_moisture_index On PlantData (moisture); 

/*Creating a view to find out which are under or over their min/max*/
Create view Plants_Over_Under_Min_Max as Select u.users_id, u.username, p.plants_id, p.tempC, p.tempCMin, p.tempCMax, p.tempFMin, p.tempFMax, p.humidity, p.humidityMin, p.humidityMax, p.pH, p.pHMin, p.pHMax 
from PlantData p join Users u using (users_id) 
where p.tempC > p.tempCMax or p.tempC < p.tempCMin or p.tempF > p.tempFMax or p.tempF < p.tempFMin or p.humidity> p. humidityMax or p. humidity < p. humidityMin or p. pH > p. pHMax or p. pH < p. pHMin; 

/*Creating a view to find out which are equal their min/max*/
Create view Plants_Equal_Min_Max as Select u.users_id, u.username, p.plants_id, p.tempC, p.tempCMin, p.tempCMax, p.tempFMin, p.tempFMax, p.humidity, p.humidityMin, p.humidityMax, p.pH, p.pHMin, p.pHMax 
from PlantData p join Users u using (users_id) 
where p.tempC = p.tempCMax or p.tempC = p.tempCMin or p.tempF = p.tempFMax or p.tempF = p.tempFMin or p.humidity= p. humidityMax or p. humidity = p. humidityMin or p. pH = p. pHMax or p. pH = p. pHMin; 
