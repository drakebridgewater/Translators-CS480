__author__ = 'Drake'

files = []
global OPTIONS
globals()["OPTIONS"] = ['lexer', 'print', 'postorder', 'tree', 'debug', 'parse']

global DEBUG
globals()["DEBUG"] = 0

if not 'current_token_index' in globals():
    current_token_index = 0

OPER_EQ = '='
OPER_ASSIGN = ':='
OPER_ADD = '+'
OPER_SUB = '-'
OPER_DIV = '/'
OPER_MULT = '*'
OPER_LT = '<'
OPER_GT = '>'
OPER_LE = '<='
OPER_GE = '>='
OPER_NE = '!='
OPER_NOT = '!'
OPER_MOD = '%'
OPER_EXP = '^'
SEMI = ';'
L_PAREN = '('
R_PAREN = ')'
OPER_AND = 'and'
OPER_OR = 'or'
OPER_NOT = 'not'
OPER_SIN = 'sin'
OPER_TAN = 'tan'
OPER_COS = 'cos'
KEYWORD_STDOUT = 'stdout'
KEYWORD_LET = 'let'
KEYWORD_IF = 'if'
KEYWORD_WHILE = 'while'
KEYWORD_TRUE = "true"
KEYWORD_FALSE = "false"
KEYWORD = 'keywords'
TYPE_BOOL = 'bool'
TYPE_INT = 'int'
TYPE_REAL = 'real'
TYPE_STRING = 'string'
TYPE_ID = 'ID'


def print_error(msg, line='NA', error_type='general'):
    print(error_type.upper() + " ERROR: [line: " + str(line) + "] " + msg)


def print_title(msg):
    print("-" * 40 + "\n" + msg.upper() + "\n" + "-" * 40)


def print_token(token, indent=0):
    print("\t" * indent + "[line: " + str(token.line) +
          ",\t ID: " + token.type +
          ",\t Value: " + str(token.value) +
          # ",\t Siblings: " + str(token.siblings) +
          "]")


def print_log(msg):
    if 'lexer' in globals()['OPTIONS']:
        print(msg)


class Token:
    type = ''
    value = ''
    line = ''
    siblings = -1