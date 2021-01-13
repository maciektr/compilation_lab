def add_f(a, b):    return a + b
def sub_f(a, b):    return a - b
def mul_f(a, b):    return a * b
def div_f(a, b):    return a / b

def dotAdd_f(a, b): return
def dotSub_f(a, b): return
def dotMul_f(a,b):  return
def dotDiv_f(a,b):  return

FUNCTION_DICT = {
    "+" : add_f,
    "-" : sub_f,
    "*" : mul_f,
    "/" : div_f,
    ".+" : dotAdd_f,
    ".-" : dotSub_f,
    ".*" : dotMul_f,
    "./" : dotDiv_f,
}

def eq_f(a, b):    return a == b
def gr_f(a, b):    return a > b
def less_f(a, b):  return a < b
def greq_f(a, b):  return a >= b
def leeq_f(a, b):  return a <= b
def noteq_f(a, b): return a != b

LOGICAL_DICT = {
    "==" : eq_f,
    ">" : gr_f,
    "<" : less_f,
    ">=" : greq_f,
    "<=" : leeq_f,
    "!=" : noteq_f,
}

class Operators:
    def __init__(self):
        pass

    def __call__(self, operator):
        res = self.get_function(operator)
        if res:
            return res
        res = self.get_logical(operator)
        return res


    def get_function(self, operator):
        if operator in FUNCTION_DICT:
            return FUNCTION_DICT[operator]
        return None

    def get_logical(self, operator):
        if operator in LOGICAL_DICT:
            return LOGICAL_DICT[operator]
        return None
