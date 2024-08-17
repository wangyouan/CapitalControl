#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: step01_sort_er_guarantee_data
# @Date: 2024/4/6
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import re
import zipfile

import pandas as pd
from pandas import DataFrame

from Constant import Constants as const


def check_for_letters(s):
    pattern = re.compile(r'[A-Za-z]', re.S)
    result = re.findall(pattern, s)
    return len(result) > 0


if __name__ == '__main__':
    zip_file_path = os.path.join(const.CSMAR_PATH, '2005_2023_ER_guarantee.zip')
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        csv_files = [file for file in zip_ref.namelist() if file.endswith('.csv')]
        with zip_ref.open(csv_files[0]) as csv_file_data:
            er_df: DataFrame = pd.read_csv(csv_file_data, on_bad_lines='skip')

    er_guarantee_name_list = er_df['GuaranteeName'].drop_duplicates()
    er_eng_name_list = er_guarantee_name_list[er_guarantee_name_list.apply(check_for_letters)]

    er_foreign_df: DataFrame = er_df.loc[er_df['GuaranteeName'].isin(er_eng_name_list)].copy()
    er_foreign_df['DeclareDate'] = pd.to_datetime(er_foreign_df['DeclareDate'], format='%Y-%m-%d')
    er_foreign_df2: DataFrame = er_foreign_df.dropna(subset=['Symbol'])
    er_symbol = er_foreign_df2['Symbol'].drop_duplicates()

    er_symbol.to_pickle(os.path.join(const.TEMP_PATH, '20240406_er_guarantee_symbol_list.pkl'))
