#!/usr/bin/env python
import os.path

# -*- coding: utf-8 -*-
# @Filename: step04_construct_regression_data
# @Date: 2024/8/19
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import pandas as pd
import numpy as np

from Constant import Constants as const

# =============================================================================

if __name__ == '__main__':

    df1 = pd.read_csv("2014_2023_firm_financial/2014_2023_firm_financial.csv", error_bad_lines=False)
    df2 = pd.read_csv("Cdata_data_guarantee.csv", error_bad_lines=False)
    df3 = pd.read_csv("2015_2021_esg_data.csv", error_bad_lines=False)

    merged_df = pd.merge(df1, df2, on=['Symbol', 'Year'], how='left')
    merged_df = pd.merge(merged_df, df3, on=['Symbol', 'Year'], how='left')

    columns_to_drop = ['tic', 'comn', 'comn_short', 'secind', 'sdind1', 'sdind2', 'tic2']
    df4 = merged_df.drop(columns=columns_to_drop)

    # Loop through each listed columns and create lagged versions
    df4 = df4.sort_values(by=['Symbol', 'Year'])
    columns_to_lag = ['esg_score', 'esg_gov_score', 'esg_risk_score', 'env_score', 'social_score']
    columns_to_drop = columns_to_lag.copy()

    for col in columns_to_lag:  # -1 forward, 1 backward
        df4[f'{col}_1'] = df4.groupby('Symbol')[col].shift(-1)
        df4[f'{col}_2'] = df4.groupby('Symbol')[col].shift(-2)
        df4[f'{col}_3'] = df4.groupby('Symbol')[col].shift(-3)
        columns_to_drop.extend([f'{col}_1', f'{col}_2', f'{col}_3'])

    df5 = df4.replace(np.inf, np.nan)
    df5.dropna(subset=columns_to_drop, inplace=True, how='all')

    df5.loc[:, 'ln_A001000000'] = df5['A001000000'].apply(np.log)
    df5.loc[:, 'After2017'] = (df5['Year'] > 2017).astype(int)
    df5.loc[:, 'Post2017'] = (df5['Year'] >= 2017).astype(int)

    # Filter the DataFrame to include only the years 2014 to 2017
    df5_filtered = df5[(df5['Year'] >= 2014) & (df5['Year'] <= 2017)]

    # Create a new column "er_foreign_gua" and set it to 0 initially
    df5['er_foreign_gua'] = 0

    # Identify Symbols with at least one "NumGuarantee" greater than 0 between 2014 and 2017
    symbols_with_gua = df5_filtered[df5_filtered['NumGuarantee'] > 0]['Symbol'].unique()

    # Set "er_foreign_gua" to 1 for these Symbols
    df5.loc[df5['Symbol'].isin(symbols_with_gua), 'er_foreign_gua'] = 1
    df5.to_stata(os.path.join(const.OUTPUT_PATH, '20240819_cc_reg_data.dta'), write_index=False, version=119)
