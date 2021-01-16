import os
import sys
import getopt

from parser import Parser
from scanner import Scanner
from type_checker import TypeChecker
from interpreter import Interpreter
from utils import exit_fail, exit_ok, stderr_print

OPTIONS = ['path=', 'lexer', 'clear', 'zip', 'use_cache', 'print_ast']
PARSER_AUTO_FILES = ['parser/parser.out', 'parser/parsetab.py']
OUT_FOLDER = 'out'


def print_main(*args):
    stderr_print(*args)

def run_lexer(scanner: Scanner, text: str):
    scanner(text)
    for tok in scanner.token():
        print_main("(%d, %d): %s(%s)" % tok)
        print_main(tok)


def rm_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


def zip_files(out):
    file_name = f'{OUT_FOLDER}/{out}.zip'
    rm_file(file_name)
    os.system(f"zip -r {file_name} ./ -x '*venv*' '*.git*' '*__pycache__*' '{OUT_FOLDER}/*'")
    exit_ok()


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
        filename = 'examples/init.m'
        if '--path' in options:
            filename = options['--path']

        print_main(f'Opening file: {filename}')
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

    if not ast:
        exit_fail('Cannot run your program: returning.')

    if '--print_ast' in options:
        ast.print_tree()

    type_checker = TypeChecker()
    type_checker(ast)
    if not type_checker.accepted:
        exit_fail('Cannot run your program: returning.')

    interpreter = Interpreter()
    interpreter(ast)


if __name__ == '__main__':
    main()
