__author__ = 'drakebridgewater'
from defines import *


class codeGen():
    def __int__(self, tree):
        self.tree = tree
        self.current_token = None
        self.stack = []
        self.next_tree_item = False

    def control(self):
        # TODO as we step through the tree convert and push element on to stack
        pass

    def post_order_walkthrough(self, node):
        for child in node:
            self.next_tree_item = False
            self.post_order_walkthrough(node)
            self.do_something(node.data)

    def do_something(self, data):
        if self.next_tree_item:
            return
        num_ops = self.oper_count(data)
        if num_ops == 1:
            if self.is_number(data):
                self.write_out()
                if self.next_tree_item:
                    return
            else:
                self.print_error("num_ops = 1 first value error")
                return
        if num_ops == 2:
            if self.write_out(self.is_number(data)):
                if self.write_out(self.is_number(data)):
                    self.write_out(data)
                else:
                    self.print_error("num_ops = 1 second value error")
            else:
                self.print_error("num_ops = 1 first value error")

        if self.is_number(data):
            if data.type is TYPE_INT:
                self.stack.append()
        if data == OPER_ADD:
            if self.is_number(data):
                self.write_out()
                if self.is_number(data):
                    self.stack.pop()

    # Function Description:
    # Only write out if data is actually data
    def write_out(self, data):
        if data.value is KEYWORD_STDOUT:
            print('.s')
        elif data.value is KEYWORD_STDOUT:
            print('.s')
        elif data.value is OPER_EQ:
            pass
        elif data.value is OPER_ASSIGN:
            pass
        elif data.value is OPER_ADD:
            pass
        elif data.value is OPER_SUB:
            pass
        elif data.value is OPER_DIV:
            pass
        elif data.value is OPER_MULT:
            pass
        elif data.value is OPER_LT:
            pass
        elif data.value is OPER_GT:
            pass
        elif data.value is OPER_LE:
            pass
        elif data.value is OPER_GE:
            pass
        elif data.value is OPER_NE:
            pass
        elif data.value is OPER_NOT:
            pass
            print(data)
        else:
            pass

    def compare(self, value1, value2):
        pass

    def is_number(self, value1):
        if hasattr(value1, "type") and value1.type in [TYPE_INT, TYPE_REAL]:
            self.next_tree_item = True
            return value1
        return False