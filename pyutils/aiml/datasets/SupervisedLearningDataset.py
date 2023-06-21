from __future__ import annotations

from typing import Literal

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import TransformerMixin

from pyutils.base import BaseDataset


class SupervisedLearningDataset(BaseDataset):
    def __init__(self, data: pd.DataFrame, category: Literal['binary', 'classification', 'regression', 'infer'] = 'infer', target: str | Literal['infer'] = 'infer') -> None:
        super().__init__(data)

        # get target and category
        self.__target = target 
        if target == 'infer':
            self.__target = self._data.columns[-1]

        self._category = category
        if category == 'infer':
            if len(self._data[self.__target].unique()) == 2:
                self._category = 'binary'

            elif len(self._data[self.__target].unique()) <= 10:
                self._category = 'classification'

            else:
                self._category = 'regression'

        # separate data and target
        self._target = self._data
        self._data = self._data.drop(self.__target, axis=1)

    @property
    def data(self) -> pd.DataFrame:
        """Data passed without target."""

        return self._data
    
    @property
    def target(self) -> pd.Series:
        """Target of data passed."""

        return self._target
        
    def base_preprocessor(self, scaler: TransformerMixin = StandardScaler(), encoder: TransformerMixin = OneHotEncoder()) -> Pipeline:
        """
        Builds and returns a baseline general preprocessor `Pipeline` instance for 
        the data passed to `__init__`.

        Parameters
        ----------
        `scaler` : `TransformerMixin`, `default=StandardScaler()`
            Scaler used on numerical values.
        `encoder` : `TransformerMixin`, `default=OneHotEncoder()`
            Encoder used on categorical values.

        Returns
        -------
        `Pipeline`
            Sklearn `Pipeline` instance.
        """

        # get numerical and categorical columns
        num_cols = self._data.select_dtypes(include=['int', 'float']).columns
        cat_cols = self._data.select_dtypes(include=['object']).columns

        # build and return pipeline
        return Pipeline([
            ('col_trans', ColumnTransformer([
                ('scaler', scaler, num_cols),
                ('enc', encoder, cat_cols)
            ]))
        ])
    