#!/usr/bin/env python
# coding:utf-8
# some simple functions
"""
Copyright (c) 2017 shakala developers (https://github.com/LandGrey/shakala)
License: GNU GENERAL PUBLIC LICENSE Version 3
"""

from __future__ import unicode_literals
import os
import platform


# order preserving
def unique(seq, idfun=None):
    if idfun is None:
        def idfun(x): return x
    seen = {}
    results = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        results.append(item)
    return results


def get_all_file(original_directory):
    filepaths = []
    results_file_list = []
    for rootpath, subdirsname, filenames in os.walk(original_directory):
        filepaths.extend([os.path.abspath(os.path.join(rootpath, _)) for _ in filenames])
    if len(filepaths) > 0:
        for _ in filepaths:
            results_file_list.append(_)
    return results_file_list


# judge run platform
def is_Windows():
    return platform.system() == "Windows"


def is_Linux():
    return platform.system() == "Linux"


def is_Mac():
    return platform.system() == "Darwin"


# Windows 10 (v1511) Adds Support for ANSI Escape Sequences
def is_higher_win10_v1511():
    if is_Windows():
        try:
            if int(platform.version().split('.')[0]) >= 10 and int(platform.version().split('.')[-1]) >= 1511:
                return True
            else:
                return False
        except:
            return False


# text highlight
class Colored(object):
    if is_Windows():
        os.system("color")
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    ORANGE = '\033[0;33;1m'
    BLUE = '\033[34m'
    FUCHSIA = '\033[35m'
    WHITE = '\033[37m'

    #: no color
    RESET = '\033[0m'

    def color_str(self, color, s):
        if is_higher_win10_v1511() or is_Linux() or is_Mac():
            return '{}{}{}'.format(getattr(self, color), s, self.RESET)
        else:
            return '{}'.format(s)

    def red(self, s):
        return self.color_str('RED', s)

    def green(self, s):
        return self.color_str('GREEN', s)

    def yellow(self, s):
        return self.color_str('YELLOW', s)

    def orange(self, s):
        return self.color_str('ORANGE', s)

    def blue(self, s):
        return self.color_str('BLUE', s)

    def fuchsia(self, s):
        return self.color_str('FUCHSIA', s)

    def white(self, s):
        return self.color_str('WHITE', s)


# python version egt 3
def py_ver_egt_3():
    if int(platform.python_version()[0]) >= 3:
        return True

cool = Colored()
