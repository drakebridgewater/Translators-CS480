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
                        try:
                            if self.gforth[len(self.gforth) - 1] != '\n':
                                self.gforth.append('\n')
                            pop_value = self.scope_stack.pop()
                            if 'whileloop' in pop_value:
                                temp = pop_value.split("whileloop")
                                self.gforth.append("whileloop" + temp[len(temp) - 1] + "\n")
                            if 'ifloop' in pop_value:
                                temp = pop_value.split("ifloop")
                                self.gforth.append("ifloop" + temp[len(temp) - 1] + "\n")
                            prev_was_declare = False
                            oper_hold = []
                        except IndexError:
                            print_error("missing left paren [d]", error_type="code_gen")
                    elif data[self.pointer].value in ['+', '-', '/', '*', '<', '>', '!', ';', ':', '%', '^']:
                        self.pointer, gcode, expr_type = self.is_math_expr(self.pointer)
                        self.gforth.append(gcode)
                elif data[self.pointer].type == TYPE_ID:
                    if self.stack[self.pointer].value not in self.variables:
                        print_error("variable " + str(self.stack[self.pointer].value) + " not declared before use")
                    if data[self.pointer].value in self.current_scope:
                        pass
                    elif prev_was_declare:
                        if data[self.pointer].value in self.variables:
                            print_error("redecloration of variable " + str(data[self.pointer].value),
                                        error_type="codegen")
                        self.current_scope.append(data[self.pointer].value)
                    else:
                        print_error("unassigned variable " + str(data[self.pointer].value), error_type="codegen")
                    self.gforth.append(str(data[self.pointer].value))

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
            print_error("missing right paren [c]", error_type="code_gen")
            if globals()['DEBUG'] == 1:
                print_title("Scope stack should be empty but has")
                print(self.scope_stack)
        self.gforth.append("cr cr bye")

    def is_let(self, x):
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
                            self.variables.append((self.stack[x - 1], TYPE_REAL))
                            self.gforth.append("fvariable")
                            x += 1
                        elif self.stack[x].value == TYPE_INT:
                            self.variables.append((self.stack[x - 1], TYPE_INT))
                            self.gforth.append("variable")
                            x += 1
                        elif self.stack[x].value == TYPE_STRING:
                            self.variables.append((self.stack[x - 1], TYPE_STRING))
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
        oper_hold = ''
        if self.stack[x].value == OPER_ASSIGN:
            x += 1
            if self.stack[x].type == TYPE_ID:
                oper_hold = self.stack[x].value
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
                expr1 = self.stack[x].value
                x += 1
            elif self.stack[x].value == L_PAREN:
                # expecting another math expression
                x += 1
                x, expr1, expr1_type = self.is_math_expr(x)
                if self.stack[x].value == R_PAREN:
                    x+=1
                else:
                    print_error("missing right paren after expression", error_type="codegem")
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
                expr2 = self.stack[x].value
                x += 1
            elif self.stack[x].value == L_PAREN:
                # expecting another math expression
                x += 1
                x, expr2, expr2_type = self.is_math_expr(x)
                if self.stack[x].value == R_PAREN:
                    x+=1
                else:
                    print_error("missing right paren after expression", error_type="codegem")
            else:
                print_error("error interpreting expr 2", error_type="codegen")

            if self.stack[x].value == R_PAREN:
                x += 1
            else:
                print_error("closing paren expected after math expression", error_type="codegen")

        # if expr1_type == TYPE_REAL and expr2_type == TYPE_REAL:
        # expr_type = TYPE_REAL
        # elif expr1_type == TYPE_REAL and expr2_type == TYPE_INT:
        #     expr_type = TYPE_REAL
        # elif expr1_type == TYPE_INT and expr2_type == TYPE_INT:
        #     expr_type = TYPE_INT
        # elif expr1_type == TYPE_INT and expr2_type == TYPE_REAL:
        #     expr_type = TYPE_REAL
        # else:
        #     print_error("un-recognizable types", error_type="codegen")

        code = str(expr1) + " " + str(expr2) + " " + str(oper)
        return x, code, expr_type

    def is_math_expr2(self, x):
        if self.stack[x].value in ['+', '-', '/', '*', '<', '>', '!', '%', '^']:
            x += 1
            if self.stack[x].type == TYPE_INT:
                x += 1
                if self.stack[x].type == TYPE_INT:  # int int
                    self.gforth.append(self.stack[x - 1].value)
                    self.gforth.append(self.stack[x].value)
                    self.gforth.append(self.stack[x - 2].value)
                elif self.stack[x].type == TYPE_REAL:  # int real
                    self.gforth.append(self.stack[x - 1].value)
                    self.gforth.append(str(self.stack[x].value) + "e0")
                    self.gforth.append("fswap")
                    self.gforth.append("s>f")
                    self.gforth.append(self.realConversions[self.stack[x - 2].value])
                elif self.stack[x].type == TYPE_ID:
                    # TODO check if the variable exists
                    self.gforth.append(self.stack[x - 1].value)  # value
                    if self.stack[x].value not in self.variables:
                        print_error("variable " + str(self.stack[x].value) + " not declared before use")
                    self.gforth.append(self.stack[x].value)  # variable
                    self.gforth.append("@")
                    self.gforth.append(self.stack[x - 2].value)
                else:
                    print_error("expected another int/real/string", error_type="codegen")
            elif self.stack[x].type == TYPE_REAL:
                x += 1
                if self.stack[x].type == TYPE_INT:  # real int
                    self.gforth.append(str(self.stack[x - 1].value) + "e0")
                    self.gforth.append(self.stack[x].value)
                    self.gforth.append("fswap")
                    self.gforth.append("s>f")
                    self.gforth.append(self.realConversions[self.stack[x - 2].value])
                elif self.stack[x].type == TYPE_REAL:  # real real
                    self.gforth.append(str(self.stack[x - 1].value) + "e0")
                    self.gforth.append(str(self.stack[x].value) + "e0")
                    self.gforth.append(self.realConversions[self.stack[x - 2].value])
                elif self.stack[x].type == TYPE_ID:
                    # TODO check if the variable exists
                    self.gforth.append(self.stack[x - 1].value)  # value
                    if self.stack[x].value not in self.variables:
                        print_error("variable " + str(self.stack[x].value) + " not declared before use")
                    self.gforth.append(self.stack[x].value)  # variable
                    self.gforth.append("@")
                    self.gforth.append(self.stack[x - 2].value)
                else:
                    print_error("expected another int/real/string", error_type="codegen")
            elif self.stack[x].type == TYPE_STRING:
                x += 1
                if self.stack[x].type == TYPE_STRING:
                    self.gforth.append('s" ' + self.stack[x - 1].value + '"')
                    self.gforth.append('s" ' + self.stack[x].value + '"')
                    if self.stack[x - 2].value == "+":
                        self.gforth.append("s" + self.stack[x - 2].value)
                    else:
                        print_error("only string concatenation is supported", error_type="codegen")
            elif self.stack[x].type == TYPE_ID:
                if self.stack[x].value not in self.variables:
                    print_error("variable " + str(self.stack[x].value) + " not declared before use")
                self.gforth.append(self.stack[x].value)
                self.gforth.append("@")
                x += 1
                if self.stack[x].type == TYPE_INT:
                    self.gforth.append(self.stack[x].value)
                elif self.stack[x].type == TYPE_REAL:
                    self.gforth.append(self.stack[x].value)
                x += 1
                self.gforth.append(self.stack[x - 3].value)
            elif self.stack[x].value == L_PAREN:
                temp_x = x
                x = self.is_math_expr(x)
                x = self.is_math_expr(x)
                self.gforth.append(self.stack[temp_x].value)

        if self.stack[x].value == R_PAREN:
            self.gforth.append(R_PAREN)
            self.scope_stack.pop()
        return x

    def is_whilestmt(self, x):
        while_stmts = ''
        if self.stack[x].value == KEYWORD_WHILE:
            x += 1
            if self.stack[x].value == L_PAREN:
                x += 1
                if self.stack[x].value in ['<', '>', '=<', '=>', '!', KEYWORD_TRUE, KEYWORD_FALSE]:
                    x += 1
                    if self.stack[x].type == TYPE_INT or self.stack[x].type == TYPE_REAL or \
                                    self.stack[x].type == TYPE_ID:
                        x += 1
                        if self.stack[x].type == TYPE_INT or self.stack[x].type == TYPE_REAL or \
                                        self.stack[x].type == TYPE_ID:
                            while_stmts = "whilestmts" + str(x - 4)
                            self.scope_stack.append(L_PAREN)
                            self.scope_stack.append(while_stmts)

                            temp_stack = []
                            # self.scope_stack.append(L_PAREN)
                            temp_stack.append(while_stmts)
                            temp_stack.append(L_PAREN)
                            self.scope_stack.append(L_PAREN)  # Because we enter this function at the 'if'

                            self.gforth.append(": " + while_stmts)
                            self.gforth.append(L_PAREN)
                            self.gforth.append("BEGIN")
                            if self.stack[x - 1].type == TYPE_ID and self.stack[x - 1].value not in self.variables:
                                print_error("variable " + str(self.stack[x - 1].value) + " not declared before use")
                            self.gforth.append(self.stack[x - 1].value)  # x
                            self.gforth.append("@")
                            if self.stack[x].type == TYPE_ID and self.stack[x].value not in self.variables:
                                print_error("variable " + str(self.stack[x].value) + " not declared before use")
                            self.gforth.append(self.stack[x].value)  # 3
                            self.gforth.append(self.stack[x - 2].value)  # <
                            self.gforth.append("while")
                            x += 1

                            if self.stack[x].value == R_PAREN:
                                self.scope_stack.pop()
                                x += 1
                                stack_val = temp_stack.pop()
                                if stack_val != L_PAREN:
                                    print_error("incorrect token", error_type="codegen")
                                else:
                                    self.gforth.append(stack_val)
                                    while self.stack[x].value != R_PAREN:
                                        temp = self.is_while_internals(x)
                                        if temp == -1:
                                            break
                                        else:
                                            x = temp
                                        self.gforth.append("TYPE ")
                                    self.scope_stack.pop()
                                    self.gforth.pop()  # remove the last 'type' from gforth

            self.gforth.append("REPEAT")
            self.gforth.append(";")
            var = temp_stack.pop()
            self.gforth.append("\n" + var + "\n")
        return x

    def is_while_internals(self, x):
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
                        if self.stack[x].type == TYPE_INT or self.stack[x].type == TYPE_REAL or \
                                        self.stack[x].type == TYPE_ID:
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
