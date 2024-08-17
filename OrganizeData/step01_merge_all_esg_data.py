#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: step01_merge_all_esg_data
# @Date: 2024/2/3
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import zipfile
from io import BytesIO

from tqdm import tqdm, trange
import pandas as pd
from pandas import DataFrame

from Constant import Constants as const

if __name__ == '__main__':
    year_esg_dfs = list()
    for year in trange(2015, 2022):
        zip_file_path = os.path.join(const.SHANGDAO_PATH, '{}.zip'.format(year))

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            excel_files = [file for file in zip_ref.namelist() if file.endswith('.xlsx')]
            for excel_file in excel_files:
                with zip_ref.open(excel_file) as excel_file_data:
                    esg_df: DataFrame = pd.read_excel(BytesIO(excel_file_data.read()), engine='openpyxl', nrows=1)
                    if esg_df.shape[1] == 13:
                        esg_df.columns = [const.TICKER, const.COMPANY_NAME, const.COMPANY_NAME_SHORT,
                                          const.SEC_INDUSTRY_CODE, const.SHANGDAO_INDUSTRY_CODE1,
                                          const.SHANGDAO_INDUSTRY_CODE2, const.YEAR, const.ESG_SCORE,
                                          const.ESG_GOV_SCORE, const.ESG_RISK_SCORE, const.ENV_SCORE,
                                          const.SOCIAL_SCORE, const.CGOV_SCORE]
                    elif esg_df.shape[1] == 14 and year < 2020:
                        esg_df.columns = [const.TICKER, const.COMPANY_NAME, const.COMPANY_NAME_SHORT,
                                          const.SEC_INDUSTRY_CODE, const.SHANGDAO_INDUSTRY_CODE1,
                                          const.SHANGDAO_INDUSTRY_CODE2, const.YEAR, const.ESG_SCORE,
                                          const.ESG_GOV_SCORE, const.ESG_RISK_SCORE, const.ENV_SCORE,
                                          const.SOCIAL_SCORE, const.CGOV_SCORE, 'Comments']
                    elif year >= 2020:
                        esg_df.columns = [const.TICKER, const.TICKER2, const.COMPANY_NAME, const.COMPANY_NAME_SHORT,
                                          const.SEC_INDUSTRY_CODE, const.SHANGDAO_INDUSTRY_CODE1,
                                          const.SHANGDAO_INDUSTRY_CODE2, const.YEAR, const.ESG_SCORE,
                                          const.ESG_GOV_SCORE, const.ESG_RISK_SCORE, const.ENV_SCORE,
                                          const.SOCIAL_SCORE, const.CGOV_SCORE]
                    else:
                        raise ValueError('Wrong number of columns {}'.format(esg_df.shape[1]))

                    year_esg_dfs.append(esg_df)

    all_esg_df: DataFrame = pd.concat(year_esg_dfs, axis=0, ignore_index=True)
    all_esg_df.to_pickle(os.path.join(const.TEMP_PATH, '2015_2021_shangdao_all_esg_data.pkl'))
