import re
import json
import csv
import argparse

parser = argparse.ArgumentParser(description='unistd.h syscall extractor')

parser.add_argument('-o', '--output', help='File to save the syscalls to', required=True)
parser.add_argument('-f', '--format', help='File format of the syscalls (json, csv)', required=True)
parser.add_argument('-i', '--input', help='Path to the unistd.h header file', default='/usr/include/asm-generic/unistd.h')

args = parser.parse_args()

with open(args.input, 'r') as file:
    source = str(file.read())
matches = re.findall(r'__NR_(.+) ([0-9]+)', source)
syscalls = []
for match in matches:
    syscalls.append({
        'id': match[1],
        'name': match[0]
    })
if args.format == 'json':
    with open(args.output, 'w') as file:
        json.dump(syscalls, file)
elif args.format == 'csv':
    with open(args.output, 'w') as file:
        writer = csv.writer(file)
        rows = []
        for syscall in syscalls:
            rows.append([syscall['id'], syscall['name']])
        writer.writerows(rows)