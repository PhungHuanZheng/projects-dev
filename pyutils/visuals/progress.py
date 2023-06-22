from __future__ import annotations

import os
import sys
import time
import math
import ctypes
import random
from colorama import init; init()


class ProgressBar:
    def __init__(self, name: str, steps: int, bar_length: int = 100, characters: tuple[str, str] = ('▓', '▒')) -> None:
        self._name = name
        self._steps = steps

        self._bar_length = bar_length
        self._characters = characters
        
        self._current_step = 0

        self._current_done = ''
        self._current_undone = self._characters[1] * self._bar_length

        self._generate_bar()

    def _generate_bar(self) -> str:
        # get characters for done and undone sections
        done_chars = round(self._current_step / self._steps * self._bar_length) * self._characters[0]
        undone_chars = (self._bar_length - len(done_chars)) * self._characters[1]

        print(f'\r{self._name} | {done_chars}{undone_chars} [{self._current_step}/{self._steps}]', end='')

    def update(self) -> None:
        self._current_step += 1
        self._generate_bar()

        # format for next line after bar done
        if self._current_step == self._steps:
            print()


class MultipleProgressBar:
    def __init__(self,  names: list[str], steps: list[int], bar_length: int = 100, characters: tuple[str, str] = ('▓', '▒')) -> None:
        self._names = names
        self._steps = steps

        self._bar_length = bar_length
        self._characters = characters
        
        self._current_steps = [0] * len(self._names)

        self._current_dones = [''] * len(self._names)
        self._current_undones = [self._characters[1] * self._bar_length] * len(self._names)

        # formatting for names
        self._name_spacing = len(max(self._names, key=len))

        print('\n' * (len(self._names) + 1))
        self._generate_bars()

    @property
    def all_done(self) -> bool:
        return all([self._current_steps[i] == steps for i, steps in enumerate(self._steps)])

    def _generate_bars(self) -> None:
        # prep individual bar lines
        # os.system('cls')
        
        print(f'\033[{len(self._names) + 3}A')
        print(f'┌┬{"─" * (self._name_spacing + 2)}┬{"─" * (self._bar_length + 2)}┬{"─" * 8}┬┐')
        
        # iterate over names
        for i, name in enumerate(self._names):
            # get done and undone sections
            done_chars = round(self._current_steps[i] / self._steps[i] * self._bar_length) * self._characters[0]
            undone_chars = (self._bar_length - len(done_chars)) * self._characters[1]

            print(f'││ {name: >{self._name_spacing}} │ {done_chars}{undone_chars} │ {100 * self._current_steps[i] / self._steps[i]:#.4g}% │')

        print(f'└┴{"─" * (self._name_spacing + 2)}┴{"─" * (self._bar_length + 2)}┴{"─" * 8}┴┘')

    def update(self, index: int) -> None:
        if self._current_steps[index] >= self._steps[index]:
            raise Exception(f'Current step ({self._current_steps[index]}) exceeded max steps ({self._steps[index]}) for bar {self._names[index]}.')
        self._current_steps[index] += 1

        self._generate_bars()
        if self.all_done: 
            sys.exit()

    def update_all(self) -> None:
        for i, _ in enumerate(self._steps):
            if self._current_steps[i] >= self._steps[i]:
                raise Exception(f'Current step ({self._current_steps[i]}) exceeded max steps ({self._steps[i]}) for bar {self._names[i]}.')
            self._current_steps[i] += 1

        self._generate_bars()   
        if self.all_done:  
            sys.exit()