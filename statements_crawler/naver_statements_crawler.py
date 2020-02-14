# Refers to https://engkimbs.tistory.com/624?category=762758

import requests
from bs4 import BeautifulSoup as Bs

URL = "https://finance.naver.com/item/main.nhn?code=005930"

samsung_electronic = requests.get(URL)
html = samsung_electronic.text

soup = Bs(html, 'html.parser')
