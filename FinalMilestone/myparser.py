__author__ = 'drakebridgewater'
from lexer import *
from defines import *


class Node(object):
    def __init__(self, data):
        # print("-"*20)
        # if hasattr(data, 'line'):
        #     print("New Node: ")
        #     print_token(data)
        # else:
        #     print("NN Str: ")
        #     print(data)
        self.data = data
        self.children = []
        self.depth = 0

    def add_child(self, obj):
        if obj is None:
            return obj
        self.children.append(obj)
        return True

    def print_tree(self):
        if globals()['DEBUG'] == 1 or 'tree' in globals()['OPTIONS']:
            print_title("print tree")
            self.print_tree_helper(self)

    def print_tree_helper(self, node, indent=0):
        indent += 1
        for child in node.children:
            if hasattr(child, "data"):
                if hasattr(child.data, "value"):
                    print_token(child.data, indent)
                else:
                    print("\t" * indent + str(child.data))
                self.print_tree_helper(child, indent)
            elif hasattr(child, "value"):
                print_token(child.data, indent)
            elif isinstance(child, int):
                print("\t" * indent + str(child))
            elif isinstance(child, str):
                print("\t" * indent + str(child))
            else:
                print("Error in print_tree_helper")
                print(child)
                return
                # else:
                # print("Failed")

    def print_postordered_tree(self):
        if globals()['DEBUG'] == 1 or 'postorder' in globals()['OPTIONS']:
            print_title("post ordered tree ")
            self.post_order_tree_print(self)

    def post_order_tree_print(self, node):
        for child in node.children:
            self.print_child(child, 0)
            self.post_order_tree_print(child)

    def print_child(self, child, indent):
        if isinstance(child, int):
            print("\t" * indent + str(child))
        elif isinstance(child, str):
            print("\t" * indent + str(child))
        elif hasattr(child, "data"):
            if hasattr(child.data, "value"):
                print_token(child.data)
            else:
                print("\t" * indent + str(child.data))
        elif hasattr(child, "value"):
            print_token(child)
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
        self.line = 1
        self.epsilon_flag = 0

    def parse_error(self, msg=''):
        if 'parse' in globals()['OPTIONS']:
            print_error(msg, self.line, "parse")

    # Function Description:
    # will return a single token as the lexer may spit out multiple
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
                print_token(self.tokens)
        finally:
            self.lexer.close_file()

    def control(self):
        try:
            self.lexer.open_file()
            if '-lexer' in globals()["OPTIONS"]:
                print_title("lexer output")
            # while self.current_state:
            self.tree.add_child(self.t())
            # globals()['current_token_index'] += 1
            self.tree.print_tree()
            if globals()['current_token_index'] > len(self.tokens):
                # if self.tokens[len(self.tokens) - 1] == -1:
                self.current_state = False  # Done reading file
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

    def t(self):
        # T --> (T)
        new_node = Node("T")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            while new_node.add_child(self.s()):
                pass
            if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                pass
            else:
                print_error("unrecoverable error", error_type="parser")
        else:
            print_error("somethings screwy", error_type='parser')
            globals()["current_token_index"] = save
            return None
        return new_node

    def s(self):
        # S --> [S' | Oper3 S | Oper3
        new_node = Node("S")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)) \
                and new_node.add_child(self.s_prime()):
            print_log("FOUND: (S' ")
        elif new_node.add_child(self.oper3()) \
                and new_node.add_child(self.s()):
            print_log("FOUND: oper3 S")
        elif new_node.add_child(self.oper3()):
            print_log("FOUND oper3")
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def s_prime(self):
        # S' --> ] | S] | Expr2] | ]S
        new_node = Node("S'")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
            print_log("FOUND: )")
        elif new_node.add_child(self.s()) \
                and new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
            print_log("FOUND: S )")
        elif new_node.add_child(self.expr2()) \
                and new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
            print_log("FOUND: expr2 )")
        elif new_node.add_child(self.is_value(self.get_token(), R_PAREN)) \
                and new_node.add_child(self.s()):
            print_log("FOUND: ) S")
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def expr(self):
        if not self.current_state:
            return None
        # Expr --> [Expr2] | Oper3
        new_node = Node("expr")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)) \
                and new_node.add_child(self.expr2()) \
                and new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
            print_log("FOUND: ( expr2 )")
        elif new_node.add_child(self.oper3()):
            print_log("FOUND: oper3")
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def expr2(self):
        if not self.current_state:
            return None
        # expr2 --> Stmt | Oper2
        new_node = Node("expr2")
        save = globals()["current_token_index"]
        if new_node.add_child(self.stmts()):
            print_log("FOUND: stmts")
        elif new_node.add_child((self.oper2())):
            print_log("FOUND: oper2")
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def oper(self):
        # Oper --> [Oper2] | Oper3
        global current_token_index
        if not self.current_state:
            return None

        new_node = Node("oper")
        saved_token_index = current_token_index
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)) \
                and new_node.add_child(self.oper2()) \
                and new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
            print_log("FOUND: (oper2)")
        elif new_node.add_child(self.oper3()):
            print_log("FOUND: oper3")
        else:
            current_token_index = saved_token_index
            # new_node.print_tree()
            return None
        return new_node

    def oper2(self):
        # Oper2 --> := Name Oper
        # | Binop Oper Oper
        # | Unop Oper
        global current_token_index
        if not self.current_state:
            return None

        new_node = Node("oper2")
        saved_token_index = current_token_index
        if new_node.add_child(self.is_value(self.get_token(), OPER_ASSIGN)) \
                and new_node.add_child(self.is_type(self.get_token(), TYPE_ID)) \
                and new_node.add_child(self.oper()):
            print_log("FOUND: := Name Oper")
        elif new_node.add_child(self.binops()) \
                and new_node.add_child(self.oper()) \
                and new_node.add_child(self.oper()):
            print_log("FOUND: Binop Oper Oper")
        elif new_node.add_child(self.unops()) \
                and new_node.add_child(self.oper()):
            print_log("FOUND: Unop Oper")
        else:
            current_token_index = saved_token_index
            return None
        return new_node

    def oper3(self):
        # Oper3 --> Constant | Name
        global current_token_index
        if not self.current_state:
            return None
        new_node = Node("oper3")
        saved_token_index = current_token_index
        if new_node.add_child(self.constants()):
            print_log("FOUND: constants")
        elif new_node.add_child(self.name()):
            print_log("FOUND: name")
        else:
            current_token_index = saved_token_index
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
            self.parse_error("missing binop or paren [b]")
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
            self.parse_error("missing unop or paren [a]")
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
            print_log("FOUND: ifstmts")
        elif new_node.add_child(self.whilestmts()):
            print_log("FOUND: whilestmts")
        elif new_node.add_child(self.letstmts()):
            print_log("FOUND: letstmts")
        elif new_node.add_child(self.printstmts()):
            print_log("FOUND: printstmts")
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def printstmts(self):
        # printstmts -> (stdout oper)
        if not self.current_state:
            return None
        new_node = Node("printstmts")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), KEYWORD_STDOUT)) \
                and new_node.add_child(self.oper()):
            print_log("FOUND: stdout oper")
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def ifstmts(self):
        # ifstmts -> if Expr If2
        if not self.current_state:
            return None
        new_node = Node("ifstmts")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), KEYWORD_IF)) \
                and new_node.add_child(self.expr()) \
                and new_node.add_child(self.ifstmts2()):
            print_log("FOUND: if expr if2")
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def ifstmts2(self):
        # ifstmts2 --> Expr | Expr Expr
        if not self.current_state:
            return None
        new_node = Node("ifstmts2")
        save = globals()["current_token_index"]
        if new_node.add_child(self.expr()):
            if new_node.add_child(self.expr()):
                pass
        else:
            globals()["current_token_index"] = save
            return None
        return new_node

    def whilestmts(self):
        # whilestmts -> (while expr exprlist)
        if not self.current_state:
            return None
        new_node = Node("whilestmts")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), KEYWORD_WHILE)):
            if new_node.add_child(self.expr()):
                if new_node.add_child(self.exprlist()):
                    pass
                else:
                    globals()["current_token_index"] = save
                    return None
            else:
                globals()["current_token_index"] = save
                return None
        else:
            globals()["current_token_index"] = save
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
            return None
        return new_node

    def letstmts(self):
        # letstmts -> (let (varlist))
        if not self.current_state:
            return None
        new_node = Node("letstmts")
        save = globals()["current_token_index"]
        if new_node.add_child(self.is_value(self.get_token(), KEYWORD_LET)):
            if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
                if new_node.add_child(self.varlist()):
                    new_node.add_child((self.is_value(self.get_token(), R_PAREN)))
                elif new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                    pass
                else:
                    globals()["current_token_index"] = save
                    return None
            else:
                globals()["current_token_index"] = save
                return None
        else:
            globals()["current_token_index"] = save
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
                    print_error("let statement error within varlist considering type", error_type="parser")
                    globals()["current_token_index"] = save
                    return new_node
            elif new_node.add_child(self.varlist()):
                return new_node
            else:
                print_error("let statement error within varlist considering variable", error_type="parser")
        else:
            globals()["current_token_index"] = save
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
