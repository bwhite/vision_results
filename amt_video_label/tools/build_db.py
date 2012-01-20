import glob
import cPickle as pickle
import os
import math

data_root = '../data/'


def prune_frame_paths(frame_paths, target_frames=10):
    target_frames = float(target_frames)
    # Remove every other path - + - +
    frame_paths = frame_paths[::2]
    return frame_paths[::int(max(1, math.ceil(len(frame_paths) / target_frames)))]


def main():
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
            frame_paths = prune_frame_paths(sorted(glob.glob(video_path + '/*')))
            for frame_path in frame_paths:
                frame_db[event][video].append(frame_path)

    with open('../db.pkl', 'w') as fp:
        pickle.dump(frame_db, fp, -1)
main()
