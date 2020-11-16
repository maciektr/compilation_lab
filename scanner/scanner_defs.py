reserved = {
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'eye': 'EYE',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'print': 'PRINT',
}

tokens = (
    'ID',
    'REAL',
    'INTNUM',
    'STRING',
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'PLUSASGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'LESSTHAN',
    'GREATERTHAN',
    'LESSOREQ',
    'GREATEROREQ',
    'NOTEQ',
    'EQUAL',
    'RANGEOP',
    *reserved.values()
)

# invalid-name
# pylint: disable=C0103

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'

t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_PLUSASGN = r'\+\='
t_SUBASSIGN = r'-\='
t_MULASSIGN = r'\*\='
t_DIVASSIGN = r'/\='
t_LESSTHAN = r'\<'
t_GREATERTHAN = r'\>'
t_LESSOREQ = r'\<\='
t_GREATEROREQ = r'\>\='
t_NOTEQ = r'\!\='
t_EQUAL = r'\=\='
t_RANGEOP = r'\:'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_REAL(t):
    r'([0-9]*)?\.([0-9]+([eE][-+]?[0-9]+)?)?'
    if t.value.endswith('.'):
        t.value = t.value[:-1]
    t.value = float(t.value if t.value else 0)
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\".*?\"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

literals = [
    '+', '-', '*', '/', '=', "'", ';', "'", '"', ',',
    '(', ')', '[', ']', '{', '}',

]

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
