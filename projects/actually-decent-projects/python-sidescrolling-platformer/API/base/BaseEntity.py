from __future__ import annotations

import os
from abc import ABC, abstractmethod, abstractproperty
from typing import Literal, Iterable

import pygame as pg

from Common.constants import FPS, GRAVITY
from API.helpers.wrappers import Vector
from API.spriting import SpriteSheet


class BaseEntity(ABC, pg.sprite.Sprite):
    UP, RIGHT, DOWN, LEFT = 'UP', 'RIGHT', 'DOWN', 'LEFT'

    """
    Base entity class to subclass for all game objects. Implements sprite
    loading, handling and animation. Instance update method `BaseEntity.AI()`
    to be implemented.
    """

    def __init__(self, base: pg.Surface, x: int, y: int, width: int, height: int) -> None:
        # basic attribute init
        self.base = base
        self.rect = pg.Rect(x, y, width, height)
        self.center = Vector(x + width // 2, y + height // 2)

        # instance attributes to be set when subclassing to game objects/instances
        self.has_gravity = True
        self.has_physics = True
        self.has_collision = True
        self.immune_time = 0
        self.velocity = 0
        self.update_interval = 1

        # falling tracker
        self.is_falling = False
        self.falling_framecount = 0

        # immunity tracker
        self.is_immune = False
        self.immune_framecount = 0

        # sprite animation and loading
        self.scale = 1
        self.spritesheets: dict[str, SpriteSheet] = {}
        self.direction = 'LEFT'
        self.current_spritesheet = None
        self.animation_name = None
        self.animation_interval = 1
        self.animation_framecount = 0
        self.animation_global_framecount = 0

        # global game loop attributes
        self.global_framecount = 0
        self.update_interval = 0

        # basic physics engine
        if self.has_physics:
            self.vel = Vector(0, 0)
            self.acc = Vector(0, 0)

    @abstractmethod
    def AI(self) -> None:
        """
        Dictates what this instance does. To be called in the main event loop
        """

        pass

    def overlaps(self, entity: BaseEntity) -> bool:
        # get current animations and masks from both
        my_mask = self.spritesheets[self.animation_name].masks[self.animation_framecount]
        other_mask = entity.spritesheets[entity.animation_name].masks[entity.animation_framecount]
        offset = (entity.rect.x - self.rect.x, entity.rect.y - self.rect.y)

        return my_mask.overlap(other_mask, offset)

    def do_physics(self) -> None:
        """
        Applies a basic physics engine to this `BaseEntity` subclass instance only
        if `self.has_physics` is `True`. Also applies pseudo-realistic falling physics.
        """

        if not self.has_physics:
            return
        
        # fall
        if self.is_falling:
            self.acc.y = min(1, (self.falling_framecount / FPS) * GRAVITY)
            self.falling_framecount += 1

        else:
            self.falling_framecount = 0
        
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        self.center.x += self.vel.x
        self.center.y += self.vel.y

        self.vel.add(self.acc)
        self.acc.mul(Vector.same(0))
        self.vel.x = 0

    def animate_sprites(self, animation_axis: int = None) -> BaseEntity:
        """
        Creates an animation for all sprites in `BaseEntity.spritesheets`. A wrapper
        for `SpriteSheet.animate`. Uses the `self.rect.width` and `self.rect.height` 
        attributes to separate frames.

        Parameters
        ----------
        `animation_axis` : `int`, `default = None`
            Axis containing the animated frames. If `None`, assumes the longer
            side is the animation axis.

        Returns
        -------
        `BaseEntity`
            This `BaseEntity` subclass instance for method chaining with animated 
            `SpriteSheet` instances.
        """

        for name, sheet in self.spritesheets.items():
            self.spritesheets[name] = sheet.animate(self.rect.width, 
                                                    self.rect.height, 
                                                    animation_axis)

        return self

    def load_spritesheets(self, *spritesheet_dicts: Iterable[dict[str, SpriteSheet]]) -> BaseEntity:
        """
        Loads a `SpriteSheet` instance to this `BaseEntity` subclass' sprites dictionary
        as a dictionary. Call `spritesheet.to_dict` with the `facing` and `directions`
        parameters passed and pass it's results to this method. 

        Parameters
        ----------
        `spritesheet_dicts` : `Iterable[dict[str, SpriteSheet]]`
            Iterable of dictionaries of the spritesheet name and its instance.

        Returns
        -------
        This `BaseEntity` subclass instance for method chaining with loaded sprites.
        """

        for spritesheet_dict in spritesheet_dicts:
            for name, sheet in spritesheet_dict.items():
                # check if name already exists
                if name in self.spritesheets:
                    raise Exception(f'Spritesheet name "{name}" already exists/has already been loaded.')
                self.spritesheets[name] = sheet

        return self
    
    def set_scale(self, factor: float = 1) -> BaseEntity:
        """
        Changes the `BaseEntity` subclass' scale to `factor` passed. Changes to the
        scale are relative to the current scale and not the original scale.

        Parameters
        ----------
        `factor` : `float:
            Scaling factor for sprites
        
        Returns
        -------
        `BaseEntity`
            Returns this `BaseEntity` subclass instance for method chaining
        """

        self.scale = factor

        self.rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width * factor, self.rect.height * factor)
        self.center = Vector(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2)

        return self

    def set_animation(self, name: str, interval: int = None) -> BaseEntity:
        """
        Sets the current animation for this `BaseEntity` subclass. If your 
        spritesheet/animation was loaded as directional, add '_DIRECTION' at 
        the end of the `name` passed to be a valid name. Optionally changes 
        this instance's `animation_interval` to speed up/slow down animation
        update rate.

        Parameters
        ----------
        `name` : `str`
            Name of the animation/spritesheet.
        `interval` : `int`
            Number of frames between animation updates.

        Returns
        -------
        `BaseEntity`
            Returns this `BaseEntity` subclass instance for method chaining

        Examples
        --------
        Directional animation
        >>> spritesheet.set_animation('anim_LEFT')

        Non-directional animation
        >>> spritesheet.set_animation('anim')
        """

        if interval is not None:
            self.animation_interval = interval

        # if new animation, reset frame count
        if name != self.animation_name:
            self.animation_framecount = 0

        self.animation_name = name
        self.current_spritesheet = self.spritesheets[name]

        return self

    def set_direction(self, direction: Literal['UP', 'RIGHT', 'DOWN', 'LEFT']) -> None:
        """
        Sets the internal direction to the new direction passed. Class attributes 
        `BaseEntity.UP`, `BaseEntity.RIGHT`, `BaseEntity.DOWN`, `BaseEntity.LEFT` can
        be used.

        Parameters
        ----------
        `direction` : `Literal['UP', 'RIGHT', 'DOWN', 'LEFT']`
            New direction.
        """

        self.direction = direction

    def show(self, *, draw_rect: bool = False) -> None:
        if draw_rect:
            pg.draw.rect(self.base, (255, 0, 0), self.rect)
        self.base.blit(self.current_spritesheet.sprites[self.animation_framecount], self.rect)

        if self.animation_global_framecount % self.animation_interval == 0:
            self.animation_framecount = (self.animation_framecount + 1) % self.current_spritesheet.n_frames

        self.animation_global_framecount += 1