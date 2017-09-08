#!/bin/python3

#Python Script to migrate passwords from esoTalk to NodeBB

from pymongo import MongoClient
import os
import mysql.connector

#MongoDB
mongodb = "your_mongo_database"
mongodb_username = "your_mongodb_username"
mongodb_password = "your_mongodb_password"


#MySQL
mysqldb = "your_mysql_database"
mysqldb_username = "your_mysqldb_username"
mysqldb_password = "your_mysqldb_password"


try:
    client = MongoClient()
    db = client["nodebb"]
    db.authenticate(mongodb_username, mongodb_password, source='admin')
    coll = db["objects"]

    cnx = mysql.connector.connect(user=mysqldb_username, password=mysqldb_password,host='127.0.0.1',database=mysqldb)
    cursor = cnx.cursor()

    for new_uid in range(20,340): #input your UID Range here. Check your database.
        user = coll.find_one({"_key":"user:" + str(new_uid)})
        if user:
           old_uid = user["_imported_uid"]
           query = ("SELECT password FROM `et_member` WHERE `memberId`= %d"%old_uid)
           cursor.execute(query)
    
           for (_password,) in cursor:
               password = _password
               print(password)
               new_pass = {}
               new_pass["passwordExpiry"] = 0
               new_pass["password"] = password
               db["objects"].update({'_id':user["_id"]}, {"$set": new_pass})

               print("update_user %d"%old_uid)
except KeyError:
    print("KeyError encountered")