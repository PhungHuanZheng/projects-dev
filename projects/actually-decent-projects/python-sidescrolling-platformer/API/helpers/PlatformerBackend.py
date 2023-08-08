from __future__ import annotations

import pygame as pg

from API.helpers import Background
from API.base import BaseEntity


class PlatformerBackend:
    def __init__(self, width: int, height: int, caption: str = '') -> None:
        # attribute init
        self.window_width = width
        self.window_height = height
        self.caption = caption

        # create window (pg.Surface)
        pg.display.set_caption(caption)
        self.__window = pg.display.set_mode((width, height))

        # game loop attributes
        self.clock = pg.time.Clock()
        self.is_running = True

        # bind background to window (idk)
        self.background = None

        # game entities
        self.REGISTERED_ENTITIES: list[BaseEntity] = []

    def set_background(self, bg: Background):
        if len(bg._tile_pos) == 0:
            bg.tile()
        self.background = bg

    def listen(self) -> None:
        # runs event loop and general checks
        for event in pg.event.get():
            # quit event
            if event.type == pg.QUIT:
                self.toggle_run()
                return
            
    def register(self, entity: BaseEntity) -> None:
        # create masks for entity's sprites
        for name, spritesheet in entity.spritesheets.items():
            spritesheet.masks.clear()

            # iterate over frames
            for sprite in spritesheet.sprites:
                mask = pg.mask.from_surface(sprite.convert_alpha())
                entity.spritesheets[name].masks.append(mask)

        self.REGISTERED_ENTITIES.append(entity)

    def toggle_run(self) -> None:
        self.is_running = not self.is_running

    @property
    def window(self) -> pg.Surface:
        return self.__window