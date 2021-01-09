import sys

import ast
from type_checker.symbol_table import SymbolTable
from interpreter.memory import *
from interpreter.exceptions import  *
from interpreter.visit import *


sys.setrecursionlimit(10000)

class Interpreter:
    @on('node')
    def visit(self, node):
        pass

    @when(ast.BinaryOperation)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(ast.Assign)
    def visit(self, node):
        pass

    # simplistic while loop interpretation
    @when(ast.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r


