class Operators:
    FUNCTION_DICT = {
        "+" : lambda a,b: a + b,
        "-" : lambda a,b: a - b,
        "*" : lambda a,b: a * b,
        "/" : lambda a,b: a / b,
        ".+" : lambda a,b: a + b,
        ".-" : lambda a,b: a - b,
        ".*" : lambda a,b: a * b,
        "./" : lambda a,b: a / b,
        "+=" : lambda a,b: a + b,
        "-=" : lambda a,b: a - b,
        "*=" : lambda a,b: a * b,
        "/=" : lambda a,b: a / b,
    }

    LOGICAL_DICT = {
        "==" : lambda a,b: a == b,
        ">" : lambda a,b: a > b,
        "<" : lambda a,b: a < b,
        ">=" : lambda a,b: a >= b,
        "<=" : lambda a,b: a <= b,
        "!=" : lambda a,b: a != b,
    }

    def __init__(self):
        pass

    def __call__(self, operator):
        res = self.get_function(operator)
        if res:
            return res
        res = self.get_logical(operator)
        return res

    def get_function(self, operator):
        if operator in self.FUNCTION_DICT:
            return self.FUNCTION_DICT[operator]
        return None

    def get_logical(self, operator):
        if operator in self.LOGICAL_DICT:
            return self.LOGICAL_DICT[operator]
        return None
