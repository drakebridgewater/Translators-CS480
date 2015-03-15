__author__ = 'Drake'
from myparser import *


class Tree():
    def __init__(self, root_value):
        self.root = Node(root_value)
        self.currentLocation = self.root
        # equal one because we just added one
        self.size = 1

    def go_home(self):
        self.currentLocation = self.root

    def add_node(self, value):
        print("adding node with token: " + value)
        new_node = Node(value)
        self.currentLocation.add_child(new_node)
        self.size += 1

    def go_to_child_node(self, child_value):
        print("trying to move to: " + child_value)
        next_move = self.currentLocation.get_child(child_value)
        print("Moving to child with token: " + next_move.get_value())
        if next_move != -1:
            self.currentLocation = next_move
        else:
            print("**error could not get child to move to")

    def get_size(self):
        return self.size

    def print_tree(self):
        print("-" * 80 + "\n\t print tree called")
        self.root.get_value()
        self.print_tree_helper(self.root)

    def print_tree_helper(self, node, indent=0):
        indent += 1
        for child in node.children:
            # if child.get_child_count() > 0:
            print("\t" * indent + child.get_value())
            self.print_tree_helper(child, indent)

    def print_postordered_tree(self):
        print("-" * 80 + "\n\t print post ordered tree called")
        self.root.get_value()
        self.post_order_tree_print(self.root)

    def post_order_tree_print(self, node):
        for child in node.children:
            self.post_order_tree_print(child)
            print(child.get_value())

