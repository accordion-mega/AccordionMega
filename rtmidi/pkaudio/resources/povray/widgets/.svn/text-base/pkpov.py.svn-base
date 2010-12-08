import os
from pk.povray.sdl import *

WHITE = Vector(1, 1, 1)
GREY = Vector(.8, .8, .8)
BLACK = Vector(.35, .35, .35)
MAROON = Vector(.65, .35, .35)
DRABGREEN = Vector(.35, .47, .35)
DRABPURPLE = Vector(.45, .45, .73)

light = LightSource((-600, 900, 600),
                    area_light='<700, 0, 0>, <0, 0, 700>, 8, 8',
                    color=(1,1,1),
                    fade_distance=100)

camera = Camera(location=(0, 15, 0),
                look_at=(0, 0, 0),
                angle=36)

plane = Plane('y', 0,
              Pigment(color=(1, 1, 1)),
              )

HEIGHT = 200
WIDTH = 266

