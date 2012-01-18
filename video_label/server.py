import gevent.monkey
gevent.monkey.patch_all()
import bottle
import argparse
import glob
import base64
import uuid
import cPickle as pickle
import random
import json
import time


@bottle.get('/')
def index():
    return bottle.static_file('index.html', root='./')


@bottle.put('/result/')
def result():
    request = bottle.request.json
    response = RESPONSE_DB[request['data_id']]
    assert response['user_id'] == request['user_id']
    assert 'user_event' not in response
    response['user_event'] = request['event']
    response['end_time'] = time.time()
    return make_data(request['user_id'])


def urlsafe_uuid():
    return base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]


@bottle.get('/:secret/results.js')
def admin_results(secret):
    if secret == SECRET:
        return json.dumps(RESPONSE_DB)


@bottle.get('/user.js')
def user():
    return {"user_id": urlsafe_uuid()}


@bottle.get('/:user_id/data.js')
def data(user_id):
    return make_data(user_id)


def make_data(user_id):
    event = random.choice(list(FRAME_DB))
    video = random.choice(list(FRAME_DB[event]))
    out = {"images": [],
           "data_id": urlsafe_uuid()}
    RESPONSE_DB[out['data_id']] = {'event': event, 'video': video,
                                   'user_id': user_id, 'start_time': time.time()}
    for frame in FRAME_DB[event][video]:
        out['images'].append({"src": 'frames/%s.jpg' % PATH_TO_KEY[frame], "width": 150})
    return out


@bottle.get('/config.js')
def config():
    return CONFIG


@bottle.get('/frames/:frame_key')
def frames(frame_key):
    frame_key = frame_key.rsplit('.', 1)[0]
    try:
        cur_data = open(KEY_TO_PATH[frame_key]).read()
    except KeyError:
        bottle.abort(404)
    bottle.response.content_type = "image/jpeg"
    return cur_data
  

def main():
    global PATH_TO_KEY, KEY_TO_PATH, FRAME_DB, ARGS, CONFIG, RESPONSE_DB, SECRET
    # Setup secret
    SECRET = urlsafe_uuid()
    print('Results URL:  /%s/results.js' % SECRET)
    # Setup DB
    RESPONSE_DB = {}
    with open('db.pkl') as fp:
        FRAME_DB, _ = pickle.load(fp)
    frames = []
    for event in FRAME_DB:
        for video in FRAME_DB[event]:
            for frame in FRAME_DB[event][video]:
                frames.append(frame)
    random.shuffle(frames)
    PATH_TO_KEY = {}
    KEY_TO_PATH = {}
    for frame in frames:
        key = urlsafe_uuid()
        PATH_TO_KEY[frame] = key
        KEY_TO_PATH[key] = frame
    print('Done loading DB')
    # Setup Config
    CONFIG = json.load(open('config.js'))
    # Setup Server
    parser = argparse.ArgumentParser(description="Serve ")
    parser.add_argument('--port', type=str, help='run webpy on this port',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')


if __name__ == "__main__":
    main()
