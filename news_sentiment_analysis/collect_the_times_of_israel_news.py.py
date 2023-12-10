import re
import time
from datetime import datetime
from datasets import Dataset
from selenium import webdriver
from bs4 import BeautifulSoup

PAUSE_BETWEEN_QUERIES = 3 # A pause duration in sec. between the requests

def get_url(timestamp):
    return (f"https://www.timesofisrael.com/wp-content/themes/rgb/ajax/topics_for_terms.php?"
            f"taxonomy=post_tag&term_id=97462&post_tag=&before_date={timestamp}&numposts=15&"
            f"is_mobile=false&post_type=&is_load_more=0")


def get_all_updates(post_id):
    return (f"https://www.timesofisrael.com/wp-content/themes/rgb/ajax/load_liveblog_entries.php?"
            f"post_id={post_id}&latest_update=0")


driver = webdriver.Chrome()
oct7timestamp = datetime(2023, 10, 7).timestamp()
current_timestamp = datetime.today().timestamp()
data = {"url": [], "datetime": [], "author": [], "title": [], "text": [], "provider": [], "source": []}

while current_timestamp > oct7timestamp:
    next_url = get_url(current_timestamp)
    driver.get(next_url)
    html = driver.page_source
    body = BeautifulSoup(html, 'html.parser')

    for day_block in body.find_all('div', class_=re.compile('item template1 news')):
        datetime_block = day_block.find('div', class_='date')
        if datetime_block is not None:
            datetime_ = datetime.strptime(datetime_block.text, '%B %d, %Y, %I:%M %p')  # November 18, 2023, 4:13 am
            current_timestamp = int(datetime_.timestamp())
            if current_timestamp < oct7timestamp:
                break
        else:
            datetime_ = None

        url_block = day_block.find('div', 'headline')
        if url_block is not None:
            url = url_block.find('a')
            url = url.get('href')
        else:
            url = None

        print(url, datetime_)

        if url:
            time.sleep(PAUSE_BETWEEN_QUERIES)
            driver.get(url)
            html = driver.page_source
            day_body = BeautifulSoup(html, 'html.parser')

            post_id_tag = day_body.find('div', id=re.compile('liveblog-'))
            post_id = post_id_tag.get('id').split('-')[1]

            driver.get(get_all_updates(post_id))
            html += driver.page_source
            day_body = BeautifulSoup(html, 'html.parser')

            for post_block in day_body.find_all('div', id=re.compile('liveblog-entry')):
                datetime_timestamp = int(post_block.find('span', attrs={"data-timestamp": True}).get('data-timestamp'))
                post_datetime = datetime.fromtimestamp(datetime_timestamp)

                title = post_block.find('h4').find('a').text
                post_url = post_block.find('h4').find('a').get('href')

                author_block = post_block.find('div', class_='byline')
                author = author_block.find('a').text if author_block is not None else None

                text_lst = []
                for text_block in post_block.find_all('p'):
                    if text_block is not None:
                        text_lst.append(text_block.text)

                text = "\n".join(text_lst)

                print('\t', title, post_datetime)
                data['url'].append(post_url)
                data['title'].append(title)
                data['datetime'].append(post_datetime.strftime('%Y-%m-%dT%H:%M:%S') if post_datetime else None)
                data['author'].append(author if author else '-')
                data['text'].append(text)
                data['provider'].append('The Times of Israel')
                data['source'].append('site-live-news')

ds = Dataset.from_dict(data)
print(ds)
ds.save_to_disk('toi_news_ds')

driver.quit()