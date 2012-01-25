import gevent
import math
import json
import base64
from gevent import monkey
monkey.patch_all()
import bottle
bottle.debug(True)

ARGS = {}
RESULTS = []
RESULT_VALS = None
GRAPHS = ''


def run(**kw):
    global ARGS
    ARGS = kw
    bottle.run(host='0.0.0.0', port=ARGS['port'], server='gevent')


@bottle.route('/body/:class_name/:feature_classifier_name/:page_num/')
def body(class_name, feature_classifier_name, page_num, per_page=25):
    global RESULTS, RESULT_VALS, GRAPHS
    class_name = base64.b16decode(class_name)
    feature_classifier_name = base64.b16decode(feature_classifier_name)
    page = int(page_num)
    page_nums = {}
    if (class_name, feature_classifier_name) != RESULT_VALS:
        RESULT_VALS = class_name, feature_classifier_name
        RESULTS = sorted(list(ARGS['get_confidence'](feature_classifier_name, class_name)), key=lambda x: x['conf'], reverse=True)
        page_nums = dict((str(x), str(x)) for x in range(int(math.ceil(len(RESULTS) / float(per_page)))))
        if ARGS['conf_graphs']:
            GRAPHS = [x.client(RESULTS) for x in ARGS['conf_graphs']]
    data = bottle.template('body', results=RESULTS[per_page * page : per_page * (page + 1)])
    return '%s(%s)' % (bottle.request.GET['callback'],
                       json.dumps({'data': data, 'page_nums': page_nums, 'graphs': GRAPHS}))


@bottle.route('/')
def index():
    return bottle.template('index',
                           classes=ARGS['list_classes'](),
                           feature_classifiers=ARGS['list_feature_classifiers']())


@bottle.route('/graph/:obj_id/:data_id')
def graph(obj_id, data_id):
    for x in ARGS['conf_graphs']:
        if str(id(x)) == obj_id:
            return x.server(data_id)


@bottle.route('/content/:content_id')
def content(content_id):
    return ARGS['get_content'](content_id)
