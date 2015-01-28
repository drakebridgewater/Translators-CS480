__author__ = 'Drake'
import sys


def main():
    tokenizer = Tokenizer()
    if len(sys.argv) != 2:
        print("Must pass file to be tokenized after script name")
    with open(sys.argv[1], 'r') as f:
        lexer = Lexer(f, tokenizer)

if __name__ == '__main__':
    main()
