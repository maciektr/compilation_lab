reserved = {
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'eye': 'EYE',
}

tokens = (
    'ID',
    'INTNUM',
    'DOTADD',
    'SUBASSIGN',
    'DOTSUB',
    'MULASSIGN',
    'DOTMUL',
    'DIVASSIGN',
    'DOTDIV',
    *reserved.values()
)

t_DOTADD = r'\.\+'
t_SUBASSIGN = r'\-='
t_DOTSUB = r'\.-'
t_MULASSIGN = r'\*='
t_DOTMUL = r'\.\*'
t_DIVASSIGN = r'\/='
t_DOTDIV = r'\./'

literals = [
    '+', '-', '*', '/', '=', "'", ';', '(', ')',
]

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
