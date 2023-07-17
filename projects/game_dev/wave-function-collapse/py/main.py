from __future__ import annotations

from classes.Grid import Grid


def main():
    grid = Grid(5, 5, './data/sky/', verbose=False)
    grid.force_collapse_random(0)

    lookup = grid.generate_matches(threshold=0.01, sections=1, depth=1)
    grid.generate(lookup, resize=(400, 400), max_tries=100, verbose=False)


if __name__ == '__main__':
    main()