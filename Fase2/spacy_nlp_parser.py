import spacy

# Cargar modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("Instalando modelo de español...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])
    nlp = spacy.load("es_core_news_sm")

class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def analizar_spacy(texto):
    doc = nlp(texto)
    
    # Análisis morfológico
    print(f"\n{Color.CYAN}{Color.BOLD}Análisis morfológico (POS tagging):{Color.ENDC}")
    for token in doc:
        print(f"  {token.text:15} → {token.pos_:10} ({token.tag_})")
    
    # Análisis sintáctico (dependencias)
    print(f"\n{Color.CYAN}{Color.BOLD}Arbol de dependencias:{Color.ENDC}")
    for token in doc:
        print(f"  {token.text:15} ← {token.dep_:10} ← {token.head.text}")
    
    # Entidades nombradas
    if doc.ents:
        print(f"\n{Color.CYAN}{Color.BOLD}Entidades nombradas:{Color.ENDC}")
        for ent in doc.ents:
            print(f"  {ent.text} → {ent.label_}")
    
    print(f"\n{Color.CYAN}{Color.BOLD}Análisis estadístico y recuento:{Color.ENDC}")
    print(f"  {Color.GREEN}- Número de tokens: {Color.ENDC}{len(doc)}")
    print(f"  {Color.GREEN}- Número de palabras: {Color.ENDC}{len([t for t in doc if not t.is_punct])}")
    print(f"  {Color.GREEN}- Recuento de categorías gramaticales:{Color.ENDC}")
    pos_counts = {}
    for token in doc:
        pos_counts[token.pos_] = pos_counts.get(token.pos_, 0) + 1
    for pos, count in pos_counts.items():
        print(f"    - {pos}: {count}")
    
    return doc


if __name__ == "__main__":

    oraciones_prueba = [
        "la niña vende la nueva computadora",
        "el inteligente estudiante estudia un viejo libro",
        "el perro mira el rápido gato",
        # Errores en el parser normal
        "gato come libro",  # Falta artículos
        "el humano lee libro",  # Humano no está en la gramática original
        "Los gato un come coche",  # Errores de concordancia
        "veo al hombre con el telescopio" # Ambiguedad
    ]
    
    for oracion in oraciones_prueba:
        print(f"\n{'='*60}")
        print(f"{Color.BLUE}{Color.BOLD}SpaCy - Analizando cadena: {Color.ENDC}'{oracion}'")
        resultados = analizar_spacy(oracion)