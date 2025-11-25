import sys
import time
from parser import parse_string

class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print("\n" + "="*70)
    print(f"{Color.BLUE}{Color.BOLD} {text} {Color.ENDC}")
    print("="*70 + "\n")

def run_test_case(description, code_input):
    print(f"{Color.CYAN}Caso de Prueba:{Color.ENDC} {description}")
    print(f"{Color.CYAN}Entrada:{Color.ENDC}  \"{code_input}\"")
    
    try:
        # Ejecutamos el parser importado
        # Nota: parse_string maneja internamente el print de errores, 
        # pero aquí capturamos el resultado booleano/excepción
        parse_string(code_input)
        print(f"\rResultado: {Color.GREEN}{Color.BOLD}[ ACEPTADO ]{Color.ENDC} - Cumple la gramática estricta.")
    except Exception as e:
        print(f"\rResultado: {Color.FAIL}{Color.BOLD}[ RECHAZADO ]{Color.ENDC} - {e}")
    
    print("-" * 70 + "\n")
    input("Presiona ENTER para seguir.")

def main():
    print_header("COMPARACIÓN DE LENGUAJES FORMALES Y NATURALES EN PARSER LL(1)")
    print(f"{Color.CYAN}Gramática:{Color.ENDC} Declaración de variables tipo int/float.\n")
    
    input("Presiona ENTER para iniciar la demostración...")

    # --- ESCENARIO 1: El camino feliz ---
    print_header("ESCENARIO 1: CÓDIGO C VÁLIDO (Soportado)")
    
    run_test_case(
        "Declaración simple de entero", 
        "int x ; $"
    )
    
    run_test_case(
        "Declaración múltiple de flotantes", 
        "float precio, impuesto, total ; $"
    )

    # --- ESCENARIO 2: Código C válido pero no soportado ---
    # Esto es crucial para mostrar que el parser es RÍGIDO
    print_header("ESCENARIO 2: CÓDIGO C VÁLIDO (No Soportado)")
    
    run_test_case(
        "Asignación de valor (Gramática no lo contempla)", 
        "int contador = 10 ; $"
    )

    run_test_case(
        "Bucle (Gramática no lo contempla)", 
        "while (contador > 0) { contador++ ; } ; $"
    )

    # --- ESCENARIO 3: Lenguaje Natural ---
    print_header("ESCENARIO 3: LENGUAJE NATURAL (Ambigüedad)")
    
    run_test_case(
        "Frase en español simple", 
        "La variable x es un entero $"
    )
    
    run_test_case(
        "Intento de engañar al parser", 
        "int ento de asignar variable ; $"
    )

    print_header("RESUMEN FINAL")
    print(f"1. {Color.GREEN}LENGUAJE FORMAL:{Color.ENDC} Estructura rígida, sin ambigüedad -> {Color.GREEN}Funciona.{Color.ENDC}")
    print(f"2. {Color.FAIL}LENGUAJE NATURAL:{Color.ENDC} Estructura libre, mucha ambigüedad -> {Color.FAIL}Falla.{Color.ENDC}")

if __name__ == "__main__":
    main()