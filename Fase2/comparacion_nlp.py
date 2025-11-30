import spacy
from spanish_parser import Lexer, Parser, analizar_oracion

# Cargar modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("Instalando modelo de español...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])
    nlp = spacy.load("es_core_news_sm")


def analizar_con_spacy(texto):
    """Analiza una oración usando spaCy"""
    doc = nlp(texto)
    
    print(f"\n{'='*60}")
    print(f"SpaCy analizando: '{texto}'")
    print('='*60)
    
    # Análisis morfológico
    print("\nAnálisis morfológico (POS tagging):")
    for token in doc:
        print(f"  {token.text:15} → {token.pos_:10} ({token.tag_})")
    
    # Análisis sintáctico (dependencias)
    print("\nÁrbol de dependencias:")
    for token in doc:
        print(f"  {token.text:15} ← {token.dep_:10} ← {token.head.text}")
    
    # Entidades nombradas
    if doc.ents:
        print("\nEntidades nombradas:")
        for ent in doc.ents:
            print(f"  {ent.text} → {ent.label_}")
    
    return doc


def comparacion_completa(oraciones):
    """Compara ambos enfoques con múltiples oraciones"""
    
    resultados = {
        "parser_formal": {"exitosas": 0, "fallidas": 0},
        "spacy": {"procesadas": 0}
    }
    
    for i, oracion in enumerate(oraciones, 1):
        print(f"\n\n{'#'*60}")
        print(f"PRUEBA {i}")
        print('#'*60)
        
        # Parser formal
        exito, parser = analizar_oracion(oracion)
        if exito:
            resultados["parser_formal"]["exitosas"] += 1
        else:
            resultados["parser_formal"]["fallidas"] += 1
        
        # spaCy
        doc = analizar_con_spacy(oracion)
        resultados["spacy"]["procesadas"] += 1
    
    return resultados


def casos_limite():
    """Prueba casos que desafían al parser formal"""
    
    print("\n\n" + "="*60)
    print("CASOS LÍMITE Y DESAFÍOS")
    print("="*60)
    print("\nEstos casos muestran las limitaciones del parser formal")
    print("comparado con herramientas de NLP modernas:\n")
    
    casos = [
        ("Vi al hombre con el telescopio", "Ambigüedad: ¿quién tiene el telescopio?"),
        ("El profe enseña programación chida", "Vocabulario coloquial no reconocido"),
        ("Los gata come un libros", "Error de concordancia (debería detectarse)"),
        ("El estudiante que estudia mucho aprueba el examen", "Cláusula relativa - fuera de la gramática"),
        ("El niño no come el libro", "Negación - no contemplada en la gramática"),
        ("El libro es leído por el estudiante", "Voz pasiva - estructura diferente"),
    ]
    
    for oracion, descripcion in casos:
        print(f"\n{'-'*60}")
        print(f"CASO: {descripcion}")
        print('-'*60)
        # Parser formal
        exito, parser = analizar_oracion(oracion)
        # spaCy
        analizar_con_spacy(oracion)


def analisis_estadistico():
    """Muestra capacidades estadísticas de spaCy"""
    print("\n\n" + "="*60)
    print("ANÁLISIS ESTADÍSTICO CON SPACY")
    print("="*60)
    
    textos = [
        "El gato negro duerme en la casa vieja",
        "Los estudiantes inteligentes estudian todos los días",
        "Mi hermana compra libros nuevos cada semana"
    ]
    
    for texto in textos:
        doc = nlp(texto)
        print(f"\nTexto: '{texto}'")
        print(f"  • Número de tokens: {len(doc)}")
        print(f"  • Número de palabras: {len([t for t in doc if not t.is_punct])}")
        pos_counts = {}
        for token in doc:
            pos_counts[token.pos_] = pos_counts.get(token.pos_, 0) + 1
        for pos, count in pos_counts.items():
            print(f"    - {pos}: {count}")


def modo_interactivo():
    """NUEVA FUNCIÓN: Permite al usuario ingresar oraciones y decidir cuándo salir"""
    print("\n" + "#"*60)
    print(" MODO INTERACTIVO DE USUARIO ")
    print("#"*60)
    
    while True:
        try:
            # 1. Solicitar oración
            texto = input("\n>> Ingresa tu oración para analizar: ").strip()
            
            if not texto:
                print("No ingresaste nada. Intenta de nuevo.")
                continue

            # 2. Realizar Análisis
            print(f"\nAnalizando: '{texto}'")
            
            print("\n--- 1. PARSER FORMAL ---")
            analizar_oracion(texto)
            
            print("\n--- 2. SPACY (NLP MODERNO) ---")
            analizar_con_spacy(texto)
            
            print("-" * 60)

            # 3. Preguntar si desea continuar (AQUÍ ESTÁ EL CAMBIO)
            opcion = input("\n¿Deseas analizar otra oración? (S/N): ").lower().strip()
            
            if opcion in ['n', 'no', 'salir', 'exit']:
                print("\n¡Gracias por usar el comparador! Cerrando...")
                break
            # Si escribe 's' o cualquier otra cosa, el bucle se repite
            
        except KeyboardInterrupt:
            print("\nInterrupción detectada. Saliendo...")
            break


if __name__ == "__main__":
    print("\n" + "="*70)
    print(" COMPARACIÓN: PARSER FORMAL vs NLP MODERNO UTILIZANDO SPACY ")
    print("="*70)
    print("1. Ejecutar demostración automática (Original)")
    print("2. Probar oraciones manualmente (Modo Interactivo)")
    
    opcion = input("\nElige una opción (1 o 2): ").strip()
    
    if opcion == "2":
        modo_interactivo()
    else:
        # Ejecutar la lógica original
        oraciones_prueba = [
            "el gato come un libro",
            "la niña pequeña lee el libro grande",
            "un estudiante estudia la computadora",
            "gato come libro",
            "El hermoso gato negro duerme plácidamente",
        ]
        
        resultados = comparacion_completa(oraciones_prueba)
        casos_limite()
        analisis_estadistico()
        
        print("\n\n" + "="*60)
        print("RESUMEN DE RESULTADOS")
        print("="*60)
        print(f"\nParser Formal:")
        print(f"  • Oraciones válidas: {resultados['parser_formal']['exitosas']}")
        print(f"  • Oraciones inválidas: {resultados['parser_formal']['fallidas']}")
        print(f"\nSpaCy (NLP Moderno):")
        print(f"  • Oraciones procesadas: {resultados['spacy']['procesadas']}")
        print(f"  • Tasa de éxito: 100% (procesa cualquier entrada)")
        
        print("\n" + "="*60)
        print("CONCLUSIONES")
        print("="*60)
        print("""
1. PRECISIÓN vs ROBUSTEZ:
   - Parser formal: Alta precisión en gramática definida, pero frágil
   - spaCy: Robusto ante variaciones, maneja casos no previstos

2. VOCABULARIO:
   - Parser formal: Limitado a vocabulario predefinido
   - spaCy: Vocabulario extenso, maneja palabras desconocidas

3. COMPLEJIDAD SINTÁCTICA:
   - Parser formal: Solo estructura Sujeto-Verbo-Objeto simple
   - spaCy: Maneja estructuras complejas, subordinadas, pasivas
        """)