import time
import sys

def imprimir_lento(texto, delay=0.03):
    """Imprime texto con efecto de escritura"""
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def pausa_presentacion(segundos=2):
    """Pausa dramática entre secciones"""
    time.sleep(segundos)

def titulo_seccion(texto):
    """Imprime título de sección destacado"""
    print("\n" + "="*70)
    print(f" {texto} ".center(70, "="))
    print("="*70 + "\n")

def demo_interactiva():
    """Demostración interactiva para la presentación"""
    
    print("\n" + "#"*70)
    print(" DEMOSTRACIÓN EN VIVO ".center(70, "#"))
    print(" Mini-Parser para Lenguaje Natural Limitado ".center(70))
    print("#"*70 + "\n")
    
    input("Presiona ENTER para comenzar la demostración...")
    
    # ============================================================
    # PARTE 1: Introducción y Contexto
    # ============================================================
    titulo_seccion("PARTE 1: INTRODUCCIÓN")
    
    imprimir_lento("En la Fase 1 aprendimos que:")
    print("  • Los lenguajes formales usan gramáticas libres de contexto (CFG)")
    print("  • Los lenguajes naturales exceden ese marco teórico")
    print("  • Los parsers tradicionales fallan con lenguaje natural")
    
    pausa_presentacion()
    imprimir_lento("\nEn esta Fase 2, hemos:")
    print("  • Diseñado una CFG para un subconjunto del español")
    print("  • Implementado un parser descendente recursivo")
    print("  • Comparado nuestro parser con herramientas modernas de NLP")
    
    input("\nPresiona ENTER para ver nuestra gramática...")
    
    # ============================================================
    # PARTE 2: Presentación de la Gramática
    # ============================================================
    titulo_seccion("PARTE 2: NUESTRA GRAMÁTICA")
    
    print("Hemos diseñado una gramática simple pero representativa:")
    print("""
    Estructura: Sujeto → Verbo → Objeto
    
    Reglas de producción:
      Oración → Sujeto Verbo Objeto
      Sujeto → Artículo Adjetivo* Sustantivo
      Objeto → Artículo Adjetivo* Sustantivo
      
    Vocabulario:
      • 6 artículos (el, la, un, una, los, las)
      • 14 sustantivos (gato, perro, niño, casa, libro, ...)
      • 11 verbos (come, bebe, lee, escribe, mira, ...)
      • 15 adjetivos (grande, pequeño, rojo, azul, hermoso, ...)
    """)
    
    input("\nPresiona ENTER para ver ejemplos válidos...")
    
    # ============================================================
    # PARTE 3: Demostración de Casos Válidos
    # ============================================================
    titulo_seccion("PARTE 3: CASOS VÁLIDOS")
    
    from spanish_parser import Lexer, Parser
    
    ejemplos_validos = [
        "el gato come un libro",
        "la niña pequeña lee el libro grande",
        "un estudiante inteligente estudia la computadora nueva"
    ]
    
    for i, oracion in enumerate(ejemplos_validos, 1):
        print(f"\n{'─'*70}")
        print(f"Ejemplo {i}: '{oracion}'")
        print('─'*70)
        
        lexer = Lexer()
        tokens = lexer.tokenizar(oracion)
        parser = Parser(tokens)
        exito = parser.parsear()
        
        if exito:
            print("\n✓ ORACIÓN VÁLIDA")
            print("\nÁrbol de parseo:")
            parser.imprimir_arbol()
        
        pausa_presentacion(1)
    
    input("\nPresiona ENTER para ver casos inválidos...")
    
    # ============================================================
    # PARTE 4: Demostración de Casos Inválidos
    # ============================================================
    titulo_seccion("PARTE 4: CASOS INVÁLIDOS (Errores Detectados)")
    
    ejemplos_invalidos = [
        ("gato come libro", "Faltan artículos"),
        ("el gato el perro", "Falta verbo"),
        ("el hermoso", "Oración incompleta"),
    ]
    
    for i, (oracion, razon) in enumerate(ejemplos_invalidos, 1):
        print(f"\n{'─'*70}")
        print(f"Ejemplo {i}: '{oracion}'")
        print(f"Razón esperada: {razon}")
        print('─'*70)
        
        lexer = Lexer()
        tokens = lexer.tokenizar(oracion)
        parser = Parser(tokens)
        exito = parser.parsear()
        
        if not exito:
            print("\n✗ ORACIÓN INVÁLIDA")
            print("\nErrores detectados:")
            for error in parser.errores:
                print(f"  • {error}")
        
        pausa_presentacion(1)
    
    input("\nPresiona ENTER para comparar con spaCy...")
    
    # ============================================================
    # PARTE 5: Comparación con spaCy
    # ============================================================
    titulo_seccion("PARTE 5: COMPARACIÓN CON NLP MODERNO (spaCy)")
    
    try:
        import spacy
        nlp = spacy.load("es_core_news_sm")
        
        print("Vamos a analizar la MISMA oración con ambos enfoques:\n")
        oracion_demo = "el pequeño gato come un libro"
        
        print("="*70)
        print(f"Oración: '{oracion_demo}'")
        print("="*70)
        
        # Nuestro parser
        print("\n【 NUESTRO PARSER FORMAL 】\n")
        lexer = Lexer()
        tokens = lexer.tokenizar(oracion_demo)
        parser = Parser(tokens)
        exito = parser.parsear()
        
        if exito:
            print("✓ Resultado: VÁLIDA")
            parser.imprimir_arbol()
        
        pausa_presentacion(2)
        
        # spaCy
        print("\n【 spaCy (NLP MODERNO) 】\n")
        doc = nlp(oracion_demo)
        
        print("Análisis morfológico:")
        for token in doc:
            print(f"  {token.text:12} → {token.pos_:8} (lema: {token.lemma_})")
        
        print("\nÁrbol de dependencias:")
        for token in doc:
            print(f"  {token.text:12} ← {token.dep_:12} ← {token.head.text}")
        
    except ImportError:
        print("⚠ spaCy no está instalado. Instalar con:")
        print("  pip install spacy")
        print("  python -m spacy download es_core_news_sm")
    
    input("\nPresiona ENTER para ver casos que desafían nuestro parser...")
    
    # ============================================================
    # PARTE 6: Limitaciones y Casos Desafiantes
    # ============================================================
    titulo_seccion("PARTE 6: LIMITACIONES DE NUESTRO PARSER")
    
    casos_desafiantes = [
        ("El niño no come el libro", 
         "Negación - no contemplada en la gramática"),
        
        ("El estudiante que estudia aprueba el examen", 
         "Cláusula relativa - estructura compleja"),
        
        ("Los gata come un libros", 
         "Error de concordancia - nuestro parser no lo detecta"),
        
        ("El profe enseña programación", 
         "Vocabulario coloquial - palabra no reconocida"),
    ]
    
    for oracion, explicacion in casos_desafiantes:
        print(f"\n{'─'*70}")
        print(f"Caso: '{oracion}'")
        print(f"Problema: {explicacion}")
        print('─'*70)
        
        lexer = Lexer()
        tokens = lexer.tokenizar(oracion)
        parser = Parser(tokens)
        exito = parser.parsear()
        
        print(f"\nNuestro parser: {'✓ VÁLIDA' if exito else '✗ INVÁLIDA'}")
        
        if not exito and parser.errores:
            print("Errores:")
            for error in parser.errores[:2]:  # Mostrar solo 2 errores
                print(f"  • {error}")
        
        pausa_presentacion(1)
    
    input("\nPresiona ENTER para ver la tabla comparativa...")
    
    # ============================================================
    # PARTE 7: Tabla Comparativa
    # ============================================================
    titulo_seccion("PARTE 7: COMPARACIÓN SISTEMÁTICA")
    
    print("""
    ┌─────────────────────┬────────────────────────┬─────────────────────────┐
    │ Criterio            │ Nuestro Parser         │ spaCy (NLP Moderno)     │
    ├─────────────────────┼────────────────────────┼─────────────────────────┤
    │ Vocabulario         │ ~50 palabras fijas     │ >500,000 palabras       │
    ├─────────────────────┼────────────────────────┼─────────────────────────┤
    │ Estructuras         │ Solo SVO simple        │ Todas las estructuras   │
    ├─────────────────────┼────────────────────────┼─────────────────────────┤
    │ Robustez            │ Frágil                 │ Muy robusto             │
    ├─────────────────────┼────────────────────────┼─────────────────────────┤
    │ Ambigüedad          │ No maneja              │ Resuelve con contexto   │
    ├─────────────────────┼────────────────────────┼─────────────────────────┤
    │ Exactitud CFG       │ 100%                   │ ~95-98%                 │
    ├─────────────────────┼────────────────────────┼─────────────────────────┤
    │ Velocidad           │ Muy rápido (O(n))      │ Más lento pero OK       │
    ├─────────────────────┼────────────────────────┼─────────────────────────┤
    │ Transparencia       │ Totalmente explicable  │ "Caja negra"            │
    ├─────────────────────┼────────────────────────┼─────────────────────────┤
    │ Escalabilidad       │ Requiere mod. manual   │ Aprende de datos        │
    └─────────────────────┴────────────────────────┴─────────────────────────┘
    """)
    
    input("\nPresiona ENTER para ver las conclusiones...")
    
    # ============================================================
    # PARTE 8: Conclusiones
    # ============================================================
    titulo_seccion("PARTE 8: CONCLUSIONES")
    
    print("""
    🎯 HALLAZGOS PRINCIPALES:
    
    1. COMPLEMENTARIEDAD
       • Los parsers formales y NLP moderno son complementarios
       • Cada uno es óptimo para diferentes tipos de problemas
    
    2. PRECISIÓN vs ROBUSTEZ
       • Parser formal: Alta precisión, pero frágil
       • NLP moderno: Robusto, pero menos predecible
    
    3. APLICABILIDAD
       • Parser formal → Lenguajes de programación, DSLs
       • NLP moderno → Lenguaje natural humano
    
    4. EXPRESIVIDAD
       • Las CFG son insuficientes para lenguaje natural completo
       • Se requiere poder expresivo mayor + contexto semántico
    
    5. APRENDIZAJE CLAVE
       • Los lenguajes de programación se DISEÑAN para ser parseables
       • Los lenguajes naturales EVOLUCIONAN naturalmente
       • Esta diferencia fundamental determina las técnicas necesarias
    """)
    
    print("\n" + "="*70)
    print(" FIN DE LA DEMOSTRACIÓN ".center(70))
    print("="*70 + "\n")
    
    print("📚 Recursos del proyecto:")
    print("  • Código fuente: spanish_parser.py")
    print("  • Comparación: nlp_comparison.py")
    print("  • Informe completo: informe_fase2.pdf")
    print("\n¡Gracias por su atención! ¿Preguntas?\n")


def demo_rapida():
    """Demostración rápida de 5 minutos"""
    
    print("\n=== DEMO RÁPIDA (5 min) ===\n")
    
    from spanish_parser import Lexer, Parser
    
    print("1. Gramática: Sujeto → Verbo → Objeto")
    print("   Vocabulario: ~50 palabras\n")
    
    print("2. Ejemplo válido:")
    oracion = "el gato come un libro"
    lexer = Lexer()
    tokens = lexer.tokenizar(oracion)
    parser = Parser(tokens)
    if parser.parsear():
        print(f"   '{oracion}' → ✓ VÁLIDA")
        parser.imprimir_arbol()
    
    print("\n3. Ejemplo inválido:")
    oracion = "gato come libro"
    tokens = lexer.tokenizar(oracion)
    parser = Parser(tokens)
    parser.parsear()
    print(f"   '{oracion}' → ✗ INVÁLIDA")
    print(f"   Error: {parser.errores[0]}")
    
    print("\n4. Comparación con spaCy:")
    print("   • Nuestro parser: 50 palabras, estructura rígida")
    print("   • spaCy: >500,000 palabras, estructuras complejas")
    
    print("\n5. Conclusión:")
    print("   Parsers formales → lenguajes diseñados (código)")
    print("   NLP moderno → lenguaje natural (humanos)")


if __name__ == "__main__":
    print("\nSelecciona el tipo de demostración:")
    print("1. Demostración completa (15-20 min)")
    print("2. Demostración rápida (5 min)")
    
    opcion = input("\nOpción (1 o 2): ").strip()
    
    if opcion == "2":
        demo_rapida()
    else:
        demo_interactiva()