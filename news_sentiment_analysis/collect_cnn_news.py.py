import re
import time
import pandas as pd
from datetime import datetime, timedelta
from datasets import Dataset
from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_all_updates(browser):
    '''
    Get all news on the page by imitating scrolling by human
    '''
    for _ in tqdm(range(20)):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-1005)")
        time.sleep(1)


browser = webdriver.Chrome()
START_DATE = datetime(2023, 10, 27)
data = {"url": [], "datetime": [], "author": [], "title": [], "text": [], "provider": [], "source": []}
current_time = START_DATE

while current_time <= datetime.today():
    print(current_time.strftime('%m-%d-%y'))
    day_url = f"https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-{current_time.strftime('%m-%d-%y')}"
    browser.get(day_url)
    get_all_updates(browser)

    page = browser.page_source
    body = BeautifulSoup(page, 'html.parser')

    posts_block = body.find('div', attrs={"id": "posts-and-button"})
    if posts_block is not None:
        print("Var#1")
        for post_block in posts_block.find_all('article'):
            header_block = post_block.find('header')

            dt_parts = header_block.find('span').text.strip().split()  # 12:09 a.m. ET, October 30, 2023
            if len(dt_parts) == 6:
                dt_str = f"{dt_parts[5]}-{dt_parts[3]}-{dt_parts[4].strip(',')}T{dt_parts[0]}{('AM' if dt_parts[1] == 'a.m.' else 'PM')}"
            else:
                hours, minutes = int(dt_str[0]), int(dt_str[2])
                post_dt = datetime.now() - timedelta(hours=hours, minutes=minutes)
            post_dt = datetime.strptime(dt_str, "%Y-%B-%dT%I:%M%p")

            title = header_block.find("h2").text

            byline = header_block.find('p')
            if byline:
                author = " ".join(byline.text.strip().split()[2:])
            else:
                author = None

            text_block = post_block.find('div', class_=re.compile("content-rendered"))
            text_lst = []
            for p in text_block.find_all('p'):
                if p is not None and p.text.strip() != "":
                    text_lst.append(p.text)
            text = '\n'.join(text_lst)

            post_id = post_block.get("id")
            post_url = f"{day_url}/{post_id}"
            # https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-10-29-23/h_102d988c6184b8575600a3f5192f9dbf

            print('\t', post_dt, title, post_url)
            data['url'].append(post_url)
            data['title'].append(title)
            data['datetime'].append(post_dt.strftime('%Y-%m-%dT%H:%M:%S') if post_dt else None)
            data['author'].append(author if author else '-')
            data['text'].append(text)
            data['provider'].append('CNN')
            data['source'].append('site-live-news')
    else:
        print("Var#2")
        posts_block = body.find('div', class_="live-story__items-container")
        if posts_block is not None:
            for post_block in posts_block.find_all('article'):
                post_dt = datetime.strptime(post_block.get('data-last-updated').split('.')[0],
                                            "%Y-%m-%dT%H:%M:%S")  # 2023-10-27T02:52:53.364Z

                header_block = post_block.find('header', class_="live-story-post__header")
                title = header_block.find("h2").text
                byline = header_block.find('span', class_="live-story-post__byline")
                if byline:
                    author = " ".join(byline.text.strip().split()[2:])
                else:
                    author = None

                text_block = post_block.find('section', class_="live-story-post__body").find('div', class_="live-story-post__content")
                text_lst = []
                for p in text_block.find_all('p'):
                    if p is not None and p.text.strip() != "":
                        text_lst.append(p.text)
                text = '\n'.join(text_lst)

                url_block = post_block.find('div', class_="social-share_compact__share-links")
                btn = url_block.find('button', attrs={"aria-label": "copy link to clipboard"})
                post_url = btn.get("data-url")

                print('\t', post_dt, title, post_url)
                data['url'].append(post_url)
                data['title'].append(title)
                data['datetime'].append(post_dt.strftime('%Y-%m-%dT%H:%M:%S') if post_dt else None)
                data['author'].append(author if author else '-')
                data['text'].append(text)
                data['provider'].append('CNN')
                data['source'].append('site-live-news')

    current_time += timedelta(days=1)

ds = Dataset.from_dict(data)
print(ds)
ds.save_to_disk('cnn_news_ds')

browser.close()
