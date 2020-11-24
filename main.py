import os
import sys
import getopt

from parser import Parser
from scanner import Scanner

OPTIONS = ['path=', 'lexer', 'clear', 'zip', 'use_cache']
PARSER_AUTO_FILES = ['parser/parser.out', 'parser/parsetab.py']
OUT_FOLDER = 'out'


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


def rm_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


def zip_files(out):
    file_name = f'{OUT_FOLDER}/{out}.zip'
    rm_file(file_name)
    os.system(f"zip -r {file_name} ./ -x '*venv*' '*.git*' '*__pycache__*' '{OUT_FOLDER}/*'")


def clear():
    for file in PARSER_AUTO_FILES:
        rm_file(file)
    rm_file(f'{OUT_FOLDER}/parser.out')
    rm_file(f'{OUT_FOLDER}/parsetab.py')


def mv_file(source, destination):
    try:
        os.rename(source, destination)
    except OSError:
        pass


def move_auto_files(mv_reversed=False):
    for file in PARSER_AUTO_FILES:
        _, name = file.split('/', 1)
        if mv_reversed:
            mv_file(f'{OUT_FOLDER}/{name}', file)
        else:
            mv_file(file, f'{OUT_FOLDER}/{name}')


def main():
    try:
        opts, _args = getopt.getopt(sys.argv[1:], '', OPTIONS)
        options = {k : v for k,v in opts} # pylint: disable=R1721
    except getopt.GetoptError as err:
        exit_fail(err)

    try:
        filename = 'examples/example1.m'
        if '--path' in options:
            filename = options['--path']

        print(f'Opening file: {filename}')
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

    if '--use_cache' not in options:
        clear()

    if '--zip' in options:
        out = options['--zip'] if options['--zip'] else 'slawecki_tratnowiecki'
        zip_files(out)

    if '--use_cache' in options:
        move_auto_files(mv_reversed=True)
    parser = Parser(lexer)
    ast = parser.parse(text)
    move_auto_files()
    ast.print_tree()


if __name__ == '__main__':
    main()
