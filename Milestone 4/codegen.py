__author__ = 'drakebridgewater'
from defines import *


class CodeGen(object):
    def __init__(self, tree):
        self.tree = tree
        self.current_token = None
        self.stack = []
        self.next_tree_item = False
        self.index = 0

    def control(self):
        # TODO as we step through the tree convert and push element on to stack
        self.get_tokens_stack()
        self.print_stack()
        while self.index < len(self.stack):
            self.do_something(self.stack[self.index])
        pass

    def out(self, msg):
        print(msg)

    def do_something(self, data):
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
            self.out('.s')
        elif data.value is KEYWORD_STDOUT:
            self.out('.s')
        elif data.value is OPER_EQ:
            self.out(OPER_EQ)
        elif data.value is OPER_ASSIGN:
            self.out(OPER_ASSIGN)
        elif data.value is OPER_ADD:
            self.out(OPER_ADD)
        elif data.value is OPER_SUB:
            self.out(OPER_SUB)
        elif data.value is OPER_SUB:
            self.out(OPER_SUB)
        elif data.value is OPER_MULT:
            self.out(OPER_MULT)
        elif data.value is OPER_LT:
            self.out(OPER_LT)
        elif data.value is OPER_GT:
            self.out(OPER_GT)
        elif data.value is OPER_LE:
            self.out(OPER_LE)
        elif data.value is OPER_GE:
            self.out(OPER_GE)
        elif data.value is OPER_NE:
            self.out(OPER_NE)
        elif data.value is OPER_NOT:
            self.out(OPER_NOT)
        else:
            print_error("Attempting to write out", error_type="codegen")
            pass

    def compare(self, value1, value2):
        pass

    def is_number(self, value1):
        if hasattr(value1, "type") and value1.type in [TYPE_INT, TYPE_REAL]:
            self.next_tree_item = True
            return value1
        return False

    def get_tokens_stack(self):
        self._get_token_stack(self.tree)

    def _get_token_stack(self, node):
        for child in node.children:
            self._get_token_stack(child)
            temp_token = self.is_token(child)
            if temp_token:
                self.stack.append(temp_token)

    def is_token(self, child):
        if isinstance(child, int):
            return None
        elif isinstance(child, str):
            return None
        elif hasattr(child, "data"):
            if hasattr(child.data, "value"):
                return child.data
            else:
                return None
        elif hasattr(child, "value"):
            return child
        else:
            return None

    def print_stack(self):
        print_title("print tree called")
        for token in self.stack:
            print_token(token)

    def post_order_walkthrough(self, node):
        for child in node:
            self.next_tree_item = False
            self.post_order_walkthrough(child)
            self.do_something(child.data)