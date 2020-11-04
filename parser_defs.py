precedence = (
    ('left', 'LESSTHAN', 'GREATERTHAN', 'LESSOREQ', 'GREATEROREQ', 'NOTEQ'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('right', 'RANGEOP'),
    ('nonassoc', 'IFINS'),
    ('nonassoc', 'ELSE'),
)

start = 'PROGRAM'

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

def p_program(p):
    """PROGRAM : INSTRUCTIONS """

def p_instructions(p):
    """INSTRUCTIONS : SINGLE_INSTRUCTION
                    | INSTRUCTIONS SINGLE_INSTRUCTION"""

def p_single_instruction(p):
    """SINGLE_INSTRUCTION : NO_COLON_INSTRUCTION
                          | INSTRUCTION ';' """

def p_no_colon_instruction(p):
    """NO_COLON_INSTRUCTION : IF
                            | WHILE
                            | FOR
                            | INSTRUCTION_BLOCK"""

def p_instruction_expression(p):
    """INSTRUCTION : EXPRESSION"""

def p_instruction_block(p):
    """INSTRUCTION_BLOCK : '{' INSTRUCTION '}'"""

def p_if(p):
    """IFINS : IF '(' EXPRESSION ')' INSTRUCTION
             | IF '(' EXPRESSION ')' INSTRUCTION ELSEINS"""

def p_else(p):
    """ELSEINS : ELSE INSTRUCTION """

def p_while(p):
    """WHILEINS : WHILE '(' EXPRESSION ')' INSTRUCTION"""

def p_for(p):
    """FORINS : FOR ID '=' RANGE INSTRUCTION"""

def p_print(p):
    """INSTRUCTION : PRINT VALUES"""

def p_id_instruction(p):
    """ID_INSTRUCTION : ID
                      | ID_PART"""

def p_instruction_assign(p):
    """INSTRUCTION : ID_INSTRUCTION PLUSASGN EXPRESSION
                   | ID_INSTRUCTION SUBASSIGN EXPRESSION
                   | ID_INSTRUCTION MULASSIGN EXPRESSION
                   | ID_INSTRUCTION DIVASSIGN EXPRESSION
                   | ID_INSTRUCTION '=' EXPRESSION"""

def p_instruction_return(p):
    """INSTRUCTION : RETURN
                   | RETURN EXPRESSION"""

def p_break_continue(p):
    """INSTRUCTION : BREAK
                   | CONTINUE"""

def p_expression_operation(p):
    """EXPRESSION : EXPRESSION '+' EXPRESSION
                  | EXPRESSION '-' EXPRESSION
                  | EXPRESSION '*' EXPRESSION
                  | EXPRESSION '/' EXPRESSION
                  | EXPRESSION DOTADD EXPRESSION
                  | EXPRESSION DOTSUB EXPRESSION
                  | EXPRESSION DOTMUL EXPRESSION
                  | EXPRESSION DOTDIV EXPRESSION"""

def p_expression_value(p):
    """EXPRESSION : ID_PART
                  | NUMERICAL
                  | LIST
                  | STRING"""

def p_numerical_num(p):
    """NUMERICAL : INTNUM
                 | REAL"""

def p_range(p):
    """RANGE : EXPRESSION ':' EXPRESSION"""

def p_values_def(p):
    """VALUES : EXPRESSION
              | RANGE
              | VALUES ',' EXPRESSION
              | VALUES ',' RANGE"""

def p_expression_id(p):
    """EXPRESSION : ID"""

def p_expression_parenthese(p):
    """EXPRESSION : '(' EXPRESSION ')'"""

def p_expression_zeros(p):
    """EXPRESSION : ZEROS '(' INTNUM ')'"""

def p_expression_ones(p):
    """EXPRESSION : ONES '(' INTNUM ')'"""

def p_expression_eye(p):
    """EXPRESSION : EYE '(' INTNUM ')'"""

def p_expression_transpose(p):
    """EXPRESSION : EXPRESSION "\'" """

def p_vector(p):
    """VALUES : ID '[' VALUES ']'"""

def p_list(p):
    """ LIST : '[' VALUES ']'"""

def p_list_extend_values(p):
    """LIST : LIST ',' EXPRESSION"""


