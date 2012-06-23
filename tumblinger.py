
from external.lingr2 import Session

import sys

if len(sys.argv) < 3: 
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
    s.enter("computer_science")
    s.say("test by python.")

