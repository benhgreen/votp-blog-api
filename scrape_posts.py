import os
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

BASE_SITE_URL = 'http://visionsofthepastblog.com/'
MONGODB_URI = os.environ.get('MONGODB_URI')

def main():
    db = MongoClient(MONGODB_URI)['votp-db']
    index_collection = db.get_collection('post_list')
    post_collection = db.get_collection('post_detail')

    for post in index_collection.find():
        if not post_collection.find_one(post.get('id')):
            resp = requests.get(post.get('url'))
            soup = BeautifulSoup(resp.text, 'html.parser')

            pic_urls = []
            for pic in soup.find_all(attrs='gallery-item'):
                pic_urls.append(pic.find('img').attrs.get('src'))

            post_time = soup.find(attrs='entry-date published').get('datetime')

            post_paragraphs = [str(p.contents[0])
                               for p in soup.find(attrs='entry-content').find_all('p')]

            post_collection.insert_one({
                'pic_urls': pic_urls,
                'id': post.get('id'),
                'title': post.get('title'),
                'post_time': post_time,
                'post_paragraphs': post_paragraphs
            })

            print('scraped post ' + post.get('id'))

if __name__ == '__main__':
    main()