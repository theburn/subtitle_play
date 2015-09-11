#!/usr/local/python2.7/bin/python 
#-*- coding:utf-8 -*-
from django.contrib.auth import *
from django.contrib.auth.models  import User,  Group
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse,  HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from subtitle_play import settings
from django.template import RequestContext
from MV.models import *

import json
import os
import time
import xml.sax.saxutils
import logging

MAX_SIZE = 1024 * 1024 * 1024 * 2   # 2G
MEDIA_ROOT = settings.MEDIA_ROOT

from common_function import get_ip_address

def __log_test(msg):
    log = logging.getLogger("audit")
    log.debug("SYSTEM SYSTEM LOG_TEST %s", msg)


@login_required
def config(request):
    return render_to_response("config.html", context_instance=RequestContext(request))

@login_required
def controllor(request):
    return render_to_response("controllor.html")

@login_required
def show(request):
    return render_to_response("show.html")

@login_required
def dispatch(request):
    return render_to_response("dispatch.html", \
                                {"IP" : get_ip_address("eth0")})



@login_required
@csrf_protect
def upload_file(request, target):
    res_upload = {"result": None}
    log_msg = {\
               "0":u"上传成功", \
               "1":u"上传文件已存在", \
               "2":u"磁盘IO错误", \
               "3":u"异常错误", \
               "4":u"HTTP方法错误", \
               "5":u"上传文件过大", \
               "10":u"上传文件已存在", \
            }
    name = "None"
    target_flag = True
    if request.method=='POST':
        try:
            if target == "mv":
                UPLOAD_PATH = os.path.join(MEDIA_ROOT, "mv_templates")
            elif target == "subtitle":
                UPLOAD_PATH = os.path.join(MEDIA_ROOT, "subtitle_templates")
            else:
                target_flag = False


            if target_flag:
                f = request.FILES.get('uploadfile')
                name = xml.sax.saxutils.escape(f.name).strip().replace(" ", "_").encode("utf-8")

                if not os.path.exists(UPLOAD_PATH):
                    os.makedirs(UPLOAD_PATH)

                filename = os.path.join(UPLOAD_PATH, name)

                if os.path.exists(filename):
                    os.remove(filename) # 先删除老的文件

                if f.size > MAX_SIZE:
                    res_upload["result"] = 5
                else:
                    with open(filename, 'wb+') as tempfile:
                        for chunk in f.chunks():
                            tempfile.write(chunk)

                    mv = MV_Template()
                    mv.mv_name = name
                    mv.mv_file_location = filename
                    mv.save()

                    res_upload["result"] = 0
            else:
                res_upload["result"] = 10
        except IOError:
            res_upload["result"] = 2
        except Exception as e:
            __log_test(e)
            res_upload["result"] = 3
    else:
        res_upload["result"] = 4


    log_event = u"上传" + name
    res_key = str(res_upload['result'])
    log = logging.getLogger("audit")
    log.debug("%s %s %s %s",  \
            request.session['ip'],  request.session['user_name'],  \
            log_event,  log_msg[res_key]) 

    return HttpResponseRedirect("/config/")

