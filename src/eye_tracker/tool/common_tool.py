#-*- coding:utf-8 -*-
"""
common tool


"""
import time
import hashlib
def verify_account_str(account):
    """
    验证account字符串的格式
    """
    if account=="":
        return False

    else:
        #[TODO]
        return True

def verify_password_str(account):
    """
    验证password字符串的格式
    """
    if account=="":
        return False

    else:
        #[TODO]
        return True

def generate_project_key(org_id,name):
    """
    生成project_key
    """
    project_key_str=str(org_id)+name+str(time.time())
    md5 = hashlib.md5()
    md5.update(project_key_str.encode('utf-8'))
    project_key=md5.hexdigest()
    return project_key

def generate_prefix(org_id,name):
    """
    生成prefix
    """
    prefix=str(org_id)+"_"+name
    return prefix

def generate_sdk_id_str(project_name,scene_name):
    """
    生成scene的sdk_id_str
    """
    sdk_id_str=project_name+scene_name+str(time.time())
    md5 = hashlib.md5()
    md5.update(sdk_id_str.encode('utf-8'))
    sdk_id_str=md5.hexdigest()
    return sdk_id_str

def random_session_name():
    """
    随机生成session_name
    """
    return random_session_name+"_"+str(int(time.time()))
