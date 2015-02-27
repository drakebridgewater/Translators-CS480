__author__ = 'drakebridgewater'
import string

from defines import *


class Lexer():
    def __init__(self, filename):
        self.line = 1
        self.filename = filename
        self.file = ''
        self.current_char = ' '
        self.pointer = 0
        self.token_list = []
        self.current_state = True  # When false throw error
        self.accepted_ops = ('=', '+', '-', '/', '*', '<', '>', '!', ';', ':', '%', '(', ')', '^')
        # tokens is a dictionary where each token is a list
        self.tokens = \
            {"keywords": [KEYWORD_STDOUT, KEYWORD_LET, KEYWORD_IF, KEYWORD_WHILE,
                          KEYWORD_TRUE, KEYWORD_FALSE, OPER_ASSIGN],
             "ops": [OPER_ASSIGN, OPER_ADD, OPER_SUB, OPER_DIV, OPER_MULT,
                     OPER_LT, OPER_GT, OPER_NOT, OPER_MOD, OPER_EXP,
                     OPER_AND, OPER_OR, OPER_NOT, OPER_NE, R_PAREN, L_PAREN],
             'type': [TYPE_BOOL, TYPE_INT, TYPE_REAL, TYPE_STRING]
            }

    def open_file(self):
        self.file = open(self.filename, 'r')

    def close_file(self):
        self.file.close()

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

    def get_next_char(self):
        try:
            self.current_char = self.file.read(1)
        except EOFError:
            print("Reached end of file")

    def get_token(self):
        self.get_next_char()
        while True and self.current_state:
            if not self.current_char:
                return -1
            if self.current_char == ' ' or self.current_char == '\t':
                self.get_next_char()
                pass
            elif self.current_char == '\n':
                self.get_next_char()
                self.line += 1
            elif self.current_char in self.accepted_ops:
                return self.is_op()
            elif self.is_letter():
                return self.identify_word()  # identify the string and add to the token list
            elif self.is_digit():
                return self.is_number()  # identify the number and add to the token list
            elif self.current_char == '"':
                return self.create_token(("ops", '"'))
                # self.parse_string()                 # parse a string
            else:
                print("Line:ERROR: Could not identify on line: " + str(
                    self.line) + " near char: '" + self.current_char + "'")
                return None

                # TODO have all functions return to a state that has the next char

    # Function Description:
    # General function to do something with the tokens once we have classified them.
    def create_token(self, token):
        new_token = Token()
        new_token.line = self.line
        new_token.type = token[0]
        new_token.value = token[1]
        return new_token

    def add_token(self, token):
        new_token = Token()
        new_token.line = self.line
        new_token.type = token[0]
        new_token.value = token[1]
        self.token_list.append(new_token)

    def print_tokens(self):
        for x in self.token_list:
            print("[line: " + x.line + ", ID: " + x.type + ", Value: " + x.value + "]")

    def is_op(self):
        item = self.current_char
        # If we see an op look to see if we see another. If we see another add the previous
        # found op
        if self.current_char is '+':
            self.get_next_char()
            return self.create_token((self.has_token(item), item))
        elif self.current_char is '-':
            self.get_next_char()
            # if self.current_char is '-':
            # item += self.current_char  # Seen -- make new token
            #    self.get_next_char()
            return self.create_token((self.has_token(item), item))
        elif self.current_char in ('<', '>', '!'):
            self.get_next_char()
            if self.current_char == '=':
                item += self.current_char
                self.get_next_char()
            return self.create_token((self.has_token(item), item))
        elif self.current_char in ':':
            self.get_next_char()
            if self.current_char is '=':
                item += self.current_char
                return self.create_token((self.has_token(item), item))
            else:
                print("Lexer Error [Line: " + str(
                    self.line) + '] the "' + self.current_char + '" symbol not recognized after colon [:]')
        elif self.current_char in '=':
            return self.create_token((self.has_token(item), item))
        elif self.current_char in ('*', '/', '(', ')', '%', '^'):
            self.get_next_char()
            return self.create_token((self.has_token(item), item))
        else:
            print("Lexer Error: [Line: " + str(self.line) + "] could not intemperate: " +
                  self.current_char)
            return -1

    def parse_string(self):
        accepted_chars = ['"']
        new_string = ''
        self.get_next_char()
        while self.current_char in accepted_chars:
            new_string += self.current_char
            self.get_next_char()
        self.token_list.append(("string", new_string))

    def identify_word(self):
        accepted_chars = list(string.ascii_letters) + list(string.digits) + list('_')
        acceptable_first_chars = list(string.ascii_letters)

        word = ''
        if self.current_char in acceptable_first_chars:
            word += self.current_char
            self.get_next_char()
            while self.current_char in accepted_chars:
                word += self.current_char
                self.get_next_char()
        token_value = word
        token_type = self.has_token(token_value)
        if token_type == -1:
            token_type = "ID"
        return self.create_token((token_type, token_value))

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

    def is_int(self):
        word = ''
        while self.is_digit(exclude=['.', 'e']):
            word += self.current_char
            self.get_next_char()

        return word

    # Function Description:
    # This function should be called after seeing the start of a number
    # If a period is present the number is converted to a float and returned
    def is_number(self, value=''):
        if value == '':
            word = self.current_char
        else:
            word = value
        self.get_next_char()

        other_accepted = ['.']  # accept additional chars if we have seen certain chars
        while self.is_digit(other_accepted):
            if self.current_char is '.':
                if '.' in other_accepted:
                    other_accepted.remove('.')
                if '.' not in word:
                    # this number is a decimal
                    word += self.current_char
                    self.get_next_char()
                else:
                    # word already contains a dot. don't get next char
                    return self.create_token(('float', float(word)))
            elif self.current_char is 'e':  # once you 'e' has been seen no decimal can be used
                if '.' in other_accepted:
                    other_accepted.remove('.')
                self.get_next_char()
                if self.current_char is '+':
                    self.get_next_char()
                    exp = self.is_int()
                    try:
                        self.get_next_char()
                        exp = int(exp)
                        word += 'e+'
                        word += str(exp)
                        try:
                            return self.create_token(("float", float(word)))
                        except ValueError:
                            print("Fatal parse error: [row: " + str(self.line) + "] when parsing char '" +
                                  str(self.current_char) + "' for: \n\t\t" + str(word))
                    except ValueError:
                        return [self.create_token(("int", word)),
                                self.create_token(("ID", "e")),
                                self.create_token((self.has_token("+"), "+"))]

                elif self.current_char is '-':
                    self.get_next_char()
                    exp = self.is_int()
                    try:
                        self.get_next_char()
                        exp = int(exp)
                        word += 'e-'
                        word += str(exp)
                        try:
                            return self.create_token(("float", float(word)))
                        except ValueError:
                            print("Fatal parse error: [row: " +
                                  str(self.line) + "] when parsing char '" +
                                  str(self.current_char) + "' for: \n\t\t" + str(word))
                    except ValueError:
                        return [self.create_token(("int", word)),
                                self.create_token(("ID", "e")),
                                self.create_token((self.has_token("-"), "-"))]
                else:
                    exp = self.is_int()
                    try:
                        exp = int(exp)
                        word += str(exp)
                        return self.create_token(("float", float(word)))
                    except ValueError:
                        print("Lexer Error: [row: " + str(self.line) + "] Unable to parse '" +
                              str(self.current_char) + "' in: " + str(exp))
            elif self.is_digit(other_accepted):
                word += self.current_char
                self.get_next_char()
            else:
                break
            if 'e' not in other_accepted:
                other_accepted.append('e')

        if '.' in word or 'e' in word:
            try:
                return self.create_token(("float", float(word)))
            except ValueError:
                print("Lexer Error (line: " + str(self.line) +
                      "): could not determine numerical token of: " + str(word))
        else:
            try:
                return self.create_token(("int", int(word)))
            except ValueError:
                print("Lexer Error (line: " + str(self.line) +
                      "): could not determine numerical token of: " + str(word))

    # Function Description:
    # checks to see if the current token in peek is a digit or '.'
    # return true if it is
    def is_digit(self, others=[], exclude=[]):
        digits = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for x in others:
            if x not in digits:
                digits.append(x)
        for x in exclude:
            if x in digits:
                digits.remove(x)
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
