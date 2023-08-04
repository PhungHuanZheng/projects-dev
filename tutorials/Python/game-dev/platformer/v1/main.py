from __future__ import annotations

import os
import json
import random
import math
import pygame

from helpers.Background import Background
from helpers.Player import Player

# read config file
with open('config.json', 'r') as config:
    config = json.load(config)

    WINDOW_SHAPE = config['window_shape']
    FPS = config['fps']


def main():
    # init pygame backend and window
    pygame.init()
    pygame.display.set_caption("Tutorial Platformer")
    window = pygame.display.set_mode((WINDOW_SHAPE[0], WINDOW_SHAPE[1]))
    clock = pygame.time.Clock()
    is_running = True

    # set up background
    background = Background('assets/Background/Blue.png')
    image, positions = background.tile(window)

    # set up player
    player = Player(100, 100, 50, 50, 'assets/MainCharacters/MaskDude')
    
    # main event loop
    while is_running: 
        clock.tick(FPS)

        # handle events
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    is_running = False
                    break

        # update objects
        player.AI()

        # draw background
        background.show(window, image, positions)
        player.show(window)


    pygame.quit()
    quit()


if __name__ == '__main__':
    main()