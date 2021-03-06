import ast.ast as ast
from utils import stderr_print


precedence = (
    ("nonassoc", 'IFX'),
    ('left', 'LESSTHAN', 'GREATERTHAN', 'LESSOREQ', 'GREATEROREQ', 'NOTEQ', 'EQUAL'),
    ('right', 'RANGEOP'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('nonassoc', 'ELSE'),
)

# invalid-name unused-argument
# pylint: disable=C0103 W0613

start = 'PROGRAM'

def p_error(p):
    if p:
        stderr_print("Syntax error at line {0}: LexToken({1}, '{2}')"\
            .format(p.lineno, p.type, p.value))
    else:
        stderr_print("Unexpected end of input")

def p_program(p):
    """PROGRAM : INSTRUCTIONS """
    p[0] = p[1]

def p_instructions(p):
    """INSTRUCTIONS : SINGLE_INSTRUCTION
                    | INSTRUCTIONS SINGLE_INSTRUCTION"""
    p[0] = ast.Instructions(
        instructions=[p[1]] + ([p[2]] if len(p) > 2 else []),
        line_number=p.lexer.lineno,
    )

def p_single_instruction(p):
    """SINGLE_INSTRUCTION : NO_COLON_INSTRUCTION
                          | INSTRUCTION ';' """
    p[0] = p[1]

def p_no_colon_instruction(p):
    """NO_COLON_INSTRUCTION : IFINS
                            | WHILEINS
                            | FORINS
                            | INSTRUCTION_BLOCK"""
    p[0] = p[1]

def p_instruction_expression(p):
    """INSTRUCTION : EXPRESSION"""
    p[0] = p[1]

def p_instruction_block(p):
    """INSTRUCTION_BLOCK : '{' INSTRUCTIONS '}'"""
    p[0] = ast.InstructionBlock(
        instructions=p[2],
        line_number=p.lexer.lineno,
    )

def p_if(p):
    """IFINS : IF '(' LOGICAL ')' SINGLE_INSTRUCTION %prec IFX
             | IF '(' LOGICAL ')' SINGLE_INSTRUCTION ELSEINS"""
    p[0] = ast.If(
        condition=p[3],
        instructions=p[5],
        else_instruction=p[6] if len(p) > 6 else None,
        line_number=p.lexer.lineno,
    )

def p_else(p):
    """ELSEINS : ELSE SINGLE_INSTRUCTION """
    p[0] = ast.Else(
        instructions=p[2],
        line_number=p.lexer.lineno,
    )

def p_while(p):
    """WHILEINS : WHILE '(' LOGICAL ')' SINGLE_INSTRUCTION"""
    p[0] = ast.While(
        condition=p[3],
        instructions=p[5],
        line_number=p.lexer.lineno,
    )

def p_for(p):
    """FORINS : FOR ID '=' RANGE SINGLE_INSTRUCTION"""
    p[0] = ast.For(
        iterator=p[2],
        value_range=p[4],
        instructions=p[5],
        line_number=p.lexer.lineno,
    )

def p_print(p):
    """INSTRUCTION : PRINT VALUES"""
    p[0] = ast.Print(
        value=p[2],
        line_number=p.lexer.lineno,
    )

def p_id_instruction(p):
    """ID_INSTRUCTION : ID_PART"""
    p[0] = p[1]

def p_id_instruction_id(p):
    """ID_INSTRUCTION : ID"""
    p[0] = ast.Variable(
        variable_name=p[1],
        line_number=p.lexer.lineno,
    )

def p_instruction_assign(p):
    """INSTRUCTION : ID_INSTRUCTION PLUSASGN EXPRESSION
                   | ID_INSTRUCTION SUBASSIGN EXPRESSION
                   | ID_INSTRUCTION MULASSIGN EXPRESSION
                   | ID_INSTRUCTION DIVASSIGN EXPRESSION
                   | ID_INSTRUCTION '=' EXPRESSION"""
    p[0] = ast.Assign(
        left=p[1],
        right=p[3],
        operator=p[2],
        line_number=p.lexer.lineno,
    )

def p_instruction_return(p):
    """INSTRUCTION : RETURN
                   | RETURN EXPRESSION"""
    p[0] = ast.Return(
        value=p[2] if len(p) > 2 else None,
        line_number=p.lexer.lineno,
    )

def p_break(p):
    """INSTRUCTION : BREAK"""
    p[0] = ast.Break(
        line_number=p.lexer.lineno,
    )

def p_continue(p):
    """INSTRUCTION : CONTINUE"""
    p[0] = ast.Continue(
        line_number=p.lexer.lineno,
    )

def p_expression_operation(p):
    """EXPRESSION : EXPRESSION '+' EXPRESSION
                  | EXPRESSION '-' EXPRESSION
                  | EXPRESSION '*' EXPRESSION
                  | EXPRESSION '/' EXPRESSION
                  | EXPRESSION DOTADD EXPRESSION
                  | EXPRESSION DOTSUB EXPRESSION
                  | EXPRESSION DOTMUL EXPRESSION
                  | EXPRESSION DOTDIV EXPRESSION"""
    p[0] = ast.BinaryOperation(
        left=p[1],
        right=p[3],
        operator=p[2],
        line_number=p.lexer.lineno,
    )

def p_expression_negative(p):
    """EXPRESSION : '-' EXPRESSION"""
    p[0] = ast.BinaryOperation(
        left=p[1],
        right=-1,
        operator='*',
        line_number=p.lexer.lineno,
    )

def p_expression_value(p):
    """EXPRESSION : ID_PART
                  | NUMERICAL"""
    p[0] = p[1]

def p_expression_list(p):
    """EXPRESSION : LIST"""
    p[0] = p[1]

def p_expression_string(p):
    """EXPRESSION : STRING"""
    p[0] = ast.String(
        value=p[1],
        line_number=p.lexer.lineno,
    )

def p_numerical_intnum(p):
    """NUMERICAL : INTNUM"""
    p[0] = ast.IntNum(
        value=p[1],
        line_number=p.lexer.lineno,
    )

def p_numerical_realnum(p):
    """NUMERICAL : REAL"""
    p[0] = ast.RealNum(
        value=p[1],
        line_number=p.lexer.lineno,
    )

def p_range(p):
    """RANGE : EXPRESSION RANGEOP EXPRESSION"""
    p[0] = ast.ValueRange(
        start = p[1],
        end = p[3],
        line_number=p.lexer.lineno,
    )

def p_values_def(p):
    """VALUES : EXPRESSION
              | RANGE"""
    p[0] = p[1]

def p_values_list_def(p):
    """VALUES : VALUES ',' RANGE
              | VALUES ',' EXPRESSION"""
    p[0] = ast.Value(
        values=[p[1], p[3]],
        line_number=p.lexer.lineno,
    )

def p_expression_id(p):
    """EXPRESSION : ID"""
    p[0] = ast.Variable(
        variable_name=p[1],
        line_number=p.lexer.lineno,
    )

def p_expression_parenthese(p):
    """EXPRESSION : '(' EXPRESSION ')'"""
    p[0] = p[2]

def p_new_dimension(p):
    """DIMENSION : INTNUM """
    p[0] = ast.Dimension(
        values=(p[1],),
        line_number=p.lexer.lineno,
    )

def p_extend_dimension(p):
    """DIMENSION : DIMENSION ',' INTNUM"""
    p[0] = p[1].append(p[3])

def p_expression_zeros(p):
    """EXPRESSION : ZEROS '(' DIMENSION ')'"""
    p[0] = ast.Zeros(
        value=p[3],
        line_number=p.lexer.lineno,
    )

def p_expression_ones(p):
    """EXPRESSION : ONES '(' DIMENSION ')'"""
    p[0] = ast.Ones(
        value=p[3],
        line_number=p.lexer.lineno,
    )

def p_expression_eye(p):
    """EXPRESSION : EYE '(' INTNUM ')'"""
    p[0] = ast.Eye(
        value=p[3],
        line_number=p.lexer.lineno,
    )

def p_expression_transpose(p):
    """EXPRESSION : EXPRESSION "\'" """
    p[0] = ast.Transpose(
        target=p[1],
        line_number=p.lexer.lineno,
    )

def p_range_partition(p):
    """PART_RANGE : RANGE
                  | INTNUM"""
    p[0] = ast.PartitionRange(
        values=[p[1]],
        line_number=p.lexer.lineno,
    )

def p_range_partition_extension(p):
    """PART_RANGE : PART_RANGE ',' RANGE
                  | PART_RANGE ',' INTNUM"""
    p[0] = p[1].append(p[3])

def p_id_part(p):
    """ID_PART : ID '[' PART_RANGE ']'"""
    p[0] = ast.Partition(
        variable=p[1],
        bounds=p[3],
        line_number=p.lexer.lineno,
    )

def p_list(p):
    """ LIST : '[' VALUES ']'"""
    p[0] = ast.List(
        values=[p[2]],
        line_number=p.lexer.lineno,
    )

# def p_list_extend_values(p):
#     """SUPERLIST : LIST ',' LIST"""
#     p[0] = ast.List(
#         values=[p[1],p[3]],
#         line_number=p.lexer.lineno,
#     )

# def p_superlist_extension(p):
#     """SUPERLIST : SUPERLIST ',' LIST"""
#     p[0] = p[1].append(p[3])

def p_logical(p):
    """LOGICAL : EXPRESSION EQUAL EXPRESSION
                | EXPRESSION LESSTHAN EXPRESSION
                | EXPRESSION GREATERTHAN EXPRESSION
                | EXPRESSION LESSOREQ EXPRESSION
                | EXPRESSION GREATEROREQ EXPRESSION
                | EXPRESSION NOTEQ EXPRESSION
    """
    p[0] = ast.Logical(
        left=p[1],
        right=p[3],
        operator=p[2],
        line_number=p.lexer.lineno,
    )
