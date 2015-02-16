#!/usr/bin/python
# __author__ = 'Drake'
import string


class Tokenizer():
    def __init__(self):
        # tokens is a dictionary where each token is a list
        self.tokens = \
            {"keywords": ['stdout', 'let', ':=', 'if', 'while', ';',
                          "true", "false"],
             "ops": ['and', 'or', 'not', '=', '+', '-', '/', '*',
                     '<', '<=', '>', '>=', '!=', '(', ')', '%', '^'],
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
                return key

        # if subgroup checking fails check all entries
        for x in self.tokens:
            if value in self.tokens[x]:
                return x
        return -1

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
        self.current_char = ' '
        self.pointer = 0
        self.tokens = tokenizer
        self.token_list = []
        self.current_state = True  # When false throw error

    def get_next_char(self):
        try:
            self.current_char = self.input.read(1)
        except EOFError:
            print("Reached end of file")

    def reed_next_char(self):
        return self.input.read(1)

    def peek(self):
        self.current_char = self.input.read(1)
        self.pointer -= 1

    def add_token(self, token):
        self.token_list.append(token)
        if self.pointer != 0:
            self.current_char = self.input.read(self.pointer)
            self.pointer = 0

    def print_tokens(self):
        for x in self.token_list:
            print(x)

    def control(self):
        while 1:
            if self.current_char == ' ' or self.current_char == '\t':
                self.get_next_char()
                pass
            elif self.current_char == '\n':
                self.get_next_char()
                self.line += 1
            elif self.current_char in ('=', '+', '-', '/', '*', '<', '>', '!', ';', '%', '(', ')'):
                self.is_operation()
            elif self.is_letter():
                self.identify_word()  # identify the string and add to the token list
            elif self.is_digit():
                self.is_number()  # identify the number and add to the token list
            elif self.current_char == '"':
                self.add_token(("ops", '"'))
                self.get_next_char()
                # self.parse_string()                 # parse a string
            else:
                print(
                    "ERROR: Could not identify on line: " + str(self.line) + " near char: '" + self.current_char + "'")
                break

    def is_operation(self):
        op = self.current_char
        if op == '+':
            pass
        elif op == '-':
            if self.current_char == '-':
                op += self.current_char
            elif self.is_digit():
                self.is_number(op)
                return
        elif op == '*':
            pass
        elif op in ('<', '>', '!'):
            self.get_next_char()
            if self.current_char == '=':
                op += self.current_char
        # elif op in ('%', ';', '/', '='):

        key = self.tokens.has_token(op)
        self.pointer = 1
        self.add_token((key, op))

    def get_assignment(self, word):
        print("receive word and going to set to expression")

    def wait_for_expression(self):
        print("looking for expression")

    def wait_for(self, value):
        while 1:
            self.current_char = self.input.read(1)
            if self.current_char == ' ' or self.current_char == '\t':
                # print("found white space")
                continue
            elif self.current_char == '\n':
                # print("found new line")
                self.line += 1
            elif self.current_char in value:
                return True
            else:
                print("ERROR (line:" + str(self.line) + ") looking for '" +
                      str(value) + "' but found '" + str(self.current_char) + "'")
                return False

    def expression_identification(self, word):
        if word in ['bool', 'int', 'real', "string"]:
            # TODO add next word to current scope with type info
            # Definition of token <TYPE, VariableName>
            print("print variable type")
            self.token_list.append(word, self.identify_word())
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

    def parse_string(self):
        accepted_chars = ['"']
        new_string = ''
        self.get_next_char()
        while self.current_char in accepted_chars:
            new_string += self.current_char
            self.get_next_char()
        self.token_list.append(("string", new_string))

    def identify_word(self):
        word = self.parse_word(list(string.ascii_letters) +
                               list(string.digits) + list('_'),
                               list(string.ascii_letters))
        # If the token is contained within the dictionary we don't need to add it
        # TODO Add to tree (next milestone)
        token_class = self.tokens.has_token(word)
        if token_class == -1:
            token_class = self.tokens.get_current_scope()
            self.tokens.add_token(token_class, word)
        self.pointer = 1
        self.add_token((token_class, word))

    # Function Description:
    # This function should be called when a word identifier or keyword is started
    # and will return the full word upon seeing invalid characters.
    def parse_word(self, accepted_chars, acceptable_first_chars=[]):
        if self.current_char not in acceptable_first_chars:
            return -1
        else:
            word = ''
            while self.current_char in accepted_chars:
                word += self.current_char
                self.get_next_char()
            return word

    # Function Description:
    # This function should be called after seeing the start of a number
    # If a period is present the number is converted to a float and returned
    def is_number(self, value=''):
        value += self.current_char
        self.peek()
        other_accepted = ['.']  # accept additional chars if we have seen certain chars
        while self.is_digit(other_accepted):
            if self.current_char == ".":  # seen our first decimal
                if '.' in other_accepted:  # we see . and we have not seen one befoe this
                    other_accepted.remove('.')
                else:
                    self.pointer = 0
                    self.add_token(("float", float(value)))
                    return float(value)
                    # the . does not get appended as it is another number
            elif self.current_char == 'e':  # once you 'e' has been seen no decimal can be used
                if '.' in other_accepted:
                    other_accepted.remove('.')
                other_accepted.append("+")
                other_accepted.append("-")
            value += self.current_char  # append the digit to the token
            self.peek()  # move to the next char
            other_accepted.append('e')  # Once a number has been seen allow seeing an e
        if '.' in value or 'e' in value:
            self.pointer = 0
            self.add_token(("float", float(value)))
            return float(value)
        else:
            try:
                self.pointer = 0
                self.add_token(("int", int(value)))
                return int(value)
            except ValueError:
                print("ERROR (line: " + str(self.line) + "): could not determine numerical token")

    # Function Description:
    # checks to see if the current token in peek is a digit or '.'
    # return true if it is
    def is_digit(self, others=[]):
        digits = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '9']
        for x in others:
            if x not in digits:
                digits.append(x)
        if self.current_char in digits:
            return True
        return False

    # Function Description:
    # checks to see if the current token in peek is a letter
    # return true if it is
    def is_letter(self, others=[]):
        letters = list(string.ascii_letters)
        for x in others:
            if x not in letters:
                letters.append(x)
        if self.current_char in letters:
            return True
        return False
