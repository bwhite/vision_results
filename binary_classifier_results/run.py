import server
import graphs
import glob
import os
import json
import base64
import imfeat

CACHE = {}
DATA = json.load(open('data.js'))


def list_class_feature_classifiers():
    return DATA.keys()


def get_confidence(class_feature_classifier_name):
    for data_id, data in DATA[class_feature_classifier_name].items():
        if data['is_positive'] is None:
            continue

        yield {'conf': float(data['confidence']),
               'polarity': data['is_positive'],
               'data_id': data_id}


def get_content(content_id):
    if content_id.endswith('.b16.html'):
        return '<img src="/content/%s.jpg" />' % base64.b16decode(content_id[:-9])
    image_data = open(base64.b16decode(content_id[:content_id.find('.b16')])).read()
    if content_id.endswith('.b16.thumb.jpg'):
        try:
            return CACHE[content_id]
        except KeyError:
            out_data = imfeat.image_tostring(imfeat.resize_image(imfeat.image_fromstring(image_data), 200, 200), 'JPEG')
            CACHE[content_id] = out_data
            return out_data
    return image_data


#_build_index()
server.run(list_class_feature_classifiers=list_class_feature_classifiers, get_confidence=get_confidence, port=8004,
           get_content=get_content, conf_graphs=[graphs.GooglePRChart(), graphs.GoogleROCChart()])
