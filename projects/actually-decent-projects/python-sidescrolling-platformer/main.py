from __future__ import annotations

import os

import pygame as pg

from Common.constants import FPS, WINDOW_SIZE, SPRITE_SCALE
from API.helpers import PlatformerBackend, Background
from API.spriting import SpriteSheet
from API.base import BaseTerrain, BaseTerrain

from Content import Player


def main():
    # init pygame backend and window
    pg.init()
    backend = PlatformerBackend(WINDOW_SIZE[0], WINDOW_SIZE[1], caption='Platformer')
    window = backend.window
    backend.set_background(Background(window, 'Assets/Background/Blue.png'))

    # init player
    player = Player(window, 200, 200, 32, 32).set_scale(2)
    player.load_spritesheets(
        SpriteSheet('Assets/MainCharacters/MaskDude/double_jump.png').scale(SPRITE_SCALE).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/fall.png').scale(SPRITE_SCALE).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/hit.png').scale(SPRITE_SCALE).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/idle.png').scale(SPRITE_SCALE).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/jump.png').scale(SPRITE_SCALE).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/run.png').scale(SPRITE_SCALE).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/wall_jump.png').scale(SPRITE_SCALE).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
    ).animate_sprites()
    player.set_animation('idle_RIGHT', 2)
    backend.register(player)

    # init terrain
    for i in range(10):
        terrain = BaseTerrain(window, i * 96, 500, 48, 48)
        terrain.load_spritesheets(
            SpriteSheet.isolate_from('Assets/Terrain/Terrain.png', 0, 0, 48, 48, name='idle').scale(SPRITE_SCALE).to_dict()
        )
        terrain.set_animation('idle')
        backend.register(terrain)

    # adjust player
    player.is_falling = True

    # main game loop
    while backend.is_running:
        # event listener and show background
        backend.clock.tick(FPS)
        backend.listen()
        backend.background.show()

        for entity in backend.REGISTERED_ENTITIES:
            for other in backend.REGISTERED_ENTITIES:
                if entity is other or not entity.has_collision:
                    continue
                
                # collision with terrain
                if entity.overlaps(other) and not isinstance(entity, BaseTerrain) and isinstance(other, BaseTerrain):
                    if entity.is_falling:
                        entity.is_falling = False
                        entity.vel.y = 0
                        entity.acc.y = 0

                    entity.rect.y = other.rect.y - entity.rect.height + 1

                else:
                    entity.is_falling = True
                    
            entity.AI()
            entity.do_physics()
            entity.show(draw_rect=False)

        # update window
        pg.display.update()

    # quit on window quit
    pg.quit()
    quit()



if __name__ == '__main__':
    main()