#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# it was from
# http://mattn.kaoriya.net/software/lang/python/20080317103644.htm
#

"""
Lingr API Module
"""
import httplib
import urllib

from urllib import urlencode
from urlparse import urlunparse
import json

__author__ = 'mattn <mattn.jp@gmail.com>'
__url__ = 'http://mattn.kaoriya.net/'
__version__ = "0.01"

"""
Lingr API Class
"""
class LingrAPI:
  """
  initialize class variables and create session.
  """
  def __init__(self, api_key, nickname, password):
    self.api_key = api_key
    self.nickname = nickname
    self.session = None
    self.conn = httplib.HTTPConnection("lingr.com") #www.lingr.com is obsolete

    body = urlencode({'api_key':self.api_key, 'user':nickname, 'password':password})
    self.conn.request('POST', '/api/session/create/', body=body)
    response = self.conn.getresponse()
    data = response.read()
    j = json.loads(data)
    if j['status'] != 'ok':
      raise Exception(j)
    self.session = j['session']

  def enter_room(self, room_id):
    self.room = room_id

  def say(self, message):
    body = urlencode({'api_key':self.api_key, 'session':self.session,'room':self.room, 'nickname':self.nickname, 'text': message})
    self.conn.request('POST', '/api/room/say', body=body)
    response = self.conn.getresponse()
    data = response.read()
    j = json.loads(data)
    if j['status'] != 'ok':
      raise Exception(j)
    return j


#  def find_room(title):
#    self.conn.request('GET', '/search/rooms',
#        body = "query=%s" % urllib.quote(title))
#    response = self.conn.getresponse()
#    data = response.read()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2: sys.exit()
    api_key = sys.argv[1]
    nickname = sys.argv[2]
    room_id = sys.argv[3]
    message = sys.argv[4]

    api = LingrAPI(api_key, nickname)
    api.enter_room(room_id)
    api.say(message)

