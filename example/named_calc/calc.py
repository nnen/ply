# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'NAME','NUMBER',
    )

literals = ['=','+','-','*','/', '(',')']

# Tokens

t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(p):
    'statement : varname=NAME "=" value=expression'
    names[p.varname] = p.value

def p_statement_expr(p):
    'statement : expr=expression'
    print(p.expr)

def p_expression_binop(p):
    '''expression : a=expression op='+' b=expression
                  | a=expression op='-' b=expression
                  | a=expression op='*' b=expression
                  | a=expression op='/' b=expression'''
    if p.op == '+'  : p[0] = p.a + p.b
    elif p.op == '-': p[0] = p.a - p.b
    elif p.op == '*': p[0] = p.a * p.b
    elif p.op == '/': p[0] = p.a / p.c

def p_expression_uminus(p):
    "expression : '-' expr=expression %prec UMINUS"
    p[0] = -p.expr

def p_expression_group(p):
    "expression : '(' expr=expression ')'"
    p[0] = p.expr

def p_expression_number(p):
    "expression : value=NUMBER"
    p[0] = p.value

def p_expression_name(p):
    "expression : name=NAME"
    try:
        p[0] = names[p.name]
    except LookupError:
        print("Undefined name '%s'" % p.name)
        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
