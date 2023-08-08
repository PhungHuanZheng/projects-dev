from __future__ import annotations

import os

import pygame as pg

from Platformer.Base import BaseEntity
from Platformer.Helpers import Background


class Canvas:
    """
    Class representation of the Pygame window and game/event loop. Used to initialize
    the Pygame backend and also to be compatibly with this `Platformer` API's 
    `BaseEntity` base class.
    """

    def __init__(self, size: tuple[int, int], title: str = '', start: tuple[int, int] = None) -> None:
        """
        Instantiates a `Canvas` instance and initalizes a set of attributes used in the
        Pygame backend and game/event loop.

        Parameters
        ----------
        `size` : `tuple[int, int]`
            Tuple of 2 integers representing the `(width, height)` of the Pygame window.
        `title` : `str`, `default = ''`
            Title of the Pygame window.
        `start` : `tuple[int, int]`, `default = None`
            Starting position of the Pygame window as in the top left corner of the window.
            If `None`, starts window in the middle of the screen.
        """
        
        # change start pos 
        if start is not None:
            os.environ['SDL_VIDEO_WINDOW_POS'] = f'{start[0]},{start[1]}'
        
        # init window
        pg.init()
        pg.display.set_caption(title)
        self.__window = pg.display.set_mode(size)

        # init gameloop stuff
        self.clock = pg.time.Clock()
        self.is_running = True

        # canvas background
        self.background = None

        # entities to update and render in game loop
        self.__REGISTERED_ENTITIES: list[BaseEntity] = []

    @property
    def REGISTERED_ENTITIES(self) -> list[BaseEntity]:
        """
        List of `BaseEntity` subclasses to be updated and rendered in the main game loop.
        """

        return self.__REGISTERED_ENTITIES
    
    @property 
    def window(self) -> pg.Surface:
        """
        Pygame window `Surface` instance. Commonly passed as the "`base`" parameters in 
        functions and methods.
        """
        
        return self.__window
    
    def register(self, entity: BaseEntity) -> None:
        """
        Registers a `BaseEntity` subclass instance to be updated and rendered in the main
        game loop

        Parameters
        ----------
        `entity` : `BaseEntity`
            A `BaseEntity` subclass instance.
        """

        self.__REGISTERED_ENTITIES.append(entity)

    def set_background(self, background: Background) -> None:
        """
        Sets the `background` attribute to the background passed.

        Parameters
        ----------
        `background` : `Background`
            `Background` instance. Calls `Background.tile()` if not yet called.
        """

        if len(background.tile_pos) == 0:
            background.tile()

        self.background = background

    def listen(self, event_ids: list[int]) -> None:
        """
        Listens for and handles the list of events passed. If an event is not present in the
        "`events`" parameter passed, it is ignored.

        Parameters
        ----------
        `event_ids` : `list[int]`
            List of integers representing the ids of the Pygame events, e.g.: `pygame.QUIT`.
        """

        # get and iterate over events
        events = pg.event.get()
        for event in events:
            # ignore events not checked for
            if event.type not in event_ids:
                continue
            
            # quit event, 'X' clicked
            if event.type == pg.QUIT:
                self.is_running = False
                return
            
    def update(self) -> None:
        """
        Updates canvas display, wrapper for `pg.display.update()`
        """
        
        pg.display.update()
