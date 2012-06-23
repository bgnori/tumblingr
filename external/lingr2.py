#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib
from urllib import urlencode
import json


HOST = "lingr.com"


class Session:
    api_key = None
    def __init__(self, user, password, nickname=None):
        assert self.api_key
        self.conn = None
        self.user = user
        self.password = password
        if nickname:
            self.nickname = nickname
        else:
            self.nickname = user

    def request(self, action, body):
        self.conn.request('POST', action, body)
        res = self.conn.getresponse()
        d = res.read()
        j = json.loads(d)
        if j['status'] != 'ok':
            raise Exception(j)
        return j

    def connect(self):
        self.conn = httplib.HTTPConnection(HOST)
        body = urlencode({'api_key':self.api_key, 'user':self.user, 'password':self.password})
        j = self.request('/api/session/create/', body=body)
        self.session = j['session']
        return self

    def disconnect(self):
        self.conn.close() #?!

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.disconnect()

    def enter(self, room):
        self.room = room

    def say(self, text):
        body = urlencode({'api_key':self.api_key, 'session':self.session,'room':self.room, 'nickname':self.nickname, 'text': text})
        j = self.request('/api/room/say', body=body)
        return j


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        sys.exit()
    Session.api_key="kzRHJn"
    with Session(sys.argv[1], sys.argv[2]) as s:
        s.enter("computer_science")
        s.say("test, by lingr2.py in python.")

