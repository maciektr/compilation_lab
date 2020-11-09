# wildcard-import unused-wildcard-import
from parser.parser_defs import * # pylint: disable=W0401 W0614

import ply.yacc as yacc

from scanner.scanner import Scanner
# unused-import
from scanner.scanner_defs import tokens # pylint: disable=W0611


class Parser:
    def __init__(self, scanner: Scanner):
        self.parser = yacc.yacc()
        self.lexer = scanner.get_lexer()

    def get_parser(self):
        return self.parser

    def parse(self, text):
        return self.parser.parse(text, lexer=self.lexer)
