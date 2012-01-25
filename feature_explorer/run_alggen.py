import server
import graphs
import glob
import os
import run
import cass_alggen as cass
run.cass = cass
import base64
import imfeat
from run import *


CACHE = {}
#INDEX = None


#def _build_index():
#    global INDEX
#    INDEX = {}
#    paths = ['/mnt/nfsdrives/shared/voc07_thumbs', '/mnt/nfsdrives/data/vision_data/voc07/VOCdevkit/VOC2007/JPEGImages/']
#    for path in paths:
#        for fn in glob.glob('%s/*.jpg' % path):
#            INDEX[os.path.basename(fn)] = fn
#    print('Index Built: [%d] Files' % len(INDEX))

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
server.run(list_classes=list_classes, list_feature_classifiers=list_feature_classifiers, get_confidence=get_confidence, port=8004,
           get_content=get_content, conf_graphs=[graphs.GooglePRChart(), graphs.GoogleROCChart()])
