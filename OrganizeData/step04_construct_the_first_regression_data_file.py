#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: step04_construct_the_first_regression_data_file
# @Date: 2024/2/5
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.stats.mstats import winsorize

from Constant import Constants as const

if __name__ == '__main__':
    sd_esg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '2015_2021_shangdao_all_esg_data.pkl'))
    csmar_fina_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '1990_2023_CSMAR_financial_data.pkl'))
    # csmar_ma_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '1995_2023_csmar_oversea_ma.pkl'))
    er_tic_list: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20240406_er_guarantee_symbol_list.pkl'))

    for key in [const.ESG_SCORE, const.ESG_GOV_SCORE, const.ESG_RISK_SCORE, const.ENV_SCORE, const.SOCIAL_SCORE,
                const.CGOV_SCORE]:
        sd_esg_df.loc[:, 'ln_{key}'.format(key=key)] = sd_esg_df[key].apply(np.log)
    sd_esg_df.loc[:, const.TICKER2] = sd_esg_df[const.TICKER]
    sd_esg_df.loc[:, const.TICKER] = sd_esg_df[const.TICKER].str[:-3].astype(int)
    for key in [const.SEC_INDUSTRY_CODE, const.SHANGDAO_INDUSTRY_CODE2, const.SHANGDAO_INDUSTRY_CODE1]:
        id_df: DataFrame = sd_esg_df[key].drop_duplicates().reset_index(drop=False).rename(
            columns={'index': f'{key}_id'})
        id_df.to_csv(os.path.join(const.TEMP_PATH, f'20240205_{key}_id.csv'), index=False)
        sd_esg_df: DataFrame = sd_esg_df.merge(id_df, how='left', on=key)
    sd_esg_df2: DataFrame = sd_esg_df.replace([np.inf, -np.inf], np.nan).drop(
        labels=['comn', 'comn_short', 'secind', 'sdind1', 'sdind2', 'Comments'], axis=1)

    # organize the data for csmar fina file
    data_keys = [key for key in csmar_fina_df.columns if key not in {const.TICKER, const.YEAR}]
    csmar_fina_df2: DataFrame = csmar_fina_df.dropna(subset=data_keys, how='all')
    for key in data_keys:
        csmar_fina_df2[key] = csmar_fina_df2[key].astype(float)

    for key in [const.TOTAL_ASSETS, const.TOTAL_LIABILITIES, const.MKVALT_A, const.MKVALT_B, const.NET_FIXED_ASSETS,
                const.NET_INTANGIBLE_ASSETS, const.CASH]:
        ln_key = 'ln_{key}'.format(key=key)
        csmar_fina_df2.loc[:, ln_key] = csmar_fina_df2[key].apply(np.log).replace([np.inf, -np.inf], np.nan)
        csmar_fina_df2.loc[csmar_fina_df2[ln_key].notnull(), ln_key] = winsorize(csmar_fina_df2[ln_key].dropna(),
                                                                                 limits=(0.01, 0.01))

    # only keep csmar data
    csmar_fina_df3: DataFrame = csmar_fina_df2.loc[csmar_fina_df2[const.YEAR] >= 2010].copy()
    csmar_fina_df3.loc[:, 'er_foreign_gua'] = csmar_fina_df3[const.TICKER].isin(set(er_tic_list)).astype(int)

    # merge regression data
    cc_reg_df: DataFrame = csmar_fina_df3.merge(sd_esg_df2, on=[const.TICKER, const.YEAR], how='left')
    for year in range(1, 6):
        tmp_sd_esg_df = sd_esg_df2.copy()
        tmp_sd_esg_df[const.YEAR] -= year
        cc_reg_df: DataFrame = cc_reg_df.merge(tmp_sd_esg_df, on=[const.TICKER, const.YEAR], how='left',
                                               suffixes=('', '_{}'.format(year)))

    drop_keys = list()
    for key in ['secind_id', 'sdind2_id', 'sdind1_id']:
        for year in range(1, 6):
            cc_reg_df.loc[:, key] = cc_reg_df[key].fillna(cc_reg_df['{}_{}'.format(key, year)])
            drop_keys.append('{}_{}'.format(key, year))
    cc_reg_df2: DataFrame = cc_reg_df.drop(drop_keys, axis=1)
    cc_reg_df2.loc[:, 'post2017'] = cc_reg_df2[const.YEAR].apply(lambda x: int(x >= 2017))
    for year in range(2013, 2022):
        cc_reg_df2.loc[:, f'dummy_{year}'] = (cc_reg_df2[const.YEAR] == year).astype(int)
    cc_reg_df2.to_pickle(os.path.join(const.TEMP_PATH, '20240406_cc_regression_data.pkl'))
    cc_reg_df2.to_stata(os.path.join(const.OUTPUT_PATH, '20240406_cc_regression_data.dta'), write_index=False)
