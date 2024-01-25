import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy

from objloader import *

def calculateBSplinePoint(x,y,z,w,t):
    t = float(t);
    
    tmp1 = numpy.array([(t**3)/6,(t**2)/6,t/6,1/6]);
    #print(tmp1);
    tmp2 = numpy.array([[-1,3,-3,1],[3,-6,3,0],[-3,0,3,0],[1,4,1,0]]);
    #print(tmp2)
    tmp3 = numpy.array([x,y,z,w]);
    #print(tmp3);

    result = numpy.matmul(tmp1, tmp2)
    #print(result)
    result2 = numpy.matmul(result, tmp3);
    #print(result2);
    return result2;


#Postavljanje scene

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)


glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)

# Učitavanje točaka za B-splajn krivulju

f = open("bSpline.txt", "r")
tmp = f.readlines();
bSplinePoints = list();

for elem in tmp:
    elem = elem[:-1];
    result = elem.split(" ");
    for i in range(len(result)):
        result[i] = float(result[i])
    bSplinePoints.append(result);


# Učitavanje objekta s materijalom
obj = OBJ("WoodTexture.obj")
obj.generate()

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
i = 0

# Glavna petlja koja pomiče objekt
print(bSplinePoints);

points = list();
k = 0;
for i in range(len(bSplinePoints)-4):
    for j in range(100):
        k += 1;
        k = k%720;
        
        point = calculateBSplinePoint(bSplinePoints[0+i],bSplinePoints[1+i],bSplinePoints[2+i],bSplinePoints[3+i],j/100) 
        x = point[0];
        y = point[1];
        z = point[2];
        
        clock.tick(200)
    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslate(x, y-4, -z - 3)
        glRotate(k/2, 0, 1, 0)
        obj.render()

        glEnable(GL_POINT_SMOOTH)
        glPointSize(3)

        if j%20 == 0:
            points.append((x,y-4,z-3))


        
        pygame.display.flip()

tmp = 1;
glTranslate(x+3, y-5, z-0.2);

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)


#Iscrtavanje putanje
for elem in points:
    glBegin(GL_POINTS);
    glColor3f(0.5 + 2.5*(elem[2] + 3), 1.0, tmp/len(points))
    glVertex3d(elem[0],elem[1],elem[2])
    clock.tick(50);
    tmp = tmp+1;
    glEnd();
    pygame.display.flip()

#Crtanje 6 tangenta
tmp = int(len(points)/6);
for i in range(len(points)):
    if i%tmp == 0:
        glBegin(GL_LINES);
        glColor3f(1, 0, 1)
        glVertex3f(points[i][0],points[i][1],points[i][2]);
        tmp2 = (points[i+1][0]-points[i][0],points[i+1][1]-points[i][1],points[i+1][2]-points[i][2])
        glVertex3f(points[i][0]+tmp2[0]*5,points[i][1]+tmp2[1]*5,points[i][2]+tmp2[2]*5);
        glEnd();
        pygame.display.flip()
        
