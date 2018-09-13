#!/usr/bin/python
#test metrics from metrics.py

import sys
import json
sys.path.append('/home/kschuma/nba')
#sys.path.append('/home/keith/nba')
import build

with open('/home/kschuma/nba/data/trimmedVU.json') as data_file:
    data=json.load(data_file)
exampleGame=build.NBA_game(data)
recievedPossession,exampleEvent=exampleGame.getEventData(3,ball=True,time=True,players=exampleGame.players)
if not recievedPossession:
    print 'invalid event ID'
print exampleEvent.head()
