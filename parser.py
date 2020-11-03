from scanner_defs import tokens
from parser_defs import *
import ply.yacc as yacc

class Parser:
    def __init__(self, lexer):
        self.parser = yacc.yacc()
        self.lexer = lexer

    def parse(self, text):
        return self.parser.parse(text, lexer=self.lexer)
