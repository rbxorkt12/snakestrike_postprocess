import numpy as np
import glob
import cv2
from os.path import join


def check_videos_open(video_list):
    for cap in video_list:
        if not cap.isOpened():
            return False
    return True


def release_videos(video_list):
    for cap in video_list:
        cap.release()


def images2video(image_path, video_path, fps):
    img_array = []
    size = (1, 1)
    file_list = sorted(glob.glob(join(image_path, '*.jpg')),key=lambda x: int(x.split('\\')[-1].rstrip('.jpg')))
    for filename in file_list:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def horizontal_concat_videos(videos, output):
    cap_list = []
    try:
        for video in videos:
            cap_list.append(cv2.VideoCapture(video))
        frameWidth = int(cap_list[0].get(cv2.CAP_PROP_FRAME_WIDTH)) * len(cap_list)
        frameHeight = int(cap_list[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap_list[0].get(cv2.CAP_PROP_FPS))
        size = (frameWidth, frameHeight)
        out = cv2.VideoWriter(output, fourcc=cv2.VideoWriter_fourcc(*'DIVX'), fps=fps, frameSize=size)
        while check_videos_open(cap_list):
            both = 0  # initalize
            for i, cap in enumerate(cap_list):
                ret, frame = cap.read()
                if ret is False:
                    release_videos([*cap_list, out])
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    return
                if i == 0:
                    both = frame
                else:
                    both = np.concatenate((both, frame), axis=1)
            out.write(both)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        release_videos([*cap_list, out])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        release_videos([*cap_list])
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def vertical_concat_videos(videos, output):
    cap_list = []
    try:
        for video in videos:
            cap_list.append(cv2.VideoCapture(video))
        frameWidth = int(np.max(list(map(lambda x: x.get(cv2.CAP_PROP_FRAME_WIDTH), cap_list))))
        frameHeight = int(np.sum(list(map(lambda x: x.get(cv2.CAP_PROP_FRAME_HEIGHT), cap_list))))
        fps = int(cap_list[0].get(cv2.CAP_PROP_FPS))
        size = (frameWidth, frameHeight)
        out = cv2.VideoWriter(output, fourcc=cv2.VideoWriter_fourcc(*'DIVX'), fps=fps, frameSize=size)
        while check_videos_open(cap_list):
            both = 0  # initalize
            for i, cap in enumerate(cap_list):
                ret, frame = cap.read()
                if ret is False:
                    release_videos([*cap_list, out])
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    return
                if i == 0:
                    both = frame
                else:
                    h, w, c = both.shape
                    h1, w1, c1 = frame.shape
                    if w < w1:  # resize right img to left size
                        both = cv2.resize(both, (w1, h))
                    elif w > w1:
                        frame = cv2.resize(frame, (w, h))
                    both = np.concatenate((both, frame), axis=0)
            out.write(both)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        release_videos([*cap_list, out])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        release_videos([*cap_list])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
