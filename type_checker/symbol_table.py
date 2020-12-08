class Scope:
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def __setitem__(self, name, symbol):
        self.dict[name] = symbol

    def __getitem__(self, name):
        if name in self.dict:
            return self.dict[name]

        return self.parent[name] if self.parent else None


class SymbolTable:
    def __init__(self, parent, name):
        """
        Parent scope and symbol table name
        """
        pass

    def __setitem__(self, name, symbol):
        """
        Put variable symbol or fundef under <name> entry
        """
        pass

    def __getitem__(self, name):
        """
        Get variable symbol or fundef from <name> entry
        """
        pass

    def get_parent_scope(self):
        pass

    def push_scope(self, name):
        pass

    def pop_scope(self):
        pass
