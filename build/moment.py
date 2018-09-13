#The NBA_moment class is meant to be a tool for working with single 'moments' within the movement JSON files provided by the NBA.

#Expected JSON structure
#A 'moments' contains (quarter, ?, game clock (seconds), shot clock (seconds),?, player+ball position)
#Shot clock can be empty (none, nonetype, etc.).
#player+ball position contains: (team ID, player ID, x coordinate, y coordinate, z coordinate).
#For ball, team ID = -1, player ID = -1, z coordinate is physically meaningful.
#For players, z position is always zero. 


import math
import pandas as pd
class moment:
    def __init__(self,rawMoment,eventID):
        self.quarter=rawMoment[0]
        if rawMoment:
            self.momentDict={}
            self.momentDict['gameClock']=rawMoment[2]
            self.momentDict['shotClock']=rawMoment[3]
            for player in rawMoment[5]:
                if player[1]==-1:
                    self.momentDict[player[1]]=(round(player[2],2),round(player[3],2),round(player[4],2))
                else:
                    self.momentDict[player[1]]=(round(player[2],2),round(player[3],2))
            self.momentDF=pd.DataFrame(self.momentDict,index=[0])
        else:
            self.momentDF=False
