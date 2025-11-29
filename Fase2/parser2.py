"""
Parser Descendente Recursivo para Español Simplificado
Fase 2 - Proyecto TLP02-2025
Gramática: Oración → Sujeto Verbo Objeto
"""

class Token:
    """Representa un token con su tipo y valor"""
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    
    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}')"


class Lexer:
    """Analizador léxico - convierte texto en tokens"""
    
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
            "hermoso", "feo", "nuevo", "viejo", "rápido", "lento",
            "inteligente", "feliz", "triste"
        }
    
    def tokenizar(self, texto):
        """Convierte una cadena de texto en lista de tokens"""
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
    """Parser descendente recursivo para gramática simplificada"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errores = []
        self.arbol = None
    
    def token_actual(self):
        """Retorna el token actual o None si llegamos al final"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def avanzar(self):
        """Avanza al siguiente token"""
        self.pos += 1
    
    def esperar(self, tipo_esperado):
        """Verifica que el token actual sea del tipo esperado"""
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
        if not self.esperar("VERBO"):
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
        if not self.esperar("ARTICULO"):
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
        if not self.esperar("SUSTANTIVO"):
            return None
        sintagma["hijos"].append({
            "tipo": "Sustantivo",
            "valor": self.token_actual().valor
        })
        self.avanzar()
        
        return sintagma
    
    def parsear(self):
        """Inicia el proceso de parseo"""
        self.arbol = self.parsear_oracion()
        return self.arbol is not None
    
    def imprimir_arbol(self, nodo=None, nivel=0):
        """Imprime el árbol de parseo de forma jerárquica"""
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


def analizar_oracion(texto):
    """Función principal para analizar una oración"""
    print(f"\n{'='*60}")
    print(f"Analizando: '{texto}'")
    print('='*60)
    
    # Tokenización
    lexer = Lexer()
    tokens = lexer.tokenizar(texto)
    print(f"\nTokens: {tokens}")
    
    # Parseo
    parser = Parser(tokens)
    exito = parser.parsear()
    
    if exito:
        print("\n✓ ORACIÓN VÁLIDA")
        print("\nÁrbol de parseo:")
        parser.imprimir_arbol()
    else:
        print("\n✗ ORACIÓN INVÁLIDA")
        print("\nErrores encontrados:")
        for error in parser.errores:
            print(f"  • {error}")
    
    return exito, parser


# Ejemplos de prueba
if __name__ == "__main__":
    print("PARSER DESCENDENTE RECURSIVO - ESPAÑOL SIMPLIFICADO")
    print("Fase 2: Mini-parser para lenguaje natural limitado\n")
    
    # Ejemplos VÁLIDOS
    print("\n" + "="*60)
    print("EJEMPLOS VÁLIDOS")
    print("="*60)
    
    oraciones_validas = [
        "el gato come un libro",
        "la niña lee el libro",
        "un pequeño perro mira la casa",
        "el estudiante inteligente estudia un libro nuevo",
        "los hermanos compran una computadora rápida"
    ]
    
    for oracion in oraciones_validas:
        analizar_oracion(oracion)
    
    # Ejemplos INVÁLIDOS
    print("\n\n" + "="*60)
    print("EJEMPLOS INVÁLIDOS")
    print("="*60)
    
    oraciones_invalidas = [
        "gato come libro",  # Falta artículos
        "el gato el perro",  # Falta verbo
        "come el libro",  # Falta sujeto
        "el gato come",  # Falta objeto
        "el hermoso",  # Oración incompleta
        "perro el come libro el",  # Orden incorrecto
    ]
    
    for oracion in oraciones_invalidas:
        analizar_oracion(oracion)