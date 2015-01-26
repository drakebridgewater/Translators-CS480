__author__ = 'Drake'
from tree import *


def main():
    print("Creating table")
    my_tree = Tree("rootvalue")
    my_tree.add_node("firstNode")
    my_tree.add_node("secondNode")
    my_tree.add_node("3Node")
    my_tree.add_node("4Node")
    my_tree.go_to_child_node("secondNode")
    my_tree.add_node("secondNode--5node")
    my_tree.add_node("secondNode--6node")
    my_tree.add_node("secondNode--7node")
    my_tree.go_home()
    my_tree.add_node("10Node")
    my_tree.go_to_child_node("10Node")
    my_tree.add_node("10Node - 1")
    my_tree.add_node("10Node - 2")
    my_tree.add_node("10Node - 3")
    my_tree.go_to_child_node("10Node - 2")
    my_tree.add_node("10Node - 2 - 1")
    my_tree.add_node("10Node - 2 - 2")
    my_tree.add_node("10Node - 2 - 3")
    print("\n\n")
    my_tree.print_tree()
    my_tree.print_postordered_tree()
    print("Tree Size: " + str(my_tree.get_size()))
    print("-"*80)

if __name__ == '__main__':
    main()
