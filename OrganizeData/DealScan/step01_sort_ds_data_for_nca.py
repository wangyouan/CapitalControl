#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: step01_sort_ds_data_for_nca
# @Date: 2024/2/28
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
Possible useful keys
Deal_Amount	Deal_Amount_Converted
Seniority_Type Secured

Number_of_Lenders
"""

import os

import pandas as pd
from pandas import DataFrame

from CapitalControl.Constant import Constants as const


def check_facility_purpose_dummy(row, purpose_set):
    return int(row['Primary_Purpose'] in purpose_set or row['Secondary_Purpose'] in purpose_set or
               row['Tertiary_Purpose'] in purpose_set or row['Deal_Purpose'] in purpose_set)


def count_covenant_number(covenant_info):
    if hasattr(covenant_info, 'split'):
        covenants = covenant_info.split(',')
        return len(covenants)
    else:
        return 0


if __name__ == '__main__':
    ds_df: DataFrame = pd.read_csv(os.path.join(r'D:\Users\wangy\Downloads', 'miibpaehauuoflhu.csv'))
    us_ds_df: DataFrame = ds_df.loc[ds_df['Country'] == 'United States'].copy()
    us_ds_tic_df: DataFrame = us_ds_df.dropna(subset=['Ticker', 'Parent_Ticker'], how='all')
    us_ds_tic_df.loc[:, const.TICKER] = us_ds_tic_df['Ticker'].fillna(us_ds_tic_df['Parent_Ticker'])
    us_ds_tic_df['Tranche_Active_Date'] = pd.to_datetime(us_ds_tic_df['Tranche_Active_Date'])
    us_ds_tic_df['Tranche_Maturity_Date'] = pd.to_datetime(us_ds_tic_df['Tranche_Maturity_Date'])
    us_ds_tic_df.loc[:, const.YEAR] = us_ds_tic_df['Tranche_Active_Date'].dt.year

    us_ds_tic_df.loc[:, 'isSecured'] = (us_ds_tic_df['Secured'] == 'Yes').astype(int)
    us_ds_tic_df.loc[:, 'isSenior'] = us_ds_tic_df['Seniority_Type'].apply(
        lambda x: isinstance(x, str) and 'senior' in x.lower()).astype(int)
    us_ds_tic_df.loc[:, 'Life'] = us_ds_tic_df.loc[:, 'Tenor_Maturity'] / 12
    us_ds_tic_df.loc[:, 'Life'] = us_ds_tic_df['Life'].fillna(
        (us_ds_tic_df.loc[:, 'Tranche_Maturity_Date'] - us_ds_tic_df.loc[:, 'Tranche_Active_Date']) / pd.Timedelta(
            '365 days'))
    us_ds_tic_df.loc[:, 'termMix'] = us_ds_tic_df.loc[:, 'Tranche_Amount'] / us_ds_tic_df.loc[:, 'Deal_Amount']
    us_ds_tic_df.loc[:, 'termMix'] = us_ds_tic_df.loc[:, 'termMix'].apply(lambda x: 1 if x > 1 else x)
    us_ds_tic_df.loc[:, 'isRevolver'] = (us_ds_tic_df['Deal_Refinancing'] == 'Yes').astype(int)
    us_ds_tic_df.loc[:, 'isSponsored'] = (us_ds_tic_df['Sponsored'] == 'Yes').astype(int)
    us_ds_tic_df.loc[:, 'finCovenantNum'] = us_ds_tic_df['All_Covenants_Financial'].apply(count_covenant_number)
    us_ds_tic_df.loc[:, 'genCovenantNum'] = us_ds_tic_df['All_Covenants_General'].apply(count_covenant_number)

    us_ds_tic_df.loc[:, 'isPerformance'] = (us_ds_tic_df['Performance_Pricing_Grid'] == 'Yes').astype(int)
    us_ds_tic_df.loc[:, 'isWorkCapital'] = us_ds_tic_df.apply(check_facility_purpose_dummy, axis=1,
                                                              purpose_set={'Working capital', 'Trade finance',
                                                                           'General Purpose/Refinance',
                                                                           'Commercial paper backup',
                                                                           'Receivables Program'})
    us_ds_tic_df.loc[:, 'isInvestment'] = us_ds_tic_df.apply(check_facility_purpose_dummy, axis=1,
                                                             purpose_set={"Real estate loan",
                                                                          "Capital expenditure",
                                                                          "Equipment Upgrade/Construction",
                                                                          "IPO Related Financing",
                                                                          "Purchase of Software/Services",
                                                                          "Purchase of Hardware",
                                                                          "Infrastructure",
                                                                          "Project Finance"})
    us_ds_tic_df.loc[:, 'isCorporate'] = us_ds_tic_df.apply(check_facility_purpose_dummy, axis=1,
                                                            purpose_set={"Sponsored Buyout", "Takeover",
                                                                         "General Purpose/Refinance",
                                                                         "Capital expenditure",
                                                                         "Collateralized Debt Obligation (CDO)",
                                                                         "Equipment Upgrade/Construction",
                                                                         "Recapitalization",
                                                                         "General Purpose/Stock Repurchase",
                                                                         "Restructuring", "Merger",
                                                                         "Debtor-in-possession",
                                                                         "Management Buyout",
                                                                         "Acquisition",
                                                                         "Leveraged Buyout",
                                                                         "Dividend Recapitalization",
                                                                         "Spinoff", "Credit Enhancement",
                                                                         "Project Finance",
                                                                         "Guarantee"})
    us_ds_tic_df.loc[:, 'isTakeOver'] = us_ds_tic_df.apply(check_facility_purpose_dummy, axis=1,
                                                           purpose_set={"Takeover",
                                                                        "Sponsored Buyout",
                                                                        "Standby takeover defense",
                                                                        "Merger",
                                                                        "Acquisition",
                                                                        "Leveraged Buyout",
                                                                        "Management Buyout"})
    us_ds_tic_df.loc[:, 'isDebtRepay'] = us_ds_tic_df.apply(check_facility_purpose_dummy, axis=1,
                                                            purpose_set={"General Purpose/Refinance",
                                                                         "Recapitalization",
                                                                         "Restructuring",
                                                                         "Debtor-in-possession",
                                                                         "Exit financing",
                                                                         "Credit Enhancement",
                                                                         "Dividend Recapitalization"})

    useful_columns = [const.TICKER, const.YEAR, 'Number_of_Lenders', 'All_In_Spread_Drawn_bps', 'isDebtRepay',
                      'isTakeOver', 'isCorporate', 'isInvestment', 'isWorkCapital', 'isPerformance', 'genCovenantNum',
                      'finCovenantNum', 'isRevolver', 'termMix', 'Life', 'isSecured', 'isSenior', 'Borrower_Id',
                      'Perm_ID', 'Borrower_Name', 'State_Province', 'City', 'LPC_Deal_ID', 'Deal_PermID', 'Deal_Amount',
                      'LPC_Tranche_ID', 'Tranche_PermID', 'isSponsored', 'Lender_Id', 'Lender_Parent_Name',
                      'Lender_Parent_Id', 'Lender_Name']
    us_ds_useful_df: DataFrame = us_ds_tic_df.loc[:, useful_columns].copy()
    us_ds_useful_df.to_pickle(os.path.join(const.TEMP_PATH, '20240314_us_ds_dataset.pkl'))
