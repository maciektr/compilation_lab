import sys
import numpy as np

import ast
from type_checker.symbol_table import SymbolTable
from interpreter.memory import MemoryStack
from interpreter.exceptions import  *
from interpreter.visit import *
from interpreter.visit import default
from interpreter.operators import Operators
from utils import stdout_print

sys.setrecursionlimit(10000)

DEBUG = False
def debug_print(*args):
    if DEBUG:
        print(*args)

def out_print(*args):
    stdout_print(*args)


class Interpreter:
    def __init__(self):
        self.memstack = MemoryStack()
        self.operators = Operators()

    def __call__(self, node):
        debug_print('call', node)
        return self.visit(node)

    @on('node')
    def visit(self, node):
        pass

    @default('node')
    def visit(self, node):
        if isinstance(node, list):
            for element in node:
                self(element)
            return

        if not node or not hasattr(node, 'children'):
            return

        for child in node.children:
            self(child)

    @when(ast.Variable)
    def visit(self, node):
        return self.memstack[node.variable_name]

    @when(ast.BinaryOperation)
    def visit(self, node):
        r1 = self(node.left)
        r2 = self(node.right)
        return self.operators(node.operator)(r1, r2)

    @when(ast.Assign)
    def visit(self, node):
        right = self(node.right)
        if node.operator != '=':
            left = self(node.left)
            right = self.operators(node.operator)(left, right)

        if isinstance(node.left, ast.Variable):
            self.memstack[node.left.variable_name] = right

    @when(ast.InstructionBlock)
    def visit(self, node):
        self.memstack.push(node.name)
        try:
            self(node.instructions)
        except InterpreterException as e:
            self.memstack.pop()
            raise e
        self.memstack.pop()

    @when(ast.While)
    def visit(self, node):
        r = None
        while self(node.condition):
            try:
                r = self(node.instructions)
            except ContinueException:
                pass
            except BreakException:
                break
        return r
    
    @when(ast.If)
    def visit(self, node):
        r = None
        if self(node.condition):
            r = self(node.instructions)
        else: r = self(node.else_instruction)
        return r

    @when(ast.For)
    def visit(self, node):
        range = node.value_range
        r_start = self(range.start)
        r_end = self(range.end)
        self.memstack[node.iterator] = r_start
        while self.memstack[node.iterator] <= r_end:
            try:
                self(node.instructions)
            except ContinueException:
                pass
            except BreakException:
                break
            self.memstack[node.iterator] += 1


    @when(ast.Break)
    def visit(self, node):
        raise BreakException()

    @when(ast.IntNum)
    def visit(self, node):
        debug_print("int ",  node.value)
        return int(node.value)

    @when(ast.RealNum)
    def visit(self, node):
        debug_print("real ", node.value)
        return float(node.value)

    @when(ast.String)
    def visit(self, node):
        debug_print("string ", node.value)
        return str(node.value)

    @when(ast.Logical)
    def visit(self, node):
        r1 = self(node.left)
        r2 = self(node.right)
        return self.operators(node.operator)(r1, r2)

    @when(ast.Eye)
    def visit(self, node):
        dim = self(node.value)
        return np.eye(dim)

    @when(ast.Dimension)
    def visit(self, node):
        res = node.values
        if len(res) == 1:
            res = res[0]
        return res

    @when(ast.List)
    def visit(self, node):
        res = np.array()
        for v in node.values:
            np.append(res, self(v))
        return res

    @when(ast.Print)
    def visit(self, node):
        out_print(self(node.value))
