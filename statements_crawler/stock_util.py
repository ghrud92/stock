# Common util for stock.
import pandas as pd
import pathlib
import json
import re


def download_stock_codes():
    base_url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?' \
               'method=download&searchType=13'
    df = pd.read_html(base_url, header=0)[0]
    return list(df.종목코드.map('{:06d}'.format).values)


def save_json(path, json_data):
    folder = re.search('.+/', path).group()
    folder = pathlib.Path(folder)
    if not folder.exists():
        folder.mkdir()
    with open(path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
        