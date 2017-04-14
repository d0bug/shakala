#!/usr/bin/env python
# coding:utf-8
#
# A tiny batch multi-ports scanner based on nmap -- shakala
#
"""
Copyright (c) 2017 shakala developers (https://github.com/LandGrey/shakala)
License: GNU GENERAL PUBLIC LICENSE Version 3
"""

from __future__ import unicode_literals
import os
import time
from lib.config import set_threads, output_path, result_file_path
from lib.cli import parse_args
from lib.handler import result_handler, select_by_port, select_by_service
from lib.process import init, start
from lib.text import shakala_art_text
from lib.fun import cool


if __name__ == "__main__":
    start_time = time.time()
    print("{}".format(cool.green(shakala_art_text)))
    arg = parse_args()

    if str(arg.threads).isdigit() and int(arg.threads) >= 1:
        set_threads(int(arg.threads))

    if arg.analyse != '':
        if os.path.exists(arg.analyse):
            result_handler(arg.analyse, result_file_path)
            if os.path.getsize(result_file_path) > 0:
                print(cool.orange("\n[+] Store in: {0}".format(result_file_path)))
            else:
                try:
                    os.remove(result_file_path)
                except:
                    pass
                print(cool.fuchsia("\n[!] analyse output nothing"))
            print(cool.orange("[+] Cost : {0:.6} seconds".format(time.time() - start_time)))
        else:
            exit(cool.red("[-] Directory:%s don't exists" % arg.analyse))
    elif arg.select[0] != '':
        if os.path.isfile(arg.select[0]):
            if str(arg.select[1]).isdigit():
                select_by_port(arg.select[0], arg.select[1])
            else:
                select_by_service(arg.select[0], arg.select[1])
        else:
            exit(cool.red("[-] File:%s don't exists" % arg.select[0]))
    else:
        if arg.rmself != 'default':
            remself = 'true'
        else:
            remself = 'false'
        try:
            init(target_choice=arg.target, port_choice=arg.port, extend_choice=arg.extend, rmself=remself)
            start()
            if os.path.exists(output_path):
                result_handler(output_path, result_file_path)
                if os.path.getsize(result_file_path) > 0:
                    print(cool.white("\n[+] Store in: {0}".format(output_path)))
                    print(cool.orange("              {0}".format(result_file_path)))
                else:
                    os.remove(result_file_path)
                    print(cool.fuchsia("\n[!] Found nothing"))
                    print(cool.white("[+] Metadata   in: {0}".format(output_path)))
            print(cool.orange("[+] Cost : {0:.6} seconds".format(time.time() - start_time)))
        except KeyboardInterrupt:
            print(cool.green("\n[*] User quit !"))

