from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Pos:
    x: int
    y: int

@dataclass
class Vec:
    x: int
    y: int