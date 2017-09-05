#!/bin/bash
read -p "Please input your mysql user:" user
read -p "Please input your mysql password:" password
mysql --user=${user} --password=${password} << eof

#delete Exchange_rate_table database

#DROP DATABASE Exchange_rate_table;

eof

mysql --user=${user} --password=${password} << eof

#init Exchange_rate_table database

CREATE DATABASE Exchange_rate_table;

USE Exchange_rate_table;

CREATE TABLE LatestInformation(
     ID INT AUTO_INCREMENT primary key,
     Currency_Name TEXT,
     Buying_Rate TEXT,
     Cash_Buying_Rate TEXT,
     Selling_Rate TEXT,
     Cash_Selling_Rate TEXT,
     Exchange_Rate_Base_Price TEXT
   )character set = utf8;

eof
