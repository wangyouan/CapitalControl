#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Filename: path_info
# @Date: 2024/2/3
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import socket


class PathInfo(object):
    # PROJECT_PATH = '/mnt/d/Onedrive/Temp/Projects/CapitalControl'
    COMPUTER_NAME = socket.gethostname()
    if COMPUTER_NAME == 'wyaamd-server001':
        PROJECT_PATH = '/home/user/projects/DGFL'
        OUTPUT_PATH = os.path.join(PROJECT_PATH, 'output')

        # DATABASE_PATH = '/mnt/d/Onedrive/Documents/data'
        DATABASE_PATH = '/home/user/data'
    else:
        PROJECT_PATH = r'D:\Onedrive\Temp\Projects\CapitalControl'
        OUTPUT_PATH = os.path.join(PROJECT_PATH, 'regression_data')

        # DATABASE_PATH = '/mnt/d/Onedrive/Documents/data'
        DATABASE_PATH = r'D:\Onedrive\Documents\data'

        # NCA_DATA_PATH = r'D:\Onedrive\Projects\NCA\data'
        # NCA_PROJECT_PATH = r'D:\Onedrive\Temp\Projects\NCA'
        # NCA_TEMP_PATH = os.path.join(NCA_PROJECT_PATH, 'temp')
        # NCA_OUTPUT_PATH = os.path.join(NCA_PROJECT_PATH, 'regression_data')

    DATA_PATH = os.path.join(PROJECT_PATH, 'data')
    TEMP_PATH = os.path.join(PROJECT_PATH, 'temp')
    REGRESSION_RESULT_PATH = os.path.join(PROJECT_PATH, 'regression_results')
    CSMAR_PATH = os.path.join(DATABASE_PATH, 'csmar')
    SHANGDAO_PATH = os.path.join(DATABASE_PATH, 'shangdao')
    COMPUSTAT_PATH = os.path.join(DATABASE_PATH, 'compustat')
