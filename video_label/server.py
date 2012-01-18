import gevent.monkey
gevent.monkey.patch_all()
import bottle
import argparse
import glob
import base64
import uuid


@bottle.get('/')
def index():
    return bottle.static_file('index.html', root='./')


@bottle.put('/result/')
def result():
    request = bottle.request.json
    user_id = request['user_id']
    data_id = request['data_id']
    event = request['event']
    print(request)
    return make_data(user_id)


@bottle.get('/user.js')
def user():
    return {"user_id": base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]}


@bottle.get('/:user_id/data.js')
def data(user_id):
    return make_data(user_id)


def make_data(user_id):
    return {"images": [{"src": "http://farm4.static.flickr.com/3267/3112736300_03ee1bb778.jpg", "width": 150},
                       {"src": "http://farm4.static.flickr.com/3267/3112736300_03ee1bb778.jpg", "width": 150},
                       {"src": "http://farm4.static.flickr.com/3267/3112736300_03ee1bb778.jpg", "width": 150}],
            "data_id": 'adataid0'}


@bottle.get('/config.js')
def config():
    return bottle.static_file('config.js', root='./')
  


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve ")
    parser.add_argument('--port', type=str, help='run webpy on this port',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
