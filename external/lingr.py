#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# from
# http://mattn.kaoriya.net/software/lang/python/20080317103644.htm
#

"""
Lingr API Module
"""
import httplib
import urllib
from xml.dom import minidom

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
  def __init__(self, api_key, nickname):
    self.api_key = api_key
    self.nickname = nickname
    self.session = None
    self.conn = httplib.HTTPConnection("www.lingr.com")
    self.conn.request('POST', '/api/session/create/',
        body = "api_key=%s" % urllib.quote(api_key))
    response = self.conn.getresponse()
    data = response.read()
    doc = minidom.parseString(data)
    if doc.getElementsByTagName('status')[0].childNodes[0].data != 'ok':
      raise Exception({
          'code' : doc.getElementsByTagName('code')[0].childNodes[0].data,
          'message' : doc.getElementsByTagName('message')[0].childNodes[0].data})
    self.session = doc.getElementsByTagName('session')[0].childNodes[0].data

  """
  destroy session.
  """
  def __del__(self):
    if self.session:
      import urllib
      from xml.dom import minidom
      self.conn.request('POST', '/api/session/destroy',
          body = "session=%s" % urllib.quote(self.session))
      response = self.conn.getresponse()
      data = response.read()
      doc = minidom.parseString(data)
      if doc.getElementsByTagName('status')[0].childNodes[0].data != 'ok':
        raise Exception({
            'code' : doc.getElementsByTagName('code')[0].childNodes[0].data,
            'message' : doc.getElementsByTagName('message')[0].childNodes[0].data})

  """
  enter room and return room_id
  """
  def enter_room(self, room_id):
    self.conn.request('POST', '/api/room/enter',
        body = "session=%s&id=%s&nickname=%s"
            % (urllib.quote(self.session), urllib.quote(room_id), urllib.quote(self.nickname)))
    response = self.conn.getresponse()
    data = response.read()
    doc = minidom.parseString(data)
    if doc.getElementsByTagName('status')[0].childNodes[0].data != 'ok':
      raise Exception({
          'code' : doc.getElementsByTagName('code')[0].childNodes[0].data,
          'message' : doc.getElementsByTagName('message')[0].childNodes[0].data})
    return doc.getElementsByTagName('ticket')[0].childNodes[0].data

  """
  say message using ticket.
  """
  def say(self, ticket, message):
    self.conn.request('POST', '/api/room/say',
        body = "session=%s&ticket=%s&message=%s"
            % (urllib.quote(self.session), urllib.quote(ticket), urllib.quote(message)))
    response = self.conn.getresponse()
    data = response.read()
    doc = minidom.parseString(data)
    if doc.getElementsByTagName('status')[0].childNodes[0].data != 'ok':
      raise Exception({
          'code' : doc.getElementsByTagName('code')[0].childNodes[0].data,
          'message' : doc.getElementsByTagName('message')[0].childNodes[0].data})
    return doc.getElementsByTagName('occupant_id')[0].childNodes[0].data

  """
  exit room
  """
  def exit_room(self, ticket):
    self.conn.request('POST', '/api/room/exit',
        body = "session=%s&ticket=%s"
            % (urllib.quote(self.session), urllib.quote(ticket)))
    response = self.conn.getresponse()
    data = response.read()
    doc = minidom.parseString(data)
    if doc.getElementsByTagName('status')[0].childNodes[0].data != 'ok':
      raise Exception({
          'code' : doc.getElementsByTagName('code')[0].childNodes[0].data,
          'message' : doc.getElementsByTagName('message')[0].childNodes[0].data})
    return doc.getElementsByTagName('status')[0].childNodes[0].data

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
    ticket = api.enter_room(room_id)
    api.say(ticket, message)
    api.exit_room(ticket)

