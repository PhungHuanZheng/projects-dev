from __future__ import annotations

import os
from typing import Any, Callable
from dataclasses import dataclass

import pygame as pg
from functools import singledispatch


class Canvas:
    """
    Object representation of the Pygame window opened. 

    Attributes
    ----------
    `width` : `int`
        Width of the window in pixels.
    `height` : `int`
        Height of the window in pixels.
    `window` : `Surface`
        Pygame `Surface` instance representing the window.

    Methods
    -------
    `listen_for(events)`
        Specifies which events the listener is to listen for and specific
        actions to take upon those events. If the action for an event is left
        as `None`, default/no action will be done. If the `events` argument is
        left as `None`, no events will be listened for. Any custom action `Callable`s 
        must have this `Canvas` instance as its first parameter.
    `colour(Color)`
        Sets the background to a single colour.
    `set_background(path, tiled)`
        Loads and sets the background from an image filepath. The image shown starts at
        the top left corner of the window at (0, 0). If the image does not fill the space
        fully, pass `True` to the "tiled" argument to tile the image over the area.
    `clear()`
        Clears the window and redraws the background set during `Canvas.set_background`.
    `update()`
        Updates the window. Wrapper for `pg.display.update`.
    """

    EVENTS = {
        pg.QUIT: lambda c: setattr(c, 'is_running', False)
    }

    def __init__(self, width: int, height: int, framerate: int, title: str = '') -> None:
        self.__width = width
        self.__height = height
        self.__target_framerate = 60
        self.__title = title

        # pygame backend and window
        pg.init()
        pg.display.set_caption(title)
        self.__window = pg.display.set_mode((width, height))

        # game loop attributes
        self.clock = pg.time.Clock()
        self.is_running = True

        # background attributes
        self.bg_image: pg.Surface = None
        self.tiles: list[_BackgroundTile] = []

    @property
    def width(self) -> int:
        """Width of the window in pixels."""

        return self.__width
    
    @property
    def height(self) -> int:
        """Height of the window in pixels."""

        return self.__height
    
    @property
    def window(self) -> pg.Surface:
        """Pygame `Surface` instance representing the window."""

        return self.__window
    
    def listen_for(self, events: dict[int | pg.event.Event, Callable[[Canvas, *Any], None]]) -> None:
        """
        Specifies which events the listener is to listen for and specific
        actions to take upon those events. If the `events` argument is
        left as `None`, all default events will be listened for. Any custom action 
        `Callable`s must have this `Canvas` instance as its first parameter.

        `Canvas.EVENTS` will show a dictionary of currently implemented events and actions.
        
        Parameters
        ----------
        `events` : `dict[int | pg.event.Event, Callable[[Canvas, *Any], None]]`
            Dictionary of event, function key value pairs. If `None`, all default
            events will be listened for and all default actions will be taken.
        """
        
        active = events if events is not None else Canvas.EVENTS
        events = pg.event.get()

        for event in events:
            if event.type in active:
                active[event.type](self)

    def colour(self, colour: pg.Color) -> None:
        """
        Sets the background to a single colour.

        Parameters
        ----------
        `colour` : `Color`
            Colour to set the background to.
        """

        self.window.fill(colour)

    def set_background(self, path: os.PathLike, tiled: bool = True) -> None:
        """
        Loads and sets the background from an image filepath. The image shown starts at
        the top left corner of the window at (0, 0). If the image does not fill the space
        fully, pass `True` to the "tiled" argument to tile the image over the area.

        If a `pygame.Color` instance is passed instead, fills the window with the colour
        passed.

        Parameters
        ----------
        `path` : `os.PathLike`
            Filepath to the image file. Image is loaded with `pygame.image.load`.
        `tiled` : `bool`, `default = True`
            Whether or not to tile the image over the window. Used when the image
            does not fill the space fully.

        See Also
        --------
        `Canvas.colour` : Sets the background to a single colour.
        """

        # load image
        self.bg_image = pg.image.load(path).convert_alpha()
        self.tiles = [_BackgroundTile(self.bg_image, (0, 0))]

        # if want to tile image
        if tiled is True:
            self.tiles.clear()

            # tile background
            for y in range(self.height // self.bg_image.get_height() + 1):
                for x in range(self.width // self.bg_image.get_width() + 1):
                    self.tiles.append(_BackgroundTile(self.bg_image, (x * self.bg_image.get_width(), y * self.bg_image.get_height())))

        # show background on window
        for tile in self.tiles:
            self.window.blit(tile.image, tile.pos)

    def clear(self) -> None:
        """
        Clears the window and redraws the background set during `Canvas.set_background`.
        """
        
        for tile in self.tiles:
            self.window.blit(tile.image, tile.pos)

    def update(self) -> None:
        """
        Updates the window. Wrapper for `pg.display.update`.
        """

        pg.display.update()

    

@dataclass
class _BackgroundTile:
    image: pg.Surface
    pos: tuple[int, int]

