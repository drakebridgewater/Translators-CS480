__author__ = 'drakebridgewater'
from lexer import *
from node import *
from defines import *


class MyParser(object):
    def __init__(self, filename):
        temp_token = Token
        temp_token.value = "root"
        temp_token.type = "root"
        temp_token.line = -1
        self.tree = Node(temp_token)
        self.lexer = Lexer(filename)
        self.stack = []
        self.current_state = True
        self.tokens = []
        self.line = 0
        self.current_token_index = 0

    def exit(self):
        self.tree.print_tree()
        exit()

    def parse_error(self, msg=''):
        print("PARSE ERROR: [line: " + str(self.line) + "] " + msg)

    # Function Description:
    # will return a single token as the lexer may spit out multiple
    def get_token(self):
        # if not self.tokens:
        if len(self.tokens) == 0:
            self.tokens.append(self.lexer.get_token())
            if self.tokens[0] == -1:
                self.current_state = False  # Done reading file
                return None
            self.line = self.tokens[0].line
        return self.tokens[self.current_token_index]

    def remove_token(self):
        # TODO instead of removing move integer to point to next value
        if len(self.tokens) > 0:
            self.tokens.pop()

    def restore_tokens(self, idx):
        self.tokens = idx.copy()

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
            # TODO I need a token!
            # while 1:
            temp = Node(self.tokens)
            print("-" * 30)
            self.tree.add_child(self.s())
            self.tree.print_tree()
            if len(self.tokens) == 0:
                return None
                # if it was unable to tokenize a float then we get a list of tokens
                # TODO where we start putting everything in a huge statement
        finally:
            self.lexer.close_file()

    def is_value(self, token, compare):
        if not self.current_state:
            return None
        save = self.tokens.copy()
        if token.value == compare:
            self.remove_token()
            return Node(token)
        else:
            self.restore_tokens(save)
            return None

    def s(self):
        if not self.current_state:
            return None
        # s -> expr S' | ( S"
        new_node = Node("S")
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            new_node.add_child(self.s_double_prime())
        elif new_node.add_child(self.expr()):
            new_node.add_child(self.s_prime())
        else:
            self.restore_tokens(save)
            print("ERROR")
            self.current_state = True
            return None
        # if len(new_node.children) > 0:
        # return new_node
        # else:
        #     return None
        return new_node

    def s_prime(self):
        if not self.current_state:
            return None
        # s' -> S S' | epsilon
        new_node = Node("S'")
        save = self.tokens.copy()
        if new_node.add_child(self.s()):
            new_node.add_child(self.s_prime())
        else:
            self.restore_tokens(save)
            new_node.add_child("epsilon")
        return new_node

    def s_double_prime(self):
        if not self.current_state:
            return None
        # S" ->  )S' | S)S'
        new_node = Node('S"')
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
            if new_node.add_child((self.s_prime())):
                pass
        elif new_node.add_child((self.s())):
            if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                new_node.add_child(self.s_prime())
        else:
            self.restore_tokens(save)
            return None
        return new_node

    def expr(self):
        if not self.current_state:
            return None
        # expr -> oper | stmts
        new_node = Node("expr")
        save = self.tokens.copy()
        if new_node.add_child(self.oper()):
            pass
        elif new_node.add_child((self.stmts())):
            pass
        else:
            self.restore_tokens(save)
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
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
            if new_node.add_child(self.is_value(self.get_token(), OPER_ASSIGN)):
                if new_node.add_child(self.tokens[0]):
                    self.remove_token()
                if self.get_token().type == "keyword":
                    if new_node.add_child(self.tokens[0]):
                        self.remove_token()
                    if new_node.add_child(self.oper()):
                        if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                            if new_node.add_child(self.tokens[0]):
                                self.remove_token()
                        else:
                            self.parse_error('missing right paren')
                            self.restore_tokens(save)
                            return None
                    else:
                        self.parse_error("missing oper")
                        self.restore_tokens(save)
                        return None
                else:
                    self.parse_error("missing keyword")
                    self.restore_tokens(save)
                    return None
            elif new_node.add_child(self.binops()):
                if new_node.add_child(self.oper()):
                    if new_node.add_child(self.oper()):
                        if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                            if new_node.add_child(self.tokens[0]):
                                self.remove_token()
                        else:
                            self.parse_error("missing expected right paren")
                            self.restore_tokens(save)
                            return None
                    else:
                        self.parse_error("missing expected oper")
                        self.restore_tokens(save)
                        return None
                else:
                    self.parse_error("missing expected oper")
            elif new_node.add_child(self.unops()):
                if new_node.add_child(self.oper()):
                    if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                        if new_node.add_child(self.tokens[0]):
                            self.remove_token()
                    else:
                        self.parse_error("missing expected right paren")
                        self.restore_tokens(save)
                        return None
                else:
                    self.parse_error("missing expected oper")
                    self.restore_tokens(save)
                    return None
            else:
                self.parse_error("missing assignment oper or binop or unop")
                self.restore_tokens(save)
                return None
        elif new_node.add_child(self.constants()):
            pass
        elif new_node.add_child(self.name()):
            pass
        else:
            self.parse_error("missing left paren constant or name")
            self.restore_tokens(save)
            return None
        return new_node

    def binops(self):
        # binops -> + | - | * | / | % | ^ | = | > | >= | < | <= | != | or | and
        if not self.current_state:
            return None
        new_node = Node("binops")
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), OPER_ADD)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_SUB)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_MULT)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_DIV)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_MOD)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_EXP)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_EQ)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_LT)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_LE)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_GT)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_GE)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_NE)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_OR)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_AND)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        else:
            self.parse_error("missing binop")
            self.restore_tokens(save)
            return None
        return new_node

    def unops(self):
        # unops -> - | not | sin | cos | tan
        if not self.current_state:
            return None
        new_node = Node("unops")
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), OPER_NOT)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_SIN)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_COS)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), OPER_TAN)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        else:
            self.restore_tokens(save)
            self.parse_error("missing unop")
            return None
        return new_node

    def constants(self):
        # constants -> string | ints | floats
        if not self.current_state:
            return None
        new_node = Node("constant")
        save = self.tokens.copy()
        if new_node.add_child(self.strings()):
            pass
        elif new_node.add_child(self.ints()):
            pass
        elif new_node.add_child(self.floats()):
            pass
        else:
            self.restore_tokens(save)
            return None
        return new_node

    def strings(self):
        # strings ->    reg_ex for str literal in C (“any alphanumeric”)
        # true | false
        if not self.current_state:
            return None
        new_node = Node("string")
        save = self.tokens.copy()
        if self.get_token().type == TYPE_STRING:
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif self.get_token().type == TYPE_BOOL:
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        else:
            self.restore_tokens(save)
            return None
        return new_node

    def name(self):
        # name -> reg_ex for ids in C (any lower and upper char
        # or underscore followed by any combination of lower,
        # upper, digits, or underscores)
        if not self.current_state:
            return None
        new_node = Node("name")
        save = self.tokens.copy()
        if self.get_token().type == TYPE_ID:
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        else:
            self.restore_tokens(save)
            return None
        return new_node

    def ints(self):
        # ints -> reg ex for positive/negative ints in C
        if not self.current_state:
            return None
        new_node = Node("int")
        save = self.tokens.copy()
        if self.get_token().type == TYPE_INT:
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        else:
            self.restore_tokens(save)
            return None
        return new_node

    def floats(self):
        # floats -> reg ex for positive/negative doubles in C
        if not self.current_state:
            return None
        new_node = Node("float")
        save = self.tokens.copy()
        if self.get_token().type == TYPE_REAL:
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        else:
            self.restore_tokens(save)
            return None
        return new_node

    def stmts(self):
        # stmts -> ifstmts | whilestmts | letstmts |printsmts
        if not self.current_state:
            return None
        new_node = Node("stmts")
        save = self.tokens.copy()
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
            self.restore_tokens(save)
            return None
        return new_node

    def printstmts(self):
        # printstmts -> (stdout oper)
        if not self.current_state:
            return None
        new_node = Node("printstmts")
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
            if new_node.add_child(self.is_value(self.get_token(), KEYWORD_STDOUT)):
                if new_node.add_child(self.tokens[0]):
                    self.remove_token()
                if new_node.add_child(self.oper()):
                    if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                        if new_node.add_child(self.tokens[0]):
                            self.remove_token()
                    else:
                        self.parse_error("missing right paren")
                        self.restore_tokens(save)
                        return None
                else:
                    self.parse_error("missing oper")
                    self.restore_tokens(save)
                    return None
            else:
                self.parse_error("missing keyword stdout")
                self.restore_tokens(save)
                return None
        else:
            self.parse_error("missing left paren")
            self.restore_tokens(save)
            return None
        return new_node

    def ifstmts(self):
        # ifstmts -> (if expr expr expr) | (if expr expr)
        if not self.current_state:
            return None
        new_node = Node("ifstmts")
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
            if new_node.add_child(self.expr()):
                if new_node.add_child(self.expr()):
                    if new_node.add_child(self.expr()):
                        if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                            if new_node.add_child(self.tokens[0]):
                                self.remove_token()
                        else:
                            self.parse_error("missing right paren")
                            self.restore_tokens(save)
                            return None
                    elif new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                        if new_node.add_child(self.tokens[0]):
                            self.remove_token()
                    else:
                        self.parse_error("missing 3 expression in if statement or right paren")
                        self.restore_tokens(save)
                        return None
                else:
                    self.parse_error("missing 2 expression in ifstmts")
                    self.restore_tokens(save)
                    return None
            else:
                self.parse_error("missing first expression in ifstmt")
                self.restore_tokens(save)
                return None
        else:
            self.parse_error("missing left paren in if statment")
            self.restore_tokens(save)
            return None
        return new_node

    def whilestmts(self):
        # whilestmts -> (while expr exprlist)
        if not self.current_state:
            return None
        new_node = Node("whilestmts")
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
            if new_node.add_child(self.is_value(self.get_token(), KEYWORD_WHILE)):
                if new_node.add_child(self.tokens[0]):
                    self.remove_token()
                if new_node.add_child(self.expr()):
                    if new_node.add_child(self.exprlist()):
                        if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                            if new_node.add_child(self.tokens[0]):
                                self.remove_token()
                        else:
                            self.parse_error("missing right paren")
                            self.restore_tokens(save)
                            return None
                    else:
                        self.parse_error("missing exprlist")
                        self.restore_tokens(save)
                        return None
                else:
                    self.parse_error("missing expression")
                    self.restore_tokens(save)
                    return None
            else:
                self.parse_error("missing while clause")
                self.restore_tokens(save)
                return None
        else:
            self.parse_error("missing left paren")
            self.restore_tokens(save)
            return None
        return new_node

    def exprlist(self):
        # exprlist -> expr | expr exprlist
        if not self.current_state:
            return None
        new_node = Node("exprlist")
        save = self.tokens.copy()
        if new_node.add_child(self.expr()):
            if new_node.add_child(self.exprlist()):
                pass
        else:
            self.parse_error("missing expr")
            self.restore_tokens(save)
            return None
        return new_node

    def letstmts(self):
        # letstmts -> (let (varlist))
        if not self.current_state:
            return None
        new_node = Node("letstmts")
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
            if new_node.add_child(self.is_value(self.get_token(), KEYWORD_LET)):
                if new_node.add_child(self.tokens[0]):
                    self.remove_token()
                if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
                    if new_node.add_child(self.tokens[0]):
                        self.remove_token()
                    if new_node.add_child(self.varlist()):
                        if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                            if new_node.add_child(self.tokens[0]):
                                self.remove_token()
                            if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                                if new_node.add_child(self.tokens[0]):
                                    self.remove_token()
                            else:
                                self.parse_error("missing right paren")
                                self.restore_tokens(save)
                                return None
                        else:
                            self.parse_error("missing right paren")
                            self.restore_tokens(save)
                            return None
                    else:
                        self.parse_error("missing varlist")
                        self.restore_tokens(save)
                        return None
                else:
                    self.parse_error("missing left paren")
                    self.restore_tokens(save)
                    return None
            else:
                self.parse_error("missing keyword let")
                self.restore_tokens(save)
                return None
        else:
            self.parse_error("missing left paren")
            self.restore_tokens(save)
            return None
        return new_node

    def varlist(self):
        # varlist -> (name type) | (name type) varlist
        if not self.current_state:
            return None
        new_node = Node("varlist")
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), L_PAREN)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
            if self.get_token().type == TYPE_ID:
                if new_node.add_child(self.tokens[0]):
                    self.remove_token()
                if new_node.add_child(self.type()):
                    if new_node.add_child(self.is_value(self.get_token(), R_PAREN)):
                        if new_node.add_child(self.tokens[0]):
                            self.remove_token()
                        if new_node.add_child(self.varlist()):
                            pass
                        return new_node
                    else:
                        self.parse_error("missing right paren")
                        self.restore_tokens(save)
                        return None
                else:
                    self.parse_error("missing type")
                    self.restore_tokens(save)
                    return None
            else:
                self.parse_error("missing name ")
                self.restore_tokens(save)
                return None
        else:
            self.parse_error("missing left paren")
            self.restore_tokens(save)
            return None

    def type(self):
        # type -> bool | int | real | string
        if not self.current_state:
            return None
        new_node = Node("type")
        save = self.tokens.copy()
        if new_node.add_child(self.is_value(self.get_token(), TYPE_BOOL)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), TYPE_INT)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), TYPE_REAL)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        elif new_node.add_child(self.is_value(self.get_token(), TYPE_STRING)):
            if new_node.add_child(self.tokens[0]):
                self.remove_token()
        else:
            self.parse_error("missing type")
            self.restore_tokens(save)
            return None
        return new_node

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


