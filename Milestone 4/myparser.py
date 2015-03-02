__author__ = 'drakebridgewater'
from lexer import *
from defines import *


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
        print("-" * 40)

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
        self.post_order_tree_print(self)

    def post_order_tree_print(self, node):
        for child in node.children:
            self.post_order_tree_print(child)
            self.print_child(child)

    def print_child(self, child, indent):
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
        elif hasattr(child, "value"):
            print("\t" * indent + "[line: " + str(child.line) +
                  ", ID: " + child.type +
                  ", Value: " + str(child.value) + "]")
        else:
            print("Error in print_tree_helper")
            print(child)
            return False
        return True


class MyParser(object):
    def __init__(self, filename):
        temp_token = Node("EMPTY")
        self.tree = Node(temp_token)
        self.lexer = Lexer(filename)
        self.current_state = True
        self.tokens = []
        self.line = 0
        self.epsilon_flag = 0

    def exit(self):
        self.tree.print_tree()
        exit()

    def parse_error(self, msg=''):
        pass
        # print("PARSE ERROR: [line: " + str(self.line) + "] " + msg)

    # Function Description:
    # will return a single token as the lexer may spit out multiple
    def get_token(self):
        # if not self.tokens:
        new_token = self.lexer.get_token()
        if new_token is not -1:
            self.tokens.append(new_token)
        if self.tokens[len(self.tokens) - 1] == -1:
            return None
        if len(self.tokens) <= globals()['current_token_index']:
            # if self.tokens[len(self.tokens) - 1] == -1:
            self.current_state = False  # Done reading file
            return None
        else:
            self.line = self.tokens[globals()['current_token_index']].line
            return self.tokens[globals()['current_token_index']]

    def print_tokens(self):
        try:
            self.lexer.open_file()
            while self.get_token():
                print("[line: " + str(self.tokens.line) +
                      ", ID: " + self.tokens.type +
                      ", Value: " + str(self.tokens.value) + "]")
        finally:
            self.lexer.close_file()

    def control(self):
        try:
            self.lexer.open_file()
            print("-" * 30)
            while self.current_state:
                self.tree.add_child(self.s())
                # globals()['current_token_index'] += 1
                self.tree.print_tree()
                self.tree.print_postordered_tree()
                if len(self.tokens) > globals()['current_token_index']:
                    # if self.tokens[len(self.tokens) - 1] == -1:
                    self.current_state = True  # Done reading file
            if len(self.tokens) == 0:
                return None
        finally:
            self.lexer.close_file()

    def is_type(self, token, compare):
        if not self.current_state:
            return None
        if isinstance(token, int):
            return None
        if token.type == compare:
            globals()['current_token_index'] += 1
            return Node(token)
        else:
            return None

    def is_value(self, token, compare):
        if not self.current_state:
            return None
        if token is None:
            return None
        if token.value == compare:
            globals()['current_token_index'] += 1
            return Node(token)
        else:
            return None

    def s(self):
        if not self.current_state:
            return None
        # s -> expr S' | ( S"
        new_node = Node("S")
        save = globals()["current_token_index"]
        if new_node.add_child(self.expr()):
            if new_node.add_child(self.s_prime()):
                if self.epsilon_flag:
                    self.epsilon_flag = 0
                    return new_node
            else:
                globals()["current_token_index"] = save
        elif new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.s_double_prime()):
                pass
            else:
                globals()["current_token_index"] = save
        else:
            globals()["current_token_index"] = save
            print("ERROR")
            self.current_state = True
            return None
        # if len(new_node.children) > 0:
        # return new_node
        # else:
        # return None
        return new_node

    def s_prime(self):
        if not self.current_state:
            return None
        # s' -> S S' | epsilon
        new_node = Node("S'")
        save = globals()["current_token_index"]
        if new_node.add_child(self.s()):
            if new_node.add_child(self.s_prime()):
                pass
            else:
                globals()["current_token_index"] = save
        else:
            new_node.add_child("epsilon")
            self.epsilon_flag = 1
            # TODO Need a double return here so that it get back to s and starts a new s
            self.current_state = False
            return None
        return new_node

    def s_double_prime(self):
        if not self.current_state:
            return None
        # S" ->  )S' | S)S'
        new_node = Node('S"')
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
            if new_node.add_child((self.s_prime())):
                pass
            else:
                globals()["current_token_index"] = save
        elif new_node.add_child((self.s())):
            if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                if new_node.add_child(self.s_prime()):
                    pass
                else:
                    globals()["current_token_index"] = save
            else:
                globals()["current_token_index"] = save
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def expr(self):
        if not self.current_state:
            return None
        # expr -> oper | stmts
        new_node = Node("expr")
        save = globals()["current_token_index"]
        if new_node.add_child(self.oper()):
            pass
        elif new_node.add_child((self.stmts())):
            pass
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def oper(self):
        if not self.current_state:
            return None
        # oper ->   ( := name oper )
        # ( binops oper oper )
        # ( unops oper )
        # constants
        # name
        new_node = Node("oper")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            l_paren_save = globals()["current_token_index"]
            temp_node = new_node
            if temp_node.add_child(self.is_value(self.get_token(), OPER_ASSIGN)):
                if temp_node.add_child(self.is_type(self.get_token(), TYPE_ID)):
                    if temp_node.add_child(self.oper()):
                        if temp_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                            new_node = temp_node
                            return new_node
                        else:
                            globals()["current_token_index"] = l_paren_save
                    else:
                        globals()["current_token_index"] = l_paren_save
                else:
                    globals()["current_token_index"] = l_paren_save
            else:
                globals()["current_token_index"] = l_paren_save

            temp_node = new_node
            if temp_node.add_child(self.binops()):
                if temp_node.add_child(self.oper()):
                    if temp_node.add_child(self.oper()):
                        if temp_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                            new_node = temp_node
                            return new_node
                        else:
                            globals()["current_token_index"] = l_paren_save
                    else:
                        globals()["current_token_index"] = l_paren_save
                else:
                    globals()["current_token_index"] = l_paren_save
            else:
                globals()["current_token_index"] = l_paren_save

            temp_node = new_node
            if temp_node.add_child(self.unops()):
                if temp_node.add_child(self.oper()):
                    if temp_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                        if temp_node.add_child(self.tokens[0]):
                            new_node = temp_node
                            return new_node
                        else:
                            globals()["current_token_index"] = l_paren_save
                    else:
                        globals()["current_token_index"] = l_paren_save
                else:
                    globals()["current_token_index"] = l_paren_save
            else:
                globals()["current_token_index"] = l_paren_save

        elif new_node.add_child(self.constants()):
            pass
        elif new_node.add_child(self.name()):
            pass
        else:
            self.parse_error("missing left paren constant or name")
            globals()["current_token_index"] = save
            return None
        return new_node

    def binops(self):
        # binops -> + | - | * | / | % | ^ | = | > | >= | < | <= | != | or | and
        if not self.current_state:
            return None
        new_node = Node("binops")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), OPER_ADD)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_SUB)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_MULT)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_DIV)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_MOD)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_EXP)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_EQ)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_LT)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_LE)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_GT)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_GE)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_NE)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_OR)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_AND)):
            pass
        else:
            self.parse_error("missing binop")
            globals()["current_token_index"] = save
            return None
        return new_node

    def unops(self):
        # unops -> - | not | sin | cos | tan
        if not self.current_state:
            return None
        new_node = Node("unops")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), OPER_NOT)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_SIN)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_COS)):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), OPER_TAN)):
            pass
        else:
            globals()["current_token_index"] = save
            self.parse_error("missing unop")
            return None
        return new_node

    def constants(self):
        # constants -> string | ints | floats
        if not self.current_state:
            return None
        new_node = Node("constant")
        save = globals()["current_token_index"]
        if new_node.add_child(self.strings()):
            pass
        elif new_node.add_child(self.ints()):
            pass
        elif new_node.add_child(self.floats()):
            pass
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def strings(self):
        # strings ->    reg_ex for str literal in C (“any alphanumeric”)
        # true | false
        if not self.current_state:
            return None
        new_node = Node("string")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_type(self.get_token(), TYPE_STRING)):
            pass
        elif new_node.add_child(self.is_type(self.get_token(), TYPE_BOOL)):
            pass
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def name(self):
        # name -> reg_ex for ids in C (any lower and upper char
        # or underscore followed by any combination of lower,
        # upper, digits, or underscores)
        if not self.current_state:
            return None
        new_node = Node("name")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_type(self.get_token(), TYPE_ID)):
            pass
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def ints(self):
        # ints -> reg ex for positive/negative ints in C
        if not self.current_state:
            return None
        new_node = Node("int")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_type(self.get_token(), TYPE_INT)):
            pass
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def floats(self):
        # floats -> reg ex for positive/negative doubles in C
        if not self.current_state:
            return None
        new_node = Node("float")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_type(self.get_token(), TYPE_REAL)):
            pass
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def stmts(self):
        # stmts -> ifstmts | whilestmts | letstmts |printsmts
        if not self.current_state:
            return None
        new_node = Node("stmts")
        save = globals()["current_token_index"]
        if new_node.add_child(self.ifstmts()):
            pass
        elif new_node.add_child(self.whilestmts()):
            pass
        elif new_node.add_child(self.letstmts()):
            pass
        elif new_node.add_child(self.printstmts()):
            pass
        else:
            self.parse_error("missing if, while, let or print statment")
            globals()["current_token_index"] = save
            return None
        return new_node

    def printstmts(self):
        # printstmts -> (stdout oper)
        if not self.current_state:
            return None
        new_node = Node("printstmts")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.is_value(self.get_token(), KEYWORD_STDOUT)):
                if new_node.add_child(self.oper()):
                    if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                        pass
                    else:
                        globals()["current_token_index"] = save
                else:
                    globals()["current_token_index"] = save
            else:
                globals()["current_token_index"] = save
        else:
            globals()["current_token_index"] = save
            self.parse_error("missing left paren")
            return None
        return new_node

    def ifstmts(self):
        # ifstmts -> (if expr expr expr) | (if expr expr)
        if not self.current_state:
            return None
        new_node = Node("ifstmts")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.expr()):
                if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                    # (if expr expr)
                    pass
                elif new_node.add_child(self.expr()):
                    if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                        # (if expr expr expr)
                        pass
                    else:
                        globals()["current_token_index"] = save
                else:
                    globals()["current_token_index"] = save
            else:
                globals()["current_token_index"] = save
        else:
            globals()["current_token_index"] = save
            self.parse_error("not an if statment")
            return None
        return new_node

    def whilestmts(self):
        # whilestmts -> (while expr exprlist)
        if not self.current_state:
            return None
        new_node = Node("whilestmts")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.is_value(self.get_token(), KEYWORD_WHILE)):
                if new_node.add_child(self.expr()):
                    if new_node.add_child(self.exprlist()):
                        if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                            pass
                        else:
                            globals()["current_token_index"] = save
                    else:
                        globals()["current_token_index"] = save
                else:
                    globals()["current_token_index"] = save
            else:
                globals()["current_token_index"] = save
        else:
            globals()["current_token_index"] = save
            self.parse_error("Not While stmts")
            return None
        return new_node

    def exprlist(self):
        # exprlist -> expr | expr exprlist
        if not self.current_state:
            return None
        new_node = Node("exprlist")
        save = globals()["current_token_index"]
        if new_node.add_child(self.expr()):
            if new_node.add_child(self.exprlist()):
                pass
            else:
                globals()["current_token_index"] = save
        else:
            globals()["current_token_index"] = save
            self.parse_error("not expression list")
            return None
        return new_node

    def letstmts(self):
        # letstmts -> (let (varlist))
        if not self.current_state:
            return None
        new_node = Node("letstmts")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.is_value(self.get_token(), KEYWORD_LET)):
                if new_node.add_child(self.varlist()):
                    if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                        pass
                    else:
                        globals()["current_token_index"] = save
                else:
                    globals()["current_token_index"] = save
            else:
                globals()["current_token_index"] = save
        else:
            globals()["current_token_index"] = save
            self.parse_error("Checked if let statement")
            return None
        return new_node

    def varlist(self):
        # varlist -> (name type) | (name type) varlist
        if not self.current_state:
            return None
        new_node = Node("varlist")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.is_type(self.get_token(), TYPE_ID)):
                if new_node.add_child(self.type()):
                    if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                        if new_node.add_child(self.varlist()):
                            return new_node
                        # (name type)
                        return new_node
                    else:
                        globals()["current_token_index"] = save
                else:
                    pass
                    # check of type failed
            else:
                globals()["current_token_index"] = save
        else:
            globals()["current_token_index"] = save
            self.parse_error("not varlist")
            return None
        return new_node

    def type(self):
        # type -> bool | int | real | string
        if not self.current_state:
            return None
        new_node = Node("type")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), "bool")):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), "int")):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), "real")):
            pass
        elif new_node.add_child(self.is_value(self.get_token(), "string")):
            pass
        else:
            globals()["current_token_index"] = save
            return None
        return new_node
