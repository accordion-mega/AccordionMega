from pk.povray.sdl import *
from pkpov import Scene, camera, light, plane

#camera.location=(4, .4, 0)
#camera.look_at=(0, .4, 0)

WIDTH = .6
HEIGHT = .3
FRAMES = 128
ROT_OFFSET = -135
ROT_RANGE = 270


white = Pigment(color=(1,1,1))
red = Pigment(color=(1, 0, 0))
real_white = Pigment(color=(1.3, 1.3, 1.3))

boot = Cone((0, 0, 0), WIDTH*1.2, (0, HEIGHT, 0), WIDTH,
            white)

sphere = Sphere((0, 0, 0), WIDTH, white,
                translate=Vector(0, 1, 0),
                scale=Vector(1, HEIGHT*.95, 1),
                )

IN_WIDTH = .1
in_trunk = Cylinder((0, HEIGHT, WIDTH), (0, HEIGHT, 0), .1,
                    real_white)
in_end1 = Sphere((0, HEIGHT, 0), IN_WIDTH)
in_end2 = Sphere((0, HEIGHT, 0), IN_WIDTH,
                 translate=(0, 0, WIDTH))
indicator = Union(in_trunk, in_end1, in_end2,
                  real_white,
                  rotate=(4, 0, 0),
                  translate=(0, .125, -.1),
                  )

knob = Union(boot, indicator, sphere,
             white,
             translate=(0, -.1, 0),
             )

RULER_WIDTH = WIDTH * 1.3
RULER_HEIGHT = 0.03

ruler_base = Cylinder((0, 0, 0), (0, RULER_HEIGHT, 0), RULER_WIDTH,
                      real_white)


ruler_tick = Box((-.04, 0, 0), (.04, RULER_HEIGHT, RULER_WIDTH),
                 real_white)

def tick_deg(skip):
    deg = 0
    while True:
       yield deg
       deg += skip

ruler_ticks = []
skip = ROT_RANGE / 10
deggen = tick_deg(skip)

deg = 0
while deg <= ROT_RANGE:
    tick = Box((-.04, 0, 0), (.04, RULER_HEIGHT, RULER_WIDTH),
               real_white,
               rotate=(0, ROT_OFFSET + deg, 0))
    ruler_ticks.append(tick)
    deg = deggen.next()

def rot(self, c): self.rotate=(0, ROT_OFFSET + ROT_RANGE * (c / FRAMES), 0)
knob._timer = rot

scene = Scene((camera, light, plane))
scene.add(knob)
scene.add(ruler_ticks)

if __name__ == '__main__':
    renderer = Renderer()
    renderer.quality=8
    renderer.clock=0
    renderer.start_row=75
    renderer.end_row=123
    renderer.start_col=110
    renderer.end_col=158
    renderer.preview=True
    renderer.pause=True
    renderer.render(scene)
