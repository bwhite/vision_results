import glob
import cPickle as pickle
import os

data_root = 'data/'

# Build initial frame structure
frame_db = {}  # [event][video] = frames
for event_path in glob.glob('%s/*' % data_root):
    if not os.path.isdir(event_path):
        continue
    event = os.path.basename(event_path)
    frame_db[event] = {}
    for video_path in glob.glob(event_path + '/*'):
        if not os.path.isdir(video_path):
            continue
        video = os.path.basename(video_path)
        frame_db[event][video] = []
        for frame_path in sorted(glob.glob(video_path + '/*'))[::2]:
            frame_db[event][video].append(frame_path)

# Gather textual descriptions
description_db = {} # [event]
for event in frame_db:
    description_db[event] = open('%s/%s.txt' % (data_root, event)).read()

with open('db.pkl', 'w') as fp:
    pickle.dump((frame_db, description_db), fp, -1)
