#The NBA_game class is meant to be a tool for working with the movement JSON files provided by the NBA.
#The movement JSON files conain a series of 'events'. Each 'event' contains a series of 'moments'.
#Each moment is a snapshot of an NBA game at a given time (shot clock and game clock), containing locations of the ball and all players. 
#An 'event' represents a sequence of moments. I am still unsure of the exact meaning of a an 'event'. 
#However, an event is not always:
    #a (basketball) possession. There are events consisting of a shot by team A, rebound by team B, made shot by team B (2 possessions). 
    #'unique'. Some events seem to overlap in the sense that a chronological ordering of all moments in all events would 'shuffle' the events.
        #(in other words, the union between game times contained any event with any other event is not necessarily null).
        #Due to data quality issues (to be further explored), a chronological ordering of all moments within a game is not advisiable.
        #Thus (for the time being) the event-moment structure provided by the NBA is essentially respected/maintaned by this NBA_game class.
#Initialize: To instantiate, call class with output of json.load(movementFileFromNBA.json)


#Expected JSON structure
#A 'moments' contains (quarter, ?, game clock (seconds), shot clock (seconds),?, player+ball position)
#Shot clock can be empty (none, nonetype, etc.).
#player+ball position contains: (team ID, player ID, x coordinate, y coordinate, z coordinate).
#For ball, team ID = -1, player ID = -1, z coordinate is physically meaningful.
#For players, z position is always zero. 
import pandas as pd
import numpy as np
import math
from moment import moment

class game:
    def __init__(self, rawGame,playByplay=False):
	self.rawGame=rawGame
        self.rawPlaybyPlay=playByplay
        self.home=rawGame["events"][0]["home"]
#        self.away=rawGame["events"][0]["visitor"]
#        self.gameDate=rawGame["gamedate"]
        self.gameID=rawGame["gameid"]
        
        self.homePlayers=pd.DataFrame(rawGame["events"][0]["home"]["players"])
        self.awayPlayers=pd.DataFrame(rawGame["events"][0]["visitor"]["players"])
        self.players=self.homePlayers.append(self.awayPlayers,ignore_index=True)
        
    ##getEventData##
    #Returns: a Pandas Dataframe if the specified event ID is found in the game, else False if event ID is not valid
    #Parameters:
        #eventID - Event ID of desired event.
    def getEvent(self,eventID):
        for rawEvent in self.rawGame["events"]:
            if rawEvent["eventId"]==str(eventID):
                event=pd.DataFrame()
                i=0
                for rawMoment in rawEvent["moments"]:
                    print i
                    i=i+1
                    if event.empty:
                        event=moment(rawMoment,rawEvent['eventId']).momentDF
                    else:
                        event=event.append(moment(rawMoment,rawEvent['eventId']).momentDF,ignore_index=True)
                event.index.names=['moment']
                return event
        return false
