from __future__ import annotations

import math
import random
from typing import Iterator

import pandas as pd


class BaseDataset:
    def __init__(self, data: pd.DataFrame = None) -> None:
        self._data = data

    def to_chunks(self, chunk_size: int = 5000) -> Iterator[pd.DataFrame]:
        """
        Splits the data into chunks of equal sizes as much as possible.

        Parameters
        ----------
        `chunk_size` : `int`
            Size of each chunk to be yielded

        Yields
        ------
        `pd.DataFrame`
            Chunk of the original data.
        """

        # get chunk bound pairs
        chunk_bounds = [i * chunk_size for i in range(math.floor(len(self._data) / chunk_size))] + [None]
        
        # return as generator object
        for i, bound in enumerate(chunk_bounds[:-1]):
            yield self._data[bound:chunk_bounds[i + 1]]
            