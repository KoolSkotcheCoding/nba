#The NBA_moment class is meant to be a tool for working with single 'moments' within the movement JSON files provided by the NBA.

#Expected JSON structure
#A 'moments' contains (quarter, ?, game clock (seconds), shot clock (seconds),?, player+ball position)
#Shot clock can be empty (none, nonetype, etc.).
#player+ball position contains: (team ID, player ID, x coordinate, y coordinate, z coordinate).
#For ball, team ID = -1, player ID = -1, z coordinate is physically meaningful.
#For players, z position is always zero. 


import math
import pandas as pd
class NBA_moment:
    def __init__(self,rawMoment,eventID,ball=False,time=False,playerList=None):#,home,away):
        self.quarter=rawMoment[0]
#collect player and ball positions into dictionary with indices (playerID,'x') where x indicates the x position.
        if rawMoment:
            self.momentDict={}
            if time is not False:
                self.momentDict['gameClock']=rawMoment[2]
                self.momentDict['shotClock']=rawMoment[3]
            if ball is not False or playerList is not False:
                for player in rawMoment[5]:
                    if player[1]==-1 and ball is True:
                        self.momentDict[(player[1],'x')]=round(player[2],2)
                        self.momentDict[(player[1],'y')]=round(player[3],2)
                        self.momentDict[(player[1],'z')]=round(player[4],2)
                    elif playerList is not None and playerList is not False:
                        if player[1] in playerList.values:
                            self.momentDict[(player[1],'x')]=round(player[2],2)
                            self.momentDict[(player[1],'y')]=round(player[3],2)
            self.momentDF=pd.DataFrame(self.momentDict, index=[0])
