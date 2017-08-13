-- create user and database for dev-env of lolhf2
CREATE USER 'lolhfdev2'@'%' IDENTIFIED BY 'lolhfdev2';
CREATE DATABASE lolhfdev2;
GRANT ALL ON lolhfdev2.* TO 'lolhfdev2'@'%';
