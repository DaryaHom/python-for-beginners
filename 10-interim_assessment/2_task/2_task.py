"""
Задание №2.
Дополнительное задание: 
Используя библиотеки для Web Scraping соберите список 20 последних новостей компании ПАО Ростелеком: 
https://www.company.rt.ru/ir/news_calendar/

Необходимо сохранить данные по следующим блокам в список словарей Python
- дата новости
- заголовок новости
- ссылка на полную статью о новости
"""

import requests
from bs4 import BeautifulSoup

base_path = 'https://www.company.rt.ru/'
url = 'ir/news_calendar/'

response = requests.get(base_path+url)
soup = BeautifulSoup(response.text, "html.parser")

news = []
items = soup.find_all('div', class_=['item', 'news_item'], limit=20)

for i in items:
    try:
        title = i.find('div', class_='item_text').string
        link = i.find('a', class_='item_link')['href']
        date = i.find('span', class_='item_date-day').string + ' ' + \
                i.find('span', class_='item_date-month').string 

        news.append({
                'date': date,
                'title': title,
                'link': link
            })
    except KeyError | AttributeError:
        continue

for i in range(len(news)):
    print(f'{i+1}: {news[i]}')
