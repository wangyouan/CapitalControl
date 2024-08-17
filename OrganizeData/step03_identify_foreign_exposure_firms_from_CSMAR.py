#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: step03_identify_foreign_exposure_firms_from_CSMAR
# @Date: 2024/2/5
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import zipfile

import pandas as pd
from pandas import DataFrame

from CapitalControl.Constant import Constants as const

if __name__ == '__main__':
    csmar_ma_path = os.path.join(const.CSMAR_PATH, 'MA')
    csmar_ma_dfs = list()
    for year_period in ['1995_1999', '2000_2004', '2005_2009', '2010_2014', '2015_2019', '2020_2023']:
        with zipfile.ZipFile(os.path.join(csmar_ma_path, f'{year_period}_Total Transaction Information.zip'),
                             'r') as zip_ref:
            xlsx_file = [file for file in zip_ref.namelist() if file.endswith('.xlsx')][0]
            with zip_ref.open(xlsx_file) as excel_file_data:
                ma_df: DataFrame = pd.read_excel(
                    excel_file_data,
                    usecols=['EventID', 'Symbol', 'FirstDeclareDate', 'Buyer_en', 'Seller_en', 'IsSucceed',
                             'MARegionTypeID']).dropna(subset=['MARegionTypeID']).iloc[2:]
                csmar_ma_dfs.append(ma_df.loc[ma_df['MARegionTypeID'] != '1'].rename(columns={'Symbol': const.TICKER}))

    csmar_ma_df: DataFrame = pd.concat(csmar_ma_dfs, ignore_index=True)
    csmar_ma_df['FirstDeclareDate'] = pd.to_datetime(csmar_ma_df['FirstDeclareDate'], format='%Y-%m-%d')
    csmar_ma_df[const.YEAR] = csmar_ma_df['FirstDeclareDate'].dt.year
    csmar_ma_df.to_pickle(os.path.join(const.TEMP_PATH, '1995_2023_csmar_oversea_ma.pkl'))
