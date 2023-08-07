from __future__ import annotations

import os

import pygame

from _constants import FPS, GRAVITY, VELOCITY, WINDOW_SIZE
from common import BaseEntity
from helpers import SpriteSheet, Background
from content import Player, Block


def main():
    # init pygame backend and related
    pygame.init()
    pygame.display.set_caption("Platformer")
    window = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))
    is_running = True
    clock = pygame.time.Clock()

    # init background
    background = Background(window, 'assets/Background/Blue.png')
    background.tile()

    # init player
    player = Player(window, 100, 100, 32, 32)
    player.load_sprites('assets/MainCharacters/MaskDude', 1, True)
    player.set_animation('idle')
    player.set_animation_interval(2)
    player.register()

    # init terrain
    for i in range(10):
        block = Block(window, i * 48, 500, 48, 48, False)
        block_anim = SpriteSheet('assets/Terrain/Terrain.png').isolate(0, 64, 48, 48)
        block.add_animation('idle', block_anim, directional=True , set_animation=True)
        block.register()

    # main game loop
    while is_running:
        clock.tick(FPS)
        background.show()

        # event listener
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                is_running = False
                break
        
        # update all entity subclass objects
        for entity in BaseEntity.REGISTERED_ENTITIES:
            # handle collisions between entities
            for other in BaseEntity.REGISTERED_ENTITIES:
                # ignore if checking self
                if entity is other:
                    continue

                if entity.overlaps(other):
                    entity._is_falling = False

            entity.AI()
            entity.show()

        pygame.display.update()

    pygame.quit()
    quit()
    

if __name__ == '__main__':
    main()