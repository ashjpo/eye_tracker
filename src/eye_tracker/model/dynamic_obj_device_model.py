#-*- coding:utf-8 -*-
"""
dynamic_obj_device_model


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
from .scene_device_model import *


def dynamic_obj_manifest_upload_model(obj_json,sdk_id_str,scene_version_id,sv_resource_folder_path):
    """
    上传dynamic_obj_manifest
    """
    sv_dobj_resource_folder_path=sv_resource_folder_path+"/dynamic_obj"
    db,cursor=connect_mysql()
    for obj in obj_json:
        obj_id=obj["id"]
        mesh=obj["mesh"]
        name=obj["name"]
        dobj_sv_dobj_resource_folder_path=sv_dobj_resource_folder_path+"/"+mesh
        scene_file_type="gltf"
        latest_screenshot_location=""
        resource_file_name_json="[]"
        if search_dobj_by_mesh_name_model(scene_version_id,mesh)==False:
            sql="insert into dynamic_obj(scene_version_id,sdk_id_str,name,mesh_name,scene_file_type,latest_screenshot_location,resource_folder_path,resource_file_name_json,create_time,last_update_time) values("+str(scene_version_id)+",'"+obj_id+"','"+name+"','"+mesh+"','"+scene_file_type+"','"+latest_screenshot_location+"','"+dobj_sv_dobj_resource_folder_path+"','"+resource_file_name_json+"',now(),now())"
            cursor.execute(sql)
            last_insert_id = cursor.lastrowid
        else:
            sql="update dynamic_obj set sdk_id_str='"+obj_id+"',name='"+name+"' where scene_version_id='"+str(scene_version_id)+"' and mesh_name='"+mesh+"'"
            cursor.execute(sql)
    db.commit()

def search_dobj_by_mesh_name_model(scene_version_id,mesh_name):
    """
    通过scene_version_id和meshname查找dobj
    """
    db,cursor=connect_mysql()
    sql_1="select id from dynamic_obj where scene_version_id="+str(scene_version_id)+" and mesh_name='"+mesh_name+"'"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    if len(results)>0:
        return True
    else:
        return False
    

def upload_dobj_without_insert_model(mesh_name,sdk_id_str,scene_version_id,sv_resource_folder_path,screenshot_file_name,file_name_list):
    """
    上传dynamic_obj之前没有在数据库中创建
    """
    sv_dobj_resource_folder_path=sv_resource_folder_path+"/dynamic_obj"
    db,cursor=connect_mysql()
    dobj_sv_dobj_resource_folder_path=sv_dobj_resource_folder_path+"/"+mesh_name
    scene_file_type="gltf"
    sql="insert into dynamic_obj(scene_version_id,mesh_name,scene_file_type,latest_screenshot_location,resource_folder_path,resource_file_name_json,create_time,last_update_time) values("+str(scene_version_id)+",'"+mesh_name+"','"+scene_file_type+"','"+screenshot_file_name+"','"+dobj_sv_dobj_resource_folder_path+"','"+json.dumps(file_name_list)+"',now(),now())"
    cursor.execute(sql)
    last_insert_id = cursor.lastrowid
    db.commit()

def upload_dobj_model(file_name_list,mesh_name,scene_version_id,screenshot_file_name):
    """
    上传动态物体
    """
    db,cursor=connect_mysql()
    sql="update dynamic_obj set resource_file_name_json='"+json.dumps(file_name_list)+"',latest_screenshot_location='"+screenshot_file_name+"' where mesh_name='"+mesh_name+"' and scene_version_id="+str(scene_version_id)
    cursor.execute(sql)
    db.commit()


def scene_version_search_by_sdk_id_str_model(sdk_id_str,version_number):
    """
    通过sdk_id_str,version_number查找scene的id和资源文件夹
    """
    scene_id=scene_search_by_sdk_id_str_model(sdk_id_str)
    if scene_id==-1:
        return None,None
    db,cursor=connect_mysql()
    sql_1="select id,resource_folder_path from scene_version where scene_id="+str(scene_id)+" and version_number="+str(version_number)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    scene_version_id=-1
    resource_folder_path=None
    for row in results:
        scene_version_id=row[0]
        resource_folder_path=row[1]
    return scene_version_id,resource_folder_path
    

