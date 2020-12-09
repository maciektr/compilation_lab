from dataclasses import dataclass
from typing import List as ListType


def flatten(values):
    def __flatten(values):
        return [item for sublist in [
            x for x in values if isinstance(x, list)
            ] for item in sublist]

    if not isinstance(values, list):
        return values

    if any(map(lambda x: isinstance(x, list), values)):
        values = [item for item in values if not isinstance(item, list)] \
        + list(reversed(__flatten(values)))

    return list(values)


def parse_list_values(values):
    if isinstance(values, Value):
        values = values.values

    if isinstance(values, list):
        values = list(map(lambda x: x.values if isinstance(x, Value) else x, values))

    return flatten(values)


# too-few-public-methods
# pylint: disable=R0903

class Node:
    @property
    def name(self):
        return self.__class__.__name__

    @property
    def children(self):
        return list(vars(self).values())


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
    value_start: Node
    value_end: Node

class Value(Node):
    def __init__(self, values):
        self.values = parse_list_values(values) if values else []

class List(Node):
    def __reduce(self):
        while isinstance(self.values, List) or isinstance(self.values, Value):
            self.values = self.values.values
        assert isinstance(self.values, list)
        self.values = list(map(lambda item: item.values if isinstance(item, Value) else item, self.values))

    def __init__(self, values):
        self.values = values if values else []
        self.__reduce()

    def __repr__(self):
        return f'<ast.List at {id(self)}: {self.values}>'

    def append(self, value):
        self.values.append(List(value))
        self.__reduce()


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
