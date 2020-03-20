# Author: Gabriel Dinse
# File: animation
# Date: 19/03/2020
# Made with PyCharm

# Standard Library

# Third party modules
import cocos
from cocos.director import director
import pyglet

# Local application imports


class AnimatedLoopSprite(cocos.layer.Layer):
    def __init__(self, images, period, position=(0, 0), loop=True):
        super().__init__()

        animation = pyglet.image.Animation.from_image_sequence(
            images, period, loop=loop)
        sprite = cocos.sprite.Sprite(animation)
        sprite.position = position
        self.add(sprite)


def main():
    director.init(width=1280, height=720, caption="Window Title Example")
    images = [pyglet.image.load("sprites/" + str(i) + ".png") for i in range(10)]
    numbers1 = AnimatedLoopSprite(images, 0.5, position=(500, 300))
    numbers2 = AnimatedLoopSprite(images, 0.1, position=(525, 300))

    scene = cocos.scene.Scene()
    scene.add(numbers1, 1)
    scene.add(numbers2, 1)
    director.run(scene)


if __name__ == "__main__":
    main()