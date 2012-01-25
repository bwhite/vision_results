import pycassa


FEATURE_CLASSIFIERS = None
CLASSES = None

cass = None  # NOTE(brandyn): This must be overriden


def list_feature_classifiers():
    global FEATURE_CLASSIFIERS
    if FEATURE_CLASSIFIERS is None:
        FEATURE_CLASSIFIERS = cass.get_column_family('feat_info').get('feature_classifiers',
                                                                      read_consistency_level=pycassa.ConsistencyLevel.QUORUM).keys()
    return FEATURE_CLASSIFIERS


def list_classes():
    global CLASSES
    if CLASSES is None:
        CLASSES = cass.get_column_family('feat_info').get('classes',
                                                          read_consistency_level=pycassa.ConsistencyLevel.QUORUM).keys()
    return CLASSES


def get_confidence(feature_classifier_name, pos_class_name, neg_class_names=None):
    col = 'conf %s' % (feature_classifier_name)
    if neg_class_names is None:
        class_names = list_classes()
    else:
        class_names = set([pos_class_name] + neg_class_names)
    for data_id, data in cass.get_column_family('feat_data').get_range(read_consistency_level=pycassa.ConsistencyLevel.ALL, columns=[col, 'class_names']):
        if 'class_names' in data:
            if set(data['class_names'].split()).intersection(class_names):
                yield {'conf': float(data[col]),
                       'class_names': data['class_names'].split(),
                       'polarity': pos_class_name in data['class_names'].split(),
                       'data_id': data_id}
        else:
            print('Warning: Row [%s] doesnt have a class_names column!' % data_id)
