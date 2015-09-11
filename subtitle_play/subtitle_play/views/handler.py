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

from common_function import get_ip_address

def __log_test(msg):
    log = logging.getLogger("audit")
    log.debug("SYSTEM SYSTEM LOG_TEST %s", msg)


def config(request):
    return render_to_response("config.html")

def controllor(request):
    return render_to_response("controllor.html")

def show(request):
    return render_to_response("show.html")

def dispatch(request):
    return render_to_response("dispatch.html", \
                                {"IP" : get_ip_address("eth0")})

