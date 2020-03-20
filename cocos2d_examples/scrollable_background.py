# Author: Gabriel Dinse
# File: scrollable_background
# Date: 19/03/2020
# Made with PyCharm

# Standard Library
import os

# Third party modules
import cocos
from cocos.director import director
import pyglet
from pyglet.window import key

# Local application imports

# Global variables
keyboard = key.KeyStateHandler()
scroller = cocos.layer.ScrollingManager()


class Mover(cocos.actions.Move):
    def __init__(self, acceleration_rate, gravity=0, friction_rate=(0, 0)):
        super().__init__()

        self.acceleration_rate = acceleration_rate
        self.friction_rate = friction_rate
        self.gravity = gravity


    def step(self, dt):
        super().step(dt)

        acceleration_x = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * \
                         self.acceleration_rate[0]
        acceleration_y = (keyboard[key.UP] - keyboard[key.DOWN]) * \
                         self.acceleration_rate[1]
        velocity_x = self.target.velocity[0]
        velocity_y = self.target.velocity[1]
        friction_x = velocity_x * self.friction_rate[0]
        friction_y = velocity_y * self.friction_rate[1]
        velocity_y += -self.gravity * dt
        self.target.velocity = (velocity_x, velocity_y)
        self.target.acceleration = (acceleration_x - friction_x,
                                    acceleration_y - friction_y)
        scroller.set_focus(self.target.x, self.target.y)


class Background(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        self.add(cocos.sprite.Sprite("sprites/background-day.png"))


class AnimatedLoopSprite(cocos.layer.Layer):
    def __init__(self, images, period, position=(0, 0), velocity=(0, 0),
                 loop=True):
        super().__init__()

        animation = pyglet.image.Animation.from_image_sequence(
            images, period, loop=loop)
        sprite = cocos.sprite.Sprite(animation)
        sprite.position = position
        sprite.velocity = velocity
        sprite.do(Mover((3000, 3000), gravity=0, friction_rate=(5, 5)))
        self.add(sprite)


def main():
    director.init(width=288, height=512, caption="Window Title Example")
    window_size = director.get_window_size()
    director.window.pop_handlers()
    director.window.push_handlers(keyboard)

    filepath = "sprites/bird"
    images = [pyglet.image.load(os.path.join(filepath, filename)) for
              filename in os.listdir(filepath)]
    bird = AnimatedLoopSprite(
        images, 0.05, position=(window_size[0] / 2, window_size[1] / 2))

    background = Background()

    scroller.add(background)

    scene = cocos.scene.Scene()
    scene.add(bird, 1)
    scene.add(scroller, 0)
    director.run(scene)


if __name__ == "__main__":
    main()
