#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: step05_merge_financial_dependent_variables
# @Date: 2024/2/26
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

import pandas as pd
from pandas import DataFrame

from Constant import Constants as const

if __name__ == '__main__':
    cs_df_all: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '1990_2023_CSMAR_financial_data.pkl'))
    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20240406_cc_regression_data.pkl'))

    useful_fina_vars = [const.NET_ROA_A, const.NET_ROA_B, const.LIABILITY_RATIO, const.CASH_RATIO, const.TANGIBLE_RATIO,
                        const.FIXED_ASSETS_RATIO, const.INTASSETS_RATIO, const.EBIT_TA_A, const.RD_EXPENSE_RATIO,
                        const.TOBINQ_A, const.TOBINQ_B, const.TOBINQ_C, const.TOBINQ_D]

    for key in useful_fina_vars:
        cs_df_all[key] = cs_df_all[key].astype(float)
    useful_fina_vars.extend([const.TICKER, const.YEAR])
    useful_var_df: DataFrame = cs_df_all[useful_fina_vars].copy()

    for year in range(1, 6):
        tmp_df: DataFrame = useful_var_df.copy()
        tmp_df.loc[:, const.YEAR] -= year

        reg_df: DataFrame = reg_df.merge(tmp_df, on=[const.TICKER, const.YEAR], how='left',
                                         suffixes=('', '_{}'.format(year)))
    reg_df.to_pickle(os.path.join(const.TEMP_PATH, '20240406_cc_regression_data_v2.pkl'))
    reg_df.to_stata(os.path.join(const.OUTPUT_PATH, '20240406_cc_regression_data_v2.dta'), write_index=False)
