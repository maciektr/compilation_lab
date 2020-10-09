import sys
import ply.lex as lex
from scanner import Scanner


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        with open(filename, "r") as file:
            text = file.read()
    except IOError:
        print(f"Cannot open {filename} file")
        sys.exit(0)

    lexer = Scanner()
    lexer(text)

    for tok in lexer.token():
        print("(%d, %d): %s(%s)" % tok)
        # print(tok)
