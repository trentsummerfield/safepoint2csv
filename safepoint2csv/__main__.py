import argparse
import csv
import datetime
import fileinput
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--out-file', default=sys.stdout)
args = parser.parse_args()

vm_start = re.compile(
    r"""<hotspot_log version='.*?' process='.*?' time_ms='(?P<timestamp>\d+)'>"""
)

safepoint_entry = re.compile(
    r"""(?P<offset>\d+.\d+):\s(?P<vmop>[\w\s]+?)\s+\[\s+(?P<threads_total>\d+)\s+(?P<threads_initially_running>\d+)\s+(?P<threads_wait_to_block>\d+)\s+\]\s+\[\s+(?P<time_spin>\d+)\s+(?P<time_block>\d+)\s+(?P<time_sync>\d+)\s+(?P<time_cleanup>\d+)\s+(?P<time_vmop>\d+)\s+\]\s+(?P<page_trap_count>\d+)"""
)

vm_start_time = datetime.datetime.fromtimestamp(0)
fields = [
    'timestamp', 'vmop', 'threads_total', 'threads_initially_running',
    'threads_wait_to_block', 'time_spin', 'time_block', 'time_sync',
    'time_cleanup', 'time_vmop', 'page_trap_count'
]


def parse_log(lines):
    global vm_start_time
    for line in lines:
        match = vm_start.match(line)
        if match:
            seconds = float(match.group('timestamp')) / 1000.0
            vm_start_time = datetime.datetime.fromtimestamp(seconds)
            continue
        match = safepoint_entry.match(line)
        if match:
            entry = match.groupdict()
            time = vm_start_time + datetime.timedelta(
                seconds=float(entry['offset']))
            entry['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S.") + str(
                int(time.microsecond / 1000))
            yield entry


def write_csv(entries, f):
    out = csv.writer(f)
    out.writerow(fields)
    for entry in entries:
        out.writerow(map(entry.get, fields))


def main():
    write_csv(parse_log(fileinput.input()), args.out_file)


if __name__ == '__main__':
    main()
