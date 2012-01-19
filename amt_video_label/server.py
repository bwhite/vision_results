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
    assert request['user_id'] in USERS_DB
    response = RESPONSE_DB[request['data_id']]
    assert response['user_id'] == request['user_id']
    # Don't double count old submissions
    if 'user_event' not in response:
        response['user_event'] = request['event']
        response['end_time'] = time.time()
        USERS_DB[request['user_id']]['tasks_finished'] += 1
        if response['user_event'] == response['event']:
            USERS_DB[request['user_id']]['tasks_correct'] += 1
    return make_data(request['user_id'])


def urlsafe_uuid():
    return base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]


@bottle.get('/:secret/results.js')
def admin_results(secret):
    if secret == SECRET:
        return json.dumps(RESPONSE_DB)


@bottle.get('/:secret/users.js')
def admin_users(secret):
    if secret == SECRET:
        return json.dumps(USERS_DB)


@bottle.get('/user.js')
def user():
    user_id = urlsafe_uuid()
    USERS_DB[user_id] = {'query_string': bottle.request.query_string,
                         'remote_addr': bottle.request.remote_addr,
                         'tasks_finished': 0,
                         'tasks_correct': 0,
                         'tasks_viewed': 0,
                         'start_time': time.time()}
    USERS_DB[user_id].update(dict(bottle.request.query))
    return {"user_id": user_id}


@bottle.get('/:user_id/data.js')
def data(user_id):
    return make_data(user_id)


def make_data(user_id):
    event = random.choice(list(FRAME_DB))
    video = random.choice(list(FRAME_DB[event]))
    cur_user = USERS_DB[user_id]
    if ARGS.mode != 'standalone' and cur_user['tasks_finished'] >= ARGS.num_tasks:
        cur_user['end_time'] = time.time()
        pct_correct = cur_user['tasks_correct'] / float(cur_user['tasks_finished'])
        pct_completed = cur_user['tasks_finished'] / float(cur_user['tasks_viewed'])
        query_string = '&'.join(['%s=%s' % x for x in [('assignmentId', cur_user.get('assignmentId', 'NoId')),
                                                       ('pct_correct', pct_correct),
                                                       ('pct_completed', pct_completed),
                                                       ('tasks_finished', cur_user['tasks_finished']),
                                                       ('tasks_viewed', cur_user['tasks_viewed']),
                                                       ('tasks_correct', cur_user['tasks_correct']),
                                                       ('time_taken', cur_user['end_time'] - cur_user['start_time'])]])
        return {'submit_url': '%s/mturk/externalSubmit?%s' % (cur_user.get('turkSubmitTo', 'http://www.mturk.com'), query_string)}
    out = {"images": [],
           "data_id": urlsafe_uuid()}
    RESPONSE_DB[out['data_id']] = {'event': event, 'video': video,
                                   'user_id': user_id, 'start_time': time.time()}
    for frame in FRAME_DB[event][video]:
        out['images'].append({"src": 'frames/%s.jpg' % PATH_TO_KEY[frame], "width": 150})
    cur_user['tasks_viewed'] += 1
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
    global PATH_TO_KEY, KEY_TO_PATH, FRAME_DB, ARGS, CONFIG, RESPONSE_DB, SECRET, USERS_DB
    # Parse command line
    parser = argparse.ArgumentParser(description="Serve ")
    parser.add_argument('--port', help='Run on this port',
                        default='8080')
    parser.add_argument('--num_tasks', help='Number of tasks per worker (unused in standalone mode)',
                        default=500, type=int)
    parser.add_argument('--mode', type=str, help='Number of tasks per worker',
                        default='standalone', choices=['amt', 'standalone'])
    ARGS = parser.parse_args()
    # Setup secret
    SECRET = urlsafe_uuid()
    open('SECRET', 'w').write(SECRET)
    print('Results URL:  /%s/results.js' % SECRET)
    print('Users URL:  /%s/users.js' % SECRET)
    # Setup DB
    USERS_DB = {}
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
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')


if __name__ == "__main__":
    main()