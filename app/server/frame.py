#!/usr/bin/env python2.7
from pytube import YouTube
import math
import imageio
import os
from PIL import Image

def get_youtube_id(url):
    return url.split("v=")[-1] if len(url.split("v=")) == 2 else url.rsplit('/', 1)[-1]

#this function downloads a video by url
#and uses openCV to return its image array
def extract_files(url, max_frame=100, fps=5):
    videoFolder = './server/videos'
    if "server" not in os.listdir("."):
        os.mkdir("server")
        os.mkdir("server/videos")
    else:
        if "videos" not in os.listdir("server"):
            os.mkdir("server/videos")
    if "frames" not in os.listdir(videoFolder):
        os.mkdir("./server/videos/frames")
    # Set filename to id
    yt = YouTube(url)
    video_id = get_youtube_id(url)
    yt.set_filename(video_id)
    # download video of certain quality
    video = yt.get('mp4', '360p')
    try:
        print("downloading videos...")
        video.download(videoFolder)
        print("done downloading video")
    except OSError:
        print("didn't need to download video")
        pass

    frames = []
    fname = "%s/%s.mp4" % (videoFolder, str(video_id))
    vid = imageio.get_reader(fname, 'ffmpeg')
    fps = vid.get_meta_data()['fps']
    dur = int(math.floor(vid.get_meta_data()['duration']))
    
    i = 0
    print("saving frames...")
    index = 0
    frameFolder = "./server/videos/frames/{0}".format(video_id)
    os.mkdir(frameFolder)
    while i < dur:
        frame = vid.get_data(int(math.floor(i * fps)))
        frames.append(frame)
        img = Image.fromarray(frame, 'RGB')
        img.save(frameFolder + "/frame-" + str(index) + ".jpg")
        i += 5
        index += 1
        if index >= max_frame:
            break
    print("done saving frames.")
    vid.close()
    return frames