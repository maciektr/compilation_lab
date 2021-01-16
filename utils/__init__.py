import sys

def stdout_print(*args):
    print(*args)

def stderr_print(*args):
    print(*args,file=sys.stderr)

def exit_fail(message: str=None):
    if message:
        stderr_print(message)
    sys.exit(1)

def exit_ok(message: str=None):
    if message:
        stderr_print(message)
    sys.exit(0)


class GenericVisit:
    def __call__(self):
        pass

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
