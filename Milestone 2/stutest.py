__author__ = 'Drake'
import sys

from scanner import Tokenizer, Lexer


def main():
    tokenizer = Tokenizer()
    if len(sys.argv) != 1:
        print("Must pass file to be tokenized after script name")
    with open("test1", 'r') as f:
        lexer = Lexer(f, tokenizer)
        lexer.control()
    print(tokenizer.tokens)

if __name__ == '__main__':
    main()
