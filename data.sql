DROP DATABASE IF EXISTS GMS;
CREATE DATABASE GMS;
USE GMS;
drop table if exists Users, PresetData, Lifecycle, Culture, UCL, DataRanges;

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

/*Adding data into the tables*/
INSERT INTO Culture VALUES (1, "Strawberry");
INSERT INTO Culture VALUES (2, "Lettuce");
INSERT INTO Culture VALUES (3, "Potato");
INSERT INTO Culture VALUES (4, "Tomato");
INSERT INTO Culture VALUES (5, "Spinach");

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

INSERT INTO PresetData VALUES (13, 3, 1, 7, 10, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (14, 3, 2, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (15, 3, 3, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (16, 3, 4, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (17, 3, 5, 16, 21, 50, 85, 5.8, 6.5);
INSERT INTO PresetData VALUES (18, 3, 6, 16, 21, 50, 85, 5.8, 6.5);

INSERT INTO PresetData VALUES (19, 4, 1, 21, 27, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (20, 4, 2, 14, 18, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (21, 4, 3, 14, 29, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (22, 4, 4, 14, 29, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (23, 4, 5, 14, 29, 65, 85, 5.5, 7.5);
INSERT INTO PresetData VALUES (24, 4, 6, 14, 29, 65, 85, 5.5, 7.5);

INSERT INTO PresetData VALUES (25, 5, 1, -6, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO PresetData VALUES (26, 5, 2, -6, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO PresetData VALUES (27, 5, 3, 10, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO PresetData VALUES (28, 5, 4, 10, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO PresetData VALUES (29, 5, 5, 10, 15.5, 40, 70, 6.0, 7.5);
INSERT INTO PresetData VALUES (30, 5, 6, 10, 15.5, 40, 70, 6.0, 7.5);

INSERT INTO Users VALUES (1, "admin", "admin@admin.com", "123");
INSERT INTO Users VALUES (2, "teomeo", "teomeo@gmail.com", "456");
INSERT INTO Users VALUES (3, "shakira", "shakira@gmail.com", "abc");
INSERT INTO Users VALUES (4, "vincent", "vincent@gmail.com", "def");
INSERT INTO Users VALUES (5, "luana", "luana@gmail.com", "123abc");

INSERT INTO UCL VALUES (1, 1, 1, 1);
INSERT INTO UCL VALUES (2, 2, 3, 2);
INSERT INTO UCL VALUES (3, 3, 1, 5);
INSERT INTO UCL VALUES (4, 4, 4, 2);

INSERT INTO DataRanges VALUES (1, 1, "2022-11-12 15:00:00", 15, 20, 70, 80, 6.0, 7.0);
