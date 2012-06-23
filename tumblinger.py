
from external import lingr2

import sys

if len(sys.argv) < 2: 
    sys.exit()

api_key="kzRHJn"
api = lingr.LingrAPI(api_key, sys.argv[1], sys.argv[2])
api.enter_room("computer_science")
print api.say("test by python.")

