

class Memory:
    def __init__(self, name):
        self.name = name
        self.data = {}

    def __contains__(self, name):
        return name in self.data

    def __getitem__(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def __setitem__(self, name, value):
        self.data[name] = value


class MemoryStack:
    def __init__(self):
        self.stack = [Memory('global')]

    def __getitem__(self, name):
        for memory in reversed(self.stack):
            if name in memory:
                return memory[name]
        return None

    def __setitem__(self, name, value):
        for memory in reversed(self.stack):
            if name in memory:
                memory[name] = value
                return

        self.stack[-1][name] = value

    def push(self, name):
        self.stack.append(Memory(name))

    def pop(self):
        return self.stack.pop()
