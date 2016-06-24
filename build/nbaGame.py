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
import nbaMoment

class NBA_game:
    def __init__(self, rawGame):
	self.rawGame=rawGame
#        self.home=rawGame["events"][0]["home"]
#        self.away=rawGame["events"][0]["visitor"]
#        self.gameDate=rawGame["gamedate"]
#        self.gameID=rawGame["gameid"]
#        self.gameIndex=['gameClock','shotClock','quarter','eventID','-1'+'_x','-1'+'_y','-1'+'_z']
#        for playerID in self.players['playerid']:
#            self.gameIndex.append(str(playerID)+'_x')
#            self.gameIndex.append(str(playerID)+'_y')
#            self.gameIndex.append(str(playerID)+'_z')
#        self.momentCnt=0
#        for event in self.rawGame["events"]:
#            for moment in event["moments"]:
#                if moment:
#                    self.momentCnt+=1
###########################################################################
        self.homePlayers=pd.DataFrame(rawGame["events"][0]["home"]["players"])
        self.awayPlayers=pd.DataFrame(rawGame["events"][0]["visitor"]["players"])

        self.players=self.homePlayers.append(self.awayPlayers,ignore_index=True)
        
    ##getEventData##
    #Returns: a tuple containing True and a Pandas Dataframe if the specified event ID is found in the game.
    #Or False and an empty list if the event ID is not present in the game (or if there are no moments within the specified event ID.
    #Parameters:
        #eventID - Event ID of desired event.
        #ball - optional argument (False by default). True - return ball movement data
        #time - optional argument (False by default). True - return shot clock and gameclock data
        #players - optional argument (False by default). List of player IDs to return. 
            #If a player ID in players is not active in the event (not on the court), that player ID will not be present in the returned dataframe.
            #If a player ID is only active (on the court) for some of the moments within the event, the dataframe will contain a column for the player
            #with Nan values for the moments the player ID is not active. 
    def getEventData(self,eventID,ball=False,time=False,players=False):
        for event in self.rawGame["events"]:
            if event["eventId"]==str(eventID):
                firstMoment=True
                target_event=[]
                for moment in event["moments"]:
                    if moment:
                        if firstMoment:
                            target_event=nbaMoment.NBA_moment(moment,event['eventId'],ball,time,players).momentDF
                            firstMoment=False
                        else:
                            target_event=target_event.append(nbaMoment.NBA_moment(moment,event['eventId'],ball,time,players).momentDF,ignore_index=True)
                if len(target_event)==0:
                    return False,[]
                else:
                    target_event.index.names=['moment']
                    return True,target_event
        return False,[]


    def nearestToBall(self,eventDF):
        eventPlayers=[player for player in  list(eventDF.columns.levels[0]) if player !=-1 and  player !='time' and player !='near ball']
        idx=pd.IndexSlice


        xdist= eventDF.loc[:,idx[eventPlayers,'x']].sub(eventDF[-1,'x'],axis=0,level='moment')**2
        ydist= eventDF.loc[:,idx[eventPlayers,'y']].sub(eventDF[-1,'y'],axis=0,level='moment')**2

        distances=[xdist.loc[:,idx[playerID,'x']].add(ydist.loc[:,idx[playerID,'y']],axis=0,level='moment') 
                for playerID in eventPlayers]

        distance=pd.concat(distances,axis=1,keys=eventPlayers)

        eventDF[('near ball','player')]=distance.idxmin(axis=1)
        eventDF[('near ball','distance')]=distance.loc[:, eventPlayers].min(axis=1).map(np.sqrt).round(2)
        return eventDF
