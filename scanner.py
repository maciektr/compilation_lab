import ply
import ply.lex as lex;
from typing import Callable

from definitions import *

class Scanner:
    def __init__(self):
        self.lexer = lex.lex()

    def __call__(self, text: str):
        self.lexer.input(text)

    def token(self):
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            yield (tok.lineno, tok.type, tok.value)
            # yield tok
