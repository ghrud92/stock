# Refers to
# https://medium.com/@doyourquant/dart-%EC%98%A4%ED%94%88-api%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EC%9E%AC%EB%AC%B4%EC%A0%9C%ED%91%9C-%ED%81%AC%EB%A1%A4%EB%A7%81-with-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%B9%84%EC%A0%95%EA%B7%9C%EC%A0%81%EC%9D%B8-%EC%BD%94%EB%94%A9-24f4acc7cdbe
# https://dart-fss.readthedocs.io/en/latest/welcome.html

import os
import requests
import OpenDartReader
import stock_util

from bs4 import BeautifulSoup as Bs


api_key = os.environ.get('DART_API_SECRET')
# url = 'https://opendart.fss.or.kr/api/corpCode.xml?' + 'crtfc_key=' + api_key
# html = requests.get(url)
# soup = Bs(html.content, 'html.parser')
# print(soup)
dart = OpenDartReader(api_key)
print(dart.list('005930'))

if __name__ == '__main__':
    stock_codes = stock_util.download_stock_codes()

