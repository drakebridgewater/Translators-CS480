__author__ = 'Drake'

files = []
options = []

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
TYPE_BOOL = 'bool'
TYPE_INT = 'int'
TYPE_REAL = 'float'
TYPE_STRING = 'string'
TYPE_ID = 'ID'


class Token:
    type = ''
    value = ''
    line = ''