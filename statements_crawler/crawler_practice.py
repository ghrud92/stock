# Refers to https://engkimbs.tistory.com/613?category=762758

import requests
from bs4 import BeautifulSoup as Bs

URL = "http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html"
page = requests.get(URL)
soup = Bs(page.content, 'html.parser')
# print(soup.prettify())

p_tags = soup.find_all('p', class_='outer-text')
# print(p_tags)

first_id_tag = soup.find_all(id="first")
# print(first_id_tag)

div_p_tag = soup.select("div p")
print(div_p_tag)
