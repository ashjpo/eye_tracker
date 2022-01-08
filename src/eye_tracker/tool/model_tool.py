#-*- coding:utf-8 -*-
"""
model tool


"""
#config
import config.web_server_config as wsg

#mysql
import pymysql
#mongodb
import pymongo

#【MYSQL】
def connect_mysql():
    """
    连接数据库
    """
    db = pymysql.connect(wsg.mysql_db_host,wsg.mysql_db_username,wsg.mysql_db_password,wsg.mysql_db_name,port=int(wsg.mysql_db_port),charset="utf8")
    cursor = db.cursor()
    return db,cursor

def disconnect_mysql(db):
    """
    断开连接数据库
    """
    db.close()

#【MONGODB】
def connect_mongodb():
    conn = pymongo.MongoClient("mongodb://"+wsg.mongodb_db_host+":"+wsg.mongodb_db_port+"/")
    db = conn[wsg.mongodb_db_name]
    return db

