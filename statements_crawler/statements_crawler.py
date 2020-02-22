# Refers to https://engkimbs.tistory.com/624?category=762758

import requests
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup as Bs


def download_stock_codes():
    base_url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?' \
               'method=download&searchType=13'
    df = pd.read_html(base_url, header=0)[0]
    return df.종목코드.map('{:06d}'.format)


def crawl_statement(code):
    base_url = 'https://finance.naver.com/item/main.nhn?code='

    html = requests.get(base_url + code).text
    soup = Bs(html, 'html.parser')

    finance_html = soup.select("div.section.cop_analysis div.sub_section")[0]
    th_data = [item.get_text().strip() for item in
               finance_html.select("thead th")]
    annual_date = th_data[3:7]
    quarter_date = th_data[7:13]

    finance_index = [item.get_text().strip() for item in
                     finance_html.select("th.h_th2")][3:]

    finance_data = [item.get_text().strip() for item in
                    finance_html.select("td")]
    finance_data = np.array(finance_data)
    finance_data.resize(len(finance_index), 10)

    finance_date = annual_date + quarter_date

    finance = pd.DataFrame(data=finance_data[0:, 0:], index=finance_index,
                           columns=finance_date)

    annual_finance = finance.iloc[:, :4]
    quarter_finance = finance.iloc[:, 4:]
    print(annual_finance)
    print(quarter_finance)


if __name__ == "__main__":
    stock_codes = list(download_stock_codes().values)
    crawl_statement(stock_codes[0])
