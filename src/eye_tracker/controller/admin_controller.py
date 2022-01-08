#-*- coding:utf-8 -*-
"""
admin_controller

FUNCTION:
    (1) organization_regist      
        组织注册
        PARM:   name,des,account,password
        RETURN: 注册成果返回org_id/否在返回false[error_1_1]

    (2) organization_list
        查询组织列表
        PARM:   无
        RETURN: 返回组织id,name,des,create_time数组

    (3) organization_detail
        查询组织基本信息
        PARM:   org_id
        RETURN: 返回组织id,name,des,create_time

    (4) organization_delete (不具体实现)
        删除组织

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.admin_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.admin_model import *

admin=Blueprint('admin',__name__)

@admin.route(cg.organization_regist_url,methods=["POST"])
def organization_regist():
    """
    [POST]
    组织注册
    """
    if request.method=='POST':
        try:
            parm=json.loads(request.get_data())
            org_name=parm['org_name']
            org_des=parm['org_des']
            org_account=parm['org_account']
            org_password=parm['org_password']
        except:
            return "-1"
        last_insert_id=organization_regist_model(org_name,org_des,org_account,org_password)
        if last_insert_id==-1:
            return "-1"
        else:
            return str(last_insert_id)
    else:
        return "-1"

@admin.route(cg.organization_list_url,methods=["GET"])
def organization_list():
    """
    [GET]
    查询组织列表
    """
    if request.method=='GET':
        organization_list=organization_list_model()
        return json.dumps(organization_list)
    else:
        return "error"
    
@admin.route(cg.organization_detail_url,methods=["GET"])
def organization_detail():
    """
    [GET]
    查询组织基本信息
    """
    if request.method=='GET':
        try:
            org_id = request.args.get("org_id")
            organization_detail=organization_detail_model(org_id)
            if organization_detail is None:
                return "error"
            else:
                return json.dumps(organization_detail)
        except:
            return "error"

    else:
        return "error"

@admin.route(cg.organization_delete_url,methods=["GET"])
def organization_delete():
    """
    [GET]
    删除组织(不具体实现)
    """
    return "[Please contact the administrator!]"



#==========================================================================

@admin.route(cg.user_regist_url,methods=["POST"])
def user_regist():
    """
    [POST]
    注册用户
    """
    if request.method=='POST':
        try:
            parm=json.loads(request.get_data())
            org_account=parm['org_account']
            org_password=parm['org_password']
            user_name=parm['user_name']
            user_des=parm['user_des']
            user_account=parm['user_account']
            user_password=parm['user_password']
        except:
            return "-1"
        last_insert_id=user_regist_model(org_account,org_password,user_name,user_des,user_account,user_password)
        if last_insert_id==-1:
            return "-1"
        else:
            return str(last_insert_id)
    else:
        return "-1"

@admin.route(cg.user_org_list_url,methods=["GET"])
def user_org_list():
    """
    [GET]
    查询某个组织下的用户
    """
    if request.method=='GET':
        try:
            org_id = request.args.get("org_id")
            organization_user_list=organization_user_list_model(org_id)
            return json.dumps(organization_user_list)
        except:
            return "error"

    else:
        return "error"

@admin.route(cg.user_detail_url,methods=["GET"])
def user_detail():
    """
    [GET]
    查看用户详情
    """
    if request.method=='GET':
        try:
            user_id = request.args.get("user_id")
            user_detail=user_detail_model(user_id)
            if user_detail is None:
                return "error"
            else:
                return json.dumps(user_detail)
        except:
            return "error"
    else:
        return "error"

@admin.route(cg.user_delete_url,methods=["GET"])
def user_delete():
    """
    [GET]
    删除某个组织下的用户(不具体实现)
    """
    return "[Please contact the administrator!]"

@admin.route(cg.user_delete_url,methods=["GET"])
def user_edit():
    """
    [GET]
    用户内容更改(不具体实现)
    """
    return "[Please contact the administrator!]"

@admin.route(cg.user_login_url,methods=["POST"])
def user_login():
    """
    [POST]
    用户登陆
    """
    if request.method=='POST':
        #try:
        parm=json.loads(request.get_data())
        user_account=parm['user_account']
        user_password=parm['user_password']
        #except:
            #return "error"
        org_id,user_id=user_login_model(user_account,user_password)
        if user_id==-1:
            return "error"
        temp={}
        temp["org_id"]=org_id
        temp["user_id"]=user_id

        return json.dumps(temp)
    else:
        return "error"