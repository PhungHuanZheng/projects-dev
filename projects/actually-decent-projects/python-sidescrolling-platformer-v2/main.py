from __future__ import annotations

import os

import pygame as pg

from Platformer.Base import BaseTerrain
from Platformer.Common.constants import FPS
from Platformer.Helpers import Canvas, Background, SpriteSheet

from Content import Player


def main():
    # init backend and window
    canvas = Canvas((1200, 600), 'Platformer', (0, 30))
    canvas.set_background(Background(canvas.window, path='Assets/Background/Blue.png'))

    # init player
    MaskDude = Player(canvas.window, 200, 200, 32, 32).register_spritesheets(spritesheet_dicts=[
        SpriteSheet('Assets/MainCharacters/MaskDude/double_jump.png').animate(32, 32).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/fall.png').animate(32, 32).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/hit.png').animate(32, 32).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/idle.png').animate(32, 32).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/jump.png').animate(32, 32).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/run.png').animate(32, 32).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT']),
        SpriteSheet('Assets/MainCharacters/MaskDude/wall_jump.png').animate(32, 32).to_dict(facing='RIGHT', directions=['LEFT', 'RIGHT'])
    ]).transform_sprites(transformations=[
        (pg.transform.scale_by, [2])
    ])
    MaskDude.set_animation(f'idle_{MaskDude.direction}', interval=2)
    canvas.register(MaskDude)
    MaskDude.is_falling = True

    # init terrain
    BasicBlock = BaseTerrain(canvas.window, 200, 500, 48, 48).register_spritesheets(spritesheet_dicts=[
        SpriteSheet.isolate_from('Assets/Terrain/Terrain.png', 0, 0, 48, 48, name='idle').to_dict()
    ]).transform_sprites(transformations=[
        (pg.transform.scale_by, [2])
    ])
    BasicBlock.set_animation('idle')
    canvas.register(BasicBlock)

    # BasicBlock = BaseTerrain(canvas.window, 296, 500, 48, 48).register_spritesheets(spritesheet_dicts=[
    #     SpriteSheet.isolate_from('Assets/Terrain/Terrain.png', 0, 0, 48, 48, name='idle').to_dict()
    # ]).transform_sprites(transformations=[
    #     (pg.transform.scale_by, [2])
    # ])
    # BasicBlock.set_animation('idle')
    # canvas.register(BasicBlock)

    # BasicBlock = BaseTerrain(canvas.window, 200, 404, 48, 48).register_spritesheets(spritesheet_dicts=[
    #     SpriteSheet.isolate_from('Assets/Terrain/Terrain.png', 0, 0, 48, 48, name='idle').to_dict()
    # ]).transform_sprites(transformations=[
    #     (pg.transform.scale_by, [2])
    # ])
    # BasicBlock.set_animation('idle')
    # canvas.register(BasicBlock)

    # main game loop
    while canvas.is_running:
        # reset background
        canvas.clock.tick(FPS)
        canvas.background.show()

        # listen for events
        canvas.listen(event_ids=[pg.QUIT])
        
        # entity loop
        for entity in canvas.REGISTERED_ENTITIES:

            entity.AI()
            entity.physics()
            entity.tick()
            entity.render()

            for other in canvas.REGISTERED_ENTITIES:
                # ignore if other is self
                if other is entity:
                    continue
                
                collision_point = entity.collided_with(other)
                if collision_point is not None:

                    # get sprite mask collision point as canvas coords
                    collision_point = list(collision_point)
                    collision_point[0] += entity.rect.x
                    collision_point[1] += entity.rect.y
                    
                    # if entity colliding with terrain
                    if not isinstance(entity, BaseTerrain) and isinstance(other, BaseTerrain):
                        print(collision_point)
                        
                        # if collide on top
                        if entity.rect.y + entity.rect.height > other.rect.y: 
                            entity.is_falling = False
                            entity.vel.y = 0
                            entity.rect.y = other.rect.y - entity.rect.height

                        # if collide on the right
                        elif entity.rect.x < other.rect.x + other.rect.width:
                            entity.is_falling = True
                            entity.vel.x = 0
                            entity.rect.x = collision_point[0]

                else:
                    entity.is_falling = True

            # pg.draw.rect(canvas.window, (255, 0, 0), BasicBlock.rect)

        # update display
        canvas.update()


if __name__ == '__main__':
    main()