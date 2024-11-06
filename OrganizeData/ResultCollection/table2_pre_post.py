#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: table2_pre_post
# @Date: 2024/11/6
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


import pandas as pd
from scipy import stats


# Function to calculate the mean, median, N, and t-test
def compare_groups(treated, control, variable):
    treated_mean = treated[variable].mean()
    treated_median = treated[variable].median()
    treated_n = treated[variable].count()

    control_mean = control[variable].mean()
    control_median = control[variable].median()
    control_n = control[variable].count()

    difference = treated_mean - control_mean
    t_stat, p_value = stats.ttest_ind(treated[variable].dropna(), control[variable].dropna(), equal_var=False)

    significance = ''
    if p_value < 0.01:
        significance = '***'
    elif p_value < 0.05:
        significance = '**'
    elif p_value < 0.1:
        significance = '*'

    return (round(treated_mean, 4), round(treated_median, 4), treated_n, round(control_mean, 4),
            round(control_median, 4), control_n, round(difference, 4), f'({round(p_value, 4)})', significance)


if __name__ == '__main__':

    # Sample data loading (replace with actual data loading code)
    data = pd.read_stata('20241104_cc_reg_data_v6.dta')

    # Filtering pre and post periods
    data_pre = data[data['year'] < 2014]
    data_post = data[data['year'] >= 2014]

    # Define the treated and control groups
    treated_pre = data_pre[data_pre['has_guarantee'] == 1]
    control_pre = data_pre[data_pre['has_guarantee'] == 0]
    treated_post = data_post[data_post['has_guarantee'] == 1]
    control_post = data_post[data_post['has_guarantee'] == 0]

    # List of variables to compare
    variables = ['CAPEX_lat_1', 'CAPEX_RDI_lat_1', 'size', 'TobinQ', 'OCF_lat', 'soe', 'lev', 'top1', 'sale_growth']

    # Creating summary tables for pre and post periods
    summary_pre = []
    summary_post = []

    for var in variables:
        # Pre-period comparison
        t_mean, t_median, t_n, c_mean, c_median, c_n, diff, p_val, sig = compare_groups(treated_pre, control_pre, var)
        summary_pre.append([var, t_mean, t_median, t_n, c_mean, c_median, c_n, diff, p_val, sig])

        # Post-period comparison
        t_mean, t_median, t_n, c_mean, c_median, c_n, diff, p_val, sig = compare_groups(treated_post, control_post, var)
        summary_post.append(
            [var, t_mean, t_median, t_n, c_mean, c_median, c_n, diff, p_val, sig])

    # Convert summaries to DataFrames
    columns = ['Variable', 'Treated Mean', 'Treated Median', 'Treated N', 'Control Mean', 'Control Median', 'Control N',
               'Difference', 'p-value', 'Significance']
    summary_pre_df = pd.DataFrame(summary_pre, columns=columns)
    summary_post_df = pd.DataFrame(summary_post, columns=columns)

    # Display results
    print("Panel A: Pre-Event Period")
    print(summary_pre_df)
    print("\nPanel B: Post-Event Period")
    print(summary_post_df)

    summary_pre_df.to_excel('Table2_summary_pre.xlsx')
    summary_post_df.to_excel('Table2_summary_post.xlsx')