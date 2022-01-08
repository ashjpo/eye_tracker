#-*- coding:utf-8 -*-
"""
scession_device_model


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

def session_search_by_session_id(session_id):
    """
    通过session_id查找sid
    """
    db,cursor=connect_mysql()
    sql_1="select id from session where session_id='"+session_id+"'"
    sid=-1
    cursor.execute(sql_1)
    results = cursor.fetchall()
    for row in results:
        sid=row[0]
    return sid




def session_insert_update_gaze_model(session_id,session_name,hmdtype,interval,formatversion,userid,properties_json,session_start_time,scene_version_id):
    """
    查看session是否存在如果存在更新，如果不存在就创建
    """
    db,cursor=connect_mysql()
    sql_1="select id from session where session_id='"+session_id+"'"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    if len(results)>0:
        s_id=-1
        for row in results:
            s_id=row[0]
        sql_2="update session set session_name='"+session_name+"',hmdtype='"+hmdtype+"',detect_interval="+str(interval)+",formatversion='"+formatversion+"',userid='"+userid+"',properties_json='"+properties_json+"',session_start_time='"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(session_start_time))+"',scene_version_id="+str(scene_version_id)+" where id="+str(s_id)
        cursor.execute(sql_2)
        db.commit()
        return s_id
    else:
        data_ids_json={}
        data_ids_json["gaze"]=[]
        data_ids_json["fixation"]=[]
        data_ids_json["dynamicobj"]=[]
        data_ids_json["event"]=[]
        data_ids_json["sensors"]=[]

        sql_2="insert into session(session_id,session_name,hmdtype,detect_interval,formatversion,userid,properties_json,session_start_time,data_ids_json,scene_version_id,create_time) values('"+session_id+"','"+session_name+"','"+hmdtype+"',"+str(interval)+",'"+formatversion+"','"+userid+"','"+properties_json+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(session_start_time))+"','"+json.dumps(data_ids_json)+"',"+str(scene_version_id)+",now())"
        #print(sql_2)
        cursor.execute(sql_2)
        s_id = cursor.lastrowid
        db.commit()
        return s_id

def session_update_data_ids_json_else_insert_model(session_id,data_id,data_type):
    """
    用于fixation dobj sensor event上传data_id如果不存在暂时创建一个session对象
    """
    db,cursor=connect_mysql()
    sql_1="select id,data_ids_json from session where session_id='"+session_id+"'"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    if len(results)==0:
        data_ids_json={}
        data_ids_json["gaze"]=[]
        data_ids_json["fixation"]=[]
        data_ids_json["dynamicobj"]=[]
        data_ids_json["event"]=[]
        data_ids_json["sensors"]=[]

        data_ids_json[data_type].append(data_id)
        sql_2="insert into session(session_id,data_ids_json,create_time) values('"+session_id+"','"+json.dumps(data_ids_json)+"',now())"
        cursor.execute(sql_2)
        s_id = cursor.lastrowid
        db.commit()
        return True
    else:
        for row in results:
            data_ids_json=row[1]
        if data_ids_json is None:
            return False
        data_ids_json=json.loads(data_ids_json)
        data_ids_json[data_type].append(data_id)
        sql_2="update session set data_ids_json='"+json.dumps(data_ids_json)+"' where session_id='"+session_id+"'"
        cursor.execute(sql_2)
        db.commit()
        return True
        
def set_mysql_session_event(session_id,event_data_json):
    """
    设置session的event_type_json,session_end_time,session_duration
    """
    db,cursor=connect_mysql()
    sql_1="select event_type_json,UNIX_TIMESTAMP(session_start_time) from session where session_id='"+session_id+"'"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    event_type_json=""
    session_start_time=0
    session_duration=None
    for row in results:
        event_type_json=row[0]
        session_start_time=row[1]
    if event_type_json=="" or event_type_json is None:
        event_type_json=[]
    else:
        event_type_json=json.loads(event_type_json)
    for d in event_data_json["data"]:
        if d["name"] not in event_type_json:
            event_type_json.append(d["name"])
        try:
            if d["name"]=="Session End":
                try:
                    session_duration=int(d["properties"]["sessionlength"])
                except:
                    session_duration=None
                if session_duration is None:
                    session_duration=int(time.time())-int(event_data_json["timestamp"])
                session_end_time=session_start_time+session_duration
        except:
            session_duration=int(time.time())-int(event_data_json["timestamp"])
            session_end_time=int(time.time())
    #if (session_duration is None) or (session_end_time is None):
    sql_2="update session set event_type_json='"+json.dumps(event_type_json)+"' where session_id='"+session_id+"'"
    '''else:
        sql_2="update session set event_type_json='"+json.dumps(event_type_json)+"',session_duration="+str(session_duration)+",session_end_time='"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(session_end_time))+"' where session_id='"+session_id+"'"'''
    cursor.execute(sql_2)
    db.commit()





def session_data_json_save_model(json_obj,data_type):
    """
    保存session数据到mongodb
    """
    db=connect_mongodb()
    table=db[data_type]
    x = table.insert_one(json_obj)
    
    return str(x.inserted_id)

def session_update_data_ids_json_model(sid,data_type,data_id):
    """
    #更新数据库中的data_ids_json
    """
    db,cursor=connect_mysql()
    sql_1="select data_ids_json,UNIX_TIMESTAMP(session_start_time) from session where id="+str(sid)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    data_ids_json=None
    session_start_time=None
    for row in results:
        data_ids_json=row[0]
        session_start_time=row[1]
    if data_ids_json is None:
        return False
    data_ids_json=json.loads(data_ids_json)
    data_ids_json[data_type].append(data_id)

    session_duration=int(time.time())-int(session_start_time)
    session_end_time=int(time.time())
    sql_2="update session set data_ids_json='"+json.dumps(data_ids_json)+"',session_duration="+str(session_duration)+",session_end_time='"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(session_end_time))+"' where id="+str(sid)
    #print(sql_2)
    cursor.execute(sql_2)
    db.commit()
    return True


