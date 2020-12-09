from type_checker.symbol_table import SymbolTable
import ast


class NodeVisitor:
    def __call__(self, node):
        visitor = self.generic_visit
        if hasattr(node, 'name'):
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

        if not node or not hasattr(node, 'children'):
            return

        for child in node.children:
            self(child)

# invalid-name no-self-use too-many-public-methods
# pylint: disable=C0103 R0201 R0904

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable('__type_checker__')
        self.loop_count = 0

    def visit_IntNum(self, node):
        return 'INT'

    def visit_RealNum(self, node):
        return 'REAL'

    def visit_String(self, node):
        return 'STRING'

    def visit_Variable(self, node):
        n_type = self.symbol_table[node.name]
        if not n_type:
            print('Variable not present in current scope')
            return 'ANY'

        return n_type

    def visit_ValueRange(self, node):
        if not self(node.start) == self(node.end) == 'INT':
            print("Range boundaries must be integers")
        return 'RANGE'

    def visit_While(self, node):
        self.loop_count += 1

        condition = self(node.condition)
        if condition != 'BOOLEAN':
            print(f'Expected condition resolving to boolean value, got {condition}')

        self.symbol_table.push_scope('WHILE')
        self(node.instructions)
        self.symbol_table.pop_scope()

        self.loop_count -= 1

    def visit_If(self, node):
        condition = self(node.condition)
        if condition != 'BOOLEAN':
            print(f'Expected condition resolving to boolean value, got {condition}')

        self.symbol_table.push_scope('IF')
        self(node.instructions)
        self.symbol_table.pop_scope()

        self.symbol_table.push_scope('IF')
        self(node.else_instruction)
        self.symbol_table.pop_scope()

    def visit_For(self, node):
        self.loop_count += 1
        n_type = self(node.value_range)
        if n_type != 'RANGE':
            print(f'Expected range, got {n_type}')

        self.symbol_table.push_scope('FOR')
        self.symbol_table[node.iterator] = 'INT'

        self(node.instructions)

        self.symbol_table.pop_scope()
        self.loop_count -= 1

    def visit_Logical(self, node):
        type1 = self(node.left)
        type2 = self(node.right)


    def visit_List(self, node):
        types = []
        for v in node.values:
            types.append(type(v))
        list_type = types[0]
        if any(list_type != item_type for item_type in types):
            print('Inconsistent types in a List')
        elif isinstance(node.values[0], ast.List):
            if any(len(node.values[0]) != len(item) for item in node.values):
                print('Inconsistent matrix vector lengths')
        else:
            print(types)

    def visit_Value(self, node):
        pass

    def visit_Partition(self, node):
        n_type = self.symbol_table[node.variable]
        if not n_type:
            print('Variable not present in current scope')

    def visit_Eye(self, node):
        type1 = self(node.value)
        if type1 != 'INT':
            print('Incorrect Eye size')

    def visit_Ones(self, node):
        type1 = self(node.value)
        if type1 != 'INT':
            print('Incorrect Ones size')

    def visit_Zeros(self, node):
        type1 = self(node.value)
        if type1 != 'INT':
            print('Incorrect Zeros size')

    def visit_Transpose(self, node):
        pass

    def visit_BinaryOperation(self, node):
        type1 = self(node.left)
        type2 = self(node.right)

    def visit_Continue(self, node):
        if self.loop_count == 0:
            print(f"Continue outside of loop")
        return None

    def visit_Break(self, node):
        if self.loop_count == 0:
            print(f"Break outside of loop")
        return None

    def visit_Return(self, node):
        type1 = self(node.value)

    def visit_Assign(self, node):
        type1 = self(node.left)
        type2 = self(node.right)
        n_type = self.symbol_table[node.left]
        if not n_type:
            self.symbol_table[node.left] = 'INT'
            

    def visit_Print(self, node):
        self(node.value)
