from __future__ import annotations

from dataclasses import dataclass


# helper dataclasses to help with data structuring
@dataclass
class Shape:
    w: int
    h: int

@dataclass
class Pos:
    x: int
    y: int