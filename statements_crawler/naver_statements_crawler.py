# Refers to https://engkimbs.tistory.com/624?category=762758

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as Bs

from common import stock_util

SAVE_PATH = "data/naver_statements.json"

def crawl_short_statement(i, code):
    url = 'https://finance.naver.com/item/main.nhn?code=%s' % code
    print(f"crawl {i} from {url}")
    html = requests.get(url).text
    soup = Bs(html, 'html.parser')
    result = {'code': code}

    company = soup.select("div.h_company div.wrap_company a")[0]
    company = company.get_text()
    result['company'] = company

    finance_html = soup.select("div.section.cop_analysis div.sub_section")
    if len(finance_html) == 0:
        print("Statement table doesn't exist", code, company)
        result['finance'] = []
        return result

    finance_html = finance_html[0]
    th_data = [item.get_text().strip() for item in
               finance_html.select("thead th")]
    annual_date = th_data[3:7]
    quarter_date = th_data[7:13]

    finance_index = ['sales', 'operating_income', 'net_income', 'operating_margin', 'net_profit_margin', 'roe', 'debt_to_equities',
                     'quick_ratio', 'reserve_ratio', 'eps', 'per', 'bps', 'pbr', 'dps', 'dividend_yield_ratio', 'dividend_payout_ratio']

    finance_data = [item.get_text().strip() for item in
                    finance_html.select("td")]
    if len(finance_data) == 1:
        print("Statement table is empty", code, company)
        result['finance'] = []
        return result

    finance_data = np.array(finance_data)
    finance_data.resize(len(finance_index), 10)

    finance_annual = pd.DataFrame(
        data=finance_data[:, :4], index=finance_index, columns=annual_date)
    finance_annual = finance_annual.to_dict()
    for i in finance_annual.keys():
        finance_annual[i]['term'] = 'annual'
        finance_annual[i]['date'] = i

    finance_quarter = pd.DataFrame(
        data=finance_data[:, 4:], index=finance_index, columns=quarter_date)
    finance_quarter = finance_quarter.to_dict()
    for i in finance_quarter.keys():
        finance_quarter[i]['term'] = 'quarter'
        finance_quarter[i]['date'] = i

    result['finance'] = list(finance_annual.values()) + list(finance_quarter.values())
    return result


if __name__ == "__main__":
    stock_codes = stock_util.download_stock_codes()
    statements = [crawl_short_statement(i, code) for i, code in enumerate(stock_codes)]
    stock_util.save_json(SAVE_PATH, statements)
