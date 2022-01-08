#-*- coding:utf-8 -*-
"""
objective_model


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
from bson import ObjectId 
from bson import json_util

def objective_create_model(sceneVersionId,name,description):
    """
    创建objective
    """
    db,cursor=connect_mysql()
    #判断是否重名
    sql_2="select id from objective where name='"+name+"'"
    cursor.execute(sql_2)
    results = cursor.fetchall()
    if len(results)>0:
        return -1
    #try:
    sql_1="insert into objective(name,des,create_time,last_update_time,scene_version_id) values('"+name+"','"+description+"',now(),now(),"+str(sceneVersionId)+")"
    cursor.execute(sql_1)
    last_insert_id = cursor.lastrowid
    db.commit()
    return last_insert_id
    #except:
        #return -1

def objective_version_create_model(objective_id,is_active,step_json):
    """
    创建objective-version
    """
    db,cursor=connect_mysql()
    try:
        sql_2="select id from objective_version where objective_id="+str(objective_id)
        cursor.execute(sql_2)
        results = cursor.fetchall()
        now_version=len(results)+1

        sql_1="insert into objective_version(objective_id,is_active,step_json,create_time,last_update_time,version_number) values("+str(objective_id)+","+str(is_active)+",'"+json.dumps(step_json)+"',now(),now(),"+str(now_version)+")"
        cursor.execute(sql_1)
        last_insert_id = cursor.lastrowid
        db.commit()
        return last_insert_id
    except:
        return -1

def objective_basic_mes_model(objective_id):
    """
    获取objective的基本信息
    """
    db,cursor=connect_mysql()
    #objective
    sql_1="select UNIX_TIMESTAMP(objective.create_time),UNIX_TIMESTAMP(objective.last_update_time),objective.id,objective.name,objective.des,scene.name,scene_version.version_number,scene.sdk_id_str,scene_version.id as scene_version_id from objective,scene_version,scene where objective.scene_version_id=scene_version.id and scene_version.scene_id=scene.id and objective.id="+str(objective_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    return_dict={}
    for row in results:
        return_dict["createdAt"]=row[0]
        return_dict["updatedAt"]=row[1]
        return_dict["id"]=row[2]
        return_dict["name"]=row[3]
        return_dict["description"]=row[4]
        return_dict["scene_name"]=row[5]
        return_dict["scene_version_number"]=row[6]
        return_dict["scene_id_str"]=row[7]
        return_dict["scene_version_id"]=row[8]
        return_dict["scene_and_version"]=row[5]+" v"+str(row[6])
    return_dict["objectiveVersions"]=[]
    
    #objective-version
    sql_2="select UNIX_TIMESTAMP(create_time),UNIX_TIMESTAMP(last_update_time),id,is_active,step_json,objective_version.version_number from objective_version where objective_id="+str(objective_id)
    cursor.execute(sql_2)
    results = cursor.fetchall()
    for row in results:
        temp={}
        temp["createdAt"]=row[0]
        temp["updatedAt"]=row[1]
        temp["id"]=row[2]
        temp["isActive"]=row[3]
        temp["startedAt"]=None
        temp["endedAt"]=None
        step_json=json.loads(row[4])
        temp["version_number"]=row[5]
        temp["objectiveComponents"]=[]
        for step in step_json:
            tstep={}
            tstep["occurrenceOperator"]=step["occurrenceOperator"]
            
            tstep["sequenceNumber"]=step["sequenceNumber"]
            
            tstep["name"]=""
            tstep["type"]=step["type"]
            tstep["occurrenceValue"]=step["occurrenceValue"]
            tstep["isStep"]=True
            try:
                tstep["dynamicObjectIds"]=step["dynamicObjectIds"]
            except:
                tstep["dynamicObjectIds"]=[]
            if tstep["type"]=="eventstep":
                tstep["eventName"]=step["eventName"]
                try:
                    tstep["eventPropertyOperator"]=step["eventPropertyOperator"]
                    tstep["eventPropertyValue"]=step["eventPropertyValue"]
                    tstep["eventPropertyName"]=step["eventPropertyName"]
                except:
                    tstep["eventPropertyOperator"]=None
                    tstep["eventPropertyValue"]=None
                    tstep["eventPropertyName"]=None
            elif tstep["type"]=="gazestep" or tstep["type"]=="fixationstep":
                tstep["durationOperator"]=step["durationOperator"]
                tstep["durationValue"]=step["durationValue"]

            temp["objectiveComponents"].append(tstep)
        return_dict["objectiveVersions"].append(temp)
    return return_dict

def get_objective_id_model(project_id):
    """
    获取project下的objective_id
    """
    db,cursor=connect_mysql()
    sql_1="select objective.id from scene_version,scene,objective where scene.pro_id="+str(project_id)+" and scene.id=scene_version.scene_id and objective.scene_version_id=scene_version.id"
    objective_id_list=[]
    cursor.execute(sql_1)
    results = cursor.fetchall()
    for row in results:
        objective_id_list.append(row[0])
    return objective_id_list

def objective_version_stepresult_model(scene_version_id,objective_version_id):
    """
    查看各步完成的程度
    """
    db,cursor=connect_mysql()
    sql_2="select data_ids_json from session where scene_version_id="+str(scene_version_id)
    cursor.execute(sql_2)
    results = cursor.fetchall()
    data_ids_json_list=[]
    for row in results:
        data_ids_json_list.append(json.loads(row[0]))


    sql_1="select step_json from objective_version where id="+str(objective_version_id)+" limit 0,1"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    step_json=None
    for row in results:
        step_json=json.loads(row[0])
    if step_json is None:
        return None

    return_json=[]
    all_session_num=len(data_ids_json_list)
    for step in step_json:
        succeeded=0
        step_type=step["type"]
        if step_type=="eventstep":
            datatype="event"
        elif step_type=="gazestep":
            datatype="gaze"
        elif step_type=="fixationstep":
            datatype="fixation"
        temp_list=[]
        for data_ids_json in data_ids_json_list:
            if_success,_=if_finish_step(data_ids_json,datatype,step)
            if if_success==True:
                succeeded+=1
                temp_list.append(data_ids_json)
        data_ids_json_list=temp_list
        temp={}
        temp["step"]=step["sequenceNumber"]
        temp["succeeded"]=succeeded
        temp["failed"]=(all_session_num-succeeded)
        return_json.append(temp)
    return return_json

def objective_version_stepresult_single_model(session_id,objective_version_id):
    """
    查看各步完成的程度(单个session)
    """
    db,cursor=connect_mysql()
    sql_2="select data_ids_json from session where id="+str(session_id)+" limit 0,1"
    cursor.execute(sql_2)
    results = cursor.fetchall()
    data_ids_json=[]
    for row in results:
        data_ids_json=json.loads(row[0])

    sql_1="select step_json from objective_version where id="+str(objective_version_id)+" limit 0,1"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    step_json=None
    objectiveResults=[]
    for row in results:
        step_json=json.loads(row[0])
    if step_json is None:
        return None
    step_index=0
    has_fail=False
    for step in step_json:
        step_type=step["type"]
        if step_type=="eventstep":
            datatype="event"
        elif step_type=="gazestep":
            datatype="gaze"
        elif step_type=="fixationstep":
            datatype="fixation"
        step_index+=1
        if_success,timestamp=if_finish_step(data_ids_json,datatype,step)
        temp={}
        temp["step"]=step_index
        temp["timestamp"]=timestamp
        if if_success==True:
            if has_fail:
                temp["result"]="failed"
            else:
                temp["result"]="succeeded"
        else:
            temp["result"]="failed"
            has_fail=True
        objectiveResults.append(temp)
    return objectiveResults


        
def if_finish_step(data_ids_json,datatype,step_json):
    mdb=connect_mongodb()
    e_table=mdb[datatype]
    point_list=[]
    x=None
    timestamp=None
    for mid in data_ids_json[datatype]:
        x=e_table.find({ "_id": ObjectId(mid)})[0]
        timestamp=x["timestamp"]
        point_list+=x["data"]
    ok_times=0
    if datatype=="event":
        for point in point_list:
            if point["name"]==step_json["eventName"]:
                pass
            else:
                continue
            if "dynamicObjectIds" in step_json:
                if len(step_json["dynamicObjectIds"])>0:
                    dynamicObjectIds=step_json["dynamicObjectIds"][0]
                    if ("dynamicId" in point.keys()) and (point["dynamicId"]==dynamicObjectIds):
                        pass
                    else:
                        continue
                else:
                    pass
            else:
                pass
            
            if ("eventPropertyName" in step_json) and ("eventPropertyValue" in step_json):
                if ("properties" in point) and (step_json["eventPropertyName"] in point["properties"]):
                    if step_json["eventPropertyOperator"]=="eq":    #等于
                        if point["properties"][step_json["eventPropertyName"]]==step_json["eventPropertyValue"]:
                            pass
                        else:
                            continue
                    elif step_json["eventPropertyOperator"]=="lt":  #小于
                        if point["properties"][step_json["eventPropertyName"]]<step_json["eventPropertyValue"]:
                            pass
                        else:
                            continue
                    elif step_json["eventPropertyOperator"]=="lte":  #小于等于
                        if point["properties"][step_json["eventPropertyName"]]<=step_json["eventPropertyValue"]:
                            pass
                        else:
                            continue
                    elif step_json["eventPropertyOperator"]=="gt":  #大于
                        if point["properties"][step_json["eventPropertyName"]]>step_json["eventPropertyValue"]:
                            pass
                        else:
                            continue
                    elif step_json["eventPropertyOperator"]=="gte":  #大于等于
                        if point["properties"][step_json["eventPropertyName"]]>=step_json["eventPropertyValue"]:
                            pass
                        else:
                            continue
            else:
                pass
                
            ok_times+=1
        if step_json["occurrenceOperator"]=="eq":    #等于
            if ok_times==step_json["occurrenceValue"]:
                return True,timestamp
            else:
                return False,timestamp
        elif step_json["occurrenceOperator"]=="lt":  #小于
            if ok_times<step_json["occurrenceValue"]:
                return True,timestamp
            else:
                return False,timestamp
        elif step_json["occurrenceOperator"]=="lte":  #小于等于
            if ok_times<=step_json["occurrenceValue"]:
                return True,timestamp
            else:
                return False,timestamp
        elif step_json["occurrenceOperator"]=="gt":  #大于
            if ok_times>step_json["occurrenceValue"]:
                return True,timestamp
            else:
                return False,timestamp
        elif step_json["occurrenceOperator"]=="gte":  #大于等于
            if ok_times>=step_json["occurrenceValue"]:
                return True,timestamp
            else:
                return False,timestamp
    elif datatype=="gaze":
        all_time=0
        for point in point_list:
            if "dynamicObjectIds" in step_json:
                if len(step_json["dynamicObjectIds"])>0:
                    dynamicObjectIds=step_json["dynamicObjectIds"][0]
                    if ("o" in point) and (point["o"]==dynamicObjectIds):
                        pass
                    else:
                        continue
                else:
                    continue
            else:
                continue
            all_time+=x["interval"]
            
        if step_json["occurrenceOperator"]=="lte":
            if all_time<=step_json["occurrenceValue"]:
                return True,timestamp
            else:
                return False,timestamp
        elif step_json["occurrenceOperator"]=="gte":
            if all_time>=step_json["occurrenceValue"]:
                return True,timestamp
            else:
                return False,timestamp
    elif datatype=="fixation":
        all_time=0
        for point in point_list:
            if "dynamicObjectIds" in step_json:
                if len(step_json["dynamicObjectIds"])>0:
                    dynamicObjectIds=step_json["dynamicObjectIds"][0]
                    if ("objectid" in point) and (point["objectid"]==dynamicObjectIds):
                        pass
                    else:
                        continue
                else:
                    continue
            else:
                continue
            all_time+=point["duration"]/1000
        
        if step_json["occurrenceOperator"]=="lte":
            if all_time<=step_json["occurrenceValue"]:
                return True,timestamp
            else:
                return False,timestamp
        elif step_json["occurrenceOperator"]=="gte":
            if all_time>=step_json["occurrenceValue"]:
                return True,timestamp
            else:
                return False,timestamp
    else:
        return False,timestamp
    

def objective_session_result_model(session_id):
    """
    通过session_id获取与该scene_version有关的objective结果
    """
    db,cursor=connect_mysql()
    sql_1="select id,scene_version_id from session where session_id='"+session_id+"'"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    scene_version_id=-1
    sid=-1
    for row in results:
        sid=row[0]
        scene_version_id=row[1]
    if scene_version_id==-1:
        return None
    sql_2="select objective_version.id,objective_version.version_number,objective.name from objective,objective_version where objective_version.objective_id=objective.id and objective.scene_version_id="+str(scene_version_id)
    cursor.execute(sql_2)
    results = cursor.fetchall()
    return_json={}
    for row in results:
        objective_version_id=row[0]
        objective_version_number=row[1]
        objective_name=row[2]
        r=objective_version_stepresult_single_model(sid,objective_version_id)
        return_json[objective_version_id]={}
        return_json[objective_version_id]["data"]=r
        return_json[objective_version_id]["objective_version_number"]=objective_version_number
        return_json[objective_version_id]["objective_name"]=objective_name
    return return_json





    






            
            
            




