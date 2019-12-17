import re
import collections
LOG_REGEX = r"(.*)\s\[(\d+)\]\s(.+)"
log_entries = {}

def print_errors(file_name):
    with open(file_name) as logfile:
        for line in logfile:
            line = line.strip()
            match = re.search(LOG_REGEX, line)
            if match:
                pid = match.group(2)
                message = match.group(3)
                full_message= match.group()
                if pid not in log_entries:
                    log_entries[pid]=collections.deque(maxlen=4)
                log_entries[pid].append(full_message)
                if "ERROR" in message:
                    print(*log_entries[pid],sep='\n')
                    print("----")
                    del(log_entries[pid])

if __name__ == "__main__":
    pass