#-*- coding:utf-8 -*-
"""
admin_model


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

def organization_regist_model(org_name,org_des,org_account,org_password):
    """
    注册org
    """
    #判断是否为空
    if org_name=="" or verify_account_str(org_account)==False or verify_password_str(org_password)==False:
        return -1
    else:
        #判断org_name是否由重复
        db,cursor=connect_mysql()
        try:
            sql_1="select id from organization where name='"+org_name+"'"
            cursor.execute(sql_1)
            results = cursor.fetchall()
            if len(results)>0:
                return -1
            else:
                #插入数据库
                sql_2="insert into organization(name,des,org_account,org_password,create_time) values('"+org_name+"','"+org_des+"','"+org_account+"','"+org_password+"',now())"
                cursor.execute(sql_2)
                last_insert_id = cursor.lastrowid
                db.commit()
                return last_insert_id
        except:
            return -1

def organization_list_model():
    """
    获取organization_list
    """
    db,cursor=connect_mysql()
    try:
        sql_1="select id,name,des,UNIX_TIMESTAMP(create_time) from organization"
        cursor.execute(sql_1)
        results = cursor.fetchall()
        organization_list=[]
        for row in results:
            temp={}
            temp["id"] = row[0]
            temp["name"] = row[1]
            temp["des"] = row[2]
            temp["create_time"] = row[3]
            organization_list.append(temp)
        return organization_list
    except:
        return []



def organization_detail_model(org_id):
    """
    获取organization_detail
    """
    db,cursor=connect_mysql()
    try:
        sql_1="select id,name,des,UNIX_TIMESTAMP(create_time) from organization where id="+org_id+" limit 0,1"
        cursor.execute(sql_1)
        results = cursor.fetchall()
        organization_list=[]
        for row in results:
            temp={}
            temp["id"] = row[0]
            temp["name"] = row[1]
            temp["des"] = row[2]
            temp["create_time"] = row[3]
            organization_list.append(temp)
        return organization_list[0]
    except:
        return None


def user_regist_model(org_account,org_password,user_name,user_des,user_account,user_password):
    """
    user注册
    """
    db,cursor=connect_mysql()
    try:
        #验证org
        sql_1="select id from organization where org_account='"+org_account+"' and org_password='"+org_password+"'"
        cursor.execute(sql_1)
        results_1 = cursor.fetchall()
        if len(results_1)==1:
            org_id=-1
            for row in results_1:
                org_id=row[0]
            #验证user_name
            sql_2="select id from user where name='"+user_name+"'"
            cursor.execute(sql_2)
            results_2 = cursor.fetchall()
            if len(results_2)==0:
                if user_name=="" or verify_account_str(user_account)==False or verify_password_str(user_password)==False:
                    return -1
                else:
                    sql_3="insert into user(name,des,user_account,user_password,create_time,power_level,org_id) values('"+user_name+"','"+user_des+"','"+user_account+"','"+user_password+"',now(),'default',"+str(org_id)+")"
                    cursor.execute(sql_3)
                    last_insert_id = cursor.lastrowid
                    db.commit()
                    return last_insert_id
            else:
                return -1
        else:
            return -1
    except:
        return -1

    
def organization_user_list_model(org_id):
    """
    organization下的user列表

    """
    db,cursor=connect_mysql()
    try:
        sql_1="select id,name,des,UNIX_TIMESTAMP(create_time),power_level from user where org_id="+str(org_id)
        cursor.execute(sql_1)
        results = cursor.fetchall()
        user_list=[]
        for row in results:
            temp={}
            temp["id"] = row[0]
            temp["name"] = row[1]
            temp["des"] = row[2]
            temp["create_time"] = row[3]
            temp["power_level"] = row[4]
            user_list.append(temp)
        return user_list
    except:
        return []

def user_detail_model(user_id):
    """
    获取user detail
    """
    db,cursor=connect_mysql()
    try:
        sql_1="select id,name,des,UNIX_TIMESTAMP(create_time),power_level from user where id="+str(user_id)+" limit 0,1"
        cursor.execute(sql_1)
        results = cursor.fetchall()
        user_list=[]
        for row in results:
            temp={}
            temp["id"] = row[0]
            temp["name"] = row[1]
            temp["des"] = row[2]
            temp["create_time"] = row[3]
            temp["power_level"] = row[4]
            user_list.append(temp)
        return user_list[0]
    except:
        return None

def user_login_model(user_account,user_password):
    db,cursor=connect_mysql()
    sql_1="select user.id as user_id,organization.id as org_id from user,organization where user.org_id=organization.id and user.user_account='"+user_account+"' and user.user_password='"+user_password+"'"
    print(sql_1)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    user_id=-1
    org_id=-1
    for row in results:
        user_id=row[0]
        org_id=row[1]
    return org_id,user_id
