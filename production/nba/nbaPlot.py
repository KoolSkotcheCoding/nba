import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy
#assumes a 3d-axes obect named ax


#List of issues:
#Line thickness not taken into account when drawing court. 
#Aspect ratio when plotting is schewed (plot appears as a cube despite range of dimensions varying). 

def draw_court(ax):


    full_length=94
    full_height=50
    paintLength=19
    paintHeight=12
    foulHeight=16
    circleRadius=6
    hoopCenter=4.75
    rimHeight=10
    rimDiameter=1.5
    threeCircle=23.75
    threeCorner=22
    threeTheta=math.degrees(math.acos(threeCorner/threeCircle))
    threeCornerLength=14
    threeCornerDepth=3
    lineThickness=0.166
    restrictedZoneRadius=4
    
    court_lines=[]
    
    #outer court
    court_lines.append(Rectangle((0,0),full_length,full_height))
    #'inner' rectangles / 'the paint'
    court_lines.append(Rectangle((0,full_height/2-paintHeight/2),paintLength,paintHeight))
    court_lines.append(Rectangle((full_length-paintLength,full_height/2-paintHeight/2),paintLength,paintHeight))
    #'outer' rectangles / the 'key'
    court_lines.append(Rectangle((0,full_height/2-foulHeight/2),paintLength,foulHeight))
    court_lines.append(Rectangle((full_length-paintLength,full_height/2-foulHeight/2),paintLength,foulHeight))
    #half court circle(s)
    #court_lines.append(Circle((full_length/2,full_height/2),2))
    court_lines.append(Circle((full_length/2,full_height/2),circleRadius))
    #'foul' cirlces/ cirlce which encloses foul line.
    court_lines.append(Circle((paintLength,full_height/2),circleRadius))
    court_lines.append(Circle((full_length-paintLength,full_height/2),circleRadius))
    #3-PT arcs
    court_lines.append(Arc((hoopCenter,full_height/2),threeCircle*2,threeCircle*2,theta1=270+threeTheta,theta2=90-threeTheta))
    court_lines.append(Arc((full_length-hoopCenter,full_height/2),threeCircle*2,threeCircle*2,theta1=90+threeTheta,theta2=270-threeTheta))
    #3-PT corners
    court_lines.append(Rectangle((0,full_height-threeCornerDepth),threeCornerLength,0))
    court_lines.append(Rectangle((0,threeCornerDepth),threeCornerLength,0))
    court_lines.append(Rectangle((full_length-threeCornerLength,full_height-threeCornerDepth),threeCornerLength,0))
    court_lines.append(Rectangle((full_length-threeCornerLength,threeCornerDepth),threeCornerLength,0))
    #restricted zone
    court_lines.append(Arc((hoopCenter,full_height/2),restrictedZoneRadius*2,restrictedZoneRadius*2,theta1=270,theta2=90))
    court_lines.append(Arc((full_length-hoopCenter,full_height/2),restrictedZoneRadius*2,restrictedZoneRadius*2,theta1=90,theta2=270))
    #half-court line
    court_lines.append(Rectangle((full_length/2,0),0,full_height))    
    

    #3D pieces of court
    #rim
    court=[]
    court.append(['rim',Circle((hoopCenter,full_height/2),rimDiameter,facecolor='none')])
    court.append(['rim',Circle((full_length-hoopCenter,full_height/2),rimDiameter,facecolor='none')])
   

 
    for line in court:
        line[1].set_facecolor('none')
        ax.add_patch(line[1])
        if line[0]=='rim':
            art3d.pathpatch_2d_to_3d(line[1], z=10)
   

    for line in court_lines:
        line.set_facecolor('none')
        ax.add_patch(line)
        art3d.pathpatch_2d_to_3d(line, z=0)
        #outer = Rectangle((0,-50), width=94, height=50)
    ax.set_xlim3d(-5, 100)
    ax.set_ylim3d(-5, 55)
    ax.set_zlim3d(0, 10)
    #return poss3D#.canvas.draw()
