#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: step02_merge_shangdao_esg_data_with_financial_data
# @Date: 2024/2/4
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import zipfile

import pandas as pd
from pandas import DataFrame

from CapitalControl.Constant import Constants as const


def sort_csmar_data(csmar_df: DataFrame):
    csmar_df['Accper'] = pd.to_datetime(csmar_df.Accper, format='%Y-%m-%d')
    csmar_df2: DataFrame = csmar_df.rename(columns={'Stkcd': const.TICKER}).sort_values(
        by=[const.TICKER, 'Accper'], ascending=True)
    csmar_df2.loc[:, const.YEAR] = csmar_df2['Accper'].dt.year
    csmar_df3: DataFrame = csmar_df2.drop_duplicates(subset=[const.TICKER, const.YEAR], keep='last')
    return csmar_df3.drop(['Accper'], axis=1)


if __name__ == '__main__':
    # load csmar balance sheet file
    with zipfile.ZipFile(os.path.join(const.CSMAR_PATH, '1990_2023_Balance Sheet.zip'), 'r') as zip_ref:
        with zip_ref.open('FS_Combas.csv') as csv_file:
            cs_bs_df: DataFrame = pd.read_csv(csv_file,
                                              usecols=['Stkcd', 'Accper', const.CASH, const.TOTAL_CURRENT_LIABILITIES,
                                                       const.NET_FIXED_ASSETS, const.NET_INTANGIBLE_ASSETS,
                                                       const.TOTAL_ASSETS, const.TOTAL_LONG_TERM_LIABILITIES,
                                                       const.TOTAL_LIABILITIES, const.SHAREHOLDER_EQUITY])
            cs_bs_df2: DataFrame = sort_csmar_data(cs_bs_df)

    # load csmar financial indicators
    cs_fi_path = os.path.join(const.CSMAR_PATH, 'Financial Indicators')
    cs_fi_dict = {'1990_2023_Solvency': (const.LIABILITY_RATIO,),
                  '1990_2023_Ratio Structure': (
                      const.CASH_RATIO, const.FIXED_ASSETS_RATIO, const.INTASSETS_RATIO, const.TANGIBLE_RATIO),
                  '1990_2023_Earning Capacity': (const.TOTAL_ROA_B, const.TOTAL_ROA_A, const.NET_ROA_A, const.NET_ROA_B,
                                                 const.EBIT_TA_A, const.RD_EXPENSE_RATIO),
                  '1990_2023_Index per Share': (const.EPS_1, const.EPS_2, const.EPS_3, const.EPS_4),
                  '1990_2023_Relative Value Index': (const.MKVALT_A, const.MKVALT_B, const.TOBINQ_A, const.TOBINQ_B,
                                                     const.TOBINQ_C, const.TOBINQ_D, const.BM_RATIO_A,
                                                     const.BM_RATIO_B)}
    cs_fi_df = DataFrame()

    for file_name in cs_fi_dict:
        with zipfile.ZipFile(os.path.join(cs_fi_path, f'{file_name}.zip'), 'r') as zip_ref:
            usecols = ['Stkcd', 'Accper']
            usecols.extend(cs_fi_dict[file_name])
            load_file_name = [i for i in zip_ref.namelist() if i.endswith('.xlsx')][0]
            with zip_ref.open(load_file_name) as xlsx_file:
                cs_df: DataFrame = pd.read_excel(xlsx_file, usecols=usecols, engine='openpyxl').iloc[2:]
                cs_df2: DataFrame = sort_csmar_data(cs_df)
                if cs_fi_df.empty:
                    cs_fi_df: DataFrame = cs_df2.copy()
                else:
                    cs_fi_df: DataFrame = cs_fi_df.merge(cs_df2, on=[const.TICKER, const.YEAR], how='outer')

    cs_fi_df[const.TICKER] = cs_fi_df[const.TICKER].astype(int)
    cs_df_all: DataFrame = cs_bs_df2.merge(cs_fi_df, how='outer', on=[const.TICKER, const.YEAR])
    cs_df_all.to_pickle(os.path.join(const.TEMP_PATH, '1990_2023_CSMAR_financial_data.pkl'))
