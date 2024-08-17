#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: step01_construt_nca_regression_data
# @Date: 2024/3/18
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constant import Constants as const

if __name__ == '__main__':
    nci_index: DataFrame = pd.read_excel(os.path.join(const.NCA_DATA_PATH, 'nci.xlsx'), sheet_name='NCI')
    idd_law_df: DataFrame = pd.read_excel(os.path.join(const.NCA_DATA_PATH, 'nci.xlsx'), sheet_name='IDD').rename(
        columns={'State': const.STATE, 'Year': const.YEAR})
    idd_states = set(idd_law_df[const.STATE])

    us_ds_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20240314_us_ds_dataset.pkl'))

    ctrl_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '1970_2023_ctat_firm_ctrl_variables.pkl'))
    ctrl_df: DataFrame = ctrl_df.loc[ctrl_df[const.YEAR] >= 1978].dropna(subset=[const.STATE])
    ctrl_nci_df: DataFrame = ctrl_df.merge(nci_index, on=[const.STATE, const.YEAR], how='left')
    ctrl_nci_df.loc[:, 'IDD_law'] = ctrl_nci_df.apply(
        lambda x: np.nan if x[const.STATE] not in idd_states else 0 if x[const.YEAR] >= idd_law_df.loc[
            idd_law_df[const.STATE] == x[const.STATE], const.YEAR].iloc[0] else 1, axis=1)

    nca_ctrl_df: DataFrame = ctrl_nci_df.dropna(subset=['IDD_law', 'nci'], how='all')
    us_ds_df.loc[:, const.YEAR] -= 1
    nca_ds_reg_df: DataFrame = us_ds_df.merge(nca_ctrl_df, on=[const.TICKER, const.YEAR], how='left')
    nca_ds_reg_df.loc[:, 'ln_Deal_Amount'] = nca_ds_reg_df['Deal_Amount'].apply(np.log).replace(
        [np.inf, -np.inf], np.nan)
    nca_ds_reg_df.loc[nca_ds_reg_df[const.YEAR].apply(lambda x: x < 1996 or x > 2016), 'IDD_law'] = np.nan
    nca_ds_reg_df.to_stata(os.path.join(const.NCA_OUTPUT_PATH, '20240318_nca_regression_data.dta'), write_index=False)
