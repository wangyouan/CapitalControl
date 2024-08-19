#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: step03_aggregrate_to_firm_year_level
# @Date: 2024/8/17
# @Author: WONG Kar Xiong
# @Email: wangyouan@gamil.com


import pandas as pd
import numpy as np


# Function to determine the year based on SignDate, StartDate, and DeclareDate
def determine_year(row):
    if pd.notna(row['SignDate']):
        return row['SignDate'].year
    elif pd.notna(row['StartDate']):
        return row['StartDate'].year
    elif pd.notna(row['DeclareDate']):
        return row['DeclareDate'].year
    else:
        return np.nan  # This row will be removed later


# =============================================================================
if __name__ == '__main__':
    df = pd.read_csv("240816_Event_level_data.csv", error_bad_lines=False)

    # Step 3
    # Remove rows where both 'ShortName' and 'FullName' are NaN
    df2 = df.dropna(subset=['ShortName', 'FullName'], how='all')

    df2['Year'] = df2.apply(determine_year, axis=1)
    df2 = df2.dropna(subset=['Year'])  # drop if no Year generated
    df2 = df2.drop(index=1678)  # error

    # Convert to numeric and identify rows with conversion errors
    df2['LoanAmount'] = df2['LoanAmount'].fillna(0)
    df2['LoanAmount'] = pd.to_numeric(df2['LoanAmount'], errors='coerce')
    df2['TotalLoan'] = df2.groupby(['Symbol', 'Year'])['LoanAmount'].transform('sum')

    # Group by 'Symbol' and 'Year' and count the number of occurrences
    df2['NumGuarantee'] = df2.groupby(['Symbol', 'Year'])['Symbol'].transform('count')

    df3 = df2[['InstitutionID', 'Symbol', 'SecurityID', 'ShortName', 'FullName',
               'TotalLoan', 'Year', 'NumGuarantee']]
    df3 = df3.drop_duplicates(['Symbol', 'Year'])
    df3 = df3.sort_values(by=['Symbol', 'Year'])

    df3.to_csv('240816_firm_year_level_data.csv', index=False, encoding='utf-8-sig')
