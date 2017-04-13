#!/usr/bin/env python
# coding:utf-8
#
# Handle scanner results
#
"""
Copyright (c) 2017 shakala developers (https://github.com/LandGrey/shakala)
License: GNU GENERAL PUBLIC LICENSE Version 3
"""
import os
from lib.fun import get_all_file, cool
from lib.config import port_selection, select_pattern, get_select_result_path


# format:127.0.0.1,80,tcp,open,http
def result_handler(original_directory, results_path):
    port_status = port_selection
    with open(results_path, 'a') as rf:
        for single_file_path in get_all_file(original_directory):
            ip = os.path.split(single_file_path)[1][:-4]
            with open(single_file_path, 'r') as f:
                for line in f.readlines():
                    match = select_pattern.findall(line.strip())
                    for status in port_status:
                        if match and match[0][2] == status:
                            rf.write("{0},{1},{2},{3},{4}\n".format
                                     (ip, match[0][0], match[0][1], status, match[0][3].strip()))


# ip port type status service
def select_by_port(original_path, port_num):
    save_path = get_select_result_path(port_num)
    with open(save_path, 'a') as s:
        with open(original_path, 'r') as f:
            for line in f.readlines():
                chunk = line.strip().split(',')
                for status in port_selection:
                    if len(chunk) == 5 and chunk[1] == port_num and chunk[3] == status:
                        print(cool.white("[+] %s" % chunk[0]))
                        s.write(chunk[0] + '\n')
    if os.path.getsize(save_path) > 0:
        print(cool.orange("\n[+] Store in: %s" % save_path))
    else:
        os.remove(save_path)
        exit(cool.fuchsia("\n[!] Select nothing"))


# ip port type status service
def select_by_service(original_path, service):
    save_path = get_select_result_path(service)
    with open(save_path, 'a') as s:
        with open(original_path, 'r') as f:
            for line in f.readlines():
                chunk = line.strip().split(',')
                for status in port_selection:
                    if len(chunk) == 5 and chunk[4] == service and chunk[3] == status:
                        print(cool.white("[+] %s" % chunk[0]))
                        s.write(chunk[0] + '\n')

    if os.path.getsize(save_path) > 0:
        print(cool.orange("\n[+] Store in: %s" % save_path))
    else:
        os.remove(save_path)
        exit(cool.fuchsia("\n[!] Select nothing"))
