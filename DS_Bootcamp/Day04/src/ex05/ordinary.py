#!/usr/bin/env python3

import sys
import os
import psutil

def read_file(path):
    with open(path, 'r') as file:
        if not os.access(path, os.R_OK):
            raise OSError("can't open file")
        return file.readlines()
    


def main():
    if len(sys.argv) != 2:
        raise Exception("Wrong number of arguments, need file path")
    lines = read_file(sys.argv[1])
    for line in lines:
        pass

    usage = psutil.Process()
    print(f"Peak memory usage= {usage.memory_info().rss / 1073741824} GB")
    print(f"User Mode Time + System Mode Time = {usage.cpu_times().user + usage.cpu_times().system}s")
    


if __name__ == '__main__':
    main()