from typing import Any, Literal


class ASCIIBox:
    def __init__(self, width: int, height: int, style: Literal['single', 'double', 'dotted'] = 'single') -> None:
        self._shape = (width, height)
        self._charset = {
            'single': ('┘', '┐', '┌', '└', '┼', '─', '├', '┤', '┴', '┬', '│'),
            'double': ('╝', '╗', '╔', '╚', '╬', '═', '╠', '╣', '╩', '╦', '║'),
            'dotted': ()
        }[style]

    def show(self) -> None:
        print(f'{self._charset[2]}{self._charset[5] * (self._shape[0] - 2)}{self._charset[1]}')
        for _ in range(self._shape[1] - 2):
            print(f'{self._charset[10]}{" " * (self._shape[0] - 2)}{self._charset[10]}')
        print(f'{self._charset[3]}{self._charset[5] * (self._shape[0] - 2)}{self._charset[0]}')


class ASCIIGrid(ASCIIBox):
    def __init__(self, width: int, height: int, style: Literal['single', 'double', 'dotted'] = 'single') -> None:
        super().__init__(width, height, style)

    def show(self) -> None:
        print(f'{self._charset[2]}{self._charset[9] * (self._shape[0] - 2)}{self._charset[1]}')
        for _ in range(self._shape[1] - 2):
            print(f'{self._charset[6]}{self._charset[4] * (self._shape[0] - 2)}{self._charset[7]}')
        print(f'{self._charset[3]}{self._charset[8] * (self._shape[0] - 2)}{self._charset[0]}')



def main():
    ASCIIBox(width=20, height=10, style='single').show()
    ASCIIGrid(width=20, height=10, style='single').show()

        


if __name__ == '__main__':
    main()