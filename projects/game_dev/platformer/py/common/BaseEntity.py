from __future__ import annotations

import os
from typing import Literal
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path

import pygame

from _constants import FPS, GRAVITY
from helpers.wrappers import Vector, Shape
from helpers import SpriteSheet


class BaseEntity(ABC, pygame.sprite.Sprite):
    """
    Base entity class to subclass for all game objects. Implements sprite
    loading, handling and animation. Instance update method `BaseEntity.AI()`
    to be implemented.
    """

    FPS = FPS
    GRAVITY = GRAVITY
    REGISTERED_ENTITIES: list[BaseEntity] = []

    def __init__(self, base: pygame.Surface, xpos: int, ypos: int, width: int, height: int, has_gravity: bool = True) -> None:
        self._base = base
        self._hitbox = pygame.Rect(xpos, ypos, width, height)
        self._center = Vector(self._hitbox.x + width // 2, self._hitbox.y + height // 2)
        self._has_gravity = has_gravity

        # collision detection
        self._mask = pygame.Mask((width, height), fill=True)
        
        self._vel = Vector(0, 0)
        self._acc = Vector(0, 0)

        self._falling_framecounter = 0
        self._is_falling = True

        self._global_framecounter = 0
        self._update_interval = 1
        self._direction = 'LEFT'

        self._sprites: dict[str, SpriteSheet] = {}
        self._animation_framecount = 0
        self._animation_speed = 0
        self._animation = None
        self._animation_frames = []

    @abstractproperty
    def category(self) -> None:
        """
        Returns the category of this `BaseEntity` subclass instance. Category name should be
        capitalized, e.g.: `'PLAYER'`, `'TERRAIN'`, `'ENEMY'`.
        """

    @abstractmethod
    def AI(self) -> None:
        """
        Dictates what this instance does. To be called in the main event loop. Call 
        `super().AI()` to apply basic physics.
        """

        # update physics
        self._hitbox.x += self._vel.x
        self._hitbox.y += self._vel.y
        self._vel.add(self._acc)
        self._acc.mult(Vector(0, 0))

        # update gravity
        if self._has_gravity and self._is_falling:
            self._acc.y = min(1, (self._falling_framecounter / BaseEntity.FPS) * BaseEntity.GRAVITY)
            self._falling_framecounter += 1
        else:
            self._acc.y = 0
            self._vel.y = 0
            self._falling_framecounter = 0

        # stop moving horizontally every frame and update global framecounter
        self._vel.x = 0
        self._global_framecounter += 1
    
    def overlaps(self, entity: BaseEntity) -> bool:
        return self._mask.overlap(
            entity._mask,
            (self._hitbox.x - entity._hitbox.x,
             self._hitbox.y - entity._hitbox.y)
        ) is not None

    def add_animation(self, name, frames: SpriteSheet, *, directional: bool = False, set_animation: bool = False) -> None:
        if name in self._sprites:
            raise ValueError(f'Animation name "{name}" already exists.')
        
        if directional:
            self._sprites[f'{name}_LEFT'] = frames.copy().flip()
            self._sprites[f'{name}_RIGHT'] = frames.copy()

        else:
            self._sprites[name] = frames.copy()

        if set_animation:
            self.set_animation(name, direction=self._direction if directional else 'NONE')

    def load_sprites(self, path: os.PathLike, scale: int = 1, directional: bool = False) -> None:
        """
        Loads a sprite sheet from a filepath or a set of sprite sheets from a folder
        path.

        Parameters
        ----------
        `path` : `PathLike`
            File or folder path to this entity's sprite sheet(s)
        """
        
        # load sprites from file/folder as SpriteSheet objects
        if os.path.isfile(path):
            name = os.path.splitext(Path(path).name)[0]
            self._sprites[name] = SpriteSheet(path).animate(self._hitbox.width, self._hitbox.height)

        elif os.path.isdir(path):
            filenames = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
            filepaths = [os.path.join(path, filename) for filename in filenames]

            for filepath in filepaths:
                name = os.path.splitext(Path(filepath).name)[0]
                self._sprites[name] = SpriteSheet(filepath).animate(self._hitbox.width, self._hitbox.height)

        # apply transformations
        if scale != 1:
            for name, sprites in self._sprites.items():
                self._sprites[name].scale(scale)

        # create directional sprites
        if directional:
            temp_sprites = {}

            for name, sprites in self._sprites.items():
                temp_sprites[f'{name}_LEFT'] = sprites.copy().flip(True, False)
                temp_sprites[f'{name}_RIGHT'] = sprites.copy()

            self._sprites = temp_sprites

    def set_animation(self, animation_name: str, *, direction: Literal['LEFT', 'RIGHT', 'NONE'] = None) -> None:
        """
        Sets the animation of the Entity subclass instance. Optionally changes its
        direction to either 'LEFT' or 'RIGHT'

        Parameters
        ----------
        `animation_name` : `str`
            Name of the animation, usually `"[filename-without-ext]_[LEFT/RIGHT]"`
        `direction` : `default = None`
            Sets the direction of the instance to either 'LEFT' or 'RIGHT'. If `None`
            is passed, direction is not changed
        """

        animation_name = animation_name if direction == 'NONE' else f'{animation_name}_{self._direction}'

        # if no change to direction
        if direction is not None:
            self._direction = direction

        # set frame back to 0 to prevent it stopping at an index out of bounds of new animation
        if animation_name != self._animation:
            self._animation_framecount = 0

        # set new animation name and frames
        self._animation = animation_name
        self._animation_frames = self._sprites[self._animation].sprites
        
    def set_animation_interval(self, interval: int) -> None:
        """
        Changes how fast the sprite animation gets update
        
        Paramaters
        ----------
        `interval` : `int`
            Number of seconds between each animation frame update.
        """
        self._update_interval = interval

    def register(self) -> None:
        """
        Registers this `BaseEntity` instance or subclass instance to the main, user-written
        list of other `BaseEntity` instances or subclass instances. Allows for mass updating 
        and rendering.
        """

        BaseEntity.REGISTERED_ENTITIES.append(self)
        
    def show(self) -> None:
        self._base.blit(self._animation_frames[self._animation_framecount], (self._hitbox.x, self._hitbox.y))
    
        # update accordingly to update rate
        if self._global_framecounter % self._update_interval == 0:
            self._animation_framecount = (self._animation_framecount + 1) % self._sprites[self._animation].n_frames

  
