ª__author__ = 'Drake'
import string


class Tokenizer():
    def __init__(self):
        # tokens is a dictionary where each value is a list
        self.tokens = \
            {"keywords": ['let', ':=', 'if', 'while', 'for', ';',
                          "true", "false"],
             "ops": ['and', 'or', 'not', '=', '+', '-', '/', '*',
                     '<', '<=', '>', '>=', '!='],
             'type': ['bool', 'int', 'real', 'string'],
             'mainScope': []}
        self.current_scope = 'mainScope'

    def get_current_scope(self):
        return self.current_scope

    # Function Description:
    # Add a token using the entire path in a list
    # Example add_token(('mainScope', 'test'))
    def add_token(self, key, value):
        # TODO create a method for adding to the token dictionary
        self.tokens[key].insert(len(self.tokens[key]), value)

    def has_token(self, value, key=''):
        # if subgroup given check it first
        if key != '':
            if value in self.tokens[key]:
                print("The token " + value + " exist")
                return True

        # if subgroup checking fails check all entries
        for x in self.tokens:
            if value in self.tokens[x]:
                print("The token " + value + " exist")
                return True
        return False

    def add_scope(self, scope_name):
        # Add new scope
        self.tokens[scope_name] = []
        # link the new scope into the current scope in order to say that it is within a scope
        self.tokens[self.current_scope] = self.tokens[scope_name]
        # set the current scope to the added scope so that variables can be added there.
        self.current_scope = scope_name


class Lexer():
    def __init__(self, file, tokenizer):
        self.line = 1
        self.input = file
        self.peek = ' '
        self.tokens = tokenizer
        self.token_list = []

    def get_next_char(self):
        try:
            self.peek = self.input.read(1)
        except EOFError:
            print("Reached end of file")

    def control(self):
        while 1:
            self.peek = self.input.read(1)
            if self.peek == ' ' or self.peek == '\t':
                print("found white space")
                continue
            elif self.peek == '\n':
                self.line += 1
            elif self.peek in ('=', '+', '-', '/', '*', '<', '>', '!', ';', '%'):
                self.is_operation()
            elif self.is_letter():
                # identify the string and add to the token list
                self.identify_string()
            elif self.is_digit():
                # identify the number and add to the token list
                self.is_number()
            elif self.peek == ')':
                # if ')' then current scope is ended
                return
            else:
                print("ERROR: Could not identify on line: " + str(self.line) + " near char: '" + self.peek + "'")
                break

    def is_operation(self):
        op = self.peek
        self.get_next_char()
        if op == '+':
            if self.peek == '+':
                op += self.peek
        elif op == '-':
            if self.peek == '-':
                op += self.peek
        elif op == '*':
            if self.peek == '*':
                op += self.peek
        elif op in ('<', '>', '!'):
            self.get_next_char()
            if self.peek == '=':
                op += self.peek
        # elif op in ('%', ';', '/', '='):
        if self.tokens.has_token(op, 'ops'):
            print("DEBUG: is_operation, self.tokens.has_token(" + op + "'ops') return true" + " on line " + str(
                self.line))
            self.token_list.append(("op", op))
        else:
            print("DEBUG: is_operation, self.tokens.has_token(" + op + "'ops') return false" + " on line " + str(
                self.line))

    def get_assignment(self, word):
        print("receive word and going to set to expression")

    def wait_for_expression(self):
        print("looking for expression")

    def wait_for(self, value):
        while 1:
            self.peek = self.input.read(1)
            if self.peek == ' ' or self.peek == '\t':
                # print("found white space")
                continue
            elif self.peek == '\n':
                # print("found new line")
                self.line += 1
            elif self.peek == value:
                return True
            else:
                print("ERROR (line:" + str(self.line) + ") looking for '" +
                      str(value) + "' but found '" + str(self.peek) + "'")
                return False

    def expression_identification(self, word):
        if word in ['bool', 'int', 'real', "string"]:
            # TODO add next word to current scope with type info
            # Definition of token <TYPE, VariableName>
            print("print variable type")
        elif word == 'for':
            self.wait_for("(")
            self.wait_for_expression()
            self.wait_for(";")
            self.wait_for_expression()
            self.wait_for(";")
            self.wait_for_expression()
            self.wait_for(")")
            self.wait_for("{")
            self.tokens.add_scope("for")  # TODO check that create a new scope works
            self.wait_for("(")
            # TODO call control as it will return to here and will have to wait for closing bracket
            self.control()  # if it returns then it saw a ')'
        elif word == "while":
            self.wait_for("(")
            self.wait_for_expression()
            self.wait_for(")")
            self.wait_for("{")
            self.tokens.add_scope("while")  # TODO check that create a new scope works
            self.wait_for("(")
            # TODO call control as it will return to here and will have to wait for closing bracket
            self.control()  # if it returns then it saw a ')'
        elif word == "if":
            self.wait_for("(")
            self.wait_for_expression()
            self.wait_for(")")
            self.wait_for("{")
            self.tokens.add_scope("if")  # TODO check that create a new scope works
            self.wait_for("(")
            # TODO call control as it will return to here and will have to wait for closing bracket
            self.control()  # if it returns then it saw a ')'

    def identify_string(self):
        word = self.parse_string(list(string.ascii_letters) +
                                 list(string.digits) + list('_'),
                                 list(string.ascii_letters))
        # If the token is contained within the dictionary we don't need to add it
        # TODO Add to tree (next milestone)
        if self.tokens.has_token(word):
            print("Already contains token")
        else:
            self.tokens.add_token(self.tokens.get_current_scope(), word)

    # Function Description:
    # This function should be called after seeing the start of a number
    # If a period is present the number is converted to a float and returned
    def is_number(self):
        # TODO: add support for values like 2.3e2 (NEEDs testing)
        value = ''
        # assume no decimal until we see one
        decimal_flag = False
        while self.is_digit():
            if self.peek == "." and decimal_flag:
                # seen our second decimal return current value as a float
                return float(value)
            elif self.peek == '.' and not decimal_flag:
                # seen our first decimal
                decimal_flag = True
            elif self.peek == 'e':
                # once you 'e' has been seen no decimal can be used
                decimal_flag = True
            # append the digit to the value
            value += self.peek
            # move to the next char
            self.get_next_char()
        if '.' in value or 'e' in value:
            return float(value)
        else:
            try:
                return int(value)
            except ValueError:
                print("ERROR (line: " + str(self.line) + "): could not determine numerical value")

    # Function Description:
    # checks to see if the current value in peek is a digit or '.'
    # return true if it is
    def is_digit(self, others=[]):
        digits = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '9', 'e']
        for x in others:
            if x not in digits:
                digits.append(x)
        if self.peek in digits:
            return True
        return False

    # Function Description:
    # checks to see if the current value in peek is a letter
    # return true if it is
    def is_letter(self, others=[]):
        letters = list(string.ascii_letters)
        for x in others:
            if x not in letters:
                letters.append(x)
        if self.peek in letters:
            return True
        return False

    # Function Description:
    # This function should be called when a word identifier or keyword is started
    # and will return the full word upon seeing invalid characters.
    def parse_string(self, accepted_chars, acceptable_first_chars=[]):
        if self.peek not in acceptable_first_chars:
            return -1
        else:
            word = ''
            while self.peek in accepted_chars:
                word += self.peek
                self.get_next_char()
            return word