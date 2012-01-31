import numpy as np
import itertools
import json
import requests
import time
import random
import scikits.learn


def google_extended_encoding(num):
    d = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.'
    num = int(num)
    if num < 0 or num > 4095:
        raise ValueError('[%s] cannot be represented!' % num)
    num = max(0, min(4095, num))
    return d[num / 64] + d[num % 64]


def xy_chart_post(xys, title):
    xys = [x for x in xys if not np.isnan(x).any()]
    xys = sorted(random.sample(xys, min(3000, len(xys))))
    xs, ys = zip(*xys)
    ys = [google_extended_encoding(x * 4095) for x in ys]
    xs = [google_extended_encoding(x * 4095) for x in xs]
    chd = 'e:%s,%s' % (''.join(xs), ''.join(ys))
    data = {'chxt': 'x,y', 'chd': chd, 'chxs': '0,676767,7.5,0,l,676767|1,676767,7.5,0,l,676767',
            'chts': '676767,8.5', 'chs': '200x200', 'cht': 'lxy', 'chtt': title, 'chls': '1', 'chid': str(time.time())}
    return requests.post('https://chart.googleapis.com/chart', data).content


class GooglePRChart(object):

    def __init__(self):
        self.charts = {}

    def client(self, results):
        polarities = []
        confs = []
        for x in results:
            polarities.append(int(x['polarity']))
            confs.append(x['conf'])
        data_id = str(len(self.charts))
        p, r, t = scikits.learn.metrics.precision_recall_curve(np.array(polarities), np.array(confs))
        print('Thresh: m[%s] M[%s]' % (np.min(t), np.max(t)))
        rps = zip(r, p)
        self.charts[data_id] = xy_chart_post(rps, 'PR+Plot')
        return {'html': '<img src="/graph/%d/%s" id="pr_chart"/>' % (id(self), data_id), 'js': ""}

    def server(self, data_id):
        return self.charts[data_id]


class GoogleROCChart(object):

    def __init__(self):
        self.charts = {}

    def client(self, results):
        polarities = []
        confs = []
        for x in results:
            polarities.append(int(x['polarity']))
            confs.append(x['conf'])
        data_id = str(len(self.charts))
        fpr, tpr, t = scikits.learn.metrics.roc_curve(np.array(polarities), np.array(confs))
        print('Thresh: m[%s] M[%s]' % (np.min(t), np.max(t)))
        fprtprs = zip(fpr, tpr)
        self.charts[data_id] = xy_chart_post(fprtprs, 'ROC+Plot')
        return {'html': '<img src="/graph/%d/%s" id="roc_chart"/>' % (id(self), data_id), 'js': ""}

    def server(self, data_id):
        return self.charts[data_id]
