
from external.lingr2 import Session

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

with Session(**config) as s:
    to_remove = []
    s.enter("computer_science")
    s.enter("bgnori")
    for i in range(4, len(sys.argv)):
        j = s.say(sys.argv[i])
        to_remove.append(j['message']['id'])

