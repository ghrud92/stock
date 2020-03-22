# Common util for stock.
import pandas as pd
import pathlib
import json
import re


_STATEMENT_TYPES = {
    'sid': str,
    'code': str,
    'company': str,
    'finance': list,
    'sales': int,
    'operating_income': int,
    'net_income': int,
    'operating_margin': float,
    'net_profit_margin': float,
    'roe': float,
    'debt_to_equities': float,
    'quick_ratio': float,
    'reserve_ratio': float,
    'eps': int,
    'per': float,
    'bps': int,
    'pbr': float,
    'dps': int,
    'dividend_yield_ratio': float,
    'dividend_payout_ratio': float,
    'term': str,
    'date': str,
    'year': int,
    'month': int,
    'consensus': bool
}


def download_stock_codes():
    base_url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?' \
               'method=download&searchType=13'
    df = pd.read_html(base_url, header=0)[0]
    return list(set(df.종목코드.map('{:06d}'.format).values))


def save_json(path, json_data):
    folder = re.search('.+/', path).group()
    folder = pathlib.Path(folder)
    if not folder.exists():
        folder.mkdir()
    with open(path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def load_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def convert_statement_types(statement_dict):
    result = {}
    for key in statement_dict.keys():
        value = statement_dict[key]
        if not value or value == '-':
            continue
        if type(value) == str:
            value = value.replace(",", "")
        result[key] = _STATEMENT_TYPES[key](value)
    return result
