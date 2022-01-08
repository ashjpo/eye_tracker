#-*- coding:utf-8 -*-
"""
participant_model


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

def create_or_update_participant(participant_id,participant_name,org_id,sid):
    db,cursor=connect_mysql()

    sql_1="select id,session_ids_json from participant where participant_id='"+participant_id+"' and org_id="+str(org_id)
    pid=-1
    session_ids_json=[]
    cursor.execute(sql_1)
    results = cursor.fetchall()
    if len(results)>0:
        for row in results:
            pid=row[0]
            session_ids_json=json.loads(row[1])
        session_ids_json.append(sid)
        sql_2="update participant set session_ids_json='"+json.dumps(session_ids_json)+"' where id="+str(pid)
    else:
        session_ids_json.append(sid)
        sql_2="insert into participant(participant_id,participant_name,session_ids_json,org_id,create_time) values('"+participant_id+"','"+participant_name+"','"+json.dumps(session_ids_json)+"',"+str(org_id)+",now())"
    cursor.execute(sql_2)
    db.commit()
    
def participant_list_model(org_id):
    db,cursor=connect_mysql()

    sql_1="select id,participant_id,participant_name,UNIX_TIMESTAMP(create_time),session_ids_json from participant where org_id="+str(org_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    return_list=[]
    for row in results:
        temp={}
        temp["id"]=row[0]
        temp["participant_id"]=row[1]
        temp["participant_name"]=row[2]
        temp["create_time"]=row[3]
        temp["session_count"]=len(json.loads(row[4]))
        return_list.append(temp)
    return return_list

def participant_detail_model(p_id):
    db,cursor=connect_mysql()
    sql_1="select id,participant_id,participant_name,UNIX_TIMESTAMP(create_time),session_ids_json from participant where id="+str(p_id)+" limit 0,1"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    if len(results)<=0:
        return None
    else:
        temp={}
        for row in results:
            temp["id"]=row[0]
            temp["participant_id"]=row[1]
            temp["participant_name"]=row[2]
            temp["create_time"]=row[3]
            temp["session_ids_json"]=json.loads(row[4])
            temp["session"]=[]
        for i in range(len(temp["session_ids_json"])):
            temp["session_ids_json"][i]=str(temp["session_ids_json"][i])
        tstr="("+",".join(temp["session_ids_json"])+")"
        sql_2="select id,session_id,scene_version_id,session_name,UNIX_TIMESTAMP(create_time),session_duration from session where id in "+tstr+"  order by session_start_time desc"
        cursor.execute(sql_2)
        results2 = cursor.fetchall()
        for row in results2:
            ttt={}
            ttt["id"]=row[0]
            ttt["session_id"]=row[1]
            ttt["scene_version_id"]=row[2]
            ttt["session_name"]=row[3]
            ttt["create_time"]=row[4]
            ttt["duration"]=row[5]
            temp["session"].append(ttt)
    return temp

    


