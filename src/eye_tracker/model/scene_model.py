#-*- coding:utf-8 -*-
"""
scene_model


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


def scene_version_id_search_by_sceneidstr_vnumber(scene_id_str,scene_version_number):
    """
    查询scene_version_number
    """
    db,cursor=connect_mysql()
    sql_1="select scene_version.id from scene_version,scene where scene.sdk_id_str='"+scene_id_str+"' and scene_version.version_number="+str(scene_version_number)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    scene_version_id=-1
    for row in results:
        scene_version_id=row[0]
    return scene_version_id

def organization_id_from_scene_version_id(scene_version_id):
    """
    通过scene_version_id获取org_id
    """
    db,cursor=connect_mysql()
    sql_1="select project.org_id from project,scene,scene_version where scene_version.scene_id=scene.id and scene.pro_id=project.id and scene_version.id="+str(scene_version_id)
    org_id=-1
    cursor.execute(sql_1)
    results = cursor.fetchall()
    for row in results:
        org_id=row[0]
    return org_id

    

def scene_detail_model(sdk_id_str):
    """
    和原版由些不同，没有查询本月
    """
    db,cursor=connect_mysql()
    #scene
    sql_1="select id,name,des,UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),pro_id,customer_id,latest_screenshot_location,if_hidden,if_public from scene where sdk_id_str='"+sdk_id_str+"' limit 0,1"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    return_dict={}
    sid=-1
    for row in results:
        sid=row[0]
        return_dict["sceneName"]=row[1]
        return_dict["createdAt"]=row[3]
        return_dict["updatedAt"]=row[4]
        return_dict["id"]=sdk_id_str
        return_dict["projectId"]=row[5]
        return_dict["customerId"]=row[6]
        return_dict["latestScreenshotLocation"]=row[7]
        return_dict["hidden"]=row[8]
        return_dict["isPublic"]=row[9]
    return_dict["versions"]=[]
    if sid==-1:
        return None
    else:
        sql_2="select UNIX_TIMESTAMP(scene_version.create_time),UNIX_TIMESTAMP(scene_version.last_update_time),scene_version.id,scene_version.version_number,scene_version.scale,scene_version.sdk_version,scene_version.scene_file_type,scene_version.latest_screenshot_location,scene_version.resource_folder_path from scene_version where scene_version.scene_id="+str(sid)
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
            temp["hasFixations"]=True
            temp["isOptimized"]=None
            temp["dynamicsUpdateKey"]=None
            temp["latest_screenshot_location"]=row[7]
            temp["resource_folder_path"]=row[8]
            sql_3="select count(id),max(UNIX_TIMESTAMP(session.session_start_time)) as latest_session from session where scene_version_id="+str(temp["id"])
            cursor.execute(sql_3)
            results_inner = cursor.fetchall()
            temp["stats"]={}
            for row_inner in results_inner:
                temp["stats"]["latest_session"]=row_inner[1]
                temp["stats"]["session_count"]=row_inner[0]
                #[TODO]
                temp["stats"]["total_gaze_time"]=None
            #2
            sql_4="select id from session where DATE_FORMAT( create_time, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' ) and scene_version_id="+str(temp["id"])
            cursor.execute(sql_4)
            results_month = cursor.fetchall()
            temp["stats"]["session_count_by_month"]=len(results_month)
            return_dict["versions"].append(temp)
        return return_dict




def scene_detail_by_pro_id_model(pro_id):
    """
    和原版由些不同，没有查询本月
    """
    db,cursor=connect_mysql()
    #scene
    sql_1="select id,name,des,UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),pro_id,customer_id,latest_screenshot_location,if_hidden,if_public,sdk_id_str from scene where pro_id="+str(pro_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    return_final_json=[]
    sid=-1
    for row in results:
        return_dict={}
        sid=row[0]
        return_dict["sid"]=sid
        return_dict["sceneName"]=row[1]
        return_dict["createdAt"]=row[3]
        return_dict["updatedAt"]=row[4]
        return_dict["id"]=row[10]
        return_dict["projectId"]=row[5]
        return_dict["customerId"]=row[6]
        return_dict["latestScreenshotLocation"]=row[7]
        return_dict["hidden"]=row[8]
        return_dict["isPublic"]=row[9]
        return_dict["versions"]=[]

        sql_2="select UNIX_TIMESTAMP(scene_version.create_time),UNIX_TIMESTAMP(scene_version.last_update_time),scene_version.id,scene_version.version_number,scene_version.scale,scene_version.sdk_version,scene_version.scene_file_type,scene_version.latest_screenshot_location from scene_version where scene_version.scene_id="+str(sid)
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
            temp["hasFixations"]=True
            temp["isOptimized"]=None
            temp["dynamicsUpdateKey"]=None
            temp["latest_screenshot_location"]=row[7]
            #1
            sql_3="select count(id),max(UNIX_TIMESTAMP(session.session_start_time)) as latest_session from session where scene_version_id="+str(temp["id"])
            cursor.execute(sql_3)
            results_inner = cursor.fetchall()
            temp["stats"]={}
            for row_inner in results_inner:
                temp["stats"]["latest_session"]=row_inner[1]
                temp["stats"]["session_count"]=row_inner[0]
                #[TODO]
                temp["stats"]["total_gaze_time"]=None
            #2
            sql_4="select id from session where DATE_FORMAT( create_time, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' ) and scene_version_id="+str(temp["id"])
            cursor.execute(sql_4)
            results_month = cursor.fetchall()
            temp["stats"]["session_count_by_month"]=len(results_month)
            return_dict["versions"].append(temp)
        return_final_json.append(return_dict)
    return return_final_json
