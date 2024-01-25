import random
import sys
from pyglet.gl import *
from pyglet import graphics
from pyglet import window


MAX_CESTICA = 5000
if len(sys.argv) > 1:
    MAX_CESTICA = int(sys.argv[1])
GRAVITACIJA = -120


def dodaj_cestice(r, g, b, x):
    global direction;
    
    cestica = batch.add(1, GL_POINTS, None,
                         ('v2f/stream', [win.width / 2 + x, xmove]), ('c3B', (r,g,b)))
    cestica.dx = (random.random() - .5) * win.width / 4
    cestica.dy = win.height * (.5 + random.random() * .2)
    cestica.dead = False
    cestica.dir = direction
    cestice.append(cestica)


def refresh(dt):
    global cestice
    global xmove;
    global direction;

    xmove += 0.2;
    xmove = xmove%500;
    if xmove < 250:
        direction = 1;
    else:
        direction = -1;
    
    for cestica in cestice:
        cestica.dy += GRAVITACIJA * dt
        cestica.dx += cestica.dir*1.2;
        vertices = cestica.vertices
        vertices[0] += cestica.dx * dt / 2
        vertices[1] += cestica.dy * dt / 2
        if vertices[1] <= 0:
            cestica.delete()
            cestica.dead = True
         
    cestice = [p for p in cestice if not p.dead]


def loop(dt):
    refresh(dt)
    if MAX_CESTICA - len(cestice) > 0:
        dodaj_cestice(int(random.random()*255),
                       int(random.random()*255),
                       int(random.random()*255), 0);
        dodaj_cestice(255,0,0,50);
        dodaj_cestice(0,0,255,-50);
        

win = window.Window(vsync=False)
batch = graphics.Batch()
cestice = list()
xmove = 0;
direction = 1;


@win.event
def on_draw():
    win.clear()
    batch.draw()

clock = pyglet.app.event_loop.clock
clock.schedule(loop)
pyglet.app.run()
