#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: figure1_trend_of_dgfl
# @Date: 2024/11/6
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt


if __name__ == '__main__':
    dgfl_df: DataFrame = pd.read_csv('240816_firm_year_level_data.csv',
                                     usecols=['Symbol', 'Year', 'TotalLoan', 'NumGuarantee'])

    df = dgfl_df.loc[dgfl_df['Year'].apply(lambda x: 2010 <= x <= 2018)].groupby('Year').sum()
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot TotalLoan on the left y-axis
    ax1.plot(df.index, df['TotalLoan'], marker='o', linestyle='-', color='b', label='Total Guaranteed Loan Amount')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Total Guaranteed Loan Amount', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True)

    # Create a second y-axis for NumGuarantee
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['NumGuarantee'], marker='o', linestyle='-', color='g', label='Number of Guarantees')
    ax2.set_ylabel('Number of Guarantees', color='g')
    ax2.tick_params(axis='y', labelcolor='g')

    # Adding the title
    plt.title('Annual Trend of Total Guaranteed Loan Amount and Number of Guarantees')

    plt.savefig('figure1_DGFL_trends.png')

    # Displaying the plot
    plt.show()
