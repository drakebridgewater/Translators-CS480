#!/usr/bin/python
__author__ = 'Drake'
import sys

from myparser import *
from codegen import *


usage = """
Usage:
    main.py [option] [files]
"""

files = []
options = []
global DEBUG
DEBUG = 0

global current_token_index
current_token_index = 0


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
    sys.setrecursionlimit(100)
    if '-d' in sys.argv:
        globals()['DEBUG'] = 1
    if len(sys.argv) > 1:
        filename = sys.argv[len(sys.argv) - 1]
    else:
        filename = "test1"
    parser = MyParser(filename)
    parser.control()
    tree = parser.tree
    tree.print_postordered_tree()
    codegen = CodeGen(tree)
    codegen.control()


if __name__ == '__main__':
    main()
