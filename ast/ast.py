from dataclasses import dataclass
from typing import List as ListType


class Node(object):
    @property
    def name(self):
        return self.__class__.__name__

class Instructions(Node):
    def __init__(self, instructions):
        self.instructions = instructions

@dataclass
class InstructionBlock(Node):
    instructions: ListType

@dataclass
class ValueRange(Node):
    start: Node
    end: Node

@dataclass
class If(Node):
    condition: Node
    instructions: InstructionBlock
    else_instruction: Node

@dataclass
class Else(Node):
    instructions: InstructionBlock

@dataclass
class For(Node):
    iterator: Node
    value_range: ValueRange
    instructions: InstructionBlock

@dataclass
class While(Node):
    condition: Node
    instructions: InstructionBlock

@dataclass
class Print(Node):
    value: Node

@dataclass
class Assign(Node):
    left: Node
    right: Node
    operator: str = '='

@dataclass
class Return(Node):
    value: Node

class Break(Node):
    pass

class Continue(Node):
    pass

@dataclass
class BinaryOperation(Node):
    left: Node
    right: Node
    operator: str

@dataclass
class IntNum(Node):
    value: int

@dataclass
class RealNum(Node):
    value: float

@dataclass
class String(Node):
    value: str

@dataclass
class Transpose(Node):
    target: Node

@dataclass
class Zeros(Node):
    value: IntNum

@dataclass
class Ones(Node):
    value: IntNum

@dataclass
class Eye(Node):
    value: IntNum

@dataclass
class Partition(Node):
    variable: Node
    value: Node

@dataclass
class Value(Node):
    values: ListType

class List(Node):
    def __init__(self, values):
        self.values = values if values else []

@dataclass
class Logical(Node):
    left: Node
    right: Node
    operator: str

@dataclass
class Variable(Node):
    name: str


class Error(Node):
    def __init__(self):
        pass
