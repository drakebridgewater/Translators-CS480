__author__ = 'drakebridgewater'

EQ = '='
OPER_ASSIGN = ':='
OPER_ADD = '+'
OPER_SUB = '-'
OPER_DIV = '/'
OPER_MULT = '*'
OPER_LT = '<'
OPER_GT = '>'
OPER_LE = '<='
OPER_GE = '>='
OPER_NE = '!='
OPER_NOT = '!'
OPER_MOD = '%'
OPER_EXP = '^'
SEMI = ';'
L_PAREN = '('
R_PAREN = ')'
OPER_AND = 'and'
OPER_OR = 'or'
OPER_NOT = 'not'
KEYWORD_STDOUT = 'stdout'
KEYWORD_LET = 'let'
KEYWORD_IF = 'if'
KEYWORD_WHILE = 'while'
KEYWORD_TRUE = "true"
KEYWORD_FALSE = "false"
TYPE_BOOL = 'bool'
TYPE_INT = 'int'
TYPE_REAL = 'real'
TYPE_STRING = 'string'


class Token:
    type = ''
    value = ''
    line = ''


class Node():
    def __init__(self, value):
        self.children = []
        self.data = value
        self.child_count = 0

    def get_number_children(self):
        return self.child_count

    def get_value(self):
        return self.data

    def get_left_child(self):
        return self.children[min(self.children)]

    def get_right_child(self):
        return self.children[max(self.children)]

    # returns the child at idx
    def get_child_at(self, idx):
        if idx <= self.children.count():
            return -1
        return self.children[idx]

    # Takes a data and return a child
    def get_child(self, child_value):
        for child in self.children:
            if child_value == child.value:
                return child

        # return a error that it does not contain data searching for
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
        self.depth = 0

    def go_home(self):
        self.currentLocation = self.root

    def add_node(self, value):
        print("adding node with data: ")
        print("[line: " + str(value.line) + ", ID: " + value.type + ", Value: " + str(value.value) + "]")
        newNode = Node(value)
        self.currentLocation.add_child(newNode)
        self.size += 1

    def go_to_child_node(self, child_value):
        print("trying to move to: " + str(child_value))
        nextMove = self.currentLocation.get_child(child_value)
        print("Moving to child with data: " + nextMove.get_value())
        if nextMove != -1:
            self.currentLocation = nextMove
        else:
            print("**error could not get child to move to")

    def get_size(self):
        return self.size

    def print_tree(self):
        print("-" * 80 + "\n\t print tree called")
        print(self.root.get_value())
        self.print_tree_helper(self.root)

    def print_postordered_tree(self):
        print("-" * 80 + "\n\t print post ordered tree called")
        print(self.root.get_value())
        self.post_order_tree_print(self.root)

    def print_tree_helper(self, node, indent=0):
        indent += 1
        for child in node.children:
            # if child.get_child_count() > 0:
            print("\t" * indent + "[line: " + str(child.data.line) + ", ID: " + child.data.type + ", Value: " + str(
                child.data.value) + "]")
            self.print_tree_helper(child, indent)

    def post_order_tree_print(self, node):
        for child in node.children:
            self.post_order_tree_print(child)
            print("[line: " + str(child.data.line) + ", ID: " + child.data.type + ", Value: " + str(
                child.data.value) + "]")


class Parser:
    def __init__(self, filename):
        self.tree = Tree(Node(Token))
        self.lexer = Lexer(filename)
        self.stack = []
        self.current_state = True
        self.temp_node = -1

    def control(self):
        try:
            self.lexer.open_file()
            # TODO I need a token!
            new_token = self.lexer.get_token()
            # TODO where we start putting everything in a huge statement
        finally:
            self.lexer.close_file()

    # I need a token
    # get toke from lexer

    def print_stack(self):
        for child in self.stack:
            print("[line: " + str(child.line) + ", ID: " + child.type + ", Value: " + str(child.value) + "]")

    def add_to_stack(self, token):
        if token.value is L_PAREN:
            self.stack.append(token)
        elif token.value is R_PAREN:
            if self.stack.pop() is L_PAREN:
                pass
            else:
                print("Syntax Error: [Line: " + str(token.line) + "] missing right parentheses")
        pass

    def add_token(self, token):
        # we receive a token
        # TODO add to stack
        self.add_to_stack(token)
        # TODO add to tree
        self.add_to_tree(token)

        print("tree" + "-" * 40)
        self.tree.add_node(token)
        print("stack" + "-" * 40)
        self.print_stack()
        print("-" * 40)
        self.tree.print_tree()

    def add_to_tree(self, token):
        if self.temp_node == -1:
            if token.value == L_PAREN:
                pass

        pass
