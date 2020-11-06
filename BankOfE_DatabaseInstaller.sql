CREATE DATABASE IF NOT EXISTS bankofe;
USE bankofe;

CREATE TABLE customerdetails (
cust_id INT(5) NOT NULL PRIMARY KEY,
name VARCHAR(50) NOT NULL,
address VARCHAR(150),
dob DATE NOT NULL,
kvc_docnum VARCHAR(20),
gender INT(1) NOT NULL,
phone VARCHAR(10) NOT NULL,
email_id VARCHAR(50),
occupation VARCHAR(30) );

CREATE TABLE customerbalance (
cust_id INT(5) NOT NULL PRIMARY KEY,
balance INT(20),
last_transaction_time TIMESTAMP );

CREATE TABLE transactions(
transac_id INT(9) NOT NULL PRIMARY KEY,
dcust INT(5) NOT NULL,
ccust INT(5) NOT NULL,
amount BIGINT(20) NOT NULL,
time TIMESTAMP NOT NULL );

CREATE TABLE credentials (
userid VARCHAR(20) NOT NULL PRIMARY KEY,
pwd VARCHAR(30) NOT NULL,
cust_id INT(5) NOT NULL,
admin INT(1) NOT NULL );

INSERT INTO credentials VALUES ("tyrellwellick","joanna66",00002,1);
INSERT INTO credentials VALUES ("sociallyencrypted","mrrobot59",00001,1);
