import sys

import ast
from type_checker.symbol_table import SymbolTable
from interpreter.memory import *
from interpreter.exceptions import  *
from interpreter.visit import *


sys.setrecursionlimit(10000)

def add_f(a, b):    return a + b
def sub_f(a, b):    return a - b
def mul_f(a, b):    return a * b
def div_f(a, b):    return a / b

def dotAdd_f(a, b): return 
def dotSub_f(a, b): return 
def dotMul_f(a,b):  return 
def dotDiv_f(a,b):  return 

FUNCTION_DICT = {
    "+" : add_f,
    "-" : sub_f,
    "*" : mul_f,
    "/" : div_f,
    ".+" : dotAdd_f,
    ".-" : dotSub_f,
    ".*" : dotMul_f,
    "./" : dotDiv_f,
}

def eq_f(a, b):    return a == b
def gr_f(a, b):    return a > b
def less_f(a, b):  return a < b
def greq_f(a, b):  return a >= b
def leeq_f(a, b):  return a <= b
def noteq_f(a, b): return a != b

LOGICAL_DICT = {
    "==" : eq_f,
    ">" : gr_f,
    "<" : less_f,
    ">=" : greq_f,
    "<=" : leeq_f,
    "!=" : noteq_f,
}


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
        oper = FUNCTION_DICT[node.operator]
        return oper(r1, r2)

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

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.IntNum)
    def visit(self, node):
        print("int " + node.value)
        return node.value 
    
    @when(AST.RealNum)
    def visit(self, node):
        print("real " + node.value)
        return node.value 
    
    @when(AST.String)
    def visit(self, node):
        print("string " + node.value)
        return node.value 
    
    @when(ast.Logical)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval
        oper = LOGICAL_DICT[node.operator]
        return oper(r1, r2)

