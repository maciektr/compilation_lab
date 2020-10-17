import ply.lex as lex

reserved = {
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'eye': 'EYE',
}

tokens = (
    'ID',           #ISSUE: Assigns "IF", "WHILE", etc. as IDs
    'INTNUM',       #ISSUE: ASSIGNS REAL AS INTNUM + '.' + INTNUM
    'REAL',         #ISSUE: ASSIGNS REAL AS INTNUM + '.' + INTNUM
    'PLUS',         #DONE, NOT TESTED  
    'MINUS',        #DONE, NOT TESTED
    'MUL',          #DONE, NOT TESTED
    'DIVIDE',       #DONE, NOT TESTED
    'LPAREN',       #DONE, NOT TESTED
    'RPAREN',       #DONE, NOT TESTED
    'LSQPAREN',     #DONE, NOT TESTED
    'RSQPAREN',     #DONE, NOT TESTED
    'LBRACK',       #DONE, NOT TESTED
    'RBRACK',       #DONE, NOT TESTED
    'DOTPLUS',      #DONE, NOT TESTED
    'DOTMINUS',     #DONE, TESTED
    'DOTMUL',       #DONE, NOT TESTED
    'DOTDIV',       #DONE, NOT TESTED
    'ASSIGN',       #DONE, NOT TESTED   
    'PLUSASGN',     #DONE, NOT TESTED 
    'MINUSASGN',    #DONE, NOT TESTED 
    'MULASGN',      #DONE, NOT TESTED 
    'DIVASGN',      #DONE, NOT TESTED   
    'LESSTHAN',     #DONE, NOT TESTED 
    'GREATERTHAN',  #DONE, NOT TESTED 
    'LESSOREQ',     #DONE, NOT TESTED 
    'GREATEROREQ',  #DONE, NOT TESTED 
    'NOTEQ',        #DONE, NOT TESTED 
    'EQUAL',        #DONE, NOT TESTED 
    'RANGEOP',      #DONE, NOT TESTED
    'TRANSPOSE',    #DONE, NOT TESTED
    'COMMA',        #DONE, NOT TESTED
    'SEMICOLON',    #DONE, NOT TESTED
    'IF',           #
    'ELSE',         #
    'FOR',          #
    'WHILE',        #
    'BREAK',        #
    'CONTINUE',     #
    'RETURN',       #
    'PRINT',        #
    'STRING',       #
    *reserved.values()
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MUL   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LSQPAREN  = r'\['
t_RSQPAREN  = r'\]'
t_LBRACK  = r'\{'
t_RBRACK  = r'\}'
t_DOTPLUS = r'\.\+'
t_DOTMINUS = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_ASSIGN = r'\='
t_PLUSASGN = r'\+\='
t_MINUSASGN = r'-\='
t_MULASGN = r'\*\='
t_DIVASGN = r'/\='
t_LESSTHAN = r'\<'
t_GREATERTHAN = r'\>'
t_LESSOREQ = r'\<\='
t_GREATEROREQ = r'\>\='
t_NOTEQ = r'\!\='
t_EQUAL = r'\=\='
t_RANGEOP = r'\:'
t_TRANSPOSE = r'\''
t_COMMA = r'\,'
t_SEMICOLON = r'\;'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t
    # doesn't work, assigns "IF", "WHILE", etc as IDs

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)    
    return t
    
def t_REAL(t):
    r'^-?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    t.value = int(t.value)    
    return t
    #doesn't work, assigns real numbers as INTNUM + '.' + INTNUM

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


literals = [
    '+', '-', '*', '/', '=', "'", ';', '(', ')',
]



