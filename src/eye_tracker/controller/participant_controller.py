#-*- coding:utf-8 -*-
"""
participant_controller

FUNCTION:
    (1) get_participant_list
        获取该org_id下的参与者列表

    (2) delete_participant [TODO]

    (3) edit_participant [TODO]

    (4) participant_detail
        获取该参与者的session+详情

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.participant_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.participant_model import *

participant=Blueprint('participant',__name__)

@participant.route(cg.participant_list_url,methods=["GET"])
def participant_list():
    """
    [GET]
    participant_list
    """
    if request.method=='GET':
        try:
            org_id=request.args.get("org_id")
        except:
            return "error"
        res=participant_list_model(org_id)
        return json.dumps(res)
    else:
        return "error"

@participant.route(cg.participant_detail_url,methods=["GET"])
def participant_detail():
    """
    [GET]
    participant_detail
    """
    if request.method=='GET':
        try:
            p_id=request.args.get("p_id")
        except:
            return "error"
        res=participant_detail_model(p_id)
        return json.dumps(res)
    else:
        return "error"