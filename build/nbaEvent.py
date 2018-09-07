import pandas as pd
import numpy as np
import nbaGame
import nbaMoment

class nba_event:
    def __init__(self,eventID,nbaGame):
        self.gameID=nbaGame.gameID
        firstMoment=False
        for event in nbaGame.rawGame["events"]:
            if event["eventId"]==str(eventID):
                for moment in event["moments"]:
                    if moment:
                        if firstMoment==False:
                            firstMoment=True
                            self.momentDF=nbaMoment.NBA_moment(moment,event['eventId'],True,True,nbaGame.players).momentDF
                        else:
                            self.momentDF=self.momentDF.append(nbaMoment.NBA_moment(moment,event['eventId'],True,True,nbaGame.players).momentDF,ignore_index=True)
                break

        self.players=[player for player in  list(self.momentDF.columns.levels[0]) if player !='time' and player !='near ball']


    
        self.playByplay=False
        for event in nbaGame.rawPlaybyPlay['resultSets'][0]['rowSet']:
            print event[1]
            if event[1]==eventID:
                self.playByplay=event
                break
