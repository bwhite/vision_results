import server
import graphs
import glob
import os
import run
import cass_aladdin as cass
run.cass = cass
from run import *

INDEX = None


def _build_index():
    global INDEX
    INDEX = {}
    paths = ['/mnt/nfsdrives/data/trecvid/TRECVID/events/E%.3d/' % x for x in range(1, 16)]
    paths += ['/mnt/nfsdrives/data/LDC2011E41/MED11TrainingDataPart2/events/E%.3d' % x for x in range(1, 16)]
    paths.append('/mnt/nfsdrives/data/trecvid/TRECVID/video/DEV/')
    paths.append('/mnt/nfsdrives/data/LDC2011E41/MED11TrainingDataPart2/video/DEV/')
    for path in paths:
        for fn in glob.glob('%s/*.mp4' % path):
            INDEX[os.path.basename(fn)] = fn
    for fn in glob.glob('/mnt/nfsdrives/shared/aladdin_thumbs/*.jpg'):
        INDEX[os.path.basename(fn)] = fn
    print('Index Built: [%d] Files' % len(INDEX))


def get_content(content_id):
    if content_id[-5:] == '.html':
        return '<video src="/content/%s.mp4" width="320" height="240" controls preload></video>' % content_id[:-5]
    if content_id[-4:] == '.jpg':
        content_id = content_id[:-4] + '.mp4.jpg'
    return open(INDEX[content_id]).read()


_build_index()
server.run(list_classes=list_classes, list_feature_classifiers=list_feature_classifiers, get_confidence=get_confidence, port=8090,
           get_content=get_content, conf_graphs=[graphs.GooglePRChart(), graphs.GoogleROCChart()])
