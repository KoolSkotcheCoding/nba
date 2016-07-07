#scripts for plotting NBA movements

import numpy as np
from scipy import integrate
import sys
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
import nbaPlot

#plot_event - function for creating animated plots of nba movement data.
#EventDF - Pandas multiindex dataframe. 
#       Will plot trajectories assuming top level of playerid and second levels labeled 'x','y','z'
#players - list of playerids indicating which columns in EventDF to plot. 
#trajectory - boolean. True to plots trajectories ('tails') of points. False to only "current" location.
#threeD - True to plot in 3D, False to plot in 2D
#saveFile - string name of mp4 file of animated plot. (MUST END in '.mp4' 
#       Leaving blank will not save video; dramatically reducing runtime.


    
def plot_event(eventDF,players=None,trajectory=False,threeD=True,saveFile=None):
    if players is not None and players is not False:
        fig = plt.figure()
        if threeD is True:
            ax = fig.add_axes([0, 0, 1, 1], projection='3d')
            nbaPlot.draw_court(ax)
        else:
            ax = fig.add_axes([0, 0, 1, 1])


        #ax.set_axis_bgcolor('black')
        colors = plt.cm.jet(np.linspace(0, 1, len(players)))
        lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
        pts = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])

        def init():
            for line, pt in zip(lines, pts):
                line.set_data([], [])
                pt.set_data([], [])
                if threeD is True:
                    line.set_3d_properties([])
                    pt.set_3d_properties([])
            if trajectory is True:
                return lines + pts
            else:
                return pts
        
            
        def animate(i):
            for line, pt, player in zip(lines,pts,players):
                x=eventDF[(player,'x')][:i].tolist()
                y=eventDF[(player,'y')][:i].tolist()
                pt.set_data(x[-1:], y[-1:])

                if threeD is True:
                    if player==-1:
                        z=eventDF[(player,'z')][:i].tolist()
                    else:
                        z=[0 for i in range(len(x))]
                    pt.set_3d_properties(z[-1:])

                if trajectory is True:
                    line.set_data(x, y)
                    if threeD is True:
                        line.set_3d_properties(z)
                    
            fig.canvas.draw()
            if trajectory is True:
                return lines + pts
            else: 
                return pts

        ax.set_xlim((-5, 100))
        ax.set_ylim((-5, 55))
        if threeD is True:
            ax.set_zlim((0, 15))

        anim = animation.FuncAnimation(fig, animate, init_func=init,frames=eventDF.shape[0], interval=200, blit=True)
       
        if saveFile is not None and saveFile is not False:
            anim.save(saveFile, fps=20, extra_args=['-vcodec', 'libx264'])

        plt.show()
