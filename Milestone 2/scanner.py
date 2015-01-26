__author__ = 'Drake'
import string
from collections import defaultdict

def main():
    tokens =
    with open(filename, 'r') as f:
        lexer = Lexer(f)

class Tokenizer():
    def __init__(self):
        self.tokens = \
            {"keywords":     ("if", "then", "while", "for",
                              "true", "false"),
             "ops":          ("and", "or", "not", '=', '+', '-', '/', '*',
                              '<', '<=', '>', '>=', '!='),
             'type':         ('bool', 'int', 'real', 'string'),
             'mainScope':    ()}
    def add_token(self, entire_path=()):
        # TODO create a method for adding to the token dictionary
        for x in entire_path:
            if x in self.tokens:
                continue
            else:
                self.tokens[x]

class Lexer():
    def __init__(self, file):
        self.line = 1
        self.input = file
        self.peek = ' '

    def control(self):
        while

    def identify_string(self, word):
        # TODO identify if the string is in the tokenizer
        word = self.parse_string(list(string.ascii_letters) +
                                 list(string.digits) + list('_'),
                                 list(string.ascii_letters))
    def scan(self):
        self.skip_white_space()

    def get_next_char(self):
        # self.peek = self.input.read(1)
        self.skip_white_space()

    def skip_white_space(self):
        while 1:
            self.peek = self.input.read(1)
            if self.peek == ' ' or self.peek == '\t':
                continue
            elif self.peek == '\n':
                self.line += 1
            else:
                break

    def number(self):
        # TODO: add support for values like 2.3e2
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
            # append the digit to the value
            value += self.peek
            # move to the next char
            self.get_next_char()
        if '.' in value:
            return float(value)
        else:
            return int(value)

    # Function Description:
    # checks to see if the current value in peek is a digit or '.'
    # return true if it is
    def is_digit(self, others=[]):
        digits = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '9']
        for x in others:
            if x not in digits:
                digits.append(x)
        if self.peek in digits:
            return True
        return False

    def is_letter(self, others=[]):
        letters = list(string.ascii_letters)
        for x in others:
            if x not in letters:
                letters.append(x)

    def parse_string(self, accepted_chars, acceptable_first_chars=[]):
        if self.peek not in acceptable_first_chars:
            return -1
        else:
            word = ''
            while self.peek in accepted_chars:
                word += self.peek
                self.get_next_char()
            return word