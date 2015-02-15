__author__ = 'drakebridgewater'
import string


# class Ops(Enum):
# EQ = '='
# ADD = '+'
#     SUB = '-'
#     DIV = '/'
#     MULT = '*'
#     LT = '<'
#     GT = '>'
#     NOT = '!'
#     SEMI = ';'
#     MOD = '%'
#     L_PAREN = '('
#     R_PAREN = ')'
#     EXP = '^'


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
        # tokens is a dictionary where each data is a list
        self.tokens = \
            {"keywords": ['stdout', 'let', ':=', 'if', 'while', ';',
                          "true", "false"],
             "ops": ['and', 'or', 'not', '=', '+', '-', '/', '*',
                     '<', '<=', '>', '>=', '!=', '(', ')', '%', '^'],
             'type': ['bool', 'int', 'real', 'string']
            }

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

    def control(self):
        with open(self.filename, 'r') as f:
            self.file = f
            while True and self.current_state:
                if not self.current_char:
                    break
                if self.current_char == ' ' or self.current_char == '\t':
                    self.get_next_char()
                    pass
                elif self.current_char == '\n':
                    self.get_next_char()
                    self.line += 1
                elif self.is_operation():
                    pass
                elif self.is_letter():
                    self.identify_word()  # identify the string and add to the token list
                elif self.is_digit():
                    self.is_number()  # identify the number and add to the token list
                elif self.current_char == '"':
                    self.send_token(("ops", '"'))
                    self.get_next_char()
                    # self.parse_string()                 # parse a string
                else:
                    print("Line:ERROR: Could not identify on line: " + str(
                        self.line) + " near char: '" + self.current_char + "'")
                    break

                    # TODO have all functions return to a state that has the next char

    def is_operation(self):
        item = self.current_char
        # If we see an op look to see if we see another. If we see another add the previous
        if self.current_char in self.accepted_ops:
            # found op
            if self.current_char is '+':
                self.get_next_char()
                self.send_token((self.has_token(item), item))
            elif self.current_char is '-':
                self.get_next_char()
                # if self.current_char is '-':
                #    item += self.current_char  # Seen -- make new token
                #    self.get_next_char()
                self.send_token((self.has_token(item), item))
            elif self.current_char in ('<', '>', '!'):
                self.get_next_char()
                if self.current_char == '=':
                    item += self.current_char
                    self.get_next_char()
                self.send_token((self.has_token(item), item))
            elif self.current_char in ':':
                self.get_next_char()
                if self.current_char is '=':
                    item += self.current_char
                    self.send_token((self.has_token(item), item))
                    self.get_next_char()
                else:
                    print("Lexer Error [Line: " + str(
                        self.line) + '] the "' + self.current_char + '" symbol not recognized after colon [:]')
            elif self.current_char in '=':
                self.send_token((self.has_token(item), item))
                self.get_next_char()
            else:
                if self.current_char in ('*', '/', '(', ')', '%', '^'):
                    self.get_next_char()
                    self.send_token((self.has_token(item), item))
                else:
                    print("Lexer Error: [Line: " + str(self.line) + "] could not intemperate: " +
                          self.current_char)
                    return False
            return True
        else:
            return False

    # Function Description:
    # General function to do something with the tokens once we have classified them.
    def send_token(self, token):
        self.add_token(token)
        print(token)

    def add_token(self, token):
        self.token_list.append(token)

    def print_tokens(self):
        for x in self.token_list:
            print(x)

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
                # TODO if part of the token is in the token list what do we do??
                self.get_next_char()
        token_value = word
        token_type = self.has_token(token_value)
        if token_type == -1:
            token_type = "ID"
        self.send_token((token_type, token_value))

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
        if self.is_digit(self.current_char):
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
                        self.send_token(('float', float(word)))
                        return
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
                                self.send_token(("float", float(word)))
                                return
                            except ValueError:
                                print("Fatal parse error: [row: " + str(self.line) + "] when parsing char '" +
                                      str(self.current_char) + "' for: \n\t\t" + str(word))
                        except ValueError:
                            self.send_token(("int", word))
                            self.send_token(("ID", "e"))
                            self.send_token((self.has_token("+"), "+"))
                            return
                    elif self.current_char is '-':
                        self.get_next_char()
                        exp = self.is_int()
                        try:
                            self.get_next_char()
                            exp = int(exp)
                            word += 'e-'
                            word += str(exp)
                            try:
                                self.send_token(("float", float(word)))
                                return
                            except ValueError:
                                print("Fatal parse error: [row: " +
                                      str(self.line) + "] when parsing char '" +
                                      str(self.current_char) + "' for: \n\t\t" + str(word))
                        except ValueError:
                            self.send_token(("int", word))
                            self.send_token(("ID", "e"))
                            self.send_token((self.has_token("-"), "-"))
                    else:
                        exp = self.is_int()
                        try:
                            exp = int(exp)
                            word += str(exp)
                            self.send_token(("float", float(word)))
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
            self.send_token(("float", float(word)))
            try:
                return float(word)
            except ValueError:
                print("Lexer Error (line: " + str(self.line) +
                      "): could not determine numerical data of: " + str(word))
        else:
            try:
                self.send_token(("int", int(word)))
                return int(word)
            except ValueError:
                print("Lexer Error (line: " + str(self.line) +
                      "): could not determine numerical data of: " + str(word))

    # Function Description:
    # checks to see if the current data in peek is a digit or '.'
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
    # checks to see if the current data in peek is a letter
    # return true if it is
    def is_letter(self, others=[]):
        letters = list(string.ascii_letters)
        for x in others:
            if x not in letters:
                letters.append(x)
        if self.current_char in letters:
            return True
        return False
