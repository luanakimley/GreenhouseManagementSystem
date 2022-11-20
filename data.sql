DROP DATABASE IF EXISTS GMS;
CREATE DATABASE GMS;
USE GMS;
drop table if exists Users, CropData, Notifications, Users_Notifications, PresetData, Lifecycle, Culture, UCL, DataRanges;

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
password varchar(100),
UNIQUE(email),
PRIMARY KEY (users_id));

create table UCL (ucl_id int NOT NULL AUTO_INCREMENT,
users_id int NOT NULL,
culture_id int NOT NULL,
lifecycle_id int NOT NULL,
PRIMARY KEY (ucl_id),
FOREIGN KEY (culture_id) REFERENCES Culture(culture_id),
FOREIGN KEY (lifecycle_id) REFERENCES Lifecycle(lifecycle_id),
FOREIGN KEY (users_id) REFERENCES Users(users_id)); 

create table CropData (crops_id int NOT NULL AUTO_INCREMENT,
ucl_id int NOT NULL,
creation_dateTime DATETIME,
temp double,
humidity int,
pH double,
moisture varchar(20),
PRIMARY KEY (crops_id),
FOREIGN KEY (ucl_id) REFERENCES UCL(ucl_id)); 

create table DataRanges (dataRanges_id int NOT NULL AUTO_INCREMENT,
ucl_id int NOT NULL,
creation_dateTime DATETIME,
tempMin double,
tempMax double,
humidityMin int,
humidityMax int,
pHMin double,
pHMax double,
PRIMARY KEY (dataRanges_id),
FOREIGN KEY (ucl_id) REFERENCES UCL(ucl_id));

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
INSERT INTO Culture VALUES (1, "Strawberry");
INSERT INTO Culture VALUES (2, "Lettuce");
INSERT INTO Culture VALUES (3, "Potato");
INSERT INTO Culture VALUES (4, "Tomato");

INSERT INTO Lifecycle VALUES (1, "Sprout");
INSERT INTO Lifecycle VALUES (2, "Seedling");
INSERT INTO Lifecycle VALUES (3, "Vegetative");
INSERT INTO Lifecycle VALUES (4, "Budding");
INSERT INTO Lifecycle VALUES (5, "Flowering");
INSERT INTO Lifecycle VALUES (6, "Ripening");

INSERT INTO PresetData VALUES (1, 1, 1, 10, 26, 65, 75, 5.8, 6.2);
INSERT INTO PresetData VALUES (2, 1, 2, 10, 26, 65, 75, 5.8, 6.2);
INSERT INTO PresetData VALUES (3, 1, 3, 10, 26, 65, 75, 5.8, 6.2);
INSERT INTO PresetData VALUES (4, 1, 4, 15, 26, 65, 75, 5.8, 6.2);
INSERT INTO PresetData VALUES (5, 1, 5, 15, 26, 65, 75, 5.8, 6.2);
INSERT INTO PresetData VALUES (6, 1, 6, 15, 26, 65, 75, 5.8, 6.2);

INSERT INTO PresetData VALUES (7, 2, 1, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO PresetData VALUES (8, 2, 2, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO PresetData VALUES (9, 2, 3, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO PresetData VALUES (10, 2, 4, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO PresetData VALUES (11, 2, 5, 10, 21, 50, 75, 6.0, 7.0);
INSERT INTO PresetData VALUES (12, 2, 6, 10, 21, 50, 75, 6.0, 7.0);


INSERT INTO PresetData VALUES (13, 1, 1, 7, 10, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (14, 1, 2, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (15, 1, 3, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (16, 1, 4, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (17, 1, 5, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (18, 1, 6, 16, 21, 50, 85, 5.8, 6.5);

INSERT INTO PresetData VALUES (19, 1, 1, 21, 27, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (20, 1, 2, 14, 18, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (21, 1, 3, 14, 29, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (22, 1, 4, 14, 29, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (23, 1, 5, 14, 29, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (24, 1, 6, 14, 29, 65, 85, 5.5, 7.5);

INSERT INTO PresetData VALUES (5, 1, 5, 18, 25, 65, 75, 5.4, 6.5);
INSERT
INSERT INTO Users VALUES (1, "admin", "admin@admin.com", "123");
INSERT INTO Users VALUES (2, "teomeo", "teomeo@gmail.com", "456");
INSERT INTO Users VALUES (3, "shakira", "shakira@gmail.com", "abc");
INSERT INTO Users VALUES (4, "vincent", "vincent@gmail.com", "def");
INSERT INTO Users VALUES (5, "luana", "luana@gmail.com", "123abc");

INSERT INTO UCL VALUES (1, 1, 1, 1);
INSERT INTO UCL VALUES (2, 2, 3, 2);
INSERT INTO UCL VALUES (3, 3, 1, 5);
INSERT INTO UCL VALUES (4, 4, 4, 2);

INSERT INTO CropData VALUES (1, 1, "2022-11-08 15:00:00", 17, 50, 6.5, "Wet");
INSERT INTO CropData VALUES (2, 1, "2022-11-09 15:00:00", 18, 75, 7.0, "Dry");
INSERT INTO CropData VALUES (3, 1, "2022-11-10 15:00:00", 20, 68, 7.0, "Wet");
INSERT INTO CropData VALUES (4, 1, "2022-11-11 15:00:00", 15, 79, 6.0, "Wet");
INSERT INTO CropData VALUES (5, 1, "2022-11-11 15:00:00", 16, 60, 6.2, "Wet");
INSERT INTO CropData VALUES (6, 1, "2022-11-12 15:00:00", 17, 72, 6.8, "Wet");
INSERT INTO CropData VALUES (7, 1, "2022-11-13 15:00:00", 20, 66, 7.0, "Wet");

INSERT INTO DataRanges VALUES (1, 1, "2022-11-12 15:00:00", 15, 20, 70, 80, 6.0, 7.0);

INSERT INTO Notifications VALUES (1, "Your crop needs wateri21, 25, 65, 75, 5.4, 6.5);ng", "warning1.png");
INSERT INTO Notifications VALUES (2, "Your crop is too warm", "warning2.png");
INSERT INTO Notifications VALUES (3, "Your crop needs more pH solution", "warning3.png");
INSERT INTO Notifications VALUES (4, "Your crop is too cold", "warning4.png");

INSERT INTO Users_Notifications VALUES (1, 1, "2022-10-08 10:45:00");
INSERT INTO Users_Notifications VALUES (1, 2, "2022-11-09 12:45:56");
INSERT INTO Users_Notifications VALUES (1, 3, "2022-11-10 12:25:12");
INSERT INTO Users_Notifications VALUES (1, 4, "2022-12-11 11:45:16");

/*Deleting data older than 7 days*/
SET GLOBAL event_scheduler = ON;

Create Event del_crops_data on SCHEDULE every 1 Day do Delete from CropData 
where datediff(Now(), creation_dateTime) > 7; 

/*Creating a view to find out which are under or over their min/max*/
Create view Crops_Over_Under_Min_Max as Select p.crops_id, p.temp, pd.tempMin, pd.tempMax, p.humidity, pd.humidityMin, pd.humidityMax, p.pH, pd.pHMin, pd.pHMax 
from CropData p join UCL ucl using (ucl_id) join PresetData pd using(culture_id)
where p.temp > pd.tempMax or p.temp < pd.tempMin or p.humidity> pd.humidityMax or p.humidity < pd.humidityMin or p.pH > pd.pHMax or p.pH < pd.pHMin; 

/*Creating a view to find out which are equal their min/max*/
Create view Crops_Equal_Min_Max as Select p.crops_id, p.temp, pd.tempMin, pd.tempMax, p.humidity, pd.humidityMin, pd.humidityMax, p.pH, pd.pHMin, pd.pHMax 
from CropData p join UCL ucl using (ucl_id) join PresetData pd using(culture_id)
where p.temp = pd.tempMax or p.temp = pd.tempMin or p.humidity = pd.humidityMax or p.humidity = pd.humidityMin or p.pH = pd.pHMax or p.pH = pd.pHMin; 
