import ast
from type_checker.symbol_table import Scope


class NodeVisitor(object):
    def __call__(self, node):
        method = f'visit_{node.name}'
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        Called if no explicit visitor function exists for a node.
        """
        if isinstance(node, list):
            for element in node:
                self(element)
            return

        for child in node.children:
            self(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.current_scope = Scope()
        self.loop_count = 0

    def visit_IntNum(self, node):
        return 'INT'

    def visit_RealNum(self, node):
        return 'REAL'

    def visit_String(self, node):
        return 'STRING'

    def visit_Variable(self, node):
        ntype = self.current_scope.get(node.str)
        if ntype == None:
            print(f'Variable not present in current scope')
            return 'ANY'
        return ntype

    def visit_ValueRange(self, node):
        if not self.visit(node.start) == self.visit(node.end) == 'INT':
            print(f"Range boundaries must be integers")
        return 'RANGE'

    def visit_While(self, node):
        self.loop_count += 1

        condt = self.visit(node.cond)
        if condt != 'BOOLEAN':
            print(f'Expected condition resolving to boolean value, got {condt}')

        self.push_scope()
        self.visit(node.instructions)
        self.pop_scope()

        self.loop_count -= 1
        return None

    def visit_If(self, node):
        condt = self.visit(node.condition)
        if condt != 'BOOLEAN':
            print(f'Expected condition resolving to boolean value, got {condt}')

        self.push_scope()
        self.visit(node.instructions)
        self.pop_scope()

        self.push_scope()
        self.visit(node.else_instruction)
        self.pop_scope()

        return None

    def visit_For(self, node):
        self.loop_count += 1
        ntype = self.visit(node.value_range)
        if ntype != 'RANGE':
            print(f'Expected range, got {ntype}')

        self.push_scope()
        self.current_scope.put(node.id, 'INT')

        self.visit(node.instructions)

        self.pop_scope()
        self.loop_count -= 1
        return None

    def visit_Variable(self, node):
        pass

    def visit_Logical(self, node):
        pass

    def visit_List(self, node):
        pass

    def visit_Value(self, node):
        pass

    def visit_Partition(self, node):
        pass

    def visit_Eye(self, node):
        pass

    def visit_Ones(self, node):
        pass

    def visit_Zeros(self, node):
        pass

    def visit_Transpose(self, node):
        pass

    def visit_BinaryOperation(self, node):
        pass

    def visit_Continue(self, node):
        pass

    def visit_Break(self, node):
        pass

    def visit_Return(self, node):
        pass

    def visit_Assign(self, node):
        pass

    def visit_Print(self, node):
        self.visit(node.value)
        return None
