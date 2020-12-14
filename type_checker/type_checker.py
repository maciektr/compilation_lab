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
        n_type = self.symbol_table[node.variable_name]
        if not n_type:
            print(f'Line {node.line_number}: Variable {node.variable_name} not present in current scope')
            return 'ANY'

        return n_type

    def visit_ValueRange(self, node):
        if not self(node.start) == self(node.end) == 'INT':
            print(f"Line {node.line_number}: Range boundaries must be integers")
        return 'RANGE'

    def visit_While(self, node):
        self.loop_count += 1

        condition = self(node.condition)
        if condition != 'BOOLEAN':
            print(f'Line {node.line_number}: Expected condition resolving to boolean value, got {condition}')

        self.symbol_table.push_scope('WHILE')
        self(node.instructions)
        self.symbol_table.pop_scope()

        self.loop_count -= 1

    def visit_If(self, node):
        condition = self(node.condition)
        if condition != 'BOOLEAN':
            print(f'Line {node.line_number}: Expected condition resolving to boolean value, got {condition}')

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
            print(f'Line {node.line_number}: Expected range, got {n_type}')

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
            print(f'Line {node.line_number}: Inconsistent types in a List')
        elif isinstance(node.values[0], ast.List):
            if any(len(node.values[0]) != len(item) for item in node.values):
                print(f'Line {node.line_number}: Inconsistent matrix vector lengths')
        return 'LIST'

    def visit_Value(self, node):
        pass

    def visit_Partition(self, node):
        n_type = self.symbol_table[node.variable]
        if not n_type:
            print(f'Line {node.line_number}: Variable {node.variable} not present in current scope')
        if n_type != 'LIST':
            print(f'Line {node.line_number}: Attempt to partition an object, which is not List')
        if n_type == 'LIST':
            list_node = self.symbol_table[node.variable + '_node']
            if len(list_node) < node.value_end or len(list_node) < node.value_start:
                print(f'Line {node.line_number}: Partition range out of bounds')

    def visit_Eye(self, node):
        type1 = self(node.value)
        if type1 != 'INT':
            print(f'Line {node.line_number}: Incorrect Eye size')

    def visit_Ones(self, node):
        type1 = self(node.value)
        if type1 != 'INT':
            print(f'Line {node.line_number}: Incorrect Ones size')

    def visit_Zeros(self, node):
        type1 = self(node.value)
        if type1 != 'INT':
            print(f'Line {node.line_number}: Incorrect Zeros size')

    def visit_Transpose(self, node):
        pass

    def visit_BinaryOperation(self, node):
        type1 = self(node.left)
        type2 = self(node.right)
        if type1 != type2:
            print(f'Line {node.line_number}: Type mismatch in {node.operator} operation')
        else:
            if node.operator in ['.+', './', '.*', '.-'] and type1 != ast.List:
                print(f'Line {node.line_number}: Operation {node.operator} allowed only for matrices')
            if isinstance(node.left, ast.List) and len(node.left.values) != len(node.right.values):
                print(f'Line {node.line_number}: Operation {node.operator} on lists with diferent sizes!')
            


    def visit_Continue(self, node):
        if self.loop_count == 0:
            print(f"Line {node.line_number}: Continue outside of loop")
        return None

    def visit_Break(self, node):
        if self.loop_count == 0:
            print(f"Line {node.line_number}: Break outside of loop")
        return None

    def visit_Return(self, node):
        type1 = self(node.value)

    def visit_Assign(self, node):
        type2 = self(node.right)
        n_type = self.symbol_table[node.left.variable_name]
        if not n_type:
            if type2 is None:
                self.symbol_table[node.left.variable_name] = 'ANY'
            elif type2 is 'LIST':
                self.symbol_table[node.left.variable_name] = type2
                self.symbol_table[node.left.variable_name + '_node'] = node.right
            else:
                self.symbol_table[node.left.variable_name] = type2
            #print(type2)
        type1 = self(node.left)
        

    def visit_Print(self, node):
        self(node.value)
