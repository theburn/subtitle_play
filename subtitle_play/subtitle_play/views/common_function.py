from django.contrib.auth import *
from django.contrib.auth.models  import User,  Group
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse,  HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context
from subtitle_play import settings
from django.template import RequestContext
from subtitle_play.music.models import *
import chardet

import socket
import fcntl
import struct
 
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                        0x8915,  # SIOCGIFADDR
                                        struct.pack('256s', ifname[:15])
                            )[20:24])



def check_music_is_exists(music_name):
    try:
        music_instance = Music.objects.get(music_name = music_name)
        return True
    except:
        return False



def check_mv_is_exists(mv_name):
    try:
        mv_instance = MV_Template.objects.get(mv_name = mv_name)
        return True
    except:
        return False


def check_subtitle_is_exists(subtitle_name):
    try:
        subtitle_instance = Subtitle_Template.objects.get(subtitle_name = subtitle_name)
        return True
    except:
        return False



def get_file_encoding(subtitle_instance):
    f=subtitle_instance.subtitle_file_location.file
    f_encoding = None
    try:
        data = f.read()
        f_encoding = chardet.detect(data)["encoding"]
    except:
        pass

    return f_encoding



