from pk.povray.sdl import *
from pkpov import Scene, camera, light, plane
from pkpov import WHITE, GREY, BLACK, MAROON, DRABGREEN, DRABPURPLE


X_SCALE = 1
INDENT = 1.05

def clocked_color(c):
    if c >= 0 and c < 3:
        return WHITE
    elif c >= 3 and c < 6:
        return GREY
    elif c >= 6 and c < 9:
        return BLACK
    elif c >= 9 and c < 12:
        return MAROON
    elif c >= 12 and c < 15:
        return DRABGREEN
    elif c >= 15 and c < 18:
        return DRABPURPLE


button = SuperEllipsoid(.3, .15,
                        pigment=Pigment(color=WHITE),
                        finish=Finish(phong=.3),
                        scale=(X_SCALE, .3, .45),
                        translate=(0, -.1, 0),
                        )

indent = SuperEllipsoid(.3, .15,
                        pigment=Pigment(color=WHITE),
                        scale=(INDENT, 4, .48),
                        )


def color_and_press(self, clock):
    self.pigment = Pigment(color=clocked_color(clock))
    down = -.1 + (-.6 * (clock % 3))
    self.translate = Vector(0, down, 0)
button._timer = color_and_press

button_plane = Difference(plane, indent)

scene = Scene((camera, light))
scene.add(button_plane)
scene.add(button)


if __name__ == '__main__':
    renderer = Renderer()
    renderer.quality=6
    renderer.clock=0.0
    renderer.start_col=99
    renderer.end_col=168
    renderer.start_row=82
    renderer.end_row=119
    renderer.preview=True
    renderer.pause=True
    renderer.pretend=False
    renderer.render(scene)
