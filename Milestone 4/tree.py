__author__ = 'Drake'


class Node():
    def __init__(self, value):
        self.children = []
        self.value = value
        self.child_count = 0

    def get_number_children(self):
        return self.child_count

    def get_value(self):
        return self.value

    def get_left_child(self):
        return self.children[min(self.children)]

    def get_right_child(self):
        return self.children[max(self.children)]

    # returns the child at idx
    def get_child_at(self, idx):
        if idx <= self.children.count():
            return -1
        return self.children[idx]

    # Takes a token and return a child
    def get_child(self, child_value):
        for child in self.children:
            if child_value == child.value:
                return child

        # return a error that it does not contain token searching for
        return -1

    def add_child(self, child):
        self.children.append(child)
        self.child_count += 1

    def print_children(self, indent):
        for child in self.children:
            print("\t" * indent + child.value)


class Tree():
    def __init__(self, rootValue):
        self.root = Node(rootValue)
        self.currentLocation = self.root
        # equal one because we just added one
        self.size = 1

    def go_home(self):
        self.currentLocation = self.root

    def add_node(self, value):
        print("adding node with token: " + value)
        newNode = Node(value)
        self.currentLocation.add_child(newNode)
        self.size += 1

    def go_to_child_node(self, child_value):
        print("trying to move to: " + child_value)
        nextMove = self.currentLocation.get_child(child_value)
        print("Moving to child with token: " + nextMove.get_value())
        if nextMove != -1:
            self.currentLocation = nextMove
        else:
            print("**error could not get child to move to")

    def get_size(self):
        return self.size

    def print_tree(self):
        print("-" * 80 + "\n\t print tree called")
        self.root.get_value()
        self.print_tree_helper(self.root)

    def print_postordered_tree(self):
        print("-" * 80 + "\n\t print post ordered tree called")
        print
        self.root.get_value()
        self.post_order_tree_print(self.root)

    def print_tree_helper(self, node, indent=0):
        indent += 1
        for child in node.children:
            # if child.get_child_count() > 0:
            print("\t" * indent + child.get_value())
            self.print_tree_helper(child, indent)

    def post_order_tree_print(self, node):
        for child in node.children:
            self.post_order_tree_print(child)
            print(child.get_value())

