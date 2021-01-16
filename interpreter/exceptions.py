class InterpreterException(Exception):
    pass

class ReturnValueException(InterpreterException):
    def __init__(self,value):
        super().__init__()
        self.value = value

class BreakException(InterpreterException):
    pass

class ContinueException(InterpreterException):
    pass
