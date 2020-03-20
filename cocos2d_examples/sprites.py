# Author: Gabriel Dinse
# File: sprites
# Date: 19/03/2020
# Made with PyCharm

# Standard Library

# Third party modules
import cocos
from cocos.director import director
import pyglet

# Local application imports


class Sprite1(cocos.layer.Layer):
    def __init__(self, filename, position=(0, 0)):
        super().__init__()

        sprite = cocos.sprite.Sprite(filename)
        sprite.position = position
        self.add(sprite)


def main():
    director.init(width=1280, height=720, caption="Window Title Example")
    sprite1 = Sprite1("sprites/bird/bluebird-midflap.png", position=(640, 360))
    sprite2 = Sprite1("sprites/background-day.png", position=(500, 360))
    scene = cocos.scene.Scene()
    scene.add(sprite1, 1)
    scene.add(sprite2, 0)
    director.run(scene)


if __name__ == "__main__":
    main()
