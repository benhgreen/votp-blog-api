import time

import os
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

BASE_SITE_URL = 'http://visionsofthepastblog.com/'
MONGODB_URI = os.environ.get('MONGODB_URI')

def main():
    browser = webdriver.Firefox()
    db = MongoClient(MONGODB_URI)['votp-db']

    browser.get(BASE_SITE_URL)
    time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    no_of_pagedowns = 40

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(.75)
        no_of_pagedowns-=1

    post_elems = browser.find_elements_by_tag_name("article")

    for post in post_elems:
        post_id = post.get_attribute('id')
        post_url = post.find_element_by_tag_name('a').get_attribute('href')
        post_title = post.find_element_by_tag_name('a').text
        img_url = post.find_element_by_tag_name('img').get_attribute('src')

        if not db.post_list.find_one({'id': post_id}):
            db.post_list.insert_one({
                'id': post_id,
                'url': post_url,
                'title': post_title,
                'img': img_url
            })
            print('inserted new post ' + post_url)

if __name__ == '__main__':
    main()