#!/usr/bin/python3

import os
import sys

import json


def create_hosts_entry(config):
    results = []
    for ip_addr, hostname in config['hosts'].items():
        results.append("%s\t\t%s" % (ip_addr, hostname))

    return results


def print_hosts_entry(config):
    lines = create_hosts_entry(config)
    for line in lines:
        print(line)


def create_ansible_line(ip_addr, hostname):
    return [
        "- lineinfile:",
        "    path: /etc/hosts",
        "    line: '%s %s'" % (ip_addr, hostname),
        "    regexp: '(\s)*%s(\s)*%s(\s)*'" % (ip_addr, hostname),
        ""
    ]


def create_ansible_common(config):
    results = []
    for ip_addr, hostname in config['hosts'].items():
        results.extend(create_ansible_line(ip_addr, hostname))

    return results


def create_ansible_localhost(hostname):
    ipv4 = create_ansible_line("127.0.0.1", hostname)
    ipv6 = create_ansible_line("::1", hostname)
    results = ipv4[:]
    results.extend(ipv6)
    return results


def write_lines_to_file(lines, file_path):
    file_handle = open(file_path, 'w')
    for line in lines:
        file_handle.write("%s\n" % line)
    file_handle.close()


def create_role(hostname):
    
    

def write_ansible_files(config, out_dir):
    


def main():
    json_file = sys.argv[1]
    out_dir = sys.argv[2]

    config = json.load(open(json_file, 'r'))
    print_hosts_entry(config)


if __name__ == "__main__":
    main()
