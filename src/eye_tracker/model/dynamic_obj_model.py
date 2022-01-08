#-*- coding:utf-8 -*-
"""
dynamic_obj_model


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

def dynamic_obj_list_model(scene_version_id):
    """
    dynamic_obj_list
    """
    db,cursor=connect_mysql()
    sql_1="select UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),id,scene_version_id,name,mesh_name,scene_file_type,sdk_id_str,latest_screenshot_location,resource_folder_path from dynamic_obj where scene_version_id="+str(scene_version_id)+" and sdk_id_str is not null"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    dynamic_obj_list=[]
    for row in results:
        temp={}
        temp["createdAt"]=row[0]
        temp["updatedAt"]=row[1]
        temp["id"]=row[2]
        temp["versionId"]=row[3]
        temp["name"]=row[4]
        temp["meshName"]=row[5]
        temp["dynamicFileType"]=row[6]
        temp["group"]=None
        temp["sdkId"]=row[7]
        temp["thumbnailLocation"]=row[9]+"/"+row[8]
        temp["externalId"]=None
        temp["externalBaseUrl"]=None
        temp["isOptimized"]=None
        dynamic_obj_list.append(temp)
    return dynamic_obj_list
        


def dynamic_obj_detail_model(dynamic_obj_id):
    """
    dynamic_obj_detail
    """
    db,cursor=connect_mysql()
    sql_1="select UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),id,scene_version_id,name,mesh_name,scene_file_type,sdk_id_str,latest_screenshot_location,resource_folder_path,resource_file_name_json from dynamic_obj where id="+str(dynamic_obj_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    temp={}
    for row in results:
        temp["createdAt"]=row[0]
        temp["updatedAt"]=row[1]
        temp["id"]=row[2]
        temp["versionId"]=row[3]
        temp["name"]=row[4]
        temp["meshName"]=row[5]
        temp["dynamicFileType"]=row[6]
        temp["group"]=None
        temp["sdkId"]=row[7]
        temp["thumbnailLocation"]=row[9]+"/"+row[8]
        temp["externalId"]=None
        temp["externalBaseUrl"]=None
        temp["isOptimized"]=None
        temp["files"]=[]
        ttt=row[10]
        if ttt!="":
            resource_file_name_json=json.loads(ttt)
            for file_name in resource_file_name_json:
                ppp={}
                ppp["createdAt"]=temp["createdAt"]
                ppp["updatedAt"]=temp["updatedAt"]
                ppp["id"]="-"
                ppp["type"]=file_name.split(".")[-1]
                ppp["name"]=file_name
                ppp["location"]=row[9]
                ppp["forDynamic"]=True
                temp["files"].append(ppp)

    return temp