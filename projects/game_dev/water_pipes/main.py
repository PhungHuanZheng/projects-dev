from __future__ import annotations

import sys; sys.path.append('../../../../projects-dev')
from importlib import reload
import pyutils; reload(pyutils)

from pyutils.core.structs import Grid


def main():
    grid = Grid(width=10, height=10)


if __name__ == '__main__':
    main()