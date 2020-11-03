precedence = (
   ("right", '='),
   ("left", '+', '-'),
   ("left", '*', '/'),
)

symtab = {}

def p_error(p):
    print("parsing error", p)

def p_start(p):
    """start : EXPRESSION
             | start EXPRESSION"""
    if   len(p)==2: print("p[1]=", p[1])
    else:           print("p[2]=", p[2])

def p_expression_number(p):
    """EXPRESSION : INTNUM"""
    p[0] = p[1]

def p_expression_var(p):
    """EXPRESSION : ID"""
    val = symtab.get(p[1])
    if val:
        p[0] = val
    else:
        p[0] = 0
        print("%s not used\n" %p[1])

def p_expression_assignment(p):
    """EXPRESSION : ID '=' EXPRESSION"""
    p[0] = p[3]
    symtab[p[1]] = p[3]

def p_expression_sum(p):
    """EXPRESSION : EXPRESSION '+' EXPRESSION
                  | EXPRESSION '-' EXPRESSION"""
    if   p[2]=='+': p[0] = p[1] + p[3]
    elif p[2]=='-': p[0] = p[1] - p[3]

def p_expression_mul(p):
    """EXPRESSION : EXPRESSION '*' EXPRESSION
                  | EXPRESSION '/' EXPRESSION"""
    if   p[2]=='*': p[0] = p[1] * p[3]
    elif p[2]=='/': p[0] = p[1] / p[3]

def p_expression_group(p):
    """EXPRESSION : '(' EXPRESSION ')'"""
    p[0] = p[2]


