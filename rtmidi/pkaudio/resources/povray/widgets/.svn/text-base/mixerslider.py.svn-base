from pk.povray.sdl import *
import pkpov

HEIGHT = 3.1
WIDTH_SCALE = 1.75
GRIP_SPLINES = 10
RANGE = HEIGHT - .8

indent = SuperEllipsoid(.1, .1,
                        pigment=Pigment(color=pkpov.WHITE),
                        scale=Vector(.4 * WIDTH_SCALE, .07, 3.1),
                        )

groove = Box((-.08, -.2, HEIGHT - .45),
             (0.08, 1, -HEIGHT + .45),
             pigment=Pigment(color=pkpov.BLACK),
             )

mixer_plane = Difference(pkpov.plane, indent, groove)

cutout_body = Cylinder((-1, .6, 0),
                       (1, .6, 0),
                       .5,
                       pigment=Pigment(color=pkpov.BLACK))

inc = 360.0 / GRIP_SPLINES
splines = []
for i in range(GRIP_SPLINES):
    spline = Cylinder((-1, 0, -.5),
                      (1, 0, -.5),
                      .05,
                      pigment=Pigment(color=(1.5, 1.5, 1.5)),
                      rotate='x * -%i' % ((i * inc) + 20),
                      )
    splines.append(spline)

splines = Union(*tuple(splines))
splines.translate  = Vector(0, .6, 0)

grip_cutout = Union(cutout_body, splines)
grip_cutout.scale=(1, 1, 1.2)


grip_body = SuperEllipsoid(.3, .2,
                           scale=Vector(.4 * WIDTH_SCALE, .3, .7),
                           pigment=Pigment(color=pkpov.BLACK),
                           )

grip = Difference(grip_body,
                  grip_cutout,
                  finish='{ phong 1 }',
                  translate=Vector(0, 0, 0),
                  )
def slide(grip, clock):
    z = (RANGE * 2) * (clock / 127.0) - RANGE
    grip.translate = (0, 0, z)
grip._timer = slide

#camera = Camera(location=(-5, .6, -1),
#                look_at=(0, 1, -1),)
#                angle=36)
camera = pkpov.camera
scene = pkpov.Scene((camera, pkpov.light, mixer_plane))
scene.add(grip)

if __name__ == '__main__':
    renderer = Renderer()
    renderer.quality=11
    renderer.clock=127.0
    renderer.start_col=107
    renderer.end_col=160
    renderer.start_row=12
    renderer.end_row=190
    renderer.preview=True
    renderer.pause=True
    renderer.pretend=False
    renderer.render(scene)
