import os

from .path_info import PathInfo


class Constants(PathInfo):
    TICKER = 'tic'
    TICKER2 = 'tic2'
    YEAR = 'year'
    COMPANY_NAME = 'comn'
    COMPANY_NAME_SHORT = 'comn_short'
    GVKEY = 'gvkey'

    STATE = 'state'

    # Variables for Shangdao ESG code
    SEC_INDUSTRY_CODE = 'secind'
    SHANGDAO_INDUSTRY_CODE1 = 'sdind1'
    SHANGDAO_INDUSTRY_CODE2 = 'sdind2'

    ESG_SCORE = 'esg_score'
    ESG_GOV_SCORE = 'esg_gov_score'
    ESG_RISK_SCORE = 'esg_risk_score'
    ENV_SCORE = 'env_score'
    SOCIAL_SCORE = 'social_score'
    CGOV_SCORE = 'cgov_score'

    # Variables for CSMAR balance sheet code
    CASH = 'A001101000'
    NET_FIXED_ASSETS = 'A001212000'
    NET_INTANGIBLE_ASSETS = 'A001218000'
    TOTAL_ASSETS = 'A001000000'
    TOTAL_CURRENT_LIABILITIES = 'A002100000'
    TOTAL_LONG_TERM_LIABILITIES = 'A002206000'
    TOTAL_LIABILITIES = 'A002000000'
    SHAREHOLDER_EQUITY = 'A003000000'

    # Variables for CSMAR income statement code
    TOTAL_PROFITS = 'B001000000'
    NET_PROFITS = 'B002000000'

    # Variables for CSMAR financial indicators
    LIABILITY_RATIO = 'F011201A'
    CASH_RATIO = 'F030201A'
    FIXED_ASSETS_RATIO = 'F030801A'
    INTASSETS_RATIO = 'F030901A'
    TANGIBLE_RATIO = 'F031001A'

    TOTAL_ROA_A = 'F050101B'
    TOTAL_ROA_B = 'F050102B'
    NET_ROA_A = 'F050201B'
    NET_ROA_B = 'F050202B'
    EBIT_TA_A = 'F051101B'
    RD_EXPENSE_RATIO = 'F053401B'

    EPS_1 = 'F090101B'
    EPS_2 = 'F090102B'
    EPS_3 = 'F090103B'
    EPS_4 = 'F090104B'

    MKVALT_A = 'F100801A'
    MKVALT_B = 'F100802A'
    TOBINQ_A = 'F100901A'
    TOBINQ_B = 'F100902A'
    TOBINQ_C = 'F100903A'
    TOBINQ_D = 'F100904A'
    BM_RATIO_A = 'F101001A'
    BM_RATIO_B = 'F101002A'
