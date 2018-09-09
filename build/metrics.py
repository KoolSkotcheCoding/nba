import pandas as pd
import numpy as np
import math
import nbaMoment


def ballHandler(eventDF):
    #grab player IDs
    eventPlayers=[player for player in  list(eventDF.columns.levels[0]) if player !=-1 and  player !='time' and player !='near ball']
    idx=pd.IndexSlice
    #calculate distance from ball to each player
    xdist= eventDF.loc[:,idx[eventPlayers,'x']].sub(eventDF[-1,'x'],axis=0,level='moment')**2
    ydist= eventDF.loc[:,idx[eventPlayers,'y']].sub(eventDF[-1,'y'],axis=0,level='moment')**2
    distances=[xdist.loc[:,idx[playerID,'x']].add(ydist.loc[:,idx[playerID,'y']],axis=0,level='moment')
        for playerID in eventPlayers]
    distance=pd.concat(distances,axis=1,keys=eventPlayers)
    #join distance and ballhandler ID column to entire event dataFrame
    eventDF[('near ball','player')]=distance.idxmin(axis=1)
    eventDF[('near ball','distance')]=distance.loc[:, eventPlayers].min(axis=1).map(np.sqrt).round(2)
    return eventDF

