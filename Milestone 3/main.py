#!/usr/bin/python
__author__ = 'Drake'
import sys
from defines import *
from myparser import *


usage = """
Usage:
    main.py [option] [files]
"""


def prepare_files(argv):
    for arg in argv:
        if arg[0] == '-':
            # collect user options
            options.append(arg)
        elif arg != argv[0]:
            # collect files
            files.append(arg)


def read_file(input_file):
    content = ""
    f = open(input_file)

    lines_raw = f.readlines()
    for i in range(0, len(lines_raw)):
        content += lines_raw[i]

    return content


def print_verbose(selected_file, content):
    print('\n', "input: parsing " + str(selected_file))
    print("-" * 40)
    print(content)
    print('\n', "output: ")
    print("-" * 40)


def main():
    if len(sys.argv) < 2:
        print(usage)
        exit()

    global options
    global files
    prepare_files(sys.argv)

    filename = sys.argv[1]
    for file in files:
        parser = MyParser(filename)
        parser.control()


if __name__ == '__main__':
    main()
