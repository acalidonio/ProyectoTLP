"""
Gramática:
  S -> TT identificador D
  TT -> int | float
  D -> coma identificador D | finInstruccion
"""

import ply.lex as lex
import sys

# Lexer

tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'keyword',
   'identificador',
   'inicioBloque',
   'finBloque',
   'finInstruccion',
   'asignacion',
   'comentario',
   'comentario_bloque',
   'cadena',
   'coma',
   'eof',
   'int',
   'float'
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/' 
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_inicioBloque = r'\{'
t_finBloque = r'\}'
t_finInstruccion = r'\;'
t_asignacion = r'\='
t_coma= r'\,'
t_eof= r'\$'


def t_int(t):
    r'int'
    return t

def t_float(t):
    r'float'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_keyword(t):
    r'(char)|(return)|(if)|(else)|(do)|(while)|(for)|(void)'
    return t

def t_identificador(t):
    r'([a-z]|[A-Z]|_)([a-z]|[A-Z]|\d|_)*'
    return t

def t_cadena(t):
    r'\".*\"'
    return t

def t_comentario(t):
    r'\/\/.*'
    pass

def t_comentario_bloque(t):
    r'\/\*(.|\n)*\*\/'
    pass

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)
    raise SyntaxError(f"Error Léxico: Carácter inesperado '{t.value[0]}' en línea {t.lexer.lineno}")

lexer = lex.lex()


# Parser LL1

S = 'S'
TT = 'TT'
D = 'D'

tabla = [
    # Producciones para S
    [S, 'identificador', None],
    [S, 'int', [TT, 'identificador', D]],
    [S, 'float', [TT, 'identificador', D]],
    [S, 'coma', None],
    [S, 'finInstruccion', None],
    
    # Producciones para TT
    [TT, 'identificador', None],
    [TT, 'int', ['int']],
    [TT, 'float', ['float']],
    [TT, 'coma',  None],
    [TT, 'finInstruccion', None],
    
    # Producciones para D
    [D, 'identificador', None],
    [D, 'int', None],
    [D, 'float', None],
    [D, 'coma', ['coma', 'identificador', D]],
    [D, 'finInstruccion', ['finInstruccion']],
]

# Se inicializa la pila con EOF y el símbolo inicial
stack = ['eof', S]

def buscar_en_tabla(no_terminal, terminal):
    """Busca una entrada en la tabla de parseo"""
    for i in range(len(tabla)):
        if tabla[i][0] == no_terminal and tabla[i][1] == terminal:
            return tabla[i][2] # Retorna la producción
    return None

def agregar_pila(produccion):
    """Agrega los elementos de una producción a la pila en orden inverso"""
    for elemento in reversed(produccion):
        if elemento != 'vacia': 
            stack.append(elemento)

def miParser(lexer):
    """Función principal del parser LL(1)"""
    
    tok = lexer.token()
    if not tok:
        # Maneja entrada vacía
        if stack == ['eof', S]:
            stack.pop()
            if stack == ['eof']: return
        raise SyntaxError("Entrada vacía no válida")

    x = stack[-1]
    
    while True:
        if x == tok.type and x == 'eof':
            #print("String correcta")
            return
        else:
            if x == tok.type and x != 'eof':
                stack.pop()
                x = stack[-1]
                tok = lexer.token()
                if not tok:
                    tok = lex.LexToken()
                    tok.type = 'eof'
            
            elif x in tokens and x != tok.type:
                # Se esperaba un terminal diferente
                raise SyntaxError(f"Error de Sintaxis: Se esperaba '{x}' pero se encontró '{tok.type}'")
            
            elif x not in tokens: 
                # Es No-Terminal: Consultar la tabla
                celda = buscar_en_tabla(x, tok.type)
                
                if celda is None:
                    # No hay entrada en la tabla
                    raise SyntaxError(f"Error de Sintaxis: Entrada inesperada '{tok.type}' para el estado '{x}' en pos {tok.lexpos}")
                else:
                    stack.pop()
                    agregar_pila(celda)
                    # print(stack)
                    x = stack[-1]
            else:
                raise SystemError("Error del parser")

def parse_string(input_text):
    """
    Añade el símbolo de fin de cadena y ejecuta el parser.
    """
    if not input_text.strip().endswith('$'):
        input_text += ' $'
        
    lexer.input(input_text)

    global stack
    stack = ['eof', S] 
    
    miParser(lexer)
    return True

def main():
    """Función principal de la aplicación"""
    if len(sys.argv) < 2:
        print("Uso: python parser.py \"<string>\"")
        return

    input_text = " ".join(sys.argv[1:])
    print(f"Entrada: {input_text}")

    try:
        parse_string(input_text)
        print("La cadena cumple con la gramática formal.")
    except (SyntaxError, SystemError) as e:
        print(f"La cadena no cumple la gramática formal.")
        print(f"{e}")

if __name__ == "__main__":
    main()