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


def create_role_file(out_dir, hostname):
    role_name = "setup_%s" % hostname
    role_dir = os.path.join(out_dir, "roles", role_name, "tasks")
    os.makedirs(role_dir, exist_ok=True)

    return role_name, os.path.join(role_dir, "main.yml")


def create_playbook(role_map):
    results = ['---', '# This playbook was generated by py-ansible-dns']
    for hostname, role_name in role_map.items():
        results.extend([
            " - name: Setup %s" % hostname,
            "   hosts: %s" % hostname,
            "   remote_user: root",
            "   roles:",
            "     - %s" % role_name,
            ""
        ])

    return results


def write_playbook(out_dir, role_map):
    out_path = os.path.join(out_dir, "playbook.yml")
    playbook = create_playbook(role_map)

    write_lines_to_file(playbook, out_path)


def write_ansible_files(config, out_dir):
    role_map = {}
    hosts_file = []
    hosts_path = os.path.join(out_dir, "hosts")

    for ip_addr, hostname in config['hosts'].items():
        role_name, role_path = create_role_file(out_dir, hostname)
        role_map[hostname] = role_name

        role_tasks = []
        role_tasks.extend(create_ansible_common(config))
        role_tasks.extend(create_ansible_localhost(hostname))
        write_lines_to_file(role_tasks, role_path)

        hosts_file.extend([
            "%s:" % hostname,
            "  hosts:",
            "    %s" % ip_addr,
            ""
        ])

    write_playbook(out_dir, role_map)
    write_lines_to_file(hosts_file, hosts_path)


def main():
    json_file = sys.argv[1]
    out_dir = sys.argv[2]

    config = json.load(open(json_file, 'r'))

    etc_hosts_path = os.path.join(out_dir, "etc_hosts")
    hosts_entry = create_hosts_entry(config)

    write_ansible_files(config, out_dir)


if __name__ == "__main__":
    main()
