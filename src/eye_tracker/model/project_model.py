#-*- coding:utf-8 -*-
"""
project_model


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
from .scene_model import *
#def project_list_model():

def project_create_model(org_id,name,description,ptype,project_key,prefix,project_resource_folder_path):
    """
    创建项目
    """
    db,cursor=connect_mysql()
    if name=="":
        return None,None
    else:
        #验证org合理性[TODO]

        #查找同名，同组织项目
        sql_1="select id from project where name='"+name+"' and org_id="+str(org_id)
        cursor.execute(sql_1)
        results_1 = cursor.fetchall()
        if len(results_1)!=0:
            return None,None
        #插入数据库
        now_time_s=int(time.time())
        now_time=int(round(now_time_s * 1000))
        sql_2="insert into project(name,des,project_key,create_time,last_update_time,org_id,image_location,project_type,prefix,resource_folder_path) values('"+name+"','"+description+"','"+project_key+"',now(),now(),"+str(org_id)+",'','"+ptype+"','"+prefix+"','"+project_resource_folder_path+"')"
        cursor.execute(sql_2)
        last_insert_id = cursor.lastrowid
        db.commit()
        return last_insert_id,now_time

def project_list_model(org_id):
    """
    获取某个org下的项目列表
    """
    db,cursor=connect_mysql()

    sql_1="select id,name,des,project_key,UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),org_id,image_location,project_type,prefix,resource_folder_path from project where org_id="+str(org_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    project_list=[]
    for row in results:
        temp={}
        temp["id"] = row[0]
        temp["name"] = row[1]
        temp["description"] = row[2]
        temp["project_key"] = row[3]
        temp["createdAt"] = row[4]
        temp["updatedAt"] = row[5]
        temp["organizationId"] = row[6]
        temp["imageLocation"] = None
        temp["projectType"] = row[8]
        temp["prefix"] = row[9]
        temp["resource_folder_path"] = row[10]
        temp["hidden"] = False
        #暂时为NONE[TODO]
        temp["stats"] = None
        project_list.append(temp)
    return project_list

def project_key_model(pro_id):
    """
    获取project_key
    """
    db,cursor=connect_mysql()
    sql_1="select project_key from project where id="+str(pro_id)+" limit 0,1"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    if len(results)!=1:
        return None
    project_key=None
    for row in results:
        project_key = row[0]
    return project_key

def project_scene_detail_model(pro_id):
    """
    场景信息+项目详情
    """
    db,cursor=connect_mysql()
    sql_1="select id,name,des,project_key,UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),org_id,image_location,project_type,prefix,resource_folder_path,project_key from project where id="+str(pro_id)+" limit 0,1"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    if len(results)!=1:
        return None
    pro_temp={}
    for row in results:
        pro_temp["id"] = row[0]
        pro_temp["name"] = row[1]
        pro_temp["description"] = row[2]
        pro_temp["project_key"] = row[3]
        pro_temp["createdAt"] = row[4]
        pro_temp["updatedAt"] = row[5]
        pro_temp["organizationId"] = row[6]
        pro_temp["imageLocation"] = None
        pro_temp["projectType"] = row[8]
        pro_temp["prefix"] = row[9]
        pro_temp["resource_folder_path"] = row[10]
        pro_temp["hidden"] = False
        pro_temp["project_key"] = row[11]
        #暂时为NONE[TODO]
        return_final_json=scene_detail_by_pro_id_model(pro_id)
        pro_temp["scenes"] = return_final_json

    return pro_temp





