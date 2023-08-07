from __future__ import annotations

from dataclasses import dataclass


@dataclass 
class Vector:
    x: int
    y: int

    def add(self, vec: Vector) -> None:
        self.x += vec.x
        self.y += vec.y

    def mult(self, vec: Vector) -> None:
        self.x *= vec.x
        self.y *= vec.y

@dataclass 
class Shape:
    w: int
    h: int
