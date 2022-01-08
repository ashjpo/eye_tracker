#-*- coding:utf-8 -*-
"""
session_model


"""
import time
import os,sys
import json
import random
import math

#tool
from tool.model_tool import *
from tool.common_tool import *
#mysql
import pymysql
#mongodb
import pymongo
from bson import ObjectId 
from bson import json_util
from .objective_model import *

def session_list_model(scene_version_id,page=0,limit=20):
    """
    获取session_list
    """
    db,cursor=connect_mysql()
    sql_2="select count(id) from session where scene_version_id="+str(scene_version_id)
    cursor.execute(sql_2)
    results2 = cursor.fetchall()
    
    sql_1="select UNIX_TIMESTAMP(create_time),id,userid,hmdtype,UNIX_TIMESTAMP(session_start_time),UNIX_TIMESTAMP(session_end_time),session_duration,session_id,session_name,detect_interval,data_ids_json from session where scene_version_id="+str(scene_version_id)+" order by session_start_time desc limit "+str(page)+","+str(limit)
    #print(sql_1)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    return_json={}
    return_json["count"]=len(results)
    return_json["pages"]=(len(results2)//limit)+1
    return_json["currentPage"]=page
    return_json["results"]=[]
    for row in results:
        temp={}
        temp["createdAt"]=row[0]
        temp["updatedAt"]=row[0]
        temp["id"]=row[1]
        temp["user"]=row[2]
        temp["hmd"]=row[3]
        temp["startTime"]=row[4]
        temp["endTime"]=row[5]
        temp["sessionLength"]=row[6]
        temp["sdkSessionId"]=row[7]
        temp["friendlyName"]=row[8]
        temp["gazeInterval"]=row[9]
        data_ids_json=json.loads(row[10])
        if len(data_ids_json["gaze"])>0:
            temp["hasGaze"]=True
        else:
            temp["hasGaze"]=None
        if len(data_ids_json["fixation"])>0:
            temp["hasFixation"]=True
        else:
            temp["hasFixation"]=None
        if len(data_ids_json["dynamicobj"])>0:
            temp["hasDynamic"]=True
        else:
            temp["hasDynamic"]=None
        if len(data_ids_json["event"])>0:
            temp["hasEvent"]=True
        else:
            temp["hasEvent"]=None
        if len(data_ids_json["sensors"])>0:
            temp["hasSensor"]=True
        else:
            temp["hasSensor"]=None
        return_json["results"].append(temp)
    return return_json

def session_metadata_model(sid):
    """
    session_metadata_model
    """
    db,cursor=connect_mysql()
    sql_1="select UNIX_TIMESTAMP(create_time),id,userid,hmdtype,UNIX_TIMESTAMP(session_start_time),UNIX_TIMESTAMP(session_end_time),session_duration,session_id,session_name,detect_interval,data_ids_json from session where id="+str(sid)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    temp={}
    for row in results:
        temp["createdAt"]=row[0]
        temp["updatedAt"]=row[0]
        temp["id"]=row[1]
        temp["user"]=row[2]
        temp["hmd"]=row[3]
        temp["startTime"]=row[4]
        temp["endTime"]=row[5]
        temp["sessionLength"]=row[6]
        temp["sdkSessionId"]=row[7]
        temp["friendlyName"]=row[8]
        temp["gazeInterval"]=row[9]
        data_ids_json=json.loads(row[10])
        if len(data_ids_json["gaze"])>0:
            temp["hasGaze"]=True
        else:
            temp["hasGaze"]=None
        if len(data_ids_json["fixation"])>0:
            temp["hasFixation"]=True
        else:
            temp["hasFixation"]=None
        if len(data_ids_json["dynamicobj"])>0:
            temp["hasDynamic"]=True
        else:
            temp["hasDynamic"]=None
        if len(data_ids_json["event"])>0:
            temp["hasEvent"]=True
        else:
            temp["hasEvent"]=None
        if len(data_ids_json["sensors"])>0:
            temp["hasSensor"]=True
        else:
            temp["hasSensor"]=None
    return temp


def session_single_queries_model(parm):
    resturn_json={}

    resturn_json["projectId"]=parm["projectId"]
    resturn_json["sceneId"]=parm["sceneId"]
    resturn_json["versionId"]=parm["versionId"]
    resturn_json["sessionId"]=parm["sessionId"]
    db,cursor=connect_mysql()
    
    sql_1="select org_id from project where id="+str(resturn_json["projectId"])+" limit 0,1"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    for row in results:
        resturn_json["organizationId"]=row[0]
    #[TODO]
    resturn_json["participantId"]=""

    sql_2="select UNIX_TIMESTAMP(session_start_time),UNIX_TIMESTAMP(session_end_time),session_duration,detect_interval,hmdtype,userid,data_ids_json,properties_json from session where session_id='"+resturn_json["sessionId"]+"' limit 0,1"
    cursor.execute(sql_2)
    results = cursor.fetchall()
    data_ids_json=None
    for row in results:
        resturn_json["date"]=row[0]
        resturn_json["endDate"]=row[1]
        resturn_json["duration"]=row[2]
        resturn_json["gazeInterval"]=row[3]
        resturn_json["hmd"]=row[4]
        resturn_json["user"]=row[5]
        data_ids_json=json.loads(row[6])

        resturn_json["warnings"]={}
        resturn_json["warnings"]["positionLimited"]=False
        resturn_json["warnings"]["gazeLimited"]=False
        resturn_json["warnings"]["fixationsLimited"]=False
        resturn_json["warnings"]["eventsLimited"]=False

        resturn_json["objectiveResults"]={}
        resturn_json["properties"]=json.loads(row[7])

    if data_ids_json is None:
        return None
    resturn_json["events"]=[]
    #查找mongodb
    mdb=connect_mongodb()
    event_table=mdb["event"]
    for event_m_id in data_ids_json["event"]:
        for x in event_table.find({ "_id": ObjectId(event_m_id)}):

            for e in x["data"]:
                et={}
                et["name"]=e["name"]
                et["date"]=e["time"]
                event_point=e["point"]
                et["x"]=event_point[0]
                et["y"]=event_point[1]
                et["z"]=event_point[2]
                try:
                    et["properties"]=e["properties"]
                except:
                    et["properties"]={}
                try:
                    et["object"]=e["dynamicId"]
                except:
                    pass
                resturn_json["events"].append(et)
    return resturn_json

def session_queries_model(parm):
    db,cursor=connect_mysql()
    sql_2="select count(id) from session where scene_version_id="+str(parm["entityFilters"]["versionId"])
    cursor.execute(sql_2)
    results2 = cursor.fetchall()
    
    sql_1="select UNIX_TIMESTAMP(create_time),id,userid,hmdtype,UNIX_TIMESTAMP(session_start_time),UNIX_TIMESTAMP(session_end_time),session_duration,session_id,session_name,detect_interval,data_ids_json from session where scene_version_id="+str(parm["entityFilters"]["versionId"])+" order by session_start_time desc limit "+str(parm["page"])+","+str(parm["limit"])
    #print(sql_1)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    return_json={}
    return_json["count"]=len(results)
    return_json["pages"]=(len(results2)//parm["limit"])+1
    return_json["currentPage"]=parm["page"]
    return_json["results"]=[]
    for row in results:
        temp={}
        temp["createdAt"]=row[0]
        temp["updatedAt"]=row[0]
        temp["id"]=row[1]
        temp["user"]=row[2]
        temp["hmd"]=row[3]
        temp["startTime"]=row[4]
        temp["endTime"]=row[5]
        temp["sessionLength"]=row[6]
        temp["sdkSessionId"]=row[7]
        temp["friendlyName"]=row[8]
        temp["gazeInterval"]=row[9]
        data_ids_json=json.loads(row[10])
        if len(data_ids_json["gaze"])>0:
            temp["hasGaze"]=True
        else:
            temp["hasGaze"]=None
        if len(data_ids_json["fixation"])>0:
            temp["hasFixation"]=True
        else:
            temp["hasFixation"]=None
        if len(data_ids_json["dynamicobj"])>0:
            temp["hasDynamic"]=True
        else:
            temp["hasDynamic"]=None
        if len(data_ids_json["event"])>0:
            temp["hasEvent"]=True
        else:
            temp["hasEvent"]=None
        if len(data_ids_json["sensors"])>0:
            temp["hasSensor"]=True
        else:
            temp["hasSensor"]=None
        temp["positionLimited"]=False
        temp["gazeLimited"]=False
        temp["fixationsLimited"]=False
        temp["eventsLimited"]=False
        
        if "includeObjectiveVersionData" in parm.keys():
            objective_version_id=parm["includeObjectiveVersionData"]
            #[TODO]
            temp["objectiveResults"]=objective_version_stepresult_single_model(temp["id"],objective_version_id)
        return_json["results"].append(temp)
    return return_json

        
def session_data_model(scene_version_id,session_id,data_type):
    db,cursor=connect_mysql()
    sql_1="select userid,UNIX_TIMESTAMP(session_start_time),session_id,hmdtype,detect_interval,formatversion,properties_json,geo_json,data_ids_json from session where session_id='"+session_id+"' and scene_version_id="+str(scene_version_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    return_json={}
    for row in results:
        return_json["userid"]=row[0]
        return_json["timestamp"]=row[1]
        return_json["sessionid"]=row[2]
        return_json["hmdtype"]=row[3]
        return_json["interval"]=row[4]
        return_json["formatversion"]=row[5]
        if data_type=="gaze":
            return_json["properties"]=json.loads(row[6])
        #[TODO]
        return_json["geo"]=None
        return_json["sessiontype"]=data_type

        data_ids_json=json.loads(row[8])
        return_json["part"]=len(data_ids_json[data_type])
        return_json["data"]=[]
        #查找mongodb
        mdb=connect_mongodb()
        e_table=mdb[data_type]
        ttt={}
        for m_id in data_ids_json[data_type]:
            for x in e_table.find({ "_id": ObjectId(m_id)}):
                ttt[x["part"]]=x
        for i in sorted (ttt):
            if i==1 and data_type=="dynamicobj":
                return_json["manifest"]=ttt[i]["manifest"]
            return_json["data"]+=ttt[i]["data"]
    return return_json


def session_slicer_field_queries_event_model(pro_id):
    db,cursor=connect_mysql()
    sql_1="select session.event_type_json from session,scene_version,scene where session.scene_version_id=scene_version.id and scene_version.scene_id=scene.id and scene.pro_id="+str(pro_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    event_list=[]
    for row in results:
        try:
            temp=json.loads(row[0])
        except:
            continue
        for t in temp:
            if t not in event_list:
                event_list.append(t)
    return event_list

def session_slicer_metric_object_queries_model(parm):
    db,cursor=connect_mysql()
    scene_version_id=parm["entityFilters"]["versionId"]
    objectIds=parm["objectIds"]
    sql_1="select data_ids_json from session where scene_version_id="+str(scene_version_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    data_ids_list=[]
    for row in results:
        data_ids_json=json.loads(row[0])
        data_ids_list.append(data_ids_json[parm["gazeType"]])

    totalSessionsWithAnyData=0      #有所有dobj的data数量
    temp={}
    for objid in objectIds:
        temp[objid]={}
        temp[objid]["TimeToFirst"]=[]   #第一次data
        temp[objid]["dataSequence"]=[]  #data发生序列
        temp[objid]["dataLength"]=[]    #data时间长度
        temp[objid]["dataCount"]=[]     #data发生次数
        temp[objid]["distinctdataCount"]=[]

    #查找mongodb
    mdb=connect_mongodb()
    e_table=mdb[parm["gazeType"]]
    session_data_list=[]
    for mid_list in data_ids_list:
        #print(mid_list)
        for i in range(len(mid_list)):
            mid=mid_list[i]
            x=e_table.find({ "_id": ObjectId(mid)})[0]
            if i==0:
                session_data_list.append(x)
            else:
                session_data_list[-1]["data"]+=x["data"]


    for session_data in session_data_list:
        obj_list=[]
        if parm["gazeType"]=="fixation":
            last_point_obj_id=""
            for point_index in range(len(session_data["data"])):
                point=session_data["data"][point_index]
                if "objectid" in point.keys():
                    point_objid=point["objectid"]
                    #第一次data
                    if point_index==0:
                        TimeToFirst=point["time"]-session_data["timestamp"]
                        temp[point_objid]["TimeToFirst"].append(TimeToFirst)
                    #data时间长度 
                    #data发生次数
                    if point_objid not in obj_list:
                        temp[point_objid]["dataLength"].append(point["duration"]/1000)
                        temp[point_objid]["dataCount"].append(1)
                        temp[point_objid]["distinctdataCount"].append(1)
                    else:
                        if last_point_obj_id!=point_objid:
                            temp[point_objid]["distinctdataCount"][-1]+=1
                        temp[point_objid]["dataLength"][-1]+=point["duration"]/1000
                        temp[point_objid]["dataCount"][-1]+=1
                    #data发生序列
                    if point_objid not in obj_list:
                        obj_list.append(point_objid)
                        dataSequence=len(obj_list)
                        temp[point_objid]["dataSequence"].append(dataSequence)
                    last_point_obj_id=point_objid
                else:
                    last_point_obj_id=""
        else:
            last_point_obj_id=""
            last_point_time=0
            for point_index in range(len(session_data["data"])):
                point=session_data["data"][point_index]
                if "o" in point.keys():
                    point_objid=point["o"]
                    now_point_time=point["time"]
                    #第一次data
                    if point_index==0:
                        TimeToFirst=point["time"]-session_data["timestamp"]
                        temp[point_objid]["TimeToFirst"].append(TimeToFirst)
                    #data时间长度 
                    #data发生次数
                    if point_objid not in obj_list:
                        temp[point_objid]["dataLength"].append(x["interval"])
                        temp[point_objid]["dataCount"].append(1)
                        temp[point_objid]["distinctdataCount"].append(1)
                    else:
                        if last_point_obj_id==point_objid:
                            temp[point_objid]["dataLength"][-1]+=(now_point_time-last_point_time)
                        else:
                            temp[point_objid]["distinctdataCount"][-1]+=1
                            temp[point_objid]["dataLength"][-1]+=x["interval"]
                        temp[point_objid]["dataCount"][-1]+=1
                    #data发生序列
                    if point_objid not in obj_list:
                        obj_list.append(point_objid)
                        dataSequence=len(obj_list)
                        temp[point_objid]["dataSequence"].append(dataSequence)
                    last_point_obj_id=point_objid
                    last_point_time=now_point_time
                else:
                    last_point_obj_id=""
                    last_point_time=0
        #totalSessionsWithAnyData
        if len(obj_list)==len(objectIds):
            totalSessionsWithAnyData+=1
    #print(temp)
    metrics={}
    for final_objid in temp.keys():
        metrics[final_objid]={}
        if parm["gazeType"]=="fixation":
            try:
                metrics[final_objid]["averageFixationInstanceDuration"]=sum_list(temp[final_objid]["dataLength"])/sum_list(temp[final_objid]["dataCount"])
            except:
                metrics[final_objid]["averageFixationInstanceDuration"]=0
            metrics[final_objid]["averageFixationCount"]=avg_list(temp[final_objid]["dataCount"])
            metrics[final_objid]["averageFixationLength"]=sum_list(temp[final_objid]["dataLength"])/len(session_data_list)
            metrics[final_objid]["totalFixationCount"]=sum_list(temp[final_objid]["dataCount"])
            metrics[final_objid]["totalFixationLength"]=sum_list(temp[final_objid]["dataLength"])
            metrics[final_objid]["totalSessionsWithAnyFixation"]=totalSessionsWithAnyData
            metrics[final_objid]["proportionOfSessionsWithAnyFixation"]=totalSessionsWithAnyData/len(data_ids_list)    #?
            metrics[final_objid]["averageTimeToFirstFixation"]=avg_list(temp[final_objid]["TimeToFirst"],"-1")
            metrics[final_objid]["averageFixationSequence"]=avg_list(temp[final_objid]["dataSequence"],"-1")
        else:   #gaze
            try:
                metrics[final_objid]["averageGazeInstanceDuration"]=sum_list(temp[final_objid]["dataLength"])/sum_list(temp[final_objid]["dataCount"])
            except:
                metrics[final_objid]["averageGazeInstanceDuration"]=0
            metrics[final_objid]["averageGazeCount"]=sum_list(temp[final_objid]["distinctdataCount"])/len(session_data_list)
            metrics[final_objid]["averageGazeLength"]=sum_list(temp[final_objid]["dataLength"])/len(session_data_list)
            metrics[final_objid]["totalGazeCount"]=sum_list(temp[final_objid]["dataCount"])
            metrics[final_objid]["totalGazeLength"]=sum_list(temp[final_objid]["dataLength"])
            metrics[final_objid]["totalSessionsWithAnyGaze"]=totalSessionsWithAnyData
            metrics[final_objid]["proportionOfSessionsWithAnyGaze"]=totalSessionsWithAnyData/len(data_ids_list)    #?
            metrics[final_objid]["averageTimeToFirstGaze"]=avg_list(temp[final_objid]["TimeToFirst"],"-1")
            metrics[final_objid]["averageGazeSequence"]=avg_list(temp[final_objid]["dataSequence"],"-1")
    final_return_json={}
    final_return_json["sessionCount"]=len(data_ids_list)
    final_return_json["metrics"]=metrics
    return final_return_json

def session_slicer_metric_group_queries_model(parm):
    db,cursor=connect_mysql()
    scene_version_id=parm["entityFilters"]["versionId"]
    dobj_g_list=[]
    objectIds=[]
    if len(parm["groups"])==0:
        final_return_json={}
        final_return_json["sessionCount"]=0
        final_return_json["metrics"]={}
        return final_return_json
    for g in parm["groups"]:
        dobj_g_list.append(g["objectIds"])
        for gid in g["objectIds"]:
            objectIds.append(gid)
    parm["objectIds"]=objectIds
    dobj_data=session_slicer_metric_object_queries_model(parm)
    analyze_data=dobj_data["metrics"]
    metrics={}
    objid_index=0
    for g in parm["groups"]:
        metrics[g["name"]]={}
        dobj_id_list=g["objectIds"]
        if parm["gazeType"]=="fixation":
            metrics[g["name"]]["averageFixationInstanceDuration"]=[]
            metrics[g["name"]]["averageFixationCount"]=[]
            metrics[g["name"]]["averageFixationLength"]=[]
            metrics[g["name"]]["totalFixationCount"]=[]
            metrics[g["name"]]["totalFixationLength"]=[]
            metrics[g["name"]]["totalSessionsWithAnyFixation"]=[]
            metrics[g["name"]]["proportionOfSessionsWithAnyFixation"]=[]
            for dobj_id in dobj_id_list:
                metrics[g["name"]]["averageFixationInstanceDuration"].append(analyze_data[dobj_id]["averageFixationInstanceDuration"])
                metrics[g["name"]]["averageFixationCount"].append(analyze_data[dobj_id]["averageFixationCount"])
                metrics[g["name"]]["averageFixationLength"].append(analyze_data[dobj_id]["averageFixationLength"])
                metrics[g["name"]]["totalFixationCount"].append(analyze_data[dobj_id]["totalFixationCount"])
                metrics[g["name"]]["totalFixationLength"].append(analyze_data[dobj_id]["totalFixationLength"])
                metrics[g["name"]]["totalSessionsWithAnyFixation"].append(analyze_data[dobj_id]["totalSessionsWithAnyFixation"])
                metrics[g["name"]]["proportionOfSessionsWithAnyFixation"].append(analyze_data[dobj_id]["proportionOfSessionsWithAnyFixation"])
            metrics[g["name"]]["averageFixationInstanceDuration"]=avg_list(metrics[g["name"]]["averageFixationInstanceDuration"])
            metrics[g["name"]]["averageFixationCount"]=avg_list(metrics[g["name"]]["averageFixationCount"])
            metrics[g["name"]]["averageFixationLength"]=avg_list(metrics[g["name"]]["averageFixationLength"])
            metrics[g["name"]]["totalFixationCount"]=avg_list(metrics[g["name"]]["totalFixationCount"])
            metrics[g["name"]]["totalFixationLength"]=avg_list(metrics[g["name"]]["totalFixationLength"])
            metrics[g["name"]]["totalSessionsWithAnyFixation"]=avg_list(metrics[g["name"]]["totalSessionsWithAnyFixation"])
            metrics[g["name"]]["proportionOfSessionsWithAnyFixation"]=avg_list(metrics[g["name"]]["proportionOfSessionsWithAnyFixation"])
                
        else:   #gaze
            metrics[g["name"]]["averageGazeInstanceDuration"]=[]
            metrics[g["name"]]["averageGazeCount"]=[]
            metrics[g["name"]]["averageGazeLength"]=[]
            metrics[g["name"]]["totalGazeCount"]=[]
            metrics[g["name"]]["totalGazeLength"]=[]
            metrics[g["name"]]["totalSessionsWithAnyGaze"]=[]
            metrics[g["name"]]["proportionOfSessionsWithAnyGaze"]=[]
            for dobj_id in dobj_id_list:
                metrics[g["name"]]["averageGazeInstanceDuration"].append(analyze_data[dobj_id]["averageGazeInstanceDuration"])
                metrics[g["name"]]["averageGazeCount"].append(analyze_data[dobj_id]["averageGazeCount"])
                metrics[g["name"]]["averageGazeLength"].append(analyze_data[dobj_id]["averageGazeLength"])
                metrics[g["name"]]["totalGazeCount"].append(analyze_data[dobj_id]["totalGazeCount"])
                metrics[g["name"]]["totalGazeLength"].append(analyze_data[dobj_id]["totalGazeLength"])
                metrics[g["name"]]["totalSessionsWithAnyGaze"].append(analyze_data[dobj_id]["totalSessionsWithAnyGaze"])
                metrics[g["name"]]["proportionOfSessionsWithAnyGaze"].append(analyze_data[dobj_id]["proportionOfSessionsWithAnyGaze"])
            metrics[g["name"]]["averageGazeInstanceDuration"]=avg_list(metrics[g["name"]]["averageGazeInstanceDuration"])
            metrics[g["name"]]["averageGazeCount"]=avg_list(metrics[g["name"]]["averageGazeCount"])
            metrics[g["name"]]["averageGazeLength"]=avg_list(metrics[g["name"]]["averageGazeLength"])
            metrics[g["name"]]["totalGazeCount"]=avg_list(metrics[g["name"]]["totalGazeCount"])
            metrics[g["name"]]["totalGazeLength"]=avg_list(metrics[g["name"]]["totalGazeLength"])
            metrics[g["name"]]["totalSessionsWithAnyGaze"]=avg_list(metrics[g["name"]]["totalSessionsWithAnyGaze"])
            metrics[g["name"]]["proportionOfSessionsWithAnyGaze"]=avg_list(metrics[g["name"]]["proportionOfSessionsWithAnyGaze"])
        objid_index+=1
    final_return_json={}
    final_return_json["sessionCount"]=dobj_data["sessionCount"]
    final_return_json["metrics"]=metrics
    return final_return_json
    
        

'''
def single_session_slicer_metric_object_queries_model(session_id,objectIds,gazeType):
    """
    单个session的数据
    """
    db,cursor=connect_mysql()
    sql_1="select data_ids_json from session where id="+str(session_id)+" limit 0,1"
    cursor.execute(sql_1)
    results = cursor.fetchall()
    data_ids_list=[]
    for row in results:
        data_ids_json=json.loads(row[0])
        data_ids_list.append(data_ids_json[gazeType])

    totalSessionsWithAnyData=0      #有所有dobj的data数量
    temp={}
    for objid in objectIds:
        temp[objid]={}
        temp[objid]["TimeToFirst"]=[]   #第一次data
        temp[objid]["dataSequence"]=[]  #data发生序列
        temp[objid]["dataLength"]=[]    #data时间长度
        temp[objid]["dataCount"]=[]     #data发生次数

    mdb=connect_mongodb()
    e_table=mdb[gazeType]
    for mid_list in data_ids_list:
        point_index=0
        obj_list=[]
        for mid in mid_list:
            x=e_table.find({ "_id": ObjectId(mid)})[0]
            if gazeType=="fixation":
                
                for point in x["data"]:
                    if "objectid" in point.keys():
                        point_objid=point["objectid"]
                        #第一次data
                        if x["part"]==1 and point_index==0:
                            TimeToFirst=point["time"]-x["timestamp"]
                            temp[point_objid]["TimeToFirst"].append(TimeToFirst)
                        #data时间长度 
                        #data发生次数
                        if point_objid not in obj_list:
                            temp[point_objid]["dataLength"].append(point["duration"]/1000)
                            temp[point_objid]["dataCount"].append(1)
                        else:
                            temp[point_objid]["dataLength"][-1]+=point["duration"]/1000
                            temp[point_objid]["dataCount"][-1]+=1
                        #data发生序列
                        if point_objid not in obj_list:
                            obj_list.append(point_objid)
                        dataSequence=len(obj_list)
                        temp[point_objid]["dataSequence"].append(dataSequence)
                        
                    point_index+=1

            else:   #gaze
                point_index=0
                obj_list=[]
                for point in x["data"]:
                    if "o" in point.keys():
                        point_objid=point["o"]
                        #第一次data
                        if x["part"]==1 and point_index==0:
                            TimeToFirst=point["time"]-x["timestamp"]
                            temp[point_objid]["TimeToFirst"].append(TimeToFirst)
                        #data时间长度 
                        #data发生次数
                        if point_objid not in obj_list:
                            temp[point_objid]["dataLength"].append(x["interval"])
                            temp[point_objid]["dataCount"].append(1)
                        else:
                            temp[point_objid]["dataLength"][-1]+=x["interval"]
                            temp[point_objid]["dataCount"][-1]+=1
                        #data发生序列
                        if point_objid not in obj_list:
                            obj_list.append(point_objid)
                        dataSequence=len(obj_list)
                        temp[point_objid]["dataSequence"].append(dataSequence)
                        
                    point_index+=1
        #totalSessionsWithAnyData
        if len(obj_list)==len(objectIds):
            totalSessionsWithAnyData+=1
    
    metrics={}
    for final_objid in temp.keys():
        metrics[final_objid]={}
        if gazeType=="fixation":
            try:
                metrics[final_objid]["averageFixationInstanceDuration"]=sum_list(temp[final_objid]["dataLength"])/sum_list(temp[final_objid]["dataCount"])
            except:
                metrics[final_objid]["averageFixationInstanceDuration"]=0
            metrics[final_objid]["averageFixationCount"]=avg_list(temp[final_objid]["dataCount"])
            metrics[final_objid]["averageFixationLength"]=avg_list(temp[final_objid]["dataLength"])
            metrics[final_objid]["totalFixationCount"]=sum_list(temp[final_objid]["dataCount"])
            metrics[final_objid]["totalFixationLength"]=sum_list(temp[final_objid]["dataLength"])
            metrics[final_objid]["totalSessionsWithAnyFixation"]=totalSessionsWithAnyData
            metrics[final_objid]["proportionOfSessionsWithAnyFixation"]=totalSessionsWithAnyData/len(data_ids_list)    #?
            metrics[final_objid]["averageTimeToFirstFixation"]=avg_list(temp[final_objid]["TimeToFirst"])
            metrics[final_objid]["averageFixationSequence"]=avg_list(temp[final_objid]["dataSequence"])
        else:   #gaze
            try:
                metrics[final_objid]["averageGazeInstanceDuration"]=sum_list(temp[final_objid]["dataLength"])/sum_list(temp[final_objid]["dataCount"])
            except:
                metrics[final_objid]["averageGazeInstanceDuration"]=0
            metrics[final_objid]["averageGazeCount"]=avg_list(temp[final_objid]["dataCount"])
            metrics[final_objid]["averageGazeLength"]=avg_list(temp[final_objid]["dataLength"])
            metrics[final_objid]["totalGazeCount"]=sum_list(temp[final_objid]["dataCount"])
            metrics[final_objid]["totalGazeLength"]=sum_list(temp[final_objid]["dataLength"])
            metrics[final_objid]["totalSessionsWithAnyGaze"]=totalSessionsWithAnyData
            metrics[final_objid]["proportionOfSessionsWithAnyGaze"]=totalSessionsWithAnyData/len(data_ids_list)    #?
            metrics[final_objid]["averageTimeToFirstGaze"]=avg_list(temp[final_objid]["TimeToFirst"],"-1")
            metrics[final_objid]["averageGazeSequence"]=avg_list(temp[final_objid]["dataSequence"],"-1")
    final_return_json={}
    final_return_json["sessionCount"]=len(data_ids_list)
    final_return_json["metrics"]=metrics
    return final_return_json
'''



def dynamic_obj_cube_agg_queries_model(parm):
    db,cursor=connect_mysql()
    if "minCount" in parm:
        minCount=parm["minCount"]
    else:
        minCount=0
    scene_version_id=parm["entityFilters"]["versionId"]
    
    if parm["aggregation"]["type"]=="objectFixation":
        objectId=parm["aggregation"]["objectId"]
        gazeType="fixation"
    elif parm["aggregation"]["type"]=="objectGaze":
        objectId=parm["aggregation"]["objectId"]
        gazeType="gaze"
    elif parm["aggregation"]["type"]=="worldFixation":
        gazeType="fixation"
    elif parm["aggregation"]["type"]=="worldGaze":
        gazeType="gaze"
    elif parm["aggregation"]["type"]=="worldPosition":
        gazeType="gaze"
    elif parm["aggregation"]["type"]=="worldEvent":
        gazeType="event"
    interval=parm["interval"]

    #筛选时间(仅有时间)[之后可以改进]
    try:
        if "timeFilters" in parm:
            start_time=int(parm["timeFilters"]["start_time"])
            end_time=int(parm["timeFilters"]["end_time"])
            sql_1="select data_ids_json from session where scene_version_id="+str(scene_version_id)
            if start_time!=-1:
                sql_1+=" and UNIX_TIMESTAMP(session_start_time)>"+str(start_time/1000)
            if end_time!=-1:
                sql_1+=" and UNIX_TIMESTAMP(session_start_time)<"+str(end_time/1000)
        else:
            sql_1="select data_ids_json from session where scene_version_id="+str(scene_version_id)
    except:
        sql_1="select data_ids_json from session where scene_version_id="+str(scene_version_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    data_ids_list=[]
    for row in results:
        data_ids_json=json.loads(row[0])
        data_ids_list.append(data_ids_json[gazeType])

    mdb=connect_mongodb()
    e_table=mdb[gazeType]
    all_point_data=[]
    
    for mid_list in data_ids_list:
        #print(mid_list)
        for mid in mid_list:
            x=e_table.find({ "_id": ObjectId(mid)})[0]
            for point in x["data"]:
                if parm["aggregation"]["type"]=="objectFixation" or parm["aggregation"]["type"]=="objectGaze":  #OBJECT
                    if gazeType=="fixation":
                        if "objectid" in point.keys():
                            if objectId==point["objectid"]:
                                all_point_data.append(point["p"])
                    else:
                        if "o" in point.keys():
                            if objectId==point["o"]:
                                all_point_data.append(point["g"])
                elif parm["aggregation"]["type"]=="worldFixation":                                                                                           #WORLD
                    if ("objectid" not in point.keys()) and ("p" in point.keys()):
                        all_point_data.append(point["p"])
                elif parm["aggregation"]["type"]=="worldGaze":                                                                                           #WORLD
                    if ("o" not in point.keys()) and ("g" in point.keys()):
                        all_point_data.append(point["g"])
                elif parm["aggregation"]["type"]=="worldPosition":
                    all_point_data.append(point["p"])
                elif parm["aggregation"]["type"]=="worldEvent":
                    all_point_data.append(point["point"])

    #获取xyz的最大最小值
    x_list=[]
    y_list=[]
    z_list=[]
    for point in all_point_data:
        x_list.append(point[0])
        y_list.append(point[1])
        z_list.append(point[2])
    try:
        x_max=max(x_list)
        y_max=max(y_list)
        z_max=max(z_list)
        x_min=min(x_list)
        y_min=min(y_list)
        z_min=min(z_list)
    except:
        x_max=0
        y_max=0
        z_max=0
        x_min=0
        y_min=0
        z_min=0

    counts=[]
    #cube
    for x_index in range(math.floor((x_max-x_min)/interval)+1):
        for y_index in range(math.floor((y_max-y_min)/interval)+1):
            for z_index in range(math.floor((z_max-z_min)/interval)+1):
                now_from_x=x_min+x_index*interval
                now_to_x=x_min+(x_index+1)*interval
                now_from_y=y_min+y_index*interval
                now_to_y=y_min+(y_index+1)*interval
                now_from_z=z_min+z_index*interval
                now_to_z=z_min+(z_index+1)*interval
                coord=[now_from_x,now_from_y,now_from_z]
                count=0
                for point in all_point_data:
                    if point[0]>=now_from_x and point[0]<=now_to_x and point[1]>=now_from_y and point[1]<=now_to_y and point[2]>=now_from_z and point[2]<=now_to_z:
                        count+=1
                if count>minCount:
                    temp={}
                    temp["count"]=count
                    temp["coord"]=coord
                    counts.append(temp)
    return_json={}
    return_json[parm["aggregation"]["name"]]={}
    return_json[parm["aggregation"]["name"]]["bin_size"]=interval
    return_json[parm["aggregation"]["name"]]["session_count"]=len(data_ids_list)
    return_json[parm["aggregation"]["name"]]["counts"]=counts
    return_json[parm["aggregation"]["name"]]["metrics"]={}
    return_json[parm["aggregation"]["name"]]["metrics"]["sessionCount"]=len(data_ids_list)
    return return_json
                



'''
def session_slicer_metric_group_queries_model(parm):
    db,cursor=connect_mysql()
    scene_version_id=parm["entityFilters"]["versionId"]
    dobj_g_list=[]
    for g in parm["groups"]:
        dobj_g_list.append(g["objectIds"])
    sql_1="select data_ids_json from session where scene_version_id="+str(scene_version_id)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    data_ids_list=[]
    for row in results:
        data_ids_json=json.loads(row[0])
        data_ids_list.append(data_ids_json[parm["gazeType"]])

    totalSessionsWithAnyData=0      #有所有dobj的data数量
    temp={}
    objid_index=0
    for dobj_g in dobj_g_list:
        temp[objid_index]={}
        temp[objid_index]["dobj_g"]=dobj_g
        temp[objid_index]["TimeToFirst"]=[]   #第一次data
        temp[objid_index]["dataSequence"]=[]  #data发生序列
        temp[objid_index]["dataLength"]=[]    #data时间长度
        temp[objid_index]["dataCount"]=[]     #data发生次数
        objid_index+=1

    #查找mongodb
    mdb=connect_mongodb()
    e_table=mdb[parm["gazeType"]]
    session_data_list=[]
    for mid_list in data_ids_list:
        #print(mid_list)
        for i in range(len(mid_list)):
            mid=mid_list[i]
            x=e_table.find({ "_id": ObjectId(mid)})[0]
            if i==0:
                session_data_list.append(x)
            else:
                session_data_list[-1]["data"]+=x["data"]
    
    for session_data in session_data_list:
        obj_g_index_list=[]
        if parm["gazeType"]=="fixation":
            last_point_obj_id=""
            for point_index in range(len(session_data["data"])):
                point=session_data["data"][point_index]
                if "objectid" in point.keys():
                    point_objid=point["objectid"]
                    temp_index=-1
                    for index in range(len(dobj_g_list)):
                        if point_objid in dobj_g_list[index]:
                            temp_index=index
                    if temp_index==-1:
                        continue
                    #第一次data
                    if point_index==0:
                        TimeToFirst=point["time"]-session_data["timestamp"]
                        temp[temp_index]["TimeToFirst"].append(TimeToFirst)
                    #data时间长度 
                    #data发生次数
                    if temp_index not in obj_g_index_list:
                        temp[temp_index]["dataLength"].append(point["duration"]/1000)
                        temp[temp_index]["dataCount"].append(1)
                        temp[temp_index]["distinctdataCount"].append(1)
                    else:
                        if last_point_obj_id!=temp_index:
                            temp[temp_index]["distinctdataCount"][-1]+=1
                        temp[temp_index]["dataLength"][-1]+=point["duration"]/1000
                        temp[temp_index]["dataCount"][-1]+=1
                    #data发生序列
                    if temp_index not in obj_list:
                        obj_list.append(temp_index)
                        dataSequence=len(obj_list)
                        temp[temp_index]["dataSequence"].append(dataSequence)
                    last_point_obj_id=temp_index
                else:
                    last_point_obj_id=""
        else:
            last_point_obj_id=""
            last_point_time=0
            for point_index in range(len(session_data["data"])):
                point=session_data["data"][point_index]
                
                if "o" in point.keys():
                    point_objid=point["o"]
                    now_point_time=point["time"]
                    temp_index=-1
                    for index in range(len(dobj_g_list)):
                        if point_objid in dobj_g_list[index]:
                            temp_index=index
                    if temp_index==-1:
                        continue
                    #第一次data
                    if point_index==0:
                        TimeToFirst=point["time"]-session_data["timestamp"]
                        temp[temp_index]["TimeToFirst"].append(TimeToFirst)
                    #data时间长度 
                    #data发生次数
                    if temp_index not in obj_g_index_list:
                        temp[temp_index]["dataLength"].append(x["interval"])
                        temp[temp_index]["dataCount"].append(1)
                        temp[temp_index]["distinctdataCount"].append(1)
                    else:
                        if last_point_obj_id==temp_index:
                            temp[temp_index]["dataLength"][-1]+=(now_point_time-last_point_time)
                        else:
                            temp[temp_index]["distinctdataCount"][-1]+=1
                            temp[temp_index]["dataLength"][-1]+=x["interval"]
                        temp[temp_index]["dataCount"][-1]+=1

                    last_point_obj_id=temp_index
                    last_point_time=now_point_time
                else:
                    last_point_obj_id=""
                    last_point_time=0
        #totalSessionsWithAnyData
        if len(obj_g_index_list)==len(dobj_g_list):
            totalSessionsWithAnyData+=1

    #查找mongodb
    mdb=connect_mongodb()
    e_table=mdb[parm["gazeType"]]
    for mid_list in data_ids_list:
        point_index=0
        obj_g_index_list=[]
        for mid in mid_list:
            x=e_table.find({ "_id": ObjectId(mid)})[0]
            if parm["gazeType"]=="fixation":
                
                for point in x["data"]:
                    if "objectid" in point.keys():
                        point_objid=point["objectid"]
                        temp_index=-1
                        for index in range(len(dobj_g_list)):
                            if point_objid in dobj_g_list[index]:
                                temp_index=index
                        if temp_index==-1:
                            continue
                        #第一次data
                        if x["part"]==1 and point_index==0:
                            TimeToFirst=point["time"]-x["timestamp"]
                            temp[temp_index]["TimeToFirst"].append(TimeToFirst)
                        #data时间长度 
                        #data发生次数
                        if temp_index not in obj_g_index_list:
                            obj_g_index_list.append(temp_index)
                            temp[temp_index]["dataLength"].append(point["duration"]/1000)
                            temp[temp_index]["dataCount"].append(1)
                        else:
                            temp[temp_index]["dataLength"][-1]+=point["duration"]/1000
                            temp[temp_index]["dataCount"][-1]+=1

                        
                    point_index+=1

            else:   #gaze
                point_index=0
                obj_list=[]
                for point in x["data"]:
                    if "o" in point.keys():
                        point_objid=point["o"]
                        temp_index=-1
                        for index in range(len(dobj_g_list)):
                            if point_objid in dobj_g_list[index]:
                                temp_index=index
                        if temp_index==-1:
                            continue
                        #第一次data
                        if x["part"]==1 and point_index==0:
                            TimeToFirst=point["time"]-x["timestamp"]
                            temp[temp_index]["TimeToFirst"].append(TimeToFirst)
                        #data时间长度 
                        #data发生次数
                        if temp_index not in obj_g_index_list:
                            obj_g_index_list.append(temp_index)
                            temp[temp_index]["dataLength"].append(x["interval"])
                            temp[temp_index]["dataCount"].append(1)
                        else:
                            temp[temp_index]["dataLength"][-1]+=x["interval"]
                            temp[temp_index]["dataCount"][-1]+=1

                        
                    point_index+=1
        #totalSessionsWithAnyData
        if len(obj_g_index_list)==len(dobj_g_list):
            totalSessionsWithAnyData+=1
        
    metrics={}
    objid_index=0
    for g in parm["groups"]:
        metrics[g["name"]]={}
        if parm["gazeType"]=="fixation":
            try:
                metrics[g["name"]]["averageFixationInstanceDuration"]=sum_list(temp[objid_index]["dataLength"])/sum_list(temp[objid_index]["dataCount"])
            except:
                metrics[g["name"]]["averageFixationInstanceDuration"]=0
            metrics[g["name"]]["averageFixationCount"]=avg_list(temp[objid_index]["dataCount"])
            metrics[g["name"]]["averageFixationLength"]=avg_list(temp[objid_index]["dataLength"])
            metrics[g["name"]]["totalFixationCount"]=sum_list(temp[objid_index]["dataCount"])
            metrics[g["name"]]["totalFixationLength"]=sum_list(temp[objid_index]["dataLength"])
            metrics[g["name"]]["totalSessionsWithAnyFixation"]=totalSessionsWithAnyData
            metrics[g["name"]]["proportionOfSessionsWithAnyFixation"]=totalSessionsWithAnyData/len(data_ids_list)    #?
        else:   #gaze
            try:
                metrics[g["name"]]["averageGazeInstanceDuration"]=sum_list(temp[objid_index]["dataLength"])/sum_list(temp[objid_index]["dataCount"])
            except:
                metrics[g["name"]]["averageGazeInstanceDuration"]=0
            metrics[g["name"]]["averageGazeCount"]=avg_list(temp[objid_index]["dataCount"])
            metrics[g["name"]]["averageGazeLength"]=avg_list(temp[objid_index]["dataLength"])
            metrics[g["name"]]["totalGazeCount"]=sum_list(temp[objid_index]["dataCount"])
            metrics[g["name"]]["totalGazeLength"]=sum_list(temp[objid_index]["dataLength"])
            metrics[g["name"]]["totalSessionsWithAnyGaze"]=totalSessionsWithAnyData
            metrics[g["name"]]["proportionOfSessionsWithAnyGaze"]=totalSessionsWithAnyData/len(data_ids_list)    #?
        objid_index+=1
    final_return_json={}
    final_return_json["sessionCount"]=len(data_ids_list)
    final_return_json["metrics"]=metrics
    return final_return_json
'''



def session_slicer_queries_model(parm):
    """
    analyze
    """ 
    #show_type
    show_type=parm["show_type"]

    if show_type=="total_event_count":
        res=total_event_count_queries(parm)
    elif show_type=="total_session_count":
        res=total_session_count_queries(parm)
    elif show_type=="max_session_length":
        res=session_length_queries(parm,"max")
    elif show_type=="min_session_length":
        res=session_length_queries(parm,"min")
    elif show_type=="avg_session_length":
        res=session_length_queries(parm,"avg")
    return res

def session_length_queries(parm,length_type):
    db,cursor=connect_mysql()
    #基本信息
    project_id=parm["entityFilters"]["projectId"]
    scene_id=parm["entityFilters"]["scene_id"]
    scene_version_id=int(parm["entityFilters"]["scene_version_id"])
    
    #[TODO]更多筛选
    #event
    evnet_filter=parm["eventFilters"]

    #time
    start_time=int(parm["timeFilters"]["start_time"])
    end_time=int(parm["timeFilters"]["end_time"])
    if length_type=="max":
        sql_1="select max(session_duration),UNIX_TIMESTAMP(create_time) from session"
    elif length_type=="min":
        sql_1="select min(session_duration),UNIX_TIMESTAMP(create_time) from session"
    elif length_type=="avg":
        sql_1="select avg(session_duration),UNIX_TIMESTAMP(create_time) from session"
    sql_1+=" where scene_version_id="+str(scene_version_id)

    if start_time!=-1:
        sql_1+=" and UNIX_TIMESTAMP(create_time)>"+str(start_time/1000)
    if end_time!=-1:
        sql_1+=" and UNIX_TIMESTAMP(create_time)<"+str(end_time/1000)
    
    if evnet_filter!="none":
        sql_1+=" and locate('"+evnet_filter+"',event_type_json)<>0"

    sql_1+=" group by DATE_FORMAT(create_time,'%Y-%m-%d')"

    return_list=[]
    print(sql_1)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    for row in results:
        temp={}
        temp["num"]=int(row[0])
        temp["time"]=row[1]
        return_list.append(temp)
    return return_list

def total_event_count_queries(parm):
    db,cursor=connect_mysql()
    #基本信息
    project_id=parm["entityFilters"]["projectId"]
    scene_id=parm["entityFilters"]["scene_id"]
    scene_version_id=int(parm["entityFilters"]["scene_version_id"])
    
    #[TODO]更多筛选
    #event
    evnet_filter=parm["eventFilters"]

    #time
    start_time=int(parm["timeFilters"]["start_time"])
    end_time=int(parm["timeFilters"]["end_time"])
    if evnet_filter!="none":
        sql_1="select LENGTH(event_type_json) - LENGTH( REPLACE (event_type_json, '"+evnet_filter+"', '')),UNIX_TIMESTAMP(create_time) from session"
    else:
        return []
    sql_1+=" where scene_version_id="+str(scene_version_id)

    if start_time!=-1:
        sql_1+=" and UNIX_TIMESTAMP(create_time)>"+str(start_time/1000)
    if end_time!=-1:
        sql_1+=" and UNIX_TIMESTAMP(create_time)<"+str(end_time/1000)
    
    if evnet_filter!="none":
        sql_1+=" and locate('"+evnet_filter+"',event_type_json)<>0"

    sql_1+=" group by DATE_FORMAT(create_time,'%Y-%m-%d')"
    return_list=[]
    print(sql_1)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    for row in results:
        temp={}
        temp["num"]=row[0]//len(evnet_filter)
        temp["time"]=row[1]
        return_list.append(temp)
    return return_list

def total_session_count_queries(parm):
    db,cursor=connect_mysql()
    #基本信息
    project_id=parm["entityFilters"]["projectId"]
    scene_id=parm["entityFilters"]["scene_id"]
    scene_version_id=int(parm["entityFilters"]["scene_version_id"])
    
    #[TODO]更多筛选
    #event
    evnet_filter=parm["eventFilters"]

    #time
    start_time=int(parm["timeFilters"]["start_time"])
    end_time=int(parm["timeFilters"]["end_time"])

    sql_1="select count(id),UNIX_TIMESTAMP(create_time) from session"
    sql_1+=" where scene_version_id="+str(scene_version_id)

    if start_time!=-1:
        sql_1+=" and UNIX_TIMESTAMP(create_time)>"+str(start_time/1000)
    if end_time!=-1:
        sql_1+=" and UNIX_TIMESTAMP(create_time)<"+str(end_time/1000)
    
    if evnet_filter!="none":
        sql_1+=" and locate('"+evnet_filter+"',event_type_json)<>0"

    sql_1+=" group by DATE_FORMAT(create_time,'%Y-%m-%d')"

    return_list=[]
    print(sql_1)
    cursor.execute(sql_1)
    results = cursor.fetchall()
    for row in results:
        temp={}
        temp["num"]=row[0]
        temp["time"]=row[1]
        return_list.append(temp)
    return return_list


    







def sum_list(tlist):
    tall=0
    for v in tlist:
        tall+=v
    return tall

def avg_list(tlist,return_error=None):
    if len(tlist)==0 and return_error is not None:
        return -1
    tall=0
    for v in tlist:
        tall+=v
    try:
        return tall/len(tlist)
    except:
        return 0