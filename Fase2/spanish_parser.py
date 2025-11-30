"""
Gramatica: Sujeto → Verbo → Objeto
"""

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    
    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}')"


class Lexer:    
    def __init__(self):
        # Vocabulario limitado
        self.articulos = {"el", "la", "un", "una", "los", "las"}
        self.sustantivos = {
            "gato", "perro", "niño", "niña", "casa", "libro", 
            "árbol", "coche", "mesa", "computadora", "teléfono",
            "profesor", "estudiante", "amigo", "hermano"
        }
        self.verbos = {
            "come", "bebe", "lee", "escribe", "mira", "compra",
            "vende", "estudia", "enseña", "construye", "usa"
        }
        self.adjetivos = {
            "grande", "pequeño", "rojo", "azul", "verde", "amarillo",
            "hermoso", "feo", "nueva", "viejo", "rápido", "lento",
            "inteligente", "feliz", "triste"
        }
    
    def tokenizar(self, texto):
        palabras = texto.lower().strip().split()
        tokens = []
        
        for palabra in palabras:
            if palabra in self.articulos:
                tokens.append(Token("ARTICULO", palabra))
            elif palabra in self.sustantivos:
                tokens.append(Token("SUSTANTIVO", palabra))
            elif palabra in self.verbos:
                tokens.append(Token("VERBO", palabra))
            elif palabra in self.adjetivos:
                tokens.append(Token("ADJETIVO", palabra))
            else:
                tokens.append(Token("DESCONOCIDO", palabra))
        
        return tokens


class Parser:   
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errores = []
        self.arbol = None
    
    def token_actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def avanzar(self):
        self.pos += 1
    
    def verificar_tipo(self, tipo_esperado):
        token = self.token_actual()
        if token is None:
            self.errores.append(f"Se esperaba {tipo_esperado} pero se llegó al final")
            return False
        if token.tipo != tipo_esperado:
            self.errores.append(
                f"Se esperaba {tipo_esperado} pero se encontró {token.tipo} ('{token.valor}')"
            )
            return False
        return True
    
    def parsear_oracion(self):
        """Oración → Sujeto Verbo Objeto"""
        arbol = {"tipo": "Oración", "hijos": []}
        
        # Parsear Sujeto
        sujeto = self.parsear_sintagma_nominal("Sujeto")
        if sujeto is None:
            return None
        arbol["hijos"].append(sujeto)
        
        # Parsear Verbo
        if not self.verificar_tipo("VERBO"):
            return None
        verbo = {"tipo": "Verbo", "valor": self.token_actual().valor}
        arbol["hijos"].append(verbo)
        self.avanzar()
        
        # Parsear Objeto
        objeto = self.parsear_sintagma_nominal("Objeto")
        if objeto is None:
            return None
        arbol["hijos"].append(objeto)
        
        # Verificar que no queden tokens
        if self.token_actual() is not None:
            self.errores.append(
                f"Tokens extra después de la oración: {self.token_actual()}"
            )
            return None
        
        return arbol
    
    def parsear_sintagma_nominal(self, nombre):
        """Sintagma → Artículo Adjetivo* Sustantivo"""
        sintagma = {"tipo": nombre, "hijos": []}
        
        # Artículo (obligatorio)
        if not self.verificar_tipo("ARTICULO"):
            return None
        sintagma["hijos"].append({
            "tipo": "Artículo", 
            "valor": self.token_actual().valor
        })
        self.avanzar()
        
        # Adjetivos (0 o más)
        while self.token_actual() and self.token_actual().tipo == "ADJETIVO":
            sintagma["hijos"].append({
                "tipo": "Adjetivo",
                "valor": self.token_actual().valor
            })
            self.avanzar()
        
        # Sustantivo (obligatorio)
        if not self.verificar_tipo("SUSTANTIVO"):
            return None
        sintagma["hijos"].append({
            "tipo": "Sustantivo",
            "valor": self.token_actual().valor
        })
        self.avanzar()
        
        return sintagma
    
    def parsear(self):
        self.arbol = self.parsear_oracion()
        return self.arbol is not None
    
    def imprimir_arbol(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.arbol
        
        if nodo is None:
            return
        
        indent = "  " * nivel
        if "valor" in nodo:
            print(f"{indent}{nodo['tipo']}: '{nodo['valor']}'")
        else:
            print(f"{indent}{nodo['tipo']}")
            if "hijos" in nodo:
                for hijo in nodo["hijos"]:
                    self.imprimir_arbol(hijo, nivel + 1)


class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def analizar_oracion(texto):
    print(f"\n{'='*60}")
    print(f"{Color.BLUE}{Color.BOLD}Analizando cadena: {Color.ENDC}'{texto}'")
    
    # Tokenización
    lexer = Lexer()
    tokens = lexer.tokenizar(texto)
    print(f"\n{Color.CYAN}{Color.BOLD}Tokens: {Color.ENDC}{tokens}")
    
    # Parseo
    parser = Parser(tokens)
    exito = parser.parsear()
    
    if exito:
        print(f"\n{Color.GREEN}{Color.BOLD}[ ACEPTADO ]{Color.ENDC} ORACIÓN VÁLIDA")
        print(f"\n{Color.CYAN}{Color.BOLD}Arbol de parseo:{Color.ENDC}")
        parser.imprimir_arbol()
    else:
        print(f"\n{Color.FAIL}{Color.BOLD}[ RECHAZADO ]{Color.ENDC} ORACIÓN INVÁLIDA")
        print(f"\n{Color.WARNING}Errores encontrados:{Color.ENDC}")
        for error in parser.errores:
            print(f"  • {error}")
    
    return exito, parser


# Ejemplos de prueba
if __name__ == "__main__":
    # Ejemplos VÁLIDOS
    print("\n" + "="*60 + "\n")
    print(f"{Color.HEADER}{Color.BOLD} EJEMPLOS VÁLIDOS{Color.ENDC}")
    
    oraciones_validas = [
        "la niña vende la nueva computadora",
        "el inteligente estudiante estudia un viejo libro",
        "el perro mira el rápido gato"
    ]
    
    for oracion in oraciones_validas:
        analizar_oracion(oracion)
    
    # Ejemplos INVÁLIDOS
    print("\n\n" + "="*60 + "\n")
    print(f"{Color.HEADER}{Color.BOLD} EJEMPLOS INVÁLIDOS{Color.ENDC}")
    
    oraciones_invalidas = [
        "gato come libro",  # Falta artículos
        "el gato el perro",  # Falta verbo
        "Los gato un come coche",  # Errores de concordancia
    ]
    
    for oracion in oraciones_invalidas:
        analizar_oracion(oracion)