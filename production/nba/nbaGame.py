#moments
#contains (quarter, ?, game clock (seconds), shot clock (seconds),
#          ?, player+ball position===position)

#shot clock can be empty (none, nonetype, etc.)
#position contains: (team ID, player ID, x position, y position, z position)

#For ball, team ID = -1, player ID = -1, z position could be physically meaningful
#For players, z position is always zero. 
import pandas as pd
import nbaMoment

class NBA_game:
    def __init__(self, rawGame):
	self.rawGame=rawGame
        self.home=rawGame["events"][0]["home"]
        self.away=rawGame["events"][0]["visitor"]
        self.gameDate=rawGame["gamedate"]
        self.gameID=rawGame["gameid"]
        
        self.homePlayers=pd.DataFrame(rawGame["events"][0]["home"]["players"])
        self.awayPlayers=pd.DataFrame(rawGame["events"][0]["visitor"]["players"])

        self.players=self.homePlayers.append(self.awayPlayers,ignore_index=True)
        
        self.gameIndex=['gameClock','shotClock','quarter','eventID','-1'+'_x','-1'+'_y','-1'+'_z']
        for playerID in self.players['playerid']:
            self.gameIndex.append(str(playerID)+'_x')
            self.gameIndex.append(str(playerID)+'_y')
            self.gameIndex.append(str(playerID)+'_z')
        
	
	        
        
        
        self.momentCnt=0
        for event in self.rawGame["events"]:
            for moment in event["moments"]:
                if moment:
                    self.momentCnt+=1
        
    def getEventData(self,eventID,ball=False,time=False,players=False):
        for event in self.rawGame["events"]:
            emptyMom=False
            if event["eventId"]==str(eventID):
                tmp=0
                target_event=[]
                for moment in event["moments"]:
                    if moment:
                        if tmp==0:
                            target_event=nbaMoment.NBA_moment(moment,event['eventId'],ball,time,playerList=players).momentDF
                            tmp+=1
                        else:
                            target_event=target_event.append(nbaMoment.NBA_moment(moment,event['eventId'],ball,time,playerList=players).momentDF,ignore_index=True)
                            tmp+=1
                if len(target_event)==0:
                    return False,[]
                else:
                    return True,target_event
        return False,[]





    def getEvent(self,eventID):
	for event in self.rawGame["events"]:
            #print event["eventId"]
            emptyMom=False
	    if event["eventId"]==str(eventID):
		tmp=0
                target_event=[]
		for moment in event["moments"]:
		    if moment:
		        if tmp==0:
			    target_event=nbaMoment.NBA_moment(moment,event['eventId'],playerList=self.players['playerid']).momentDF
			    tmp+=1
                        else:
                            target_event=target_event.append(nbaMoment.NBA_moment(moment,event['eventId'],playerList=self.players).momentDF,ignore_index=True)
			    tmp+=1
                if len(target_event)==0:
                    return False,[]
                else:
                    return True,target_event
        return False,[]

def timeElapsed(event):
    return event[:][['gameClock','shotClock']]
