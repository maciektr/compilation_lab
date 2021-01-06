import ast
from type_checker.symbol_table import SymbolTable


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

# invalid-name no-self-use too-many-public-methods unused-argument
# pylint: disable=C0103 R0201 R0904 W0613

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable('__type_checker__')
        self.loop_count = 0

    def visit_Dimension(self, node):
        return 'DIMENSION'

    def visit_IntNum(self, node):
        return 'INT'

    def visit_RealNum(self, node):
        return 'REAL'

    def visit_String(self, node):
        return 'STRING'

    def visit_Variable(self, node):
        n_type = self.symbol_table[node.variable_name]
        if not n_type:
            print(f'Line {node.line_number}: Variable {node.variable_name} not present in '
                'current scope')
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
            print(f'Line {node.line_number}: Expected condition resolving to boolean value,'
                ' got {condition}')

        self.symbol_table.push_scope('WHILE')
        self(node.instructions)
        self.symbol_table.pop_scope()

        self.loop_count -= 1

    def visit_If(self, node):
        condition = self(node.condition)
        if condition != 'BOOLEAN':
            print(f'Line {node.line_number}: Expected condition resolving to boolean value,'
                ' got {condition}')

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
        # type1 = self(node.left)
        # type2 = self(node.right)
        return 'BOOLEAN'

    def visit_List(self, node):
        list_type = type(node.values[0])
        if any(list_type != type(item) for item in node.values):
            print(f'Line {node.line_number}: Inconsistent types in a List')

        if isinstance(node.values[0], ast.List):
            if any(len(node.values[0]) != len(item) for item in node.values):
                print(f'Line {node.line_number}: Inconsistent matrix vector lengths')

        return 'LIST'

    def visit_Value(self, node):
        pass

    @staticmethod
    def valid_list_bounds(array, bounds):
        def between(value, end, start=0):
            return  start <= value < end

        def __do_check(to_validate, bounds):
            if len(to_validate) != len(bounds):
                return False
            i = 0
            for bound in bounds:
                if isinstance(bound, ast.ValueRange):
                    if not between(bound.start, to_validate[i]):
                        return False
                    if not between(bound.end, to_validate[i] + 1):
                        # (+1) since ValueRange.end points to first not taken element
                        return False
                elif isinstance(bound, ast.IntNum):
                    if not between(bound.value, to_validate[i]):
                        return False
                i += 1
            return True

        if  isinstance(array, (ast.Eye, ast.Ones, ast.Zeros)):
            return __do_check(array.value.values, bounds)

        to_validate = [array[0]]
        while isinstance(array[0], list):
            array = array[0]
            to_validate.append(array[0])

        return __do_check(to_validate, bounds)

    def visit_Partition(self, node):
        n_type = self.symbol_table[node.variable]
        if not n_type:
            print(f'Line {node.line_number}: Variable {node.variable} not present in current scope')
        if n_type != 'LIST':
            print(f'Line {node.line_number}: Attempt to partition an object, which is not List')
        if n_type == 'LIST':
            list_node = self.symbol_table[node.variable + '_node']
            if not self.valid_list_bounds(list_node, node.bounds):
                print(f'Line {node.line_number}: Partition range out of bounds')

    def visit_Eye(self, node):
        type1 = self(node.value)
        if type1 != 'DIMENSION':
            print(f'Line {node.line_number}: Incorrect Eye size')
        return 'LIST'

    def visit_Ones(self, node):
        type1 = self(node.value)
        if type1 != 'DIMENSION':
            print(f'Line {node.line_number}: Incorrect Ones size')
        return 'LIST'

    def visit_Zeros(self, node):
        type1 = self(node.value)
        if type1 != 'DIMENSION':
            print(f'Line {node.line_number}: Incorrect Zeros size')
        return 'LIST'

    def visit_Transpose(self, node):
        target_type = self(node.target)
        if target_type != 'LIST':
            print(f'Line {node.line_number}: Transpose can be run only on a matrix')

    def visit_BinaryOperation(self, node):
        type1 = self(node.left)
        type2 = self(node.right)
        if type1 != type2:
            print(f'Line {node.line_number}: Type mismatch in {node.operator} operation')
        else:
            if node.operator in ['.+', './', '.*', '.-'] and type1 != 'LIST':
                print(f'Line {node.line_number}: Operation {node.operator} allowed'
                    ' only for matrices')
            if isinstance(node.left, ast.List) and len(node.left.values) != len(node.right.values):
                print(f'Line {node.line_number}: Operation {node.operator} on lists with'
                    ' diferent sizes!')

    def visit_Continue(self, node):
        if self.loop_count == 0:
            print(f"Line {node.line_number}: Continue outside of loop")

    def visit_Break(self, node):
        if self.loop_count == 0:
            print(f"Line {node.line_number}: Break outside of loop")

    def visit_Return(self, node):
        # type1 = self(node.value)
        pass

    def visit_Assign(self, node):
        def get_variable_name(variable):
            if isinstance(variable, ast.Variable):
                return variable.variable_name
            if isinstance(variable, ast.Partition):
                return variable.variable
            return None

        right_type = self(node.right)
        left_name = get_variable_name(node.left)
        if right_type is None:
            self.symbol_table[left_name] = 'ANY'
        elif right_type == 'LIST':
            self.symbol_table[left_name] = right_type
            self.symbol_table[left_name + '_node'] = node.right
        else:
            self.symbol_table[left_name] = right_type

    def visit_Print(self, node):
        self(node.value)
