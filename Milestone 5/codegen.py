__author__ = 'drakebridgewater'
from defines import *


class Scope:
    paren = ''
    prev_was_string = False
    prev_was_real = False


class CodeGen(object):
    def __init__(self, tree):
        self.tree = tree
        self.current_token = None
        self.stack = []
        self.scope_stack = []
        self.current_scope = []
        self.gforth = []
        self.next_tree_item = False
        self.index = 0
        self.oper_count = {
            OPER_EQ: 2,
            OPER_ASSIGN: 2,
            OPER_ADD: 2,
            OPER_SUB: 2,
            OPER_DIV: 2,
            OPER_MULT: 2,
            OPER_LT: 2,
            OPER_GT: 2,
            OPER_LE: 2,
            OPER_GE: 2,
            OPER_NE: 2,
            OPER_NOT: 2,
            OPER_MOD: 2,
            OPER_EXP: 2,
            SEMI: 2,
            L_PAREN: 2,
            R_PAREN: 2,
            OPER_AND: 2,
            OPER_OR: 2,
            OPER_NOT: 1,
            OPER_SIN: 1,
            OPER_TAN: 1,
            OPER_COS: 1}
        self.other_tokens = {
            KEYWORD_STDOUT: '.s',
            KEYWORD_LET: 'let',
            KEYWORD_IF: 'if',
            KEYWORD_WHILE: 'while',
            KEYWORD_TRUE: "true",
            KEYWORD_FALSE: "false",
            TYPE_BOOL: 'bool',
            TYPE_INT: 'int',
            TYPE_REAL: 'float',
            TYPE_STRING: 'string'
        }
        self.conversions = {
            "%": "mod",
            "!=": "<>"
        }
        self.realConversions = {
            "+": "f+",
            "-": "f-",
            "*": "f*",
            "/": "f/",
            "mod": "fmod",
            "<": "f<",
            "<=": "f<=",
            ">": "f>",
            ">=": "f>=",
            "=": "f=",
            "<>": "f<>",
            "sin": "fsin",
            "cos": "fcos",
            "tan": "ftan",
        }

    def control(self):
        # TODO as we step through the tree convert and push element on to stack
        self.get_tokens_stack()
        self.print_stack()
        print_title("CODE_GEN -- in progress")
        self.write_out()
        for x in self.gforth:
            print(x, end=" ")

    @staticmethod
    def out(msg):
        print(msg)

    # Function Description:
    # Only write out if data is actually data
    def write_out(self):
        data = self.stack
        prev_was_string = False
        prev_was_real = False
        prev_was_int = False
        prev_was_assign = False
        append_end = False
        oper_hold = ''

        for x in range(len(self.stack)):
            try:
                convert = False

                if prev_was_real:
                    if data[x].value in self.realConversions:
                        oper_hold = self.realConversions[data[x].value]
                    if data[x].type == TYPE_INT:
                        convert = True

                if data[x].type == TYPE_ID:
                    if data[x].value in self.current_scope:
                        pass
                    elif prev_was_assign:
                        self.current_scope.append(data[x].value)
                    else:
                        print_error("unassigned variable " + str(data[x].value), error_type="codegen")
                    self.gforth.append(str(data[x].value))
                elif data[x].type == TYPE_REAL:
                    if not prev_was_real:
                        prev_was_real = True
                    elif prev_was_real:
                        append_end = True
                    if prev_was_int:
                        append_end = True
                        convert = True
                    self.gforth.append(str(data[x].value) + 'e0')
                elif data[x].type == TYPE_STRING:
                    if not prev_was_string:
                        prev_was_string = True
                    elif prev_was_string:
                        convert = True
                        append_end = True
                    self.gforth.append('s" ' + str(data[x].value) + '"')
                elif data[x].type is TYPE_INT:
                    additional = ''
                    if not prev_was_int:
                        prev_was_int = True
                    elif prev_was_int:
                        append_end = True
                    if prev_was_real:
                        convert = True
                        additional = ' fswap'
                        append_end = True
                    self.gforth.append(str(data[x].value) + additional)
                elif data[x].value in ['=', '+', '-', '/', '*', '<', '>', '!', ';', ':', '%', '^']:
                    oper_hold = data[x].value
                elif data[x].value in self.other_tokens:
                    self.gforth.append(self.other_tokens[data[x].value])
                elif data[x].value == OPER_ASSIGN:
                    self.gforth.append("Assign")
                    prev_was_assign = True
                elif data[x].value is L_PAREN:
                    self.scope_stack.append(L_PAREN)
                elif data[x].value is R_PAREN:
                    try:
                        # prev_was_string = False
                        # prev_was_real = False
                        self.gforth.append('\n')
                        self.scope_stack.pop()
                        prev_was_string = False
                        prev_was_real = False
                        prev_was_int = False
                        append_end = False
                        oper_hold = ''
                    except IndexError:
                        print_error("missing left paren", error_type="code_gen")
                else:
                    print_error("unrecognized symbol " + str(data[x].value), error_type="codegen")
                if convert:
                    if prev_was_string:
                        oper_hold = 's+'

                if append_end:
                    if prev_was_real:
                        self.gforth.append('s>f')
                        self.gforth.append(self.realConversions[oper_hold])
                    else:
                        self.gforth.append(oper_hold)

            finally:
                pass
        if len(self.scope_stack) != 0:
            print_error("missing right paren", error_type="code_gen")

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
