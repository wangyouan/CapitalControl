#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: path_info
# @Date: 2024/2/3
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os


class PathInfo(object):
    # PROJECT_PATH = '/mnt/d/Onedrive/Temp/Projects/CapitalControl'
    PROJECT_PATH = r'D:\Onedrive\Temp\Projects\CapitalControl'
    TEMP_PATH = os.path.join(PROJECT_PATH, 'temp')
    OUTPUT_PATH = os.path.join(PROJECT_PATH, 'regression_data')

    # DATABASE_PATH = '/mnt/d/Onedrive/Documents/data'
    DATABASE_PATH = r'D:\Onedrive\Documents\data'
    CSMAR_PATH = os.path.join(DATABASE_PATH, 'csmar')
    SHANGDAO_PATH = os.path.join(DATABASE_PATH, 'shangdao')
    COMPUSTAT_PATH = os.path.join(DATABASE_PATH, 'compustat')

    NCA_DATA_PATH = r'D:\Onedrive\Projects\NCA\data'
    NCA_PROJECT_PATH = r'D:\Onedrive\Temp\Projects\NCA'
    NCA_TEMP_PATH = os.path.join(NCA_PROJECT_PATH, 'temp')
    NCA_OUTPUT_PATH = os.path.join(NCA_PROJECT_PATH, 'regression_data')