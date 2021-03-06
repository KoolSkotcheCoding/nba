#scripts for plotting NBA movements

import numpy as np
from scipy import integrate
import sys
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
import nbaPlot


def ballPlot_3D(tempPoss):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    nbaPlot.draw_court(ax)
    colors = plt.cm.jet(np.linspace(0, 1, 1))
    lines = sum([ax.plot([], [], [], '-', c=c)
                     for c in colors], [])
    pts = sum([ax.plot([], [], [], 'o', c=c)
                   for c in colors], [])
    #eventPlayers=[player for player in  list(tempPoss.columns.levels[0]) if player !='time' and player !='near ball'] 
    #eventPlayers=[-1]
    def init():
        for line, pt in zip(lines, pts):
            line.set_data([], [])
            line.set_3d_properties([])
            pt.set_data([], [])
            pt.set_3d_properties([])
        return lines + pts

    def animate(i):
        for line, pt in zip(lines,pts):
        #for line, pt, player in zip(lines,pts,eventPlayers):
            #print(player)
            x=tempPoss[(-1,'x')][:i].tolist()
            y=tempPoss[(-1,'y')][:i].tolist()
            line.set_data(x, y)
            z=[0 for i in range(len(x))]
            #z=tempPoss[(-1,'z')][:i].tolist()
            pt.set_data(x[-1:], y[-1:])
            #if player==-1:
            #z=tempPoss[(player,'z')][:i].tolist()
            #else:
            #    z=[0]
            line.set_3d_properties(z)
            pt.set_3d_properties(z[-1:])
            fig.canvas.draw()
        return lines + pts
    
    ax.set_xlim((-5, 100))
    ax.set_ylim((-5, 55))
    ax.set_zlim((0, 15))
    
    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=tempPoss.shape[0], interval=200, blit=True)

    #anim.save('lorentz_factractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

    plt.show()


