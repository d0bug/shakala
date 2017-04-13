#!/usr/bin/env python
# coding:utf-8
# shakala configuration file
"""
Copyright (c) 2017 shakala developers (https://github.com/LandGrey/shakala)
License: GNU GENERAL PUBLIC LICENSE Version 3
"""
from __future__ import unicode_literals
import os
import re
import sys
import time
import subprocess
from lib.fun import py_ver_egt_3

if 'nmap.org' in subprocess.Popen('nmap', shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stdout.read().decode():
    scan_command = r'nmap --dns-servers 114.114.114.114,8.8.8.8 -Pn -sS -T 5 -p'
else:
    scan_command = r'your nmap path' \
                   r' --dns-servers 114.114.114.114,8.8.8.8 -Pn -sS -T 5 -p'

shakala_name = "shakala"
shakala_threads = 50
global_parse_flag = False
port_selection = ["open", ]

original_ip_count = 0
parsed_ip_count = 0
scan_items_count = 0

# source pool
ports_pool = []
targets_pool = []
domains_pool = []
results_pool = []


try:
    root_path = (os.path.join(os.path.dirname(os.path.abspath(sys.argv[0]))).encode('utf-8').decode()
                 if py_ver_egt_3() else unicode(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0]))), 'utf-8'))
except:
    exit("\n[-] Please ensure pydictor root path is ascii strings!")


def get_time():
    return str(time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time())))

output_path = os.path.join(root_path, 'outputs', get_time())
result_file_path = os.path.join(root_path, 'outputs', 'result_' + get_time() + '.txt')
port_list_file_path = os.path.join(root_path, 'lib', 'ports.txt')

# some description
cli_no_extend = "no"
cli_net_extend = "256"
cli_all_port = "all"

ip_pattern = re.compile(r'(\d{1,3}[.])(\d{1,3}[.])(\d{1,3}[.])(\d{1,3})')

domain_pattern = re.compile(r'([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}')

select_pattern = re.compile('^(.*?)/(.*?) .*(open|filtered|close|unfiltered).(.*?)$')


def get_select_result_path(description='none'):
    return os.path.join(root_path, 'outputs', 'select_' + description + '_' + get_time() + '.txt')


def get_port_string():
    global nmap_port_string
    return nmap_port_string


def set_port_string(new_port_string):
    global nmap_port_string
    nmap_port_string = new_port_string


def get_global_parse_flag():
    global global_parse_flag
    return global_parse_flag


def set_global_parse_flag(new_flag):
    global global_parse_flag
    global_parse_flag = new_flag


def get_count(get_original_ip_count=False, get_parsed_ip_count=False, get_scan_items_count=False):
    global original_ip_count
    global parsed_ip_count
    global scan_items_count
    if get_original_ip_count:
        return original_ip_count
    elif get_parsed_ip_count:
        return parsed_ip_count
    elif get_scan_items_count:
        return scan_items_count
    else:
        exit("[-] cannot get any count")


def set_count(set_original_ip_count=False, set_parsed_ip_count=False, set_scan_items_count=False):
    global original_ip_count
    global parsed_ip_count
    global scan_items_count

    if set_original_ip_count:
        original_ip_count += 1
    elif set_parsed_ip_count:
        parsed_ip_count += 1
    elif set_scan_items_count:
        scan_items_count += 1
    else:
        exit("[-] cannot set any count")


def get_threads():
    global shakala_threads
    return shakala_threads


def set_threads(new_threads):
    global shakala_threads
    shakala_threads = new_threads
