import json

import os
from flask import Flask, request
from pymongo import MongoClient
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)

MONGODB_URI = os.environ.get('MONGO_URL')

@app.route('/posts')
def post_list():
    db = MongoClient(MONGODB_URI)['votp-db']
    ret = [{
        'id': post.get('id'),
        'img': post.get('img'),
        'title': post.get('title'),
        'url': post.get('url')
           } for post in db.get_collection('post_list').find()]
    return json.dumps({'post_list': ret}, indent=4)


@app.route('/post')
def post_detail():
    post_id = request.args.get('id')
    db = MongoClient(MONGODB_URI)['votp-db']

    post = db.get_collection('post_detail').find_one({'id': post_id})
    return json.dumps({
        'result': {
            'pic_urls': post.get('pic_urls'),
            'id': post.get('id'),
            'title': post.get('title'),
            'post_time': post.get('post_time'),
            'post_paragraphs': post.get('post_paragraphs')
        }
    }, indent=4)

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()