#!/usr/local/python2.7/bin/python    
#coding:utf-8

import os.path
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.websocket
import json
import os
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

######Django Setting######
sys.path.append('/home/Data/subtitle_play/subtitle_play')
sys.path.append('/home/Data/subtitle_play/subtitle_play/subtitle_play')
os.environ.setdefault("DJANGO_SETTINGS_MODULE",  "subtitle_play.settings")
from subtitle_play.music.models import *
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from tornado.options import define, options

define("port", default=10030, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("<html></html>")

class SocketHandler(tornado.websocket.WebSocketHandler):
    """docstring for SocketHandler"""
    socket_id_map = {"controllor":None, "show":None}

    @staticmethod
    def send_only(p2pClients, message):
        ''' 发送给某个客户端 '''
        print "send_only message = %s" %message
        for p2pClient in p2pClients:
            p2pClient.write_message(json.dumps(message))


    def open(self):        
        try:
            self.write_message(json.dumps({
                'type': 'sys',
                'message': 'Welcome to Subtitle_Play ! id: ' + str(id(self)),
                }))
        except:
            print "open error"


    def on_close(self):
        try:
            self.write_message(json.dumps({
                'type': 'sys',
                'message': 'ByeBye! id: ' + str(id(self)),
                }))
        except:
            print "open error"



    def on_message(self, message):
        print "message = %s" %message
        s = message.split("#@#")
        if len(s) == 2:
            msg_type = s[0] # lyric or mv
            msg_content = s[1]
            msg = {'type' : msg_type,
                   'message' : msg_content,
                  }

            if msg_type in ("lyric", "mv"):
                p2pClients = (SocketHandler.socket_id_map.setdefault("show", None), )
                if p2pClients[0] is None:
                    print "socket_id get error"
                else:
                    SocketHandler.send_only(p2pClients, msg)
                    
            elif msg_type == "register":
                if msg_content in ("controllor", "show"):
                    if msg_content == "controllor":
                        socket_id_map["controllor"] = self
                    else:
                        socket_id_map["show"] = self

                else:
                    print "Register : content is error!"

            else:
                print "msg type is error!"

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/", IndexHandler),
                (r"/chat", SocketHandler)
                ]
        settings = dict(
                #template_path=os.path.join(os.path.dirname(__file__), "templates"),
                #static_path=os.path.join(os.path.dirname(__file__), "static"),
                debug=False,
                )
        tornado.web.Application.__init__(self, handlers, **settings)

##MAIN
if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
