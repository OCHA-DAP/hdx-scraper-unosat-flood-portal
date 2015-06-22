#!/bin/bash

#
# Running the script. The latter is for
# having access to the log from an API
# endpoint. The URL can be sent via 
# email notification.
#
source venv/bin/activate
python tool/scripts/example_collect/ > tool/http/log.txt