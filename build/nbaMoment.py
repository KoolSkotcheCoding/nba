import math
import pandas as pd
class NBA_moment:
    def __init__(self,rawMoment,eventID,ball=False,time=False,playerList=None):#,home,away):
        self.quarter=rawMoment[0]
        if rawMoment:
            self.momentDict={}
            self.momentDict['gameClock']=rawMoment[2]
            self.momentDict['shotClock']=rawMoment[3]
        
        
        
            #collect player and ball positions into dictionary with indices (playerID,'x') where x indicates the x position.
            if ball is False and time is False and playerList is False:
                for player in rawMoment[5]:
                    if player[1]==-1:
                        self.momentDict[(player[1],'x')]=round(player[2],2)
                        self.momentDict[(player[1],'y')]=round(player[3],2)
                        self.momentDict[(player[1],'z')]=round(player[4],2)
            else:
                if playerList is not None:
                    for player in rawMoment[5]:
                        if player[1] in playerList.values:
                            self.momentDict[(player[1],'x')]=round(player[2],2)
                            self.momentDict[(player[1],'y')]=round(player[3],2)
                        elif player[1]==-1:
                            self.momentDict[(player[1],'x')]=round(player[2],2)
                            self.momentDict[(player[1],'y')]=round(player[3],2)
                            self.momentDict[(player[1],'z')]=round(player[4],2)
                
                
            self.momentDF=pd.DataFrame(self.momentDict, index=[0])
