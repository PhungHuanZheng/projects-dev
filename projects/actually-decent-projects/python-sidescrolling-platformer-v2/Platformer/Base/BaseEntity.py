from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, Callable, Iterable, Literal

import pygame as pg

from Platformer.Common.constants import FPS, GRAVITY
from Platformer.Helpers.Wrappers import Vector
from Platformer.Helpers import SpriteSheet


class BaseEntity(ABC, pg.sprite.Sprite):
    def __init__(self, base: pg.Surface, x: int, y: int, width: int, height: int) -> None:
        super().__init__()

        # basic init
        self.base = base
        self.direction = 'RIGHT'

        # attribute control
        if not hasattr(self, 'has_physics'): self.has_physics = False
        if not hasattr(self, 'has_gravity'): self.has_gravity = False
        if not hasattr(self, 'has_collision'): self.has_collision = False
        if not hasattr(self, 'is_fixed'): self.is_fixed = False
        if not hasattr(self, 'is_alive'): self.is_alive = False
        if not hasattr(self, 'jump_count'): self.jump_count = 1

        # positioning and bounding box
        self.rect = pg.Rect(x, y, width, height)
        self.center = x + width // 2, y + height // 2

        # physics
        if self.has_physics:
            self.vel = Vector(0, 0)
            self.acc = Vector(0, 0)

        # gravity
        if self.has_gravity:
            self.falling_framecount = 0
            self.is_falling = False

        # collision
        if self.has_collision:
            self.mask: pg.Mask = None

        # alive
        if self.is_alive:
            self.HP = 0
            self.DEF = 0
            self.immunity_frames = 10
            self.is_immune = False

        # animation
        self.animations: dict[str, SpriteSheet] = {}
        self.current_animaton: str = None
        self.current_spritesheet: SpriteSheet = None
        self.animation_framecount = 0
        self.animation_update_interval = 1

        # update ticker
        self.global_framecount = 0
        self.global_update_interval = 1

    @abstractmethod
    def AI(self) -> None:
        """
        Dictates what this instance does. To be called in the main event loop
        """

        pass

    def register_spritesheets(self, spritesheet_dicts: list[dict[str, SpriteSheet]]) -> BaseEntity:
        """
        Registers an `Iterable` of `SpriteSheet` instances to this `BaseEntity` subclass
        instance's "`animations`" attribute. Sprite transformations should be done through
        `BaseEntity.transform_sprites` as changes to individual spritesheets may not sync 
        with the entity's positon and bounding box related attributes and methods.

        Parameters
        ----------
        `spritesheet_dicts` : `list[SpriteSheet]`
            A dictionary of iterables of `SpriteSheet` instances.
        """

        for spritesheet_dict in spritesheet_dicts:
            for name, spritesheet in spritesheet_dict.items():
                self.animations[name] = spritesheet

        return self

    def transform_sprites(self, transformations: list[tuple[Callable[[pg.Surface], pg.Surface], Iterable[Any]]]) -> BaseEntity:
        """
        Transformations to apply to spritesheets/sprites in `BaseEntity.animations`. Tranformations
        are applied one after another, e.g.: `scale_by(2)` -> `scale_by(0.5)` results in no change to the 
        sprite size.

        Parameters
        ----------
        `transformations` : `list[tuple[Callable[[pg.Surface], pg.Surface], Iterable[Any]]]`
            List of Python callables which take in a `Surface` instance as an input and ouputs
            a `Surface` instance of the transformed input. All transformation functions/methods
            passed should have a `Surface` type for its first parameter. Arguments passed should be 
            for the parameters that come after the `Surface` parameter.

        Examples
        --------
        Method call example
        >>> BaseEntity.transform_sprites([
        ...     (pg.transform.scale_by, (0.5)),
        ...     (pg.transform.flip, (True, False))
        ... ])
        """

        for transformation in transformations:

            if 'scale_by' in str(transformation[0]):
                factor = transformation[1][0]
                self.rect.width *= factor
                self.rect.height *= factor

            for name, spritesheet in self.animations.items():
                for i, frame in enumerate(spritesheet.sprites):
                    spritesheet.sprites[i] = transformation[0](frame, *transformation[1])
                self.animations[name] = spritesheet

        return self
    
    def set_animation(self, name: str, interval: int = None) -> None:
        """
        Changes the current animation to another by name. If the animation to change to
        is directional, add '_{DIRECTION}' to the end of it or the animtaion name will not
        be recognized. Optionally the update speed/interval between frames can be changed.

        Parameters
        ----------
        `name` : `str`
            Name of new animation.
        `interval` : `int`, `default = None`
            New interval between frames for this animation. If `None`, ignored.
        """

        if self.current_animaton != name:
            self.animation_framecount = 0

        if interval is not None:
            self.animation_update_interval = interval

        self.current_animaton = name
        self.current_spritesheet = self.animations[name]

        if self.has_collision:
            self.mask = pg.mask.from_surface(self.animations[name].sprites[self.animation_framecount].convert_alpha())

    def set_direction(self, direction: Literal['UP', 'RIGHT', 'DOWN', 'LEFT']) -> None:
        """
        Sets the facing direction of the current sprite rendered.

        Parameters
        ----------
        `direction` : `Literal['UP', 'RIGHT', 'DOWN', 'LEFT']`
            New direction for sprite to show.
        """

        self.direction = direction

    def tick(self) -> None:
        """
        Called in the main game loop, updates internal frame counters/tickers.
        """ 

        if self.has_physics:
            self.vel.x = 0
        self.global_framecount += 1

    def physics(self) -> None:
        """
        Applies a basic physics engine on the `BaseEntity` subclass instance. if `BaseEntity.has_gravity`
        is False, exits silently.
        """

        if self.has_physics:
            self.rect.x += self.vel.x
            self.rect.y += self.vel.y
            
            self.vel.add(self.acc)
            self.acc.mul(Vector.same(0))

        if self.has_gravity:
            if self.is_falling:
                self.acc.y = min(1, (self.falling_framecount / FPS) * GRAVITY)
                self.falling_framecount += 1

            else:
                self.falling_framecount = 0

    def collided_with(self, other: BaseEntity) -> tuple[int, int] | None:
        """
        Checks if this `BaseEntity` subclass instance is colliding with another `BaseEntity` subclass instance 
        passed. Returns the point of collision if there exists one else `None`. If one of the entities has 
        `BaseEntity.has_collision` set as `False`, silently exits.

        Parameters
        ----------
        `other` : `BaseEntity`
            The other entity.
        """

        if not self.has_collision or not other.has_collision:
            return

        return pg.sprite.collide_mask(self, other)

    def render(self) -> None:
        """
        Draws/animates the current animation onto the `base`. If `BaseEntity.current_animation`
        is `None`, draws the bounding box `BaseEntity.rect` instead.
        """

        if self.current_animaton is None:
            pg.draw.rect(self.base, (255, 0, 0), self.rect)
            return
        
        if self.has_collision:
            self.mask = pg.mask.from_surface(self.current_spritesheet.sprites[self.animation_framecount].convert_alpha())
        
        self.base.blit(self.current_spritesheet.sprites[self.animation_framecount], self.rect)

        if self.global_framecount % self.animation_update_interval == 0:
            self.animation_framecount = (self.animation_framecount + 1) % self.current_spritesheet.n_frames
