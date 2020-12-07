import ast.ast as ast


def add_to_class(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


def print_ind(value, indent=0):
    if isinstance(value, ast.Node):
        value.print_tree(indent)
        return

    if isinstance(value, list):
        for item in value:
            print_ind(item, indent)
        return

    print('|  ' * indent, value, sep='')


# no-member function-redefined
# pylint: disable=E1101 E0102
# too-few-public-methods no-self-use
# pylint: disable=R0903 R0201


class TreePrinter:
    @add_to_class(ast.Node)
    def print_tree(self, indent=0):
        raise Exception("print_tree not defined in class " + self.name)

    @add_to_class(ast.Instructions)
    def print_tree(self, indent=0):
        for instruction in self.instructions:
            instruction.print_tree(indent)

    @add_to_class(ast.Error)
    def print_tree(self, indent=0):
        pass

    @add_to_class(ast.InstructionBlock)
    def print_tree(self, indent=0):
        self.instructions.print_tree(indent)

    @add_to_class(ast.ValueRange)
    def print_tree(self, indent=0):
        print_ind('RANGE', indent)
        print_ind(self.start, indent + 1)
        print_ind(self.end, indent + 1)

    @add_to_class(ast.If)
    def print_tree(self, indent=0):
        print_ind('IF', indent)
        print_ind(self.condition, indent + 1)
        print_ind(self.instructions, indent + 1)
        print_ind(self.else_instruction, indent + 1)

    @add_to_class(ast.Else)
    def print_tree(self, indent=0):
        print_ind('ELSE', indent)
        print_ind(self.instructions, indent + 1)

    @add_to_class(ast.For)
    def print_tree(self, indent=0):
        print_ind('FOR', indent)
        print_ind(self.iterator, indent + 1)
        print_ind(self.value_range, indent + 1)
        print_ind(self.instructions, indent + 1)


    @add_to_class(ast.While)
    def print_tree(self, indent=0):
        print_ind('WHILE', indent)
        print_ind(self.condition, indent + 1)
        print_ind(self.instructions, indent + 1)

    @add_to_class(ast.Print)
    def print_tree(self, indent=0):
        print_ind('PRINT', indent)
        print_ind(self.value, indent + 1)

    @add_to_class(ast.Assign)
    def print_tree(self, indent=0):
        print_ind(self.operator, indent)
        print_ind(self.left, indent + 1)
        print_ind(self.right, indent + 1)

    @add_to_class(ast.Return)
    def print_tree(self, indent=0):
        print_ind('RETURN', indent)
        print_ind(self.value, indent + 1)

    @add_to_class(ast.Break)
    def print_tree(self, indent=0):
        print_ind('BREAK', indent)

    @add_to_class(ast.Continue)
    def print_tree(self, indent=0):
        print_ind('CONTINUE', indent)

    @add_to_class(ast.BinaryOperation)
    def print_tree(self, indent=0):
        print_ind(self.operator, indent)
        print_ind(self.left, indent + 1)
        print_ind(self.right, indent + 1)

    @add_to_class(ast.IntNum)
    def print_tree(self, indent=0):
        print_ind(self.value, indent)

    @add_to_class(ast.RealNum)
    def print_tree(self, indent=0):
        print_ind(self.value, indent)

    @add_to_class(ast.String)
    def print_tree(self, indent=0):
        print_ind(self.value, indent)

    @add_to_class(ast.Transpose)
    def print_tree(self, indent=0):
        print_ind('TRANSPOSE', indent)
        print_ind(self.target, indent + 1)

    @add_to_class(ast.Zeros)
    def print_tree(self, indent=0):
        print_ind('ZEROS', indent)
        print_ind(self.value, indent + 1)

    @add_to_class(ast.Ones)
    def print_tree(self, indent=0):
        print_ind('ONES', indent)
        print_ind(self.value, indent + 1)

    @add_to_class(ast.Eye)
    def print_tree(self, indent=0):
        print_ind('EYES', indent)
        print_ind(self.value, indent + 1)

    @add_to_class(ast.Partition)
    def print_tree(self, indent=0):
        print_ind('PARTITION', indent)
        print_ind(self.variable, indent + 1)
        print_ind(self.value_start, indent + 1)
        print_ind(self.value_end, indent + 1)

    @add_to_class(ast.Value)
    def print_tree(self, indent=0):
        print_ind(self.values, indent)

    @add_to_class(ast.List)
    def print_tree(self, indent=0):
        print_ind('LIST', indent)
        print_ind(self.values, indent+1)

    @add_to_class(ast.Logical)
    def print_tree(self, indent=0):
        print_ind(self.operator, indent)
        print_ind(self.left, indent + 1)
        print_ind(self.right, indent + 1)

    @add_to_class(ast.Variable)
    def print_tree(self, indent=0):
        print_ind(self.name, indent)
