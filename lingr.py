#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib
from urllib import urlencode
import json

'''
    ToDo(?)
    support message removal.
    there is no offical api for it.
    #http://lingr.com/room/computer_science/archives/2012/06-23#message-10303741
'''

HOST = "lingr.com"

class Session:
    api_key = None

    #https://github.com/lingr/lingr/wiki/Lingr-API
    mappings = {
            "api_session_create":"/api/session/create",
            "api_session_verify":"/api/session/verify",
            "api_session_destroy":"/api/session/destroy",
            "api_room_show":"/api/room/show",
            "api_room_get_archives":"/api/room/get_archives",
            "api_room_subscribe":"/api/room/subscribe",
            "api_room_unsubscribe":"/api/room/unsubscribe",
            "api_room_say":"/api/room/say",
            "api_user_get_rooms":"/api/user/get_rooms"}

    def __init__(self, user, password, nickname=None):
        '''
            Lingr ignores nickname!
        '''
        assert self.api_key
        self.conn = None
        self.user = user
        self.password = password

        self.values = {}
        if nickname:
            self.values["nickname"] = nickname
        else:
            self.values["nickname"] = user
        self.values['api_key'] = self.api_key

    def param(self, kw):
        d = {}
        d.update(self.values)
        d.update(kw)
        return d

    def __getattr__(self, name):
        assert name in self.mappings
        def handler(**args):
            self.conn.request('POST', self.mappings[name], urlencode(self.param(args)))
            res = self.conn.getresponse()
            d = res.read()
            j = json.loads(d)
            if j['status'] != 'ok':
                raise Exception(j)
            return j
        return handler

    def connect(self):
        self.conn = httplib.HTTPConnection(HOST)
        j = self.api_session_create(user=self.user, password=self.password)
        self.values['session']=j['session']
        return self

    def disconnect(self):
        self.conn.close() #?!

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.disconnect()

    def enter(self, room):
        self.values['room'] = room

    def say(self, text):
        return self.api_room_say(text=text)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        sys.exit()
    Session.api_key="kzRHJn"
    with Session(sys.argv[1], sys.argv[2]) as s:
        s.enter("computer_science")
        s.say("test, by lingr2.py in python.")

