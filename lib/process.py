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
import sys
import socket
import itertools
import threading
import subprocess
from lib.fun import cool, unique, get_all_file, py_ver_egt_3
from lib.config import scan_command, output_path, domains_pool, get_port_string, get_threads, \
    set_port_string, get_count, set_count, get_global_parse_flag, targets_pool, set_global_parse_flag, ports_pool, \
    domain_pattern, ip_pattern, cli_net_extend, cli_no_extend, cli_all_port

try:
    import Queue
except:
    import queue as Queue


def create_output_file():
    if not os.path.exists(output_path):
        try:
            os.mkdir(output_path)
            print(cool.white("[+] Create output path success"))
        except:
            exit(cool.red("[-] Create output path: %s failed\n" % output_path))


def check_cmd_status():
    try:
        test_cmd = scan_command + '0 127.0.0.1'
        cmd = subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not ("0/tcp" in str(cmd.communicate())):
            exit(cool.red("[-] command %s error!\n" % test_cmd))
        else:
            print(cool.white("[+] Test command sucess"))
    except:
        exit(cool.red("[-] Test command failed, Please ensure config.py nmap command is correct\n"))


def target_use_file(file_path):
    with open(file_path, 'r') as target_file:
        for t in unique(target_file.readlines()):
            try:
                if t.startswith('http'):
                    t = ((t.strip()).split('/')[2]).split(":")[0]
                else:
                    t = (t.strip()).split(":")[0]
            except:
                pass
            if len(t) > 0 and '#' not in t[0]:
                if ip_pattern.findall(t):
                    set_count(set_original_ip_count=True)
                    targets_pool.append(t)
                elif domain_pattern.findall(t):
                    set_global_parse_flag(new_flag=True)
                    domains_pool.append(t)


def port_use_file(file_path):
    with open(file_path, 'r') as port_file:
        for port in unique(port_file.readlines()):
            port = port.strip()
            if port != '' and port[0] != "#":
                ports_pool.append((port.split("#")[0]).strip())
    set_port_string(",".join(ports_pool))


def init_target(target_choice):
    # target choice
    # file
    if os.path.isfile(target_choice):
        target_use_file(target_choice)
    # dir
    elif os.path.exists(target_choice):
        for _ in get_all_file(target_choice):
            target_use_file(_)
    # other
    else:
        specify_targets = target_choice.split(',')
        for targetschunk in specify_targets:
            if targetschunk.startswith("http"):
                targetschunk = ((targetschunk.strip()).split("/")[2]).split(":")[0]
            else:
                targetschunk = (targetschunk.strip()).split(":")[0]
            t_dic = {1: [], 2: [], 3: [], 4: []}
            # range
            if "-" in targetschunk:
                sc_chunk = targetschunk.split(".")
                if len(sc_chunk) != 4:
                    exit(cool.red("[-] Targets Error\n"))
                else:
                    for r in range(0, 4):
                        if "-" in sc_chunk[r]:
                            sc_chunk_split = sc_chunk[r].split("-")
                            if not (len(sc_chunk_split) == 2 and sc_chunk_split[0].isdigit()
                                    and sc_chunk_split[1].isdigit() and int(sc_chunk_split[0]) <= int(sc_chunk_split[1])
                                    and 0 <= int(sc_chunk_split[0]) <= 255 and 0 <= int(sc_chunk_split[1]) <= 255):
                                exit(cool.red("[-] Targets range error\n"))
                            else:
                                if len(sc_chunk_split) == 1:
                                    t_dic[r + 1].append(sc_chunk[0])
                                for _ in range(int(sc_chunk_split[0]), int(sc_chunk_split[1]) + 1):
                                    t_dic[r + 1].append(_)
                        else:
                            if not (sc_chunk[r].isdigit() and 0 <= int(sc_chunk[r]) <= 255):
                                exit(cool.red("[-] Specify error ip address\n"))
                            t_dic[r + 1].append(sc_chunk[r])
                for item in itertools.product(t_dic[1], t_dic[2], t_dic[3], t_dic[4]):
                    targets_pool.append(
                        "{0}.{1}.{2}.{3}".format(str(item[0]), str(item[1]), str(item[2]), str(item[3])))
            # single or multi
            else:
                if domain_pattern.findall(targetschunk):
                    domains_pool.append(targetschunk)
                    set_global_parse_flag(True)
                elif ip_pattern.findall(targetschunk):
                    targets_pool.append(targetschunk)
                else:
                    print(cool.fuchsia("[!] Invalid target %s" % targetschunk))
    if len(targets_pool) != 0 or len(domains_pool) != 0:
        print(cool.white("[+] Load {0} ip and {1} domain".format(len(targets_pool), len(domains_pool))))
    else:
        exit(cool.red("[-] Cannot find target\n"))


