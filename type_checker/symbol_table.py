class Scope:
    def __init__(self, name: str, parent=None):
        self.dict = dict()
        self.name = name
        self.parent : Scope = parent

    def __setitem__(self, name, symbol):
        self.dict[name] = symbol

    def __getitem__(self, name):
        if name in self.dict:
            return self.dict[name]

        return self.parent[name] if self.parent else None

    def __contains__(self, name):
        return name in self.dict


class SymbolTable:
    def __init__(self, name, parent=None):
        """
        Parent scope and symbol table name
        """
        self.current_scope = Scope(name, parent)

    def __contains__(self, name):
        return name in self.current_scope

    def __setitem__(self, name, symbol):
        """
        Put variable symbol or fundef under <name> entry
        """
        self.current_scope[name] = symbol

    def __getitem__(self, name):
        """
        Get variable symbol or fundef from <name> entry
        """
        return self.current_scope[name]

    @property
    def parent_scope(self):
        return self.current_scope.parent

    def push_scope(self, name):
        self.current_scope = Scope(name, self.current_scope)

    def pop_scope(self):
        scope = self.current_scope
        self.current_scope = scope.parent
        return scope
