
from lingr import Session
from pyblr import Pyblr

from oauth2 import Client, Consumer, Token
import yaml
import sys



if len(sys.argv) < 3: 
    print 'need user and password'
    sys.exit()

config = {}
config['user']= sys.argv[1]
config['password']= sys.argv[2]

if len(sys.argv) == 3: 
    config['nickname']= None
else:
    config['nickname']= sys.argv[3]

Session.api_key = "kzRHJn"

with open("tumblr-oauth.txt") as f:
    d = yaml.load(f)
    client = Client(Consumer(d["consumer_key"], d["consumer_secret"]), Token(d["user_key"], d["user_secret"]))
    t = Pyblr(client)

    with Session(**config) as s:
        to_remove = []
        s.enter("bgnori")
    
        j = t.posts('bgnori.tumblr.com')
        for post in reversed(j['posts']):
            if 'photos' in post:
                for x in post['photos']:
                    s.say(x['original_size']['url'])

