#!/usr/bin/python
__author__ = 'Drake'
import sys

from myparser import *
from codegen import *


usage = """
Usage:
    main.py [option] [files]
    -d or -debug\t\t Show lots of debug stuff (development only)
    -tree \t\t\t Show the parse tree
    -postorder \t\t\t Show the post order traversal of the tree
    -lexer  \t\t\t Show the lexer output (not helpful, but shows how nodes are created)
    -print \t\t\t Show the gforth code

    With no arguments this will run test1 by default
"""

files = []

global current_token_index
current_token_index = 0


def read_file(input_file):
    content = ""
    f = open(input_file)

    lines_raw = f.readlines()
    for i in range(0, len(lines_raw)):
        content += lines_raw[i]

    return content


def print_verbose(selected_file):
    print_title("IBTL file: " + selected_file)
    print('\n', "input: parsing " + str(selected_file))
    with open(selected_file, "r") as file:
        text = file.read()
        print(text)


def main():
    sys.setrecursionlimit(100)
    print("-"*80)
    if len(sys.argv) > 1:
        filename = sys.argv[len(sys.argv) - 1]
    else:
        filename = "test2"

    if '-help' in sys.argv or '-usage' in sys.argv or '-h' in sys.argv:
        print(usage)
        return 0
    if '-d' in sys.argv or '-debug' in sys.argv:
        globals()['DEBUG'] = 1
        globals()['OPTIONS'].append("DEBUG")
    else:
        globals()['DEBUG'] = 0
    if '-input' in sys.argv:
        print_verbose(filename)
    if '-tree' in sys.argv:
        globals()['OPTIONS'].append("tree")
    if '-postorder'in sys.argv:
        globals()['OPTIONS'].append("postorder")
    if '-print' in sys.argv:
        globals()['OPTIONS'].append("print")
    if '-lexer' in sys.argv:
        globals()['OPTIONS'].append("lexer")


    parser = MyParser(filename)
    parser.control()
    tree = parser.tree
    tree.print_postordered_tree()
    codegen = CodeGen(tree)
    gforth = codegen.control()

    outfile = filename.split(".")[0] + ".out" + ".fs"
    print("\n\n\ngforth code in:  " + outfile)
    with open(outfile, "w+") as file:
        for x in gforth:
            file.write(str(x) + " ")




if __name__ == '__main__':
    main()
