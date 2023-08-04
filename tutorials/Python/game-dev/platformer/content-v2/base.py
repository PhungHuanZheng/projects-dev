from __future__ import annotations

import os
import pygame
from abc import ABC, abstractmethod

from wrappers import Pos, Vec   
from constants import FPS, VELOCITY, GRAVITY


class BaseEntity(ABC, pygame.sprite.Sprite):
    # class properties
    VELOCITY = VELOCITY
    GRAVITY = GRAVITY
    FPS = FPS

    def __init__(self, base: pygame.Surface, xpos: int, ypos: int, width: int, height: int) -> None:
        self._base = base
        self._global_frame = 0
        self._update_rate = 1

        self._hitbox = pygame.Rect(xpos, ypos, width, height)
        self._center = Pos(xpos + width / 2, ypos + height / 2)
        self._mask = None
        self._sprite_set: dict[str, pygame.Surface] = {}

        self._animation_sprite_set = None
        self._fall_frames = 0
        self._animation_frame = 0
        self._animation = None
        self._animation_sprite = None

        self._direction = 'right'
        self._has_gravity = True

        self._vel = Vec(0, 0)
        self._acc = Vec(0, 0)

    def load_spritesheet(self, path: os.PathLike, width: int, height: int, scale: int = 1, directional: bool = False) -> None:
        """
        Loads a set of sprites from a folder path or a single sprite from an image
        path for this subclass instance. If a spritesheet is an image set instead
        of a single image, it is loaded as a list of images by its `width` and `height`
        passed.

        Parameters
        ----------
        `path` : `os.PathLike`
            Folder or filepath to this `BaseEntity` subclass' spritesheet.
        `width` : `int`
            Width of a single image in the sprite sheet.
        `height` : `int`
            Height of a single image in the sprite sheet.
        `scale` : `int`, `default = 1`
            How much to scale the sprite up or down by.
        `directional` : `bool`, `default = False`
            If True, adds a direction `_left` and `_right` to all sprite names in `_sprite_set`
        """

        # if single file
        if os.path.isfile(path):
            filename = print(os.path.basename(path))
            self._sprite_set[os.path.splitext(filename)[0]] = pygame.image.load(path).convert_alpha()
        
        # if folder of multiple files
        elif os.path.isdir(path):
            for filename in os.listdir(path):
                if not os.path.isfile(os.path.join(path, filename)):
                    continue

                self._sprite_set[os.path.splitext(filename)[0]] = pygame.image.load(os.path.join(path, filename)).convert_alpha()

        # iterate over populated sprite set and split images if sprite sheet
        for name, image in self._sprite_set.items():
            img_width, img_height = image.get_width(), image.get_height()

            # check that at least one side of the image is the same as its width or height
            if img_width != width and img_height != height:
                raise Exception(f'Expecting a single column or row of sprites to animate, ' + 
                                f'instead got {img_height // height} rows and {img_width // width} ' + 
                                f'columns at spritesheet {name}.')
                
            # if is single image
            if img_width == width and img_height == height:
                self._sprite_set[name] = [pygame.transform.scale_by(image, scale)]
                continue

            # lastly if single column/row of images, split by longer side
            longer_side = img_width if img_width > img_height else img_height
            constant_side = width if img_width < img_height else height
            num_frames = longer_side // constant_side

            temp_sprites = []
            for i in range(num_frames):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width if longer_side == img_width else 0, 
                                   i * height if longer_side == img_height else 0,
                                   width, height)

                surface.blit(self._sprite_set[name], (0, 0), rect)
                temp_sprites.append(pygame.transform.scale_by(surface, scale))

            self._sprite_set[name] = temp_sprites

        # if directional sprites
        if directional:
            new_sheet: dict[str, list[pygame.Surface]] = {}
            for name, sprites in self._sprite_set.items():
                new_sheet[f'{name}_left'] = [pygame.transform.flip(sprite, True, False) for sprite in sprites]
                new_sheet[f'{name}_right'] = sprites

            self._sprite_set = new_sheet

    def partition_spritesheet(self, path: os.PathLike, x: int, y: int, width: int, height: int, scale: int = 1, directional: bool = False) -> None:
        """
        Partitions a single frame of animation from a sprite sheet at the passed
        coordinates with the passed size.
        """

        # load whole spritesheet
        spritesheet = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(x, y, width, height)
        surface.blit(spritesheet, (0, 0), rect)
        self._sprite_set['aaa_right'] = [surface]

    def toggle_gravity(self, has_gravity: bool) -> None:
        self._has_gravity = has_gravity

    def set_animation(self, name: str, *, direction: str = None) -> None:
        if direction is not None:
            self._direction = direction
            
        self._animation = name
        self._animation_sprite_set = self._sprite_set[f'{name}_{self._direction}']

    def set_update_rate(self, rate: float) -> None:
        self._update_rate = 1 / rate

    @abstractmethod
    def AI(self, *args, **kwargs) -> None:
        """
        Method dictating updates to this entity, call super().AI() before your
        implementation for basic physics updates on position.
        """

        # basic physics update
        self._hitbox.x += self._vel.x
        self._hitbox.y += self._vel.y
        self._center.x += self._vel.x
        self._center.y += self._vel.y

        self._vel.x += self._acc.x
        self._vel.y += self._acc.y

        # update gravity
        self._vel.y += min(1, (self._fall_frames / BaseEntity.FPS) * BaseEntity.GRAVITY)
        self._fall_frames += 1

        self._vel.x = 0

    def show(self) -> None:
        # grab sprite name and apply facing direction
        self._animation_sprite = self._animation_sprite_set[self._animation_frame]
        self._base.blit(self._animation_sprite, (self._hitbox.x, self._hitbox.y))
        pygame.display.update()

        # update mask with current sprite
        self._mask = pygame.mask.from_surface(self._animation_sprite)

        if self._global_frame % self._update_rate == 0:
            self._animation_frame = (self._animation_frame + 1) % len(self._animation_sprite_set)
        self._global_frame += 1
        

