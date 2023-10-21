from __future__ import annotations

import os
import sys
from importlib import reload

import pygame as pg

sys.path.insert(0, '../../../../projects-dev')
import pyutils; reload(pyutils)

from pyutils.gamedev.twoD.spriting import SpriteSheet
from pyutils.gamedev.twoD.canvas import Canvas


def main():
    # init canvas and background
    canvas = Canvas(800, 600, framerate=60, title='Platformer')
    canvas.set_background('Assets/Background/Blue.png')
    window = canvas.window

    # init player
    ss = SpriteSheet('Assets/MainCharacters/MaskDude/idle.png') \
                    .animate(32, 32, 'HORIZONTAL') 
    print(ss.to_dict(directional=True, facing='RIGHT'))

    # main game loop
    while canvas.is_running:
        canvas.clock.tick(60)
        canvas.listen_for(events=None)
        canvas.clear()

        ss.display_on(window, (0, 0), interval=1)

        canvas.update()

if __name__ == '__main__':
    main()