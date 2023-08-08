from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Vector:
    x: int
    y: int

    def add(self, vec: Vector) -> None:
        self.x += vec.x
        self.y += vec.y

    def sub(self, vec: Vector) -> None:
        self.x -= vec.x
        self.y -= vec.y

    def div(self, vec: Vector) -> None:
        self.x /= vec.x
        self.y /= vec.y

    def mul(self, vec: Vector) -> None:
        self.x *= vec.x
        self.y *= vec.y

    @classmethod
    def same(cls, num: float) -> Vector:
        return Vector(num, num)