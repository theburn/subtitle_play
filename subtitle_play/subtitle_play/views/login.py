#!/usr/local/python2.7/bin/python 
#-*- coding:utf-8 -*-
from django.contrib.auth import *
from django.contrib.auth.models  import User,  Group
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse,  HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
import json
from django.contrib.auth.decorators import login_required
import time

import logging

TITLE = u"为爱欢呼第五季--赣州站"



def __log_test(msg):
    log = logging.getLogger("audit")
    log.debug("SYSTEM SYSTEM LOG_TEST %s", msg)


#********************************#
#   User Login and Logout        #
#********************************#

#用户登录验证
@csrf_protect
def auth_login(request):
    res_login = {'res_login':""}
    log_msg = {\
               "0": u"用户登录成功",\
               "1": u"输入用户名或者密码错误",\
               }

    if request.is_ajax() and request.method == "POST":
        username  =  request.POST.get('username', '').strip(" ")
        password  =  request.POST.get('password', '').strip(" ")
        #获取用户IP
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        #保存ip到session
        request.session['ip'] = ip
        #保存username到session
        request.session['user_name'] = username

        #####
        update_user = authenticate(username = username,  password = password)
        if update_user is not None and update_user.is_active:
            login(request, update_user)
            res_login['res_login'] = "0"
        else:
            res_login['res_login'] = "1"
    else:
        res_login['res_login'] = "1"

        

    log_event = u"用户登录系统"
    res_key = str(res_login['res_login'])
    log = logging.getLogger("audit")
    log.debug("%s %s %s %s",  \
            request.session['ip'],  request.session['user_name'],  \
            log_event,  log_msg[res_key]) 

    res_login_json = json.dumps(res_login)
    return JsonResponse(res_login_json)



#用户退出
@login_required
def auth_logout(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")


