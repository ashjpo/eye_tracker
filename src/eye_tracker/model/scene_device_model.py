#-*- coding:utf-8 -*-
"""
scene_model


"""
import time
import os,sys
import json
import random

#tool
from tool.model_tool import *
from tool.common_tool import *
#mysql
import pymysql
#mongodb
import pymongo

def scene_upload_project_mes_model(project_key):
    """
    上传scene时查询project相关内容
    """
    db,cursor=connect_mysql()
    sql_1="select id,name,des,org_id,resource_folder_path from project where project_key='"+project_key+"' limit 0,1"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    project_mes=None
    for row in results:
        project_mes={}
        project_mes["id"]=row[0]
        project_mes["name"]=row[1]
        project_mes["des"]=row[2]
        project_mes["org_id"]=row[3]
        project_mes["resource_folder_path"]=row[4]
    return project_mes

def create_scene_model(scene_name,scene_des,sdk_id_str,pro_id,customer_id,latest_screenshot_location,resource_folder_path):
    """
    插入scene
    """
    db,cursor=connect_mysql()
    sql_1="insert into scene(name,des,create_time,last_update_time,sdk_id_str,pro_id,customer_id,latest_screenshot_location,resource_folder_path) values('"+scene_name+"','"+scene_des+"',now(),now(),'"+sdk_id_str+"',"+str(pro_id)+",'"+customer_id+"','"+latest_screenshot_location+"','"+resource_folder_path+"')"
    cursor.execute(sql_1)
    last_insert_id = cursor.lastrowid
    db.commit()
    return last_insert_id

def create_scene_version_model(scene_id,scene_file_type,sdk_version,scale,mesh_name,latest_screenshot_location,resource_file_name_json,scene_version_resource_folder_path):
    """
    插入scene-version
    """
    db,cursor=connect_mysql()
    sql_1="select id from scene_version where scene_id="+str(scene_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    now_version=len(results)+1

    sql_2="insert into scene_version(version_number,scene_id,scene_file_type,sdk_version,scale,mesh_name,latest_screenshot_location,resource_file_name_json,resource_folder_path,create_time,last_update_time) values("+str(now_version)+","+str(scene_id)+",'"+scene_file_type+"','"+sdk_version+"',"+str(scale)+",'"+mesh_name+"','"+latest_screenshot_location+"','"+resource_file_name_json+"','"+scene_version_resource_folder_path+"',now(),now())"
    cursor.execute(sql_2)
    last_insert_id = cursor.lastrowid
    db.commit()
    return last_insert_id
    
def get_scene_setting_model(sdk_id_str):
    """
    获取场景设置
    """
    db,cursor=connect_mysql()
    sql_1="select id,UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),customer_id,pro_id,name,if_public,if_hidden from scene where sdk_id_str='"+sdk_id_str+"'"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    return_dict={}
    scene_id=-1
    for row in results:
        scene_id=row[0]
        return_dict["createdAt"]=row[1]
        return_dict["updatedAt"]=row[2]
        return_dict["customerId"]=row[3]
        return_dict["projectId"]=row[4]
        return_dict["sceneName"]=row[5]
        return_dict["isPublic"]=row[6]
        return_dict["hidden"]=row[7]
        return_dict["id"]=sdk_id_str
    return_dict["versions"]=[]
    sql_2="select UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),id,version_number,scale,sdk_version,scene_file_type from scene_version where scene_id="+str(scene_id)
    cursor.execute(sql_2)
    results = cursor.fetchall()
    for row in results:
        temp={}
        temp["createdAt"]=row[0]
        temp["updatedAt"]=row[1]
        temp["id"]=row[2]
        temp["versionNumber"]=row[3]
        temp["scale"]=row[4]
        temp["sdkVersion"]=row[5]
        temp["sceneFileType"]=row[6]
        #[TODO]
        temp["hasFixations"]=False
        temp["isOptimized"]=None
        temp["dynamicsUpdateKey"]=None

        return_dict["versions"].append(temp)
    return return_dict

def scene_search_by_sdk_id_str_model(sdk_id_str):
    """
    通过sdk_id_str查找scene
    """
    db,cursor=connect_mysql()
    sql_1="select id from scene where sdk_id_str='"+sdk_id_str+"'"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    scene_id=-1
    for row in results:
        scene_id=row[0]
    disconnect_mysql(db)
    return scene_id

def scene_version_resource_path_search_model(sdk_id_str,version_number):
    """
    通过sdk_id_str查找scene-version
    """
    scene_id=scene_search_by_sdk_id_str_model(sdk_id_str)
    if scene_id==-1:
        return None
    db,cursor=connect_mysql()
    sql_1="select resource_folder_path from scene_version where scene_id="+str(scene_id)+" and version_number="+str(version_number)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    resource_folder_path=None
    for row in results:
        resource_folder_path=row[0]
    return resource_folder_path
    


