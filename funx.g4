grammar funx;

root: def_fun* expr? EOF;

def_fun: F args? L body R;

args: args args
    | VAR
    ;

body : (expr | instr)* ;

expr: '(' expr ')' #PARENTESIS
    | expr (MUL | DIV | MOD) expr #MULDIVMOD
    | expr (SUM | RES) expr #SUMRES
    | NUM #NUM
    | VAR #EXPRVAR	
    | call_fun #CALLFUN	
    ;

call_fun: F call_args?;

call_args: call_args call_args
    | expr
    ;

instr: asign
    | condi
    | iter
    | boolean
    ;

asign: VAR '<-' expr;

condi: 'if' boolean L body R ('else' L body R)?;

iter: 'while' boolean L body R;

boolean: expr EQ expr
        | expr NEQ expr
        | expr LT expr
        | expr GT expr
        | expr LEQT expr
        | expr GEQT expr
        ;

COMENTARIO : ('#' ~( '\r' | '\n' )*) -> skip;

EQ: '=';
NEQ: '!=';
LT: '<';
GT: '>';
LEQT: '<=';
GEQT: '>=';

L: '{';
R: '}';

F : [A-Z]+([a-z]|[A-Z]|[0-9])*;

VAR: [a-z]+;

NUM : [0-9]+ ;
SUM : '+' ;
RES : '-' ;
MOD : '%' ;
MUL : '*' ;
DIV : '/' ;
WS : [ \t\n]+ -> skip;