import sys
import shlex
import spacy
from typing import List, Optional

class NLPDemo:
    """
    Encapsula la aplicación de demostración de NLP, gestionando el estado
    (modelo spaCy cargado, modo de salida) de forma segura.
    """
    
    # --- Constantes de Clase ---
    # Se definen a nivel de clase, son compartidas por todas las instancias.
    BANNER = r'''
NLP Demo (spaCy) - REPL interactivo
Comandos:
  :q                salir
  :h                ayuda (este mensaje)
  :brief on|off     alterna salida breve (solo entidades y noun chunks)

Modelos (Small - rápidos, menos precisos):
  :model es         modelo Español (es_core_news_sm)
  :model en         modelo Inglés (en_core_web_sm)

Modelos (Medium - más lentos, más precisos):
  :model es_md      modelo Español (es_core_news_md)
  :model en_md      modelo Inglés (en_core_web_md)
'''

    MODELS = {
        "es": "es_core_news_sm",
        "en": "en_core_web_sm",
        "es_md": "es_core_news_md",
        "en_md": "en_core_web_md"
    }

    CODE_HINTS = {
        'int', 'bool', 'cout', 'cin', 'if', 'else', 'while', 'for', 
        '==', '&&', '||', ';', '{', '}', '(', ')', '->', '::',
        'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'JOIN',
        'def', 'class', 'import', 'elif', 'print'
    }

    # --- Métodos de Instancia ---
    
    def __init__(self):
        """
        Constructor: Inicializa el estado de la instancia.
        No se carga ningún modelo aquí; se cargará en run_app.
        """
        # El estado ahora está "encapsulado" y protegido dentro de 'self'
        # 'Optional[spacy.Language]' es type hinting: "puede ser None o un objeto nlp de spaCy"
        self.nlp: Optional[spacy.Language] = None
        self.model_name: Optional[str] = None
        self.brief_output: bool = False

    def _load_spacy_model(self, model_key: str) -> bool:
        """
        Intenta cargar un modelo de spaCy por su clave ('es', 'es_md', etc.).
        Actualiza el estado de la instancia (self.nlp) si tiene éxito.
        Devuelve True si se cargó, False si falló.
        """
        model_to_load = self.MODELS.get(model_key)
        if not model_to_load:
            print(f"Error: Clave de modelo '{model_key}' no válida.")
            print(f"Usa una de las claves definidas en :h (ej: :model es_md)")
            return False

        print(f"\nCargando modelo '{model_to_load}'... (puede tardar si es grande)")
        try:
            # Actualiza el estado de la instancia
            self.nlp = spacy.load(model_to_load)
            self.model_name = model_to_load
            print(f"[OK] Modelo cargado: {self.model_name}")
            return True
        except (IOError, OSError) as e:
            print(f"\n--- ERROR AL CARGAR MODELO (¿Instalado?) ---")
            print(f"Error: No se pudo cargar el modelo '{model_to_load}'.")
            print(f"  Asegúrate de tenerlo instalado:")
            print(f"  python -m spacy download {model_to_load}")
            print(f"Detalle: {e}")
            print("------------------------------------------\n")
            return False
        # Captura para cualquier otro error inesperado
        except Exception as e:
            print(f"\n--- ERROR INESPERADO ---")
            print(f"Detalle: {e}")
            print("--------------------------\n")
            return False

    def _looks_like_code(self, text: str) -> bool:
        """Heurística simple para detectar si el texto parece código."""
        words = set(text.split())
        for hint in self.CODE_HINTS:
            if hint in text: 
                return True
            if hint in words: 
                return True
        return False

    def analyze_text(self, text: str):
        """
        Analiza un texto dado usando el modelo NLP cargado en la instancia.
        """
        if not self.nlp:
            print("[Error] No hay un modelo spaCy cargado.")
            return

        doc = self.nlp(text)
        print(f"\n== spaCy (modelo: {self.model_name}) ==")
        print(f"Entrada: {text}\n")

        # 1. Tokens (usa el estado self.brief_output)
        if not self.brief_output:
            print("1) Tokens (texto | lemma | POS | dep | cabeza)")
            for t in doc:
                print(f" - {t.text:15} | {t.lemma_:15} | {t.pos_:6} | {t.dep_:12} | {t.head.text}")

        print("\n2) Frases nominales (noun chunks):")
        chunks = list(doc.noun_chunks) if hasattr(doc, 'noun_chunks') else []
        if chunks:
            for ch in chunks:
                print(f" - {ch.text}")
        else:
            print(" - (no detectadas)")

        print("\n3) Entidades nombradas (texto | etiqueta):")
        if doc.ents:
            for ent in doc.ents:
                print(f" - {ent.text:25} | {ent.label_}")
        else:
            print(" - (no se encontraron entidades)")

        print("\n4) Observaciones (Heurística):")
        # Llama al método de la instancia
        if self._looks_like_code(text):
            print(" - PARECE CÓDIGO FORMAL: spaCy no está diseñado para esto.")
            print("   El análisis de NLP (POS/dep) probablemente sea incorrecto.")
            print("   Un parser descendente formal SÍ entendería esta estructura.")
        else:
            print(" - PARECE LELENGUAJE NATURAL: spaCy está diseñado para esto.")
            print("   El análisis de NLP (POS/dep/NER) debería ser útil.")
            print("   Un parser formal (ej: C++) fallaría instantáneamente con esta entrada.")

    def run_repl(self):
        """
        Ejecuta el bucle interactivo (REPL).
        Asume que un modelo ya fue cargado por run_app.
        """
        print(self.BANNER)
        print(f"[OK] Modelo inicial cargado: {self.model_name}")

        while True:
            try:
                line = input("\nnlp> ")
            except (EOFError, KeyboardInterrupt):
                print("\nSaliendo...")
                break

            if not line.strip():
                continue

            # --- Manejo de Comandos ---
            if line.strip() in (":q", ":quit", ":exit"):
                break
            elif line.strip() in (":h", ":help"):
                print(self.BANNER)
            elif line.startswith(":model"):
                parts = shlex.split(line)
                if len(parts) == 2:
                    self._load_spacy_model(parts[1])
                     # Llama al método de la instancia
                else:
                    print("Uso: :model [clave_modelo] (ej: :model es_md)")
            elif line.startswith(":brief"):
                parts = shlex.split(line)
                if len(parts) == 2 and parts[1] in ("on", "off"):
                    self.brief_output = (parts[1] == "on")
                     # Actualiza el estado de la instancia
                    print(f"[OK] brief = {self.brief_output}")
                else:
                    print("Uso: :brief on | :brief off")
            else:
                # --- Análisis de Texto ---
                try:
                    self.analyze_text(line)
                except Exception as e:
                    print(f"[Error inesperado] {e}")

    def run_app(self, argv: List[str]):
        """
        Lógica principal de la aplicación: carga modelos y decide
        si correr el REPL o un análisis único.
        """
        # 1. Cargar modelo inicial
        if not self._load_spacy_model("es"):
            if not self._load_spacy_model("en"):
                print("\nError fatal: No se pudo cargar ningún modelo. Saliendo.")
                print("Instala un modelo para continuar, ej:")
                print("  python -m spacy download es_core_news_sm")
                return # Termina la ejecución

        # 2. Decidir modo de operación
        if len(argv) >= 2 and argv[1] == "--repl":
            self.run_repl()
        elif len(argv) >= 2:
            text_to_analyze = " ".join(argv[1:])
            self.analyze_text(text_to_analyze)
        else:
            print(self.BANNER)
            print("\nPara iniciar, ejecuta: python nlp_demo_spacy.py --repl")

# --- Punto de entrada del script ---

def main(argv: List[str]):
    """
    Función principal: crea la instancia de la aplicación
    y ejecuta su lógica principal.
    """
    app = NLPDemo()
    app.run_app(argv)

if __name__ == "__main__":
    # sys.argv es la lista de argumentos de la línea de comandos
    main(sys.argv)