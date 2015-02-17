__author__ = 'Drake'


class Node(object):
    def __init__(self, data):
        if hasattr(data, "value"):
            print("New Node: " + str(data.value))
        else:
            print("NN Str: " + str(data))
        self.data = data
        self.children = []
        self.depth = 0

    def add_child(self, obj):
        if obj is None:
            return obj
        self.children.append(obj)
        return True

    # need to set depth recursively
    def set_depth(self, t):
        if t is not None or t != str:
            if len(t.children) > 0:
                for i in t.children:
                    if i is not None:
                        i.depth = t.depth + 1
                        self.set_depth(i)
        self.set_depth()

    def get_child_at(self, index):
        return self.children[index]

    def get_first_child_at_parent(self, obj):
        if len(obj.children) > 0:
            return obj.children[0]
        else:
            return self.children[0]

    def get_first_child_at_parent_level(self, obj, level):
        if level == 0:
            return self.children[0]
        else:
            if level >= 1:
                if len(obj.children) > 0:
                    return obj.children[0]
                else:
                    return self.children[0]
            else:
                return self.children[0]

    @staticmethod
    def get_parent_depth(obj):
        return obj.depth

    def print_tree(self):
        print("-" * 40 + "\n\t print tree called")
        # print(self.data)
        self.print_tree_helper(self)

    def print_tree_helper(self, node, indent=0):
        indent += 1
        for child in node.children:
            # if child.get_child_count() > 0:
            # if child.data is not None:
            if isinstance(child, int):

                print("\t" * indent + str(child))
            elif isinstance(child, str):
                print("\t" * indent + str(child))
            elif hasattr(child, "data"):
                if hasattr(child.data, "value"):
                    print("\t" * indent + "[line: " + str(child.data.line) +
                          ", ID: " + child.data.type +
                          ", Value: " + str(child.data.value) + "]")
                else:
                    print("\t" * indent + str(child.data))
                self.print_tree_helper(child, indent)
            elif hasattr(child, "value"):
                print("\t" * indent + "[line: " + str(child.line) +
                      ", ID: " + child.type +
                      ", Value: " + str(child.value) + "]")
            else:
                print("Error in print_tree_helper")
                print(child)
                return
                # else:
                # print("Failed")

    def print_postordered_tree(self):
        print("-" * 80 + "\n\t print post ordered tree called")
        print(self.root.get_value())
        self.post_order_tree_print(self.root)

    def post_order_tree_print(self, node):
        for child in node.children:
            self.post_order_tree_print(child)
            print("[line: " + str(child.data.line) + ", ID: " + child.data.type + ", Value: " + str(
                child.data.value) + "]")