#!/usr/local/python2.7/bin/python 
#-*- coding:utf-8 -*-
from django.contrib.auth import *
from django.contrib.auth.models  import User,  Group
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse,  HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from subtitle_play import settings
from django.template import RequestContext
from subtitle_play.music.models import *
from django.core.files.uploadedfile import UploadedFile

import copy
import json
import os
import time
import xml.sax.saxutils
import logging
import sys
import chardet
reload(sys)
sys.setdefaultencoding("utf-8")

MAX_SIZE = 1024 * 1024 * 1024 * 2   # 2G
MEDIA_ROOT = settings.MEDIA_ROOT

from common_function import get_ip_address, check_music_is_exists, check_mv_is_exists, check_subtitle_is_exists, \
                            get_file_encoding

def __log_test(msg):
    log = logging.getLogger("audit")
    log.debug("SYSTEM SYSTEM LOG_TEST %s", msg)


@login_required
def config(request):
    try:
        all_music_instance_list = Music.objects.all()
    except:
        all_music_instance_list = []

    return render_to_response("config.html", \
                            {
                                "music_list":all_music_instance_list, \
                            }, \
                             context_instance=RequestContext(request)
                            )

@login_required
def controllor(request):
    try:
        all_music_instance_list = Music.objects.all()
    except:
        all_music_instance_list = []

    return render_to_response("controllor.html", \
                            {
                                "music_list":all_music_instance_list, \
                                "IP" : get_ip_address("eth0"), \
                            }, \
                             context_instance=RequestContext(request)
                            )



@login_required
def show(request):
    return render_to_response("show.html",
                            {
                                "IP" : get_ip_address("eth0"), \
                            }, \
                        )

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
    exists_flag = False
    if request.method=='POST':
        try:
            if target == "mv":
                UPLOAD_PATH = os.path.join(MEDIA_ROOT, "mv_templates")
            elif target == "subtitle":
                UPLOAD_PATH = os.path.join(MEDIA_ROOT, "subtitle_templates")
            else:
                target_flag = False


            if target_flag:
                uploadfile = request.FILES.get('files[]')
                f = UploadedFile(uploadfile)
                name = xml.sax.saxutils.escape(f.name).strip().replace(" ", "_").encode("utf-8")

                if not os.path.exists(UPLOAD_PATH):
                    os.makedirs(UPLOAD_PATH)

                filename = os.path.join(UPLOAD_PATH, name)

                if os.path.exists(filename):
                    exists_flag = True
                else:
                    if f.file.size > MAX_SIZE:
                        res_upload["result"] = 5
                    else:
                        if target == "mv":
                            for mv_instance in MV_Template.objects.all():
                                if name == mv_instance.mv_name:
                                    exists_flag = True
                                    break

                            if not exists_flag:
                                mv = MV_Template()
                                mv.mv_name = name
                                mv.mv_file_location = f
                                mv.save()
                        elif target == "subtitle":
                            for subtitle_instance in Subtitle_Template.objects.all():
                                if name == subtitle_instance.subtitle_name:
                                    exists_flag = True
                                    break

                            if not exists_flag:
                                subtitle = Subtitle_Template()
                                subtitle.subtitle_name = name
                                subtitle.subtitle_file_location = f
                                subtitle.save()

                        if exists_flag:
                            res_upload["result"] = 10
                        else:
                            res_upload["result"] = 0
            else:
                res_upload["result"] = 3
        except IOError:
            res_upload["result"] = 2
        except Exception as e:
            __log_test(e)
            res_upload["result"] = 3
    else:
        res_upload["result"] = 4


    log_event = u"上传" + name
    res_key = str(res_upload['result'])
    __log_test(res_key)
    log = logging.getLogger("audit")
    log.debug("%s %s %s %s",  \
            request.session['ip'],  \
            request.session['user_name'],  \
            log_event,  \
            log_msg[res_key]) 

    result = []
    if exists_flag:
        result.append({"exists":True})
    else:
        result.append({"name":name,
                       "size":f.file.size,
                       })
    
    return HttpResponse(json.dumps(result), content_type="application/json")









@login_required
def get_mv_template(request):
    res_mv = {"result":None, "mv_list":[]}
    if request.is_ajax() and request.method == "GET":
        try:
            mv_all = MV_Template.objects.all()
            for mv in mv_all:
                res_mv["mv_list"].append(mv.mv_name)

            if len(res_mv["mv_list"]) == 0:
                res_mv["mv_list"] = "Empty"
            
            res_mv["result"] = 0
        except:
            res_mv["result"] = 1
            res_mv["mv_list"] = "ERROR_1"
    else:
        res_mv["result"] = 2
        res_mv["mv_list"] = "ERROR_2"

    return JsonResponse(res_mv)


@login_required
def get_subtitle_template(request):
    res_subtitle = {"result":None, "subtitle_list":[]}
    if request.is_ajax() and request.method == "GET":
        try:
            subtitle_all = Subtitle_Template.objects.all()
            for subtitle in subtitle_all:
                res_subtitle["subtitle_list"].append(subtitle.subtitle_name)

            if len(res_subtitle["subtitle_list"]) == 0:
                res_subtitle["subtitle_list"] = "Empty"

            res_subtitle["result"] = 0
        except:
            res_subtitle["subtitle_list"] = "ERROR_1"
            res_subtitle["result"] = 1
    else:
        res_subtitle["result"] = 2
        res_subtitle["subtitle_list"] = "ERROR_2"

    return JsonResponse(res_subtitle)







@login_required
@csrf_protect
def post_music(request):
    res_post = {"result":None}
    if request.is_ajax() and request.method == "POST":
        try:
            music_name = request.POST.get("music_name",None).strip()
            mv_name = request.POST.get("mv_name",None).strip()
            subtitle_name = request.POST.get("subtitle_name",None).strip()

            music_is_exists = check_music_is_exists(music_name)
            mv_is_exists = check_mv_is_exists(mv_name)
            subtitle_is_exists= check_subtitle_is_exists(subtitle_name)

            #__log_test(music_name)
            if mv_is_exists and subtitle_is_exists:
                if music_is_exists:
                    music_instance = Music.objects.get(music_name = music_name)
                    #__log_test("i see you")
                else:
                    music_instance = Music(music_name = music_name)
                    #__log_test("i see you new")

                mv_instance = MV_Template.objects.get(mv_name = mv_name)
                subtitle_instance = Subtitle_Template.objects.get(subtitle_name = subtitle_name)

                music_instance.music_mv_id = mv_instance.id
                music_instance.music_subtitle_id = subtitle_instance.id

                music_instance.save()
                res_post["result"] = 0

            else:
                res_post["result"] = 1

        except:
            res_post["result"] = 2
    else:
        res_post["result"] = 3

    return JsonResponse(res_post)




@login_required
def get_music_list(request):
    res_music = {"result":None, "music_list":[]}
    if request.is_ajax() and request.method == "GET":
        try:
            music_all = Music.objects.all()
            for music in music_all:
                res_music["music_list"].append(music.music_name)
            
            res_music["result"] = 0
        except:
            res_music["result"] = 1
    else:
        res_music["result"] = 3

    return JsonResponse(res_music)




@login_required
def get_music_args(request):
    res_music = {"result":None, "args_list":{"mv":None, "subtitle":None}}
    if request.is_ajax() and request.method == "GET":
        try:
            music_name = request.GET.get("music_name", None)
            if music_name is not None:
                music_instance = Music.objects.get(music_name = music_name)
                res_music["args_list"]["mv"] = music_instance.music_mv.mv_name
                res_music["args_list"]["subtitle"] = music_instance.music_subtitle.subtitle_name
                res_music["result"] = 0
            else:
                res_music["result"] = 4
            
        except:
            res_music["result"] = 1
    else:
        res_music["result"] = 3

    return JsonResponse(res_music)


@login_required
def get_music_lyric(request):
    res_music = {"result":None, "lyric":[]}
    if request.is_ajax() and request.method == "GET":
        try:
            music_name = request.GET.get("music_name", None)
            if music_name is not None:
                music_instance = Music.objects.get(music_name = music_name)
                f = copy.deepcopy(music_instance.music_subtitle)
                f_encoding = get_file_encoding(f)
                if f_encoding.lower() in ("gbk", "gb2312"):
                    for line in music_instance.music_subtitle.subtitle_file_location.readlines():
                        res_music["lyric"].append(line.decode("gbk").encode("utf-8"))
                else:
                    for line in music_instance.music_subtitle.subtitle_file_location.readlines():
                        res_music["lyric"].append(line)
                res_music["result"] = 0
            else:
                res_music["result"] = 4
            
        except:
            res_music["result"] = 1
    else:
        res_music["result"] = 3

    return JsonResponse(res_music)










@login_required
@csrf_protect
def delete_music(request):
    res_delete = {"result":None}
    if request.is_ajax() and request.method == "POST":
        try:
            music_name = request.POST.get("music_name",None).strip()
            music_is_exists = check_music_is_exists(music_name)

            if music_is_exists:
                music_instance = Music.objects.get(music_name = music_name)
                music_instance.delete()
                res_delete["result"] = 0
            else:
                res_delete["result"] = 1

        except:
            res_delete["result"] = 2
    else:
        res_delete["result"] = 3

    return JsonResponse(res_delete)





