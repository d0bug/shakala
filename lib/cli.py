#!/usr/bin/env python
# coding:utf-8
# parse command line arguments
"""
Copyright (c) 2017 shakala developers (https://github.com/LandGrey/shakala)
License: GNU GENERAL PUBLIC LICENSE Version 3
"""

from __future__ import unicode_literals
import sys
import argparse
from lib.fun import cool
from lib.config import cli_all_port, cli_net_extend, cli_no_extend, get_threads, port_list_file_path


def parse_args():
    parser = argparse.ArgumentParser(prog='shakala',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description=cool.green('*[+] A tiny batch multi-ports scanner base on nmap. [+]*\n') +
                                                 cool.green(' [+] Build by LandGrey    email:LandGrey@qq.com\n'),
                                     usage=cool.orange('''
shakala.py [options]
         -t         target
         -p         port
         -e         extend
         -a         dir
         -s         file port |  service
         --rmself   will remove itself
         --threads  threads'''.format(cli_all_port, cli_no_extend, cli_net_extend)))

    parser.add_argument('-t', dest='target', metavar='target', type=str, default="",
                        help=cool.yellow('''
specify  www.example.com,192.168.1.11,192.168.1-10.1-10
dir      use all files in specify directory
path     use single file'''))

    parser.add_argument('-p', dest='port', metavar='port', type=str,
                        default=port_list_file_path, help=cool.yellow('''
specify  80-89,888,8080-8088
{0:8} use all ports: 0-65535
path     (default): {1}'''.format(cli_all_port, port_list_file_path)))

    parser.add_argument('-e', dest='extend', metavar='mode', type=str, default=cli_no_extend,
                        help=cool.yellow('''
numbers  increase or decrease numbers target in /24 range
{0:8} extend whole network address: /24
{1:8} (default)'''.format(cli_net_extend, cli_no_extend)))

    parser.add_argument('-a', dest='analyse', metavar='dir', type=str, default='',
                        help=cool.yellow('''
dir      analyse the result use directory'''))

# original_path, service
    parser.add_argument('-s', dest='select', metavar='select', type=str, nargs=2, default=('', ''),
                        help=cool.yellow('''
file_path port_or_service
         file must be shakala 'result_' prefix file'''))

    parser.add_argument('--rmself', dest='rmself', action="store_true", default='default',
                        help=cool.yellow('''
provide for '-e extend' '''))

    parser.add_argument('--threads', dest='threads', metavar='threads', type=str, default=get_threads(),
                        help=cool.yellow('''
threads  default:{0}'''.format(get_threads())))

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    return args
