
from external.lingr2 import Session

import sys

if len(sys.argv) < 3: 
    sys.exit()

config = {}
if len(sys.argv) == 3: 
    config['user']= sys.argv[1]
    config['password']= sys.argv[2]
    config['nickname']= None

else:
    config['user']= sys.argv[1]
    config['password']= sys.argv[2]

Session.api_key = "kzRHJn"

with Session(**config) as s:
    s.enter("computer_science")
    s.say("test by python.")

