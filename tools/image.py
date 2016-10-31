#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import color
from ast import literal_eval as to_tuple
from glob import glob
from shutil import (
    copyfile, rmtree
)
from helpers import pc



# def avg_color_data(images_format):
#     result = {}
#     _dict = {}
#     _list = []
#     images = glob(images_format)

#     n=0
#     for img in images:
#         sys.stdout.write("\r {} of {}".format(n, len(images)))
#         sys.stdout.flush()
#         avg = color.avg_color(img)
#         #avg = color.dominant(img)
#         if not _dict.has_key("{}{}{}".format(*avg)):
#             _dict[ "{}{}{}".format(*avg) ] = img
#             _list.append( avg )
#         n += 1

#     return (_list, _dict)


# def build_set(_list, _dict):
#     image_list = []
#     _list.sort(key=lambda rgb: color.luminance(*rgb))
#     for c_item in _list:
#         #complementary = color.complementary_rgb(c_item)
#         #closest_color = color.find_closest(complementary, _list)
#         #close_colors = color.find_close(complementary, _list)

#         #for x in range(4):
#         image_list.append(_dict.get("{}{}{}".format(*c_item)))

#         #for x in range(4):
#         #image_list.append(_dict.get("{}{}{}".format(*closest_color)))

#     return image_list


# def avg_color_data(images_format):
#     result = {}
#     _dict = {}
#     _list = []

#     for img in glob(images_format):
#         sys.stdout.write("\rProcessing: {}".format(img))
#         sys.stdout.flush()
#         pal = color.extract_palette(img,1)

#         rgb_color = (0,0,0)
#         try:
#             rgb_color = map(to_tuple, color.in_format(pal, 'rgb'))[0]
#             _list.append(rgb_color)
#         except:
#             pass

#         if not _dict.has_key("{}".format(rgb_color)):
#             _dict["{}".format(rgb_color)] = [img]
#         else:
#             _dict["{}".format(rgb_color)].append(img)


#     print _dict

#     return (_list, _dict)

def color_data(images_format, by_type='avg'):
    result = {}
    _dict = {}
    _list = []
    images = glob(images_format)
    total = len(images)

    n = 0
    for img in images:
        sys.stdout.write("\r {} of {} ({}%)".format(n, total, pc(n, total)))
        sys.stdout.flush()
        if by_type == 'avg':
            rgb_color = color.avg_color(img)
        elif by_type == 'dom':
            rgb_color = color.dominant(img)
        n += 1

        if not _dict.has_key("{}".format(rgb_color)):
            _dict["{}".format(rgb_color)] = [img]
        else:
            _dict["{}".format(rgb_color)].append(img)

    return _dict


def build_set(_dict, sort_by='hsv'):
    image_list = []
    _list = _dict.keys()
    if sort_by == 'hls':
        _list.sort(key=lambda rgb: color.rgb_to_hls(to_tuple(rgb)))
    elif sort_by == 'hsl':
        _list.sort(key=lambda rgb: color.rgb_to_hsl(to_tuple(rgb)))
    elif sort_by == 'hsv':
        _list.sort(key=lambda rgb: color.rgb_to_hsv(to_tuple(rgb)))
    elif sort_by == 'lum':
        _list.sort( key=lambda rgb: color.luminance(to_tuple(rgb)))

    rgb_list = map(to_tuple, _list)
    for c_item in _list:
        image_list += _dict.get("{}".format(c_item))

    return image_list


def build_set_complementary(_dict, sort_by='hsv', every=4):
    image_list = []
    _list = _dict.keys()
    if sort_by == 'hls':
        _list.sort(key=lambda rgb: color.rgb_to_hls(to_tuple(rgb)))
    elif sort_by == 'hsl':
        _list.sort(key=lambda rgb: color.rgb_to_hsl(to_tuple(rgb)))
    elif sort_by == 'hsv':
        _list.sort(key=lambda rgb: color.rgb_to_hsv(to_tuple(rgb)))
    elif sort_by == 'lum':
        _list.sort( key=lambda rgb: color.luminance(to_tuple(rgb)))

    n = 0
    for c_item in _list:
        if n % every == 0:
            complementary = color.complementary_rgb(to_tuple(c_item))
            closest_color = color.find_closest(complementary, map(to_tuple, _list))
            image_list += _dict.get("{}".format(str(closest_color)))

        image_list += _dict.get("{}".format(c_item))
        n += 1

    return image_list


def copy(image_list, image_dest, image_format):
    img_n=0
    for img in image_list:
        if os.path.isfile(img):
            copyfile(img,
                     os.path.join(image_dest,
                                  image_format % img_n))
        img_n += 1

    return None


def clean_cache(cache_dirs):
    map(rmtree, cache_dirs)


def make_cache(cache_dirs):
    map(os.makedirs, cache_dirs)
