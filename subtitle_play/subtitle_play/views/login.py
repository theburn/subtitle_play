#!/usr/local/python2.7/bin/python 
#-*- coding:utf-8 -*-
from django.contrib.auth import *
from django.contrib.auth.models  import User,  Group
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse,  HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from patch_site.patch_models.models import *
import time

import Image,ImageDraw,ImageFont,random,StringIO
import logging

TITLE = u"上海市城域网安全管理系统"
LOGIN_LIMIT = 5
TIME_LIMIT = 5 * 60



def __log_test(msg):
    log = logging.getLogger("audit")
    log.debug("SYSTEM SYSTEM LOG_TEST %s", msg)




def __check_ip_login_limit(ip):
    try:
        ip_instance = LoginErrList.objects.get(IP = ip)
        if ip_instance.Number >= LOGIN_LIMIT:
            return True
        else:
            return False
    except:
        return None


def __create_ip_login(ip):
    try:
        ip_instance = LoginErrList()
        ip_instance.IP = ip
        ip_instance.Number = 0
        ip_instance.Time = str(int(time.time()))
        ip_instance.save()
        return True
    except:
        import django.db                                                                                                        
        django.db.close_connection()
        return False

def add_num_to_ip_login(ip):
    try:
        ip_instance = LoginErrList.objects.get(IP = ip)
        ip_instance.Number += 1
        if ip_instance.Number >= LOGIN_LIMIT:
            ip_instance.Time = str(int(time.time()))
        ip_instance.save()
        return True
    except:
        import django.db                                                                                                        
        django.db.close_connection()
        return False

def __clean_num_to_ip_login(ip):
    try:
        ip_instance = LoginErrList.objects.get(IP = ip)
        ip_instance.Number = 0
        ip_instance.save()
        return True
    except:
        import django.db                                                                                                        
        django.db.close_connection()
        return False

def __cmp_time_ip_login(ip):
    try:
        ip_instance = LoginErrList.objects.get(IP = ip)
        now_time = int(time.time())
        if now_time - int(ip_instance.Time) >= TIME_LIMIT:
            return True
        else:
            return False
    except:
        import django.db                                                                                                        
        django.db.close_connection()
        return False



def ip_is_limit(ip):
    if __check_ip_login_limit(ip) is None:
        __create_ip_login(ip)
        return False

    if __check_ip_login_limit(ip) is False:
        return False

    if __check_ip_login_limit(ip) is True and \
            __cmp_time_ip_login(ip) is True:
        __clean_num_to_ip_login(ip)
        return False
    else:
        return True
    


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
               "2": u"用户禁止登录",\
               "3": u"用户不存在",\
               "4": u"输入用户名或者密码错误",\
               "10": u"验证码错误",\
               "20": u"尝试次数过多，请稍后登录",\
               }
    username  =  request.POST.get('user', '').strip(" ")
    password  =  request.POST.get('pass', '').strip(" ")
    checkcode =  request.POST.get('checkcode', '').strip(" ")
    #获取用户IP
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    #保存ip到session
    request.session['ip'] = ip
    #保存username到session
    request.session['user_name'] = username


    ####check_ip_limit####
    if ip_is_limit(ip) is True:
        res_login['res_login'] = "20"
        res_login_json = simplejson.dumps(res_login)
        return HttpResponse(res_login_json,  mimetype = 'application/json')

    ####check_code####
    if not checkcode:
        add_num_to_ip_login(ip)
        res_login['res_login'] = "10"
        res_login_json = simplejson.dumps(res_login)
        return HttpResponse(res_login_json,  mimetype = 'application/json')

    ca = Captcha(request, True)
    if not ca.check(checkcode):
        add_num_to_ip_login(ip)
        res_login['res_login'] = "30"
        res_login_json = simplejson.dumps(res_login)
        return HttpResponse(res_login_json,  mimetype = 'application/json')

    
    #####
    update_user = authenticate(username = username,  password = password)
    if update_user is not None and update_user.is_active:
        __clean_num_to_ip_login(ip)
        login(request, update_user)
        res_login['res_login'] = "0"
    else:
        add_num_to_ip_login(ip)
        if username is not None and username != "" and username != "null" and\
        password is not None and password != "" and password != "null":
            try:
                user = User.objects.get(username  =  username)
                if user.is_active  ==  False:
                    res_login['res_login'] = "2"
                else:
                    res_login['res_login'] = "4"
            except User.DoesNotExist:
                res_login['res_login'] = "3"
        else:
            res_login['res_login'] = "1"
    

    log_event = u"用户登录系统"
    res_key = str(res_login['res_login'])
    log = logging.getLogger("audit")
    log.debug("%s %s %s %s",  \
            request.session['ip'],  request.session['user_name'],  \
            log_event,  log_msg[res_key]) 

    res_login_json = simplejson.dumps(res_login)
    return HttpResponse(res_login_json,  mimetype = 'application/json')



#用户退出
@login_required
def auth_logout(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")


def get_checkcode(request):
    figures         = ['a','b','c','d','e','f','g','h','j','k',\
                        'm','n','p','q','s','t','u','v','w','x',\
                        'y','z',2,3,4,5,6,7,8,9]
    ca              = Captcha(request, True)
    ca.words        = [''.join([str(random.sample(figures,1)[0]) for i in range(0,4)])]
    ca.type         = 'word'
    ca.img_width    = 100
    ca.img_height   = 45
    return ca.display()


@login_required
def get_user_info(request):
    result_info = {"username":None}
    if request.is_ajax() and request.method  == 'GET':
        result_info["username"]= request.user.username

    result_info_json = simplejson.dumps(result_info)
    return HttpResponse(result_info_json,  mimetype = 'application/json')




#用户修改密码
@login_required
@csrf_protect
def user_edit_pass(request):
    result_pass = {'result':""}
    log_msg = { \
               "0" : u"修改成功",\
               "1" : u"修改失败",\
               "4" : u"参数错误",\
            }
    if request.is_ajax() and request.method  == 'POST':
        current_user = request.user.username
        user = User.objects.get(username = current_user)
        old_pass = request.POST.get('old_pass', '')
        new_pass = request.POST.get('new_pass', '')
        new_again_pass = request.POST.get('new_again_pass', '')
        chk_pass = user.check_password(old_pass)
        if new_pass  == new_again_pass and new_pass !='' and chk_pass is True:
            user.set_password(new_pass)
            user.save()
            result_pass['result'] = "0"
        else:
            result_pass['result'] = "1"
    else:
        result_pass['result'] = "4"


    log_event = u"用户修改密码"
    res_key = str(result_pass['result'])
    log = logging.getLogger("audit")
    log.debug("%s %s %s %s",  \
            request.session['ip'],  request.session['user_name'],  \
            log_event,  log_msg[res_key]) 

    
    result_pass_json = simplejson.dumps(result_pass)
    return HttpResponse(result_pass_json,  mimetype = 'application/json')


