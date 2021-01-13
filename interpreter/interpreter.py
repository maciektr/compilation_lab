import sys

import ast
from type_checker.symbol_table import SymbolTable
from interpreter.memory import MemoryStack
from interpreter.exceptions import  *
from interpreter.visit import *
from interpreter.operators import Operators

sys.setrecursionlimit(10000)

class Interpreter:
    def __init__(self):
        self.memstack = MemoryStack()
        self.operators = Operators()

    def __call__(self, node):
        return self.visit(node)

    @on('node')
    def visit(self, node):
        pass

    @when(ast.BinaryOperation)
    def visit(self, node):
        r1 = self(node.left)
        r2 = self(node.right)
        return self.operators(node.operator)(r1, r2)

    @when(ast.Assign)
    def visit(self, node):
        right = self(node.right)
        if node.oper != '=':
            left = self(left)
            right = self.operators(node.oper)(left, right)

        if isinstance(node.left, ast.Variable):
            self.memstack[node.left.variable_name] = node.right

    @when(ast.While)
    def visit(self, node):
        r = None
        while self(node.cond):
            r = self(node.body)
        return r

    @when(ast.Break)
    def visit(self, node):
        raise BreakException()

    @when(ast.IntNum)
    def visit(self, node):
        print("int " + node.value)
        return int(node.value)

    @when(ast.RealNum)
    def visit(self, node):
        print("real " + node.value)
        return float(node.value)

    @when(ast.String)
    def visit(self, node):
        print("string " + node.value)
        return str(node.value)

    @when(ast.Logical)
    def visit(self, node):
        r1 = self(node.left)
        r2 = self(node.right)
        return self.operators(node.operator)(r1, r2)