def init_port(port_choice):
    # port choice
    # file
    if os.path.isfile(port_choice):
        port_use_file(port_choice)
    # all port
    elif port_choice == cli_all_port:
        set_port_string("0-65535")
        for _ in range(0, 65536):
            ports_pool.append(str(_))
    # other
    else:
        specify_ports = port_choice.split(',')
        for portchunk in specify_ports:
            # range
            portchunk = portchunk.strip()
            if "-" in portchunk:
                port_split = portchunk.split("-")
                if not (len(port_split) == 2 and port_split[0].isdigit() and port_split[1].isdigit()
                        and int(port_split[0]) <= int(port_split[1])):
                    exit(cool.red("[-] Port range error\n"))
                else:
                    for _ in range(int(port_split[0]), int(port_split[1]) + 1):
                        ports_pool.append(str(_))
            # single or multi
            elif str(portchunk).isdigit() and 0 <= int(portchunk) <= 65535:
                ports_pool.append(portchunk)
            else:
                exit(cool.red("[-] Specify port error\n"))
        set_port_string(port_choice.strip())

    if len(ports_pool) != 0:
        print(cool.orange("[+] Load: {0} ports".format(len(ports_pool))))
    else:
        exit(cool.red("[-] Cannot find port"))


def init_extend(extend_choice, rmself):
    # no
    if extend_choice == cli_no_extend:
        print(cool.white("[+] Use extend mode: %s" % cli_no_extend))
    # other
    elif extend_choice.isdigit() and int(extend_choice) > 0:
        if extend_choice == cli_net_extend:
            print(cool.white("[+] Use extend mode: /24"))
            tmp1 = []
            rm1 = []
            for _ in targets_pool:
                rm1.append(_)
                e_split = _.split(".")
                for e in range(0, 256):
                    tmp1.append("{0}.{1}.{2}.{3}".format(e_split[0], e_split[1], e_split[2], str(e)))
            targets_pool.extend(tmp1)
            if rmself == 'true':
                rmlistself(rm1, targets_pool)

        elif 1 <= int(extend_choice) <= 255:
            print(cool.orange("[+] Use extend mode: +/- %s" % extend_choice))
            tmp2 = []
            rm2 = []
            for _ in targets_pool:
                rm2.append(_)
                e_split = _.split(".")
                for e in range(min(int(e_split[3]) - int(extend_choice), int(e_split[3]) - 1) if int(e_split[3]) -
                        int(extend_choice) >= 0 else 0, min(int(e_split[3]) + int(extend_choice) + 1, 256)):
                    tmp2.append("{0}.{1}.{2}.{3}".format(e_split[0], e_split[1], e_split[2], str(e)))
            targets_pool.extend(tmp2)

            if rmself == 'true':
                rmlistself(rm2, targets_pool)


def rmlistself(rmlist, rawlist):
    for _ in rmlist:
        while rawlist.count(_) != 0:
            rawlist.remove(_)


def init(target_choice, port_choice, extend_choice,  rmself):
    print(cool.green("[+] Init ..."))
    print(cool.white("[+] Threads: {0}".format(str(get_threads()))))
    check_cmd_status()
    init_target(target_choice)
    init_port(port_choice)
    auto_choose_start()
    init_extend(extend_choice, rmself=rmself)
    print(cool.orange("[+] Load: {0} targets".format(len(unique(targets_pool)))))
    if len(unique(targets_pool)) > 0:
        create_output_file()
    print(cool.green("[+] Init sucess\n"))


def build_worker_pool(queue, size):
    workers = []
    for _ in range(size):
        worker = Shakala(queue)
        worker.start()
        workers.append(worker)
    return workers


def auto_choose_start():
    if get_global_parse_flag():
        # print(cool.white("[+] Parsing domain to ip ..."))
        start(parse=True)
        set_global_parse_flag(False)
        print(cool.white("\n[+] Parsed domains to: {0} ip".format(get_count(get_parsed_ip_count=True))))


def start(parse=False):
    queue = Queue.Queue()
    worker_threads = build_worker_pool(queue, get_threads())
    if not parse:
        for x in unique(targets_pool):
            queue.put(x)
    else:
        for x in unique(domains_pool):
            queue.put(x)
    for worker in worker_threads:
        queue.put('quit')
    for worker in worker_threads:
        worker.join()


class Shakala(threading.Thread):
    def __init__(self, queue):
            threading.Thread.__init__(self)
            self._queue = queue

    def run(self):
        while True:
            target = self._queue.get()
            # for python 3 'unicode', and python 2 'str'
            if not py_ver_egt_3() and isinstance(target, unicode) and target == "quit":
                break
            elif isinstance(target, str) and target == "quit":
                break

            try:
                if get_global_parse_flag():
                    ip = socket.gethostbyname(target)
                    targets_pool.append(ip)
                    set_count(set_parsed_ip_count=True)
                    sys.stdout.write(cool.white("\r[+] Parsing {0:16} -> {1}".format(target, ip)))
                    sys.stdout.flush()
                else:
                    single_target_file = os.path.join(output_path, target + '.txt')
                    with open(single_target_file, 'a') as f:
                        command = subprocess.Popen('{0}{1} {2}'.format(scan_command, get_port_string(),
                                                                       target), shell=True, stdout=f)
                        c = command.communicate()
                        set_count(set_scan_items_count=True)
                        sys.stdout.write(cool.green("\r[+] Scan {0:15}, {1} items completed".format
                                         (target, get_count(get_scan_items_count=True))))
                        sys.stdout.flush()
            except KeyboardInterrupt:
                exit(cool.green("\n[*] User quit !"))
            except:
                pass
