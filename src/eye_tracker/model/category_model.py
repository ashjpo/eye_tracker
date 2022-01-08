#-*- coding:utf-8 -*-
"""
category_model


"""
import time
import os,sys
import json
import random
import datetime

#tool
from tool.model_tool import *
from tool.common_tool import *
#mysql
import pymysql
#mongodb
import pymongo
from bson import ObjectId 
from bson import json_util

def create_category_model(name,scene_version_id):
    """
    创建category
    """
    db,cursor=connect_mysql()
    sql_1="select id from category where name='"+name+"'"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    if len(results)>0:
        return -1
    sql_2="insert into category(name,scene_version_id,create_time,last_update_time) values('"+name+"',"+str(scene_version_id)+",now(),now())"
    cursor.execute(sql_2)
    last_insert_id = cursor.lastrowid
    db.commit()
    return last_insert_id

def create_group_model(categoryId,name):
    """
    创建group
    """
    db,cursor=connect_mysql()
    sql_1="select id from cat_group where name='"+name+"' and cat_id="+str(categoryId)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    if len(results)>0:
        return -1
    dynamicObjectsIds_json="[]"
    sql_2="insert into cat_group(cat_id,name,dynamicObjectsIds_json,create_time,last_update_time) values("+str(categoryId)+",'"+name+"','"+dynamicObjectsIds_json+"',now(),now())"
    cursor.execute(sql_2)
    last_insert_id = cursor.lastrowid
    db.commit()
    return last_insert_id

def category_detail_model(categoryId):
    """
    获取单个category详情
    """
    db,cursor=connect_mysql()
    sql_1="select UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),id,name,autoCreatedType from category where id="+str(categoryId)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    return_json={}
    for row in results:
        return_json["createdAt"]=row[0]
        return_json["updatedAt"]=row[1]
        return_json["id"]=row[2]
        return_json["name"]=row[3]
        return_json["autoCreatedType"]=row[4]
    return_json["dynamicObjectGroups"]=[]
    sql_2="select UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),id,name,dynamicObjectsIds_json from cat_group where cat_id="+str(categoryId)
    cursor.execute(sql_2)
    results = cursor.fetchall()
    for row in results:
        temp={}
        temp["createdAt"]=row[0]
        temp["updatedAt"]=row[1]
        temp["id"]=row[2]
        temp["name"]=row[3]
        temp["dynamicObjectsIds"]=json.loads(row[4])
        return_json["dynamicObjectGroups"].append(temp)
    return return_json
    
def set_dobj_to_group_model(parm,g_id):
    """
    向group中设置dobj
    """
    db,cursor=connect_mysql()
    sql_2="select dynamicObjectsIds_json from cat_group where id="+str(g_id)
    cursor.execute(sql_2)
    results = cursor.fetchall()
    dynamicObjectsIds_json=None
    for row in results:
        dynamicObjectsIds_json=row[0]
    if dynamicObjectsIds_json is None:
        dynamicObjectsIds=[]
    elif dynamicObjectsIds_json=="":
        dynamicObjectsIds=[]
    else:
        dynamicObjectsIds=json.loads(dynamicObjectsIds_json)
    dynamicObjectsIds+=parm["dynamicObjectsIds"]
    sql_1="update cat_group set dynamicObjectsIds_json='"+json.dumps(dynamicObjectsIds)+"' where id="+str(g_id)
    print(sql_1)
    cursor.execute(sql_1)
    db.commit()

def get_obj_category_list_model(scene_version_id):
    """
    get_obj_category_list
    """
    db,cursor=connect_mysql()
    sql_1="select id from category where scene_version_id="+str(scene_version_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    id_list=[]
    for row in results:
        id_list.append(row[0])
    rlist=[]
    for mid in id_list:
        rlist.append(category_detail_model(mid))
    return rlist