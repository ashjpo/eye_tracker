#-*- coding:utf-8 -*-
"""
dynamic_obj_device_controller

FUNCTION:
    (1) upload_dynamic_object_manifest
        上传dynamic object manifest
        【同】/v0/objects/4f39879a-d0f9-4924-bb12-6e0e14ad6b95?version=1

    (2) get_dynamic_object_manifest
        获取dynamic object manifest
        【同】...

    (3) upload_dynamic_object
        上传dynamic object
        【同】/v0/objects/2836bfbc-9a81-46e6-bf66-6598c49b4ea3/cube?version=1

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.dynamic_obj_device_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.dynamic_obj_device_model import *

dynamic_obj_device=Blueprint('dynamic_obj_device',__name__)

@dynamic_obj_device.route(cg.get_dynamic_object_manifest_url,methods=["GET"])
def get_dynamic_object_manifest(sdk_id_str):
    """
    [GET]
    获取dynamic object manifest
    """
    if request.method=='GET':
        pass

    else:
        return "error"

@dynamic_obj_device.route(cg.upload_dynamic_object_url,methods=["POST"])
def upload_dynamic_object(sdk_id_str,mesh_name):
    """
    [POST]
    上传dynamic object
    """
    if request.method=='POST':
        try:
            scene_version_number=request.args.get("version")
        except:
            return "error"

        file_name_list=[]
        file_list=[]
        screenshot_file_name=""
        #3d文件
        for file in request.files.getlist('file'): # 这里改动以存储多份文件
            if file and allowed_file(file.filename):
                file_name_list.append(file.filename)
                file_list.append(file)
                if file.filename=="cvr_object_thumbnail.png":
                    screenshot_file_name="cvr_object_thumbnail.png"
        #查找scene_version_id，sv_resource_folder_path
        scene_version_id,sv_resource_folder_path=scene_version_search_by_sdk_id_str_model(sdk_id_str,scene_version_number)
        save_dobj_path=wsg.app_root_path+sv_resource_folder_path+"/dynamic_obj/"+mesh_name
        #判断是否数据库中已经存在dobj
        if search_dobj_by_mesh_name_model(scene_version_id,mesh_name):
            print("upload_dynamic_object",True)
            #创建dobj的资源文件夹
            create_scene_version_dobj_resource_folder(sv_resource_folder_path,mesh_name)
            #获取上传的文件
            for i in range(len(file_name_list)):
                fname=file_name_list[i]
                file=file_list[i]
                file.save(save_dobj_path+"/"+fname)
            #插入数据库
            upload_dobj_model(file_name_list,mesh_name,scene_version_id,screenshot_file_name)
            return "ok"
        else:
            print("upload_dynamic_object",False)
            #创建dobj的资源文件夹
            create_scene_version_dobj_resource_folder(sv_resource_folder_path,mesh_name)
            #获取上传的文件
            for i in range(len(file_name_list)):
                fname=file_name_list[i]
                file=file_list[i]
                file.save(save_dobj_path+"/"+fname)
            #上传dynamic_obj之前没有在数据库中创建
            upload_dobj_without_insert_model(mesh_name,sdk_id_str,scene_version_id,sv_resource_folder_path,screenshot_file_name,file_name_list)
            return "ok"
    else:
        return "error"

        
        

@dynamic_obj_device.route(cg.upload_dynamic_object_manifest_url,methods=["POST"])
def upload_dynamic_object_manifest(sdk_id_str):
    """
    [POST]
    上传dynamic object manifest
    """
    if request.method=='POST':
        try:
            parm=json.loads(request.get_data())
        except:
            return "error"
        try:
            scene_version_number=request.args.get("version")
        except:
            return "error"
        
        #查找scene_version_id，sv_resource_folder_path
        scene_version_id,sv_resource_folder_path=scene_version_search_by_sdk_id_str_model(sdk_id_str,scene_version_number)
        #创建dobj的资源文件夹
        for obj in parm["objects"]:
            mesh_name=obj["mesh"]
            create_scene_version_dobj_resource_folder(sv_resource_folder_path,mesh_name)

        dynamic_obj_manifest_upload_model(parm["objects"],sdk_id_str,scene_version_id,sv_resource_folder_path)
        return "ok"
    else:
        return "error"

def create_scene_version_dobj_resource_folder(sv_folder,dobj_mesh_name):
    """
    创建scene_version_dobj的资源文件夹
    """
    scene_resource_folder_path=wsg.app_root_path+sv_folder+"/dynamic_obj/"+dobj_mesh_name
    print(scene_resource_folder_path)
    print("CREATE scene_version_dobj RESOURCE FOLDER",scene_resource_folder_path)
    if os.path.exists(scene_resource_folder_path)==False:
        os.makedirs(scene_resource_folder_path)
    return scene_resource_folder_path

ALLOWED_EXTENSIONS=['log','png','jpg','gif','gltf','bin','json']
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS