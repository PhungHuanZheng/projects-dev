from __future__ import annotations

import os
import json
import random
import math
import pygame

from base import BaseEntity
from constants import FPS, VELOCITY, GRAVITY, WINDOW_SHAPE
from classes.Background import Background
from classes.Player import Player
from classes.Block import Block


def main():
    # init pygame backend and related
    pygame.init()
    pygame.display.set_caption("Tutorial Platformer")
    window = pygame.display.set_mode((WINDOW_SHAPE[0], WINDOW_SHAPE[1]))
    clock = pygame.time.Clock()
    is_running = True

    # set up background
    background = Background(window, asset_path='../assets/Background/Blue.png')
    background.tile()

    # set up player
    player = Player(window, 100, 100, 32, 32)
    player.load_spritesheet(path='../assets/MainCharacters/MaskDude', 
                        width=32, height=32, 
                        scale=2, directional=True)
    player.set_animation('run')
    player.set_update_rate(0.5)

    # set up terrain
    block = Block(window, 200, 200, 96, 96)
    block.partition_spritesheet('../assets/Terrain/Terrain.png', 0, 0, 48, 48, 1, False)
    block.set_animation('aaa')

    # main game loop
    while is_running:
        clock.tick(FPS)
        background.show()

        # handle events
        for event in pygame.event.get():
            # quit event 
            if event.type == pygame.QUIT:
                is_running = False
                break

        # render all entities
        for _, entity in locals().items():
            if isinstance(entity, BaseEntity):
                entity.AI()
                entity.show()

        pygame.display.update()

    # loop breaks, game loop ends
    pygame.quit()
    quit()



if __name__ == '__main__':
    main()