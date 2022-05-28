CREATE DATABASE tcss506;
USE tcss506;

CREATE TABLE `ADMIN`(
	`username` varchar(15) PRIMARY KEY,
    `password` varchar(12) NOT NULL
);
INSERT INTO `ADMIN` VALUES
	('admin','12345678');
SELECT* FROM ADMIN;

CREATE TABLE `CUSTOMER`(
	`username` varchar(15) PRIMARY KEY,
    `password` varchar(12) NOT NULL,
    `address` varchar(300) NOT NULL,
    `phone` varchar(15) NOT NULL
);
INSERT INTO `CUSTOMER` VALUES
	('testcustomer','00000000','university of washington tacoma','111-111-1111');
SELECT* FROM CUSTOMER;
    
CREATE TABLE `RESTAURANT`(
	`username` varchar(15) PRIMARY KEY,
    `password` varchar(12) NOT NULL,
    `address` varchar(300) NOT NULL,
    `phone` varchar(15) NOT NULL,
    `img_res` varchar(50)
);
INSERT INTO `RESTAURANT` VALUES
	('pizza shop','00000000','university of washington tacoma','111-111-1112',null);
SELECT* FROM RESTAURANT;

CREATE TABLE `MENU`(
	`dishname` varchar(15) PRIMARY KEY,
	`restaurant` varchar(15) NOT NULL,
    `price` DECIMAL(5,2) NOT NULL,
    `imgsrc` varchar(50),
	FOREIGN KEY (restaurant)
    REFERENCES RESTAURANT(username)
);
INSERT INTO MENU VALUES
	('cheese pizza', 'pizza shop', 26.00, null),
    ('vegitable pizza', 'pizza shop', 20.00, null);
SELECT* FROM MENU;

CREATE TABLE `ORDERS`(
	`customer` varchar(15),
    `restaurant` varchar(15),
    `dishname` varchar(15),
    `price` DECIMAL(5,2) NOT NULL,
    `img_res` varchar(50),
	FOREIGN KEY (customer)
    REFERENCES CUSTOMER(username),
	FOREIGN KEY (restaurant)
    REFERENCES RESTAURANT(username),
	FOREIGN KEY (dishname)
    REFERENCES MENU(dishname),
    PRIMARY KEY (customer,restaurant,dishname)
);
INSERT INTO `ORDERS` VALUES
	('testcustomer','pizza shop','cheese pizza',26.00,null);
SELECT* FROM ORDERS;