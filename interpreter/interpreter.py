import sys
import ast

import numpy as np

from interpreter.memory import MemoryStack
from interpreter.exceptions import BreakException, ContinueException, InterpreterException
from interpreter.visit import default, when, on
from interpreter.operators import Operators
from utils import stdout_print, GenericVisit

sys.setrecursionlimit(10000)

# function-redefined no-self-use
# pylint: disable=E0102 R0201


DEBUG = False
def debug_print(*args):
    if DEBUG:
        print(*args)

def out_print(*args):
    stdout_print(*args)


class Interpreter(GenericVisit):
    def __init__(self):
        self.memstack = MemoryStack()
        self.operators = Operators()

    def __call__(self, node):
        debug_print('call', node)
        return self.visit(node)

    @on('node')
    def visit(self, node):
        pass

    @default()
    def visit(self, node):
        self.generic_visit(node)

    @when(ast.Variable)
    def visit(self, node):
        return self.memstack[node.variable_name]

    @when(ast.BinaryOperation)
    def visit(self, node):
        left = self(node.left)
        right = self(node.right)
        return self.operators(node.operator)(left, right)

    @when(ast.Assign)
    def visit(self, node):
        right = self(node.right)
        if node.operator != '=':
            left = self(node.left)
            right = self.operators(node.operator)(left, right)

        if isinstance(node.left, ast.Variable):
            self.memstack[node.left.variable_name] = right
        elif isinstance(node.left, ast.Partition):
            bounds = self.__part_bounds(node.left)
            self.memstack[node.left.variable][bounds] = right

    @when(ast.InstructionBlock)
    def visit(self, node):
        self.memstack.push(node.name)
        try:
            self(node.instructions)
        except InterpreterException as error:
            self.memstack.pop()
            raise error
        self.memstack.pop()

    @when(ast.While)
    def visit(self, node):
        res = None
        while self(node.condition):
            try:
                res = self(node.instructions)
            except ContinueException:
                pass
            except BreakException:
                break
        return res

    @when(ast.If)
    def visit(self, node):
        res = None
        if self(node.condition):
            res = self(node.instructions)
        else:
            res = self(node.else_instruction)
        return res

    @when(ast.For)
    def visit(self, node):
        bound = node.value_range
        r_start = self(bound.start)
        r_end = self(bound.end)
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
        left = self(node.left)
        right = self(node.right)
        return self.operators(node.operator)(left, right)

    @when(ast.Eye)
    def visit(self, node):
        dim = self(node.value)
        if not dim and isinstance(node.value, int):
            dim = node.value
        return np.eye(dim)

    @when(ast.Ones)
    def visit(self, node):
        return np.ones(node.value.values)

    @when(ast.Zeros)
    def visit(self, node):
        return np.zeros(node.value.values)

    @staticmethod
    def __part_bounds(node):
        def parse_bound(bound):
            if isinstance(bound, int):
                return bound
            if isinstance(bound, ast.IntNum):
                return bound.value
            if isinstance(bound, ast.ValueRange):
                return slice(parse_bound(bound.start), parse_bound(bound.end))
            return None
        return tuple(map(parse_bound, node.bounds.values))

    @when(ast.Partition)
    def visit(self, node):
        bounds = self.__part_bounds(node)
        return self.memstack[node.variable][bounds]

    @when(ast.Dimension)
    def visit(self, node):
        res = node.values
        if len(res) == 1:
            res = res[0]
        return res

    @when(ast.List)
    def visit(self, node):
        res = []
        for val in node.values:
            res.append(self(val))
        return np.array(res)

    @when(ast.Transpose)
    def visit(self, node):
        val = self.memstack[node.target.variable_name]
        return np.transpose(val)

    @when(ast.Print)
    def visit(self, node):
        out_print(self(node.value))
