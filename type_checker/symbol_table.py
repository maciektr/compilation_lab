class Scope:
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def put(self, name, symbol):
        self.dict[name] = symbol

    def get(self, name):
        if name in self.dict:
            return self.dict[name]
        if self.parent == None:
            return None
        return self.parent.get(name)


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        pass

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        pass

    def get(self, name): # get variable symbol or fundef from <name> entry
        pass

    def getParentScope(self):
        pass

    def pushScope(self, name):
        pass

    def popScope(self):
        pass
