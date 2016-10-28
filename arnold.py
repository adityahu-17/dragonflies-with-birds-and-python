#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import random
from utils import (
    color, image, video
)
import os
import sys
import argparse
import tempfile

import time
import datetime as dt


__file = os.path.basename(__file__)
TEMP_DIR = tempfile.mkdtemp("-arnold")
CACHE_DIR = os.path.join(TEMP_DIR, "cache")
FV_DIR = os.path.join(CACHE_DIR, "from")
TV_DIR = os.path.join(CACHE_DIR, "to")
IMG_FORMAT = "img%09d.jpg"
IMG_GLOB = "img*.jpg"

def msg(msg, verbose=False):
    if verbose:
        print ( msg )


def write_file(filename, content):
    f = open(filename, 'w')
    f.write("\n".join(content))
    f.close()


def test(input_video):
    output_video = "cut_{}".format(input_video.replace("/","_"))
    video_length = float(video.length(input_video))
    dur = 1.0
    time_run = 0

    x = 0
    filelist = []
    while time_run < video_length:
        time_run += dur
        print( time_run, video_length)
        video.cut(time_run, dur,
                  input_video, "cut_{}_{}".format(x,output_video))
        filelist += ["file 'cut_{}_{}'".format(x,output_video)] * 5
        x+=1

    write_file("list_{}.txt".format(output_video), filelist)
    video.concat("list_{}.txt".format(output_video), "final_{}".format(output_video))

    sys.exit(0)

def clean(filelist):
    for filename in filelist:
        try:
            os.remove(filename)
        except OSError:
            pass


def arnoldise(input_video, output_video):
    video_length = int(float(video.length(input_video)))

    filelist = []
    for x in range(video_length):
        t = x if x > 9 else "0{}".format(x)

        video.cut("00:00:{}".format(t), "00:00:02",
                  input_video, "cut_{}_{}".format(x,output_video))

        filelist += ["cut_{}_{}".format(x,output_video)] * random.randrange(2,10)

    write_file("list_{}.txt".format(output_video),
               map(lambda f: "file '{}'".format(f), filelist))
    video.concat("list_{}.txt".format(output_video), output_video)
    clean(filelist + ["list_{}.txt".format(output_video)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test',
                        action="store_true",
                        help="test. doesn't do anything.")
    parser.add_argument('-i', '--input-video',
                        type=str,
                        help="Use this video as source")
    parser.add_argument('-o', '--output-video',
                        type=str,
                        required=False,
                        help="Use this video as source. Default: output.mp4")

    args = parser.parse_args()

    if args.test:
        test(args.input_video)
    if args.input_video:
        arnoldise(args.input_video,
                  args.output_video or "output.mp4")
    else:
        print("{} -h".format(__file))
