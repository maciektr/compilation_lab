import os
import sys
import getopt

from parser.parser import Parser
from scanner.scanner import Scanner

OPTIONS = ['path=', 'lexer', 'clear']


def exit_fail(message: str=None):
    if message:
        print(message)
    sys.exit(1)


def exit_ok(message: str=None):
    if message:
        print(message)
    sys.exit(0)


def run_lexer(scanner: Scanner, text: str):
    scanner(text)
    for tok in scanner.token():
        print("(%d, %d): %s(%s)" % tok)
        print(tok)


def run_parser(parser: Parser, text: str):
    parser.parse(text)


def clear():
    def rm(path):
        try:
            os.remove(path)
        except OSError:
            pass
    rm('parser/parser.out')
    rm('parser/parsetab.py')


def main():
    try:
        opts, _args = getopt.getopt(sys.argv[1:], '', OPTIONS)
        options = {k : v for k,v in opts}
    except getopt.GetoptError as err:
        exit_fail(err)

    try:
        filename = 'examples/example1.m'
        if '--path' in options:
            filename = options['--path']

        with open(filename, "r") as file:
            text = file.read()
    except IOError:
        exit_ok(f"Cannot open {filename} file")

    if '--clear' in options:
        clear()
        exit_ok()

    lexer = Scanner()

    if '--lexer' in options:
        run_lexer(lexer, text)
        exit_ok()

    clear()
    parser = Parser(lexer)
    run_parser(parser, text)


if __name__ == '__main__':
    main()
