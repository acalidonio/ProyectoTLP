import sys

try:
    from spanish_parser import analizar_oracion
    from spacy_nlp_parser import analizar_spacy
except ImportError as e:
    print(f"Error: No se encontraron los archivos necesarios ({e}).")
    print("Asegúrate de ejecutar este script en la carpeta Fase2 junto con spanish_parser.py y spacy_nlp_parser.py")
    sys.exit(1)

class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_separator(title):
    print("\n" + "="*80)
    print(f"{Color.HEADER}{Color.BOLD} {title} {Color.ENDC}")
    print("="*80)

def run_comparison():
    # Lista de cadenas de prueba estratégicas
    test_cases = [
        "la niña vende la nueva computadora",
        "el inteligente estudiante estudia un viejo libro",
        "el perro mira el rápido gato",
        # Errores en el parser normal
        "gato come libro",  # Falta artículos
        "el humano lee libro",  # Humano no está en la gramática original
        "Los gato un come coche",  # Errores de concordancia
        "veo al hombre con el telescopio" # Ambiguedad
    ]

    print_separator("COMPARACIÓN EN TIEMPO REAL: PARSER FORMAL vs NLP (spaCy)")
    
    input(f"{Color.WARNING}\nPresiona ENTER para iniciar las pruebas...{Color.ENDC}")

    for i, sentence in enumerate(test_cases, 1):
        print(f"\n\n{Color.CYAN}{'='*60}{Color.ENDC}")
        print(f"{Color.CYAN} PRUEBA #{i}: {Color.ENDC}\"{sentence}\"")
        print(f"{Color.CYAN}{'='*60}{Color.ENDC}\n")

        # Analisis con Parser Formal
        print(f"{Color.BLUE}{Color.BOLD}PARSER FORMAL (spanish_parser.py){Color.ENDC}")
        try:
            analizar_oracion(sentence)
        except Exception as e:
            print(f"{Color.FAIL}Error en Parser Formal: {e}{Color.ENDC}")
            
        print("\n" + "-"*40 + "\n")

        # Analisis con SpaCy NLP
        print(f"{Color.BLUE}{Color.BOLD}PARSER NLP (spacy_nlp_parser.py){Color.ENDC}")
        try:
            analizar_spacy(sentence)
        except Exception as e:
            print(f"{Color.FAIL}Error en Parser NLP: {e}{Color.ENDC}")

        # Pausa entre pruebas para poder leer
        if i < len(test_cases):
            input(f"\n{Color.WARNING}Presiona ENTER para continuar...{Color.ENDC}")

if __name__ == "__main__":
    run_comparison()