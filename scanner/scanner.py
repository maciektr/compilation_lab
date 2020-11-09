import ply.lex as lex

# wildcard-import unused-wildcard-import
from scanner.scanner_defs import * # pylint: disable=W0401 W0614


class Scanner:
    def __init__(self):
        self.lexer = lex.lex()
        self.last_text = None

    def __call__(self, text: str):
        self.last_text = text
        self.lexer.input(text)

    def get_lexer(self):
        return self.lexer

    def find_column(self, token):
        text = self.last_text
        line_start = text.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def token(self):
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            yield (tok.lineno, self.find_column(tok), tok.type, tok.value)
            # yield tok
