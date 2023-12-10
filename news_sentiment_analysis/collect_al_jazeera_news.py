import re
import time
import html
import pandas as pd
from datetime import datetime
from datasets import Dataset
from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_all_updates(browser):
    '''
    Get all news on the page by imitating scrolling by human
    '''
    for _ in tqdm(range(100)):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5500)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5450)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5400)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5350)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5300)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5250)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5200)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5150)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5100)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5050)")
        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-5000)")
        time.sleep(.5)

        page = browser.page_source
        body = BeautifulSoup(page, 'html.parser')
        res = body.find_all(string="Welcome to our live coverage")
        if res:
            break

data = {"url": [], "datetime": [], "author": [], "title": [], "text": [], "provider": [], "source": []}
BASE_URL = 'https://www.aljazeera.com'

next_url = 'https://www.aljazeera.com/news/liveblog/2023/11/25/israel-hamas-live-news-prisoners-and-captives-welcomed-home'
oct7timestamp = datetime(2023, 10, 7).timestamp()
current_timestamp = datetime.today().timestamp()
browser = webdriver.Chrome()

while next_url and current_timestamp >= oct7timestamp:
    browser.get(next_url)
    get_all_updates(browser)

    page = browser.page_source
    body = BeautifulSoup(page, 'html.parser')
    year, month, day = next_url.split('/')[5:8]
    current_timestamp = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').timestamp()
    print(f"{year}-{month}-{day}", next_url)

    for post_block in body.find_all('div', class_='card-live'):
        time_block = post_block.find('div', class_='date-relative__time')
        if time_block is not None:
            post_time = time_block.text.strip()[1:-1].split()[0]
            post_datetime = datetime.strptime(f"{year}-{month}-{day}T{post_time}:00", '%Y-%m-%dT%H:%M:%S')
        else:
            post_datetime = None

        title_block = post_block.find('h2')
        title = title_block.text if title_block is not None else None

        author = None

        whatsapp_link = post_block.find('a', attrs={'aria-label': 'Share on Whatsapp'})
        if whatsapp_link is not None:
            post_url = html.unescape(whatsapp_link.get('href').split('?')[1].split('=')[1])
        else:
            post_url = None

        text_lst = []
        for p in post_block.find('div', class_='card-live__content').find_all('p'):
            if p is not None:
                text_lst.append(p.text)
        text = '\n'.join(text_lst)

        print('\t', post_datetime, title)
        data['url'].append(post_url)
        data['title'].append(title)
        data['datetime'].append(post_datetime.strftime('%Y-%m-%dT%H:%M:%S') if post_datetime else None)
        data['author'].append(author if author else '-')
        data['text'].append(text)
        data['provider'].append('Al Jazeera')
        data['source'].append('site-live-news')

    next_url_block = post_block.find('a', href=re.compile('/news/liveblog/2023'))
    if next_url_block is not None:
        next_url = BASE_URL + next_url_block.get('href')
    else:
        next_url = None

ds = Dataset.from_dict(data)
print(ds)
ds.save_to_disk('aljazeera_news_ds')

browser.close()