__author__ = 'drakebridgewater'
from defines import *
from myparser import *


class Scope:
    paren = ''
    prev_was_string = False
    prev_was_real = False


class CodeGen(object):
    def __init__(self, tree):
        self.error_flag = False
        self.tree = tree
        self.current_token = None
        self.stack = []
        self.scope_stack = []
        self.current_scope = []
        self.variables = []
        self.gforth = []
        self.index = 0
        self.pointer = 0
        self.other_tokens = {
            # KEYWORD_STDOUT: '.s',
            # KEYWORD_LET: 'let',
            KEYWORD_IF: 'if',
            KEYWORD_WHILE: 'while',
            KEYWORD_TRUE: "true",
            KEYWORD_FALSE: "false"
            # TYPE_BOOL: 'bool',
            # TYPE_INT: 'int',
            # TYPE_REAL: 'float',
            # TYPE_STRING: 'string'
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
        if '-print' in globals()['OPTIONS']:
            print_title("CODE_GEN -- in progress")
        self.print_stack()
        print_log((("-"*15 + "codegen-log" + "-"*15)+"\n")*3)
        self.write_out()
        self.gforth = self.rem_sll(self.gforth, L_PAREN)
        self.gforth = self.rem_sll(self.gforth, R_PAREN)

        if 'print' in globals()['OPTIONS']:
            print_title("gforth code")
            for x in self.gforth:
                print(x, end=" ")
        return self.gforth

    def rem_sll(self, L, item):
        answer = []
        for i in L:
            if i != item:
                answer.append(i)
        return answer

    @staticmethod
    def out(msg):
        print(msg)

    def check_variable_type(self, id):
        for x in self.variables:
            if x[0] == id:
                return x[1]
        return None

    def add_variable(self, id, type):
        if type in [TYPE_REAL, TYPE_STRING, TYPE_INT, TYPE_BOOL] \
                and not self.check_variable_type(id):
            self.variables.append((id, type))
        else:
            print_error("variable " + str(id) + " already exists", error_type="codegen")

    def write_out(self):
        data = self.stack
        prev_was_declare = False

        while self.pointer <= len(self.stack) - 1:
            try:
                if data[self.pointer].type == 'ops':
                    if data[self.pointer].value is L_PAREN:
                        self.gforth.append(L_PAREN)
                        self.scope_stack.append(L_PAREN)
                    elif data[self.pointer].value is R_PAREN:
                        self.gforth.append(R_PAREN)
                    elif data[self.pointer].value in ['+', '-', '/', '*', '<', '>', '!', ';', ':', '%', '^']:
                        self.pointer, gcode, expr_type = self.is_math_expr(self.pointer)
                        self.gforth.append(gcode)
                elif data[self.pointer].type == TYPE_ID:
                    if self.check_variable_type(data[self.pointer].value):
                        print_error("error variable " + str(data[self.pointer].value) + "does not exist yet")
                elif data[self.pointer].type == 'keywords':
                    if data[self.pointer].value == OPER_ASSIGN:  # :=
                        self.pointer = self.is_assign(self.pointer)
                    elif data[self.pointer].value == KEYWORD_STDOUT:
                        self.pointer = self.is_stdout(self.pointer)
                    elif data[self.pointer].value == KEYWORD_LET:  # Declare
                        self.pointer = self.is_let(self.pointer)
                    elif data[self.pointer].value == KEYWORD_IF:
                        self.pointer = self.is_ifstmt(self.pointer)
                    elif data[self.pointer].value == KEYWORD_WHILE:
                        self.pointer = self.is_whilestmt(self.pointer)
                elif data[self.pointer].type == TYPE_STRING:  # An actual string
                    self.gforth.append('s" ' + str(data[self.pointer].value) + '"')
                elif data[self.pointer].type == TYPE_INT:
                    self.gforth.append(str(data[self.pointer].value))
                elif data[self.pointer].type == TYPE_REAL:
                    self.gforth.append(str(data[self.pointer].value) + "e0")
            finally:
                self.pointer += 1
        if len(self.scope_stack) != 0:
            if globals()['DEBUG'] == 1:
                print_title("Scope stack should be empty but has")
                print(self.scope_stack)
        self.gforth.append("cr cr bye")


    def is_let(self, x):  # Declaration
        print_log("FOUND: in: let, stack:" + str(x) + " value: " + str(self.stack[x].value) + " type: " + str(
            self.stack[x].type))
        temp_scope = []
        if self.stack[x].value == KEYWORD_LET:
            x += 1
            if self.stack[x].value == L_PAREN:  # let *( ( x int) )
                temp_scope.append(L_PAREN)
                x += 1
                while self.stack[x].value == L_PAREN:
                    temp_scope.append(L_PAREN)
                    x += 1
                    # self.gforth.append("variable")
                    if self.stack[x].type == TYPE_ID:
                        var_hold_x = x
                        x += 1
                        if self.stack[x].value == TYPE_REAL:
                            self.variables.append((self.stack[x - 1].value, TYPE_REAL))
                            self.gforth.append("fvariable")
                            x += 1
                        elif self.stack[x].value == TYPE_INT:
                            self.variables.append((self.stack[x - 1].value, TYPE_INT))
                            self.gforth.append("variable")
                            x += 1
                        elif self.stack[x].value == TYPE_STRING:
                            self.variables.append((self.stack[x - 1].value, TYPE_STRING))
                            self.gforth.append("variable")
                            x += 1
                        else:
                            print_error("let statement error", error_type="codegen")
                        self.gforth.append(self.stack[var_hold_x].value)
                        if self.stack[x].value == R_PAREN:
                            x += 1
                            temp_scope.pop()
                            self.gforth.append("\n")
        if self.stack[x].value == R_PAREN:
            if len(temp_scope) > 0:
                temp_scope.pop()
            x += 1
        if len(temp_scope) != 0:
            print_error("expected to see final closing bracket on let stmt", error_type="codegen")
        return x

    def is_stdout(self, x, if_stmts=False):
        print_log("FOUND: in: stdout, stack:" + str(x) + " value: " + str(self.stack[x].value) + " type: " + str(
            self.stack[x].type))
        if self.stack[x].value == KEYWORD_STDOUT:
            x += 1
            if self.stack[x].value == L_PAREN:
                self.gforth.append(L_PAREN)
                x += 1
                x, gcode, expr_type = self.is_math_expr(x)
                self.gforth.append(gcode)
                if not if_stmts:
                    self.gforth.append(".")
                x += 1
                if self.stack[x].value == R_PAREN:
                    self.gforth.append(R_PAREN)
            elif self.stack[x].type == TYPE_STRING:
                self.gforth.append('s" ' + self.stack[x].value + '"')
                if not if_stmts:
                    self.gforth.append(".s")
            elif self.stack[x].type == TYPE_INT:
                self.gforth.append(str(self.stack[x].value))
                if not if_stmts:
                    self.gforth.append(".s")
            elif self.stack[x].type == TYPE_REAL:
                self.gforth.append(str(self.stack[x].value) + "e0")
                if not if_stmts:
                    self.gforth.append("f.s")
        return x

    def is_assign(self, x):
        print_log("FOUND: in: assign, stack:" + str(x) + " value: " + str(self.stack[x].value) + " type: " + str(
            self.stack[x].type))
        oper_hold = ''
        if self.stack[x].value == OPER_ASSIGN:
            x += 1
            if self.stack[x].type == TYPE_ID:
                oper_hold = self.stack[x].value
                oper_hold_type = self.check_variable_type(oper_hold)
                if None == oper_hold_type:
                    print_error("variable " + str(oper_hold) + " not declared", error_type='codegen')
                x += 1
                if self.stack[x].value == L_PAREN:
                    x += 1
                    x, gcode, expr_type = self.is_math_expr(x)
                    self.gforth.append(gcode)
                    if self.stack[x].value == R_PAREN:
                        x += 1
                    self.gforth.append(oper_hold)  # append ID
                elif self.stack[x].type == TYPE_STRING:
                    self.gforth.append('s" ' + self.stack[x - 1].value + '"')
                    self.gforth.append(self.stack[x - 1].value)
                elif self.stack[x].type == TYPE_INT:
                    self.gforth.append(str(self.stack[x].value))
                    self.gforth.append(self.stack[x - 1].value)
                elif self.stack[x].type == TYPE_REAL:
                    self.gforth.append(str(self.stack[x].value) + "e0")
                    self.gforth.append(self.stack[x - 1].value)
                elif self.stack[x].type == TYPE_ID:
                    self.gforth.append(str(self.stack[x].value))
                    self.gforth.append(self.stack[x - 1].value)
                else:
                    print_error("in assignment missing value", error_type="codegen")

        self.gforth.append("!")
        if oper_hold != '':
            self.gforth.append(oper_hold)
            self.gforth.append("@")
            self.gforth.append("\n")
        if self.stack[x].value == R_PAREN:
            x += 1
        return x

    def is_math_expr(self, x):
        print_log("FOUND: in: math_expr, stack:" + str(x) + " value: " + str(self.stack[x].value) + " type: " + str(
            self.stack[x].type))
        oper = ''
        expr1 = ''
        expr2 = ''
        expr1_type = ''
        expr2_type = ''
        expr_type = ''

        if self.stack[x].value in ['+', '-', '/', '*', '<', '>', '!', '%', '^']:
            oper = self.stack[x].value
            x += 1

            # EXPR 1
            if self.stack[x].type == TYPE_INT:
                expr1 = self.stack[x].value
                expr1_type = TYPE_INT
                x += 1
            elif self.stack[x].type == TYPE_REAL:
                expr1 = self.stack[x].value
                expr1_type = TYPE_REAL
                x += 1
            elif self.stack[x].type == TYPE_STRING:
                expr1 = self.stack[x].value
                expr1_type = TYPE_STRING
                x += 1
            elif self.stack[x].type == TYPE_ID:
                oper_hold = self.stack[x].value
                expr1_type = self.check_variable_type(oper_hold)
                if None == expr1_type:
                    print_error("variable " + str(oper_hold) + " not declared", error_type='codegen')
                expr1 = oper_hold
                x += 1
            elif self.stack[x].value == L_PAREN:
                # expecting another math expression
                x += 1
                x, expr1, expr1_type = self.is_math_expr(x)
                if self.stack[x].value == R_PAREN:
                    x += 1
            else:
                print_error("error interpreting expr 1", error_type="codegen")


            # EXPR 2
            if self.stack[x].type == TYPE_INT:
                expr2 = self.stack[x].value
                expr2_type = TYPE_INT
                x += 1
            elif self.stack[x].type == TYPE_REAL:
                expr2 = self.stack[x].value
                expr2_type = TYPE_REAL
            elif self.stack[x].type == TYPE_STRING:
                expr2 = self.stack[x].value
                expr2_type = TYPE_STRING
                x += 1
            elif self.stack[x].type == TYPE_ID:
                oper_hold = self.stack[x].value
                expr2_type = self.check_variable_type(oper_hold)
                if None == expr2_type:
                    print_error("variable " + str(oper_hold) + " not declared", error_type='codegen')
                expr2 = oper_hold
                x += 1
            elif self.stack[x].value == L_PAREN:
                # expecting another math expression
                x += 1
                x, expr2, expr2_type = self.is_math_expr(x)
                if self.stack[x].value == R_PAREN:
                    x += 1
                else:
                    print_error("missing right paren after expression", error_type="codegem")
            else:
                print_error("error interpreting expr 2", error_type="codegen")

            if self.stack[x].value == R_PAREN:
                x += 1

        # if expr1_type == TYPE_REAL and expr2_type == TYPE_REAL:
        # expr_type = TYPE_REAL
        # elif expr1_type == TYPE_REAL and expr2_type == TYPE_INT:
        # expr_type = TYPE_REAL
        # elif expr1_type == TYPE_INT and expr2_type == TYPE_INT:
        # expr_type = TYPE_INT
        # elif expr1_type == TYPE_INT and expr2_type == TYPE_REAL:
        #     expr_type = TYPE_REAL
        # else:
        #     print_error("un-recognizable types", error_type="codegen")

        code = str(expr1) + " " + str(expr2) + " " + str(oper)
        return x, code, expr_type

    def is_whilestmt(self, x):
        print_log("FOUND: in: while, stack:" + str(x) + " value: " + str(self.stack[x].value) + " type: " + str(
            self.stack[x].type))
        whilestmt = ''
        parens = []
        if self.stack[x].value == KEYWORD_WHILE:
            whilestmt = "whilestmts" + str(x)
            self.gforth.append(": " + whilestmt + " ")
            x += 1
            if self.stack[x].value == L_PAREN:
                parens.append(L_PAREN)
                x += 1
                x, gcode, expr_type = self.is_math_expr(x)
                self.gforth.append(gcode)
                self.gforth.append("while")

                data = self.stack
                while len(parens) > 0:
                    if data[x].type == 'ops':
                        if data[x].value is L_PAREN:
                            parens.append(L_PAREN)
                            x += 1
                        elif data[x].value is R_PAREN:
                            if parens.pop(-1) != L_PAREN:
                                print_error("must have equal parens in while statements", error_type="codegen")
                            x += 1
                        elif data[x].value in ['+', '-', '/', '*', '<', '>', '!', ';', ':', '%', '^']:
                            x, gcode, expr_type = self.is_math_expr(x)
                            self.gforth.append(gcode)
                            x += 1
                    elif data[x].type == 'keywords':
                        if data[x].value == OPER_ASSIGN:  # :=
                            x = self.is_assign(x)
                            x += 1
                        elif data[x].value == KEYWORD_STDOUT:
                            x = self.is_stdout(x)
                            x += 1
                        elif data[x].value == KEYWORD_LET:  # Declare
                            x = self.is_let(x)
                            x += 1
                        elif data[x].value == KEYWORD_IF:
                            x = self.is_ifstmt(x)
                            x += 1
                        elif data[x].value == KEYWORD_WHILE:
                            x = self.is_whilestmt(x)
                            x += 1
                    elif data[x].type == TYPE_STRING:  # An actual string
                        self.gforth.append('s" ' + str(data[x].value) + '"')
                        x += 1
                    elif data[x].type == TYPE_INT:
                        self.gforth.append(str(data[x].value))
                        x += 1
                    elif data[x].type == TYPE_REAL:
                        self.gforth.append(str(data[x].value) + "e0")
                        x += 1

                self.gforth.append("REPEAT")
                self.gforth.append(";")
                self.gforth.append(whilestmt + " . \n")

        return x

    def is_while_internals(self, x):
        print_log("FOUND: in: while_internals, stack:" + str(x) + " value: " + str(self.stack[x].value) + " type: " + str(
            self.stack[x].type))
        if self.stack[x].value == L_PAREN:
            x += 1
            x = self.is_stdout(x, True)
            x, gcode, expr_type = self.is_math_expr(x)
            self.gforth.append(gcode)
            x = self.is_assign(x)

            x += 1
            if self.stack[x].value == R_PAREN:
                x += 1
        else:
            print_error("missing left paren [e]", error_type='codegen')
            return -1
        return x

    def is_ifstmt(self, x):
        print_log("FOUND: in: if, stack:" + str(x) + " value: " + str(self.stack[x].value) + " type: " + str(
            self.stack[x].type))
        if_stmts = ''
        if self.stack[x].value == KEYWORD_IF:
            x += 1
            if self.stack[x].value == L_PAREN:
                x += 1
                if self.stack[x].value in ['<', '>', '=<', '=>', '!', KEYWORD_TRUE, KEYWORD_FALSE]:
                    x += 1
                    if self.stack[x].type == TYPE_INT or self.stack[x].type == TYPE_REAL or \
                                    self.stack[x].type == TYPE_ID:
                        x += 1
                        # TODO fix the variable checking here
                        if self.stack[x].type == TYPE_INT or self.stack[x].type == TYPE_REAL or \
                                        self.stack[x].type == TYPE_ID:
                            # TODO fix the variable checking here
                            if_stmts = "ifloop" + str(x - 4)
                            self.scope_stack.append(if_stmts)

                            temp_stack = []
                            # self.scope_stack.append(L_PAREN)
                            temp_stack.append(if_stmts)  # Because we enter this function at the 'if'
                            temp_stack.append(L_PAREN)

                            self.gforth.append(": " + if_stmts)
                            self.gforth.append(L_PAREN)
                            if self.stack[x - 1].type == TYPE_ID and self.stack[x - 1].value not in self.variables:
                                print_error("variable " + str(self.stack[x - 1].value) + " not declared before use")
                            self.gforth.append(self.stack[x - 1].value)  # x
                            self.gforth.append("@")
                            if self.stack[x].type == TYPE_ID and self.stack[x].value not in self.variables:
                                print_error("variable " + str(self.stack[x].value) + " not declared before use")
                            self.gforth.append(self.stack[x].value)  # 3
                            self.gforth.append(self.stack[x - 2].value)  # <
                            self.gforth.append("if")
                            x += 1

                            if self.stack[x].value == R_PAREN:
                                x += 1
                                stack_val = temp_stack.pop()
                                if stack_val != L_PAREN:
                                    print_error("incorrect token", error_type="codegen")
                                else:
                                    self.gforth.append(stack_val)
                                    while self.stack[x].value != R_PAREN:
                                        x = self.is_if_internals(x)
                                        self.gforth.append("TYPE else")
                                    self.scope_stack.pop()
            self.gforth.append("then")
            self.gforth.append(";")
            var = temp_stack.pop()
            self.gforth.append("\n" + var + "\n")
        return x

    def is_if_internals(self, x):
        print_log("FOUND: in: if_internals, stack:" + str(x) + " value: " + str(self.stack[x].value) + " type: " + str(
            self.stack[x].type))
        if self.stack[x].value == L_PAREN:
            x += 1
            x = self.is_stdout(x, True)
            x, gcode, expr_type = self.is_math_expr(x)
            self.gforth.append(gcode)

            x += 1
            if self.stack[x].value == R_PAREN:
                x += 1
                pass
            else:
                print_error("missing right paren [b]", error_type='codegen')
        else:
            print_error("missing left paren", error_type='codegen')
        return x

    def get_tokens_stack(self):
        self._get_token_stack(self.tree)
        self.print_stack()

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
        if globals()['DEBUG'] == 1:
            print_title("print stack called")
            for token in self.stack:
                print_token(token)
