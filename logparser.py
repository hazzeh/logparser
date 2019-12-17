import re
import collections
import argparse
LOG_REGEX = r"(.*)\s\[(\d+)\]\s(.+)"
log_entries = {}

def process_logline(line):
    match = re.search(LOG_REGEX, line)
    if match:
        pid = match.group(2)
        message = match.group(3)
        full_message= match.group()
        if pid not in log_entries:
            log_entries[pid]=collections.deque(maxlen=4)
        log_entries[pid].append(full_message)
        if message.startswith("ERROR:"):
            print(*log_entries[pid], sep='\n')
            print("----")
            del(log_entries[pid])

def print_errors(file_name):
    with open(file_name) as logfile:
        for line in logfile:
            process_logline(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process logfile.")
    parser.add_argument("file_name", help="File to be parsed")
    args = parser.parse_args()
    print_errors(args.file_name)
