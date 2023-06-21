from __future__ import annotations

from typing import Literal

import pandas as pd

from pyutils.base import BaseDataset


class SupervisedLearningDataset(BaseDataset):
    def __init__(self, data: pd.DataFrame, category: Literal['binary', 'classification', 'regression', 'infer'] = 'infer', target: str | Literal['infer'] = 'infer') -> None:
        super().__init__(data)

        # get target and category
        self.__target = target 
        if target == 'infer':
            
        self.__category = category if category != 'infer' else   
