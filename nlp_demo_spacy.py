import sys        # Módulo para acceder a parámetros del sistema, como sys.argv
import shlex      # Módulo para parsear cadenas de texto complejas (como comandos con espacios)
import spacy      # La librería principal de NLP que estamos utilizando

# Definición de la clase NLPDemo que encapsula toda la lógica de la aplicación
class NLPDemo:
    # --- Constantes de Clase ---
    # Banner de bienvenida y ayuda que se muestra al iniciar el REPL o sin argumentos.
    BANNER = r'''
NLP Demo (spaCy) - REPL interactivo
Comandos:
  :q                salir
  :h                ayuda (este mensaje)
  :model es         cambiar a modelo español (es_core_news_sm)
  :model en         cambiar a modelo inglés (en_core_web_sm)
  :brief on|off     alterna salida breve (solo entidades y noun chunks)

Uso:
  Ejecuta: python nlp_demo_spacy.py --repl
  Escribe texto en lenguaje natural o código C/C++-like y presiona Enter.
  Ejemplos:
    nlp> Juan come manzanas en San Salvador.
    nlp> int x = 5 + y;

Notas:
  Si no tienes modelos instalados:
    pip install spacy
    python -m spacy download es_core_news_sm
    (opcional) python -m spacy download en_core_web_sm
'''
    # Diccionario que mapea códigos de idioma a los nombres de los modelos spaCy.
    MODELS = {
        "es": "es_core_news_sm",
        "en": "en_core_web_sm"
    }
    # Conjunto de palabras clave para una heurística rápida para detectar si el texto parece código.
    CODE_HINTS = {'int', 'bool', 'cout', 'cin', 'if', 'else', 'while', 'for', '==', '&&', '||', ';', '{', '}', '(', ')'}

    # --- Método Constructor ---
    # Se ejecuta al crear una nueva instancia de NLPDemo.
    def __init__(self, prefer_es=True):
        self.nlp = None             # Objeto principal de spaCy (el pipeline de procesamiento), inicialmente None.
        self.model_name = None      # Nombre del modelo spaCy cargado, inicialmente None.
        self.brief_output = False   # Bandera para controlar la salida breve en el análisis, inicialmente False.
        self.prefer_es = prefer_es  # Bandera para indicar la preferencia inicial de idioma (español), True por defecto.
        self._load_spacy_model()    # Llama al método para cargar el modelo spaCy al inicializar la clase.

    # --- Métodos Privados (Auxiliares) ---

    # Método para cargar los modelos de spaCy.
    def _load_spacy_model(self):
        # Determina el orden en que se intentarán cargar los modelos, basado en 'prefer_es'.
        # Si prefer_es es True, intenta español, luego inglés. Si es False, intenta inglés, luego español.
        model_order = ["es", "en"] if self.prefer_es else ["en", "es"]
        
        last_error = None # Variable para guardar el último error si falla la carga.

        # Itera a través del orden de modelos definido.
        for lang_code in model_order:
            model_to_load = self.MODELS[lang_code] # Obtiene el nombre completo del modelo del diccionario MODELS.
            try:
                self.nlp = spacy.load(model_to_load) # Intenta cargar el modelo de spaCy.
                self.model_name = model_to_load      # Si tiene éxito, guarda el nombre del modelo.
                return                               # Sale de la función, la carga fue exitosa.
            except Exception as e:
                last_error = e                       # Si falla, guarda el error y continúa con el siguiente modelo.
        
        # Si el bucle termina y ningún modelo se pudo cargar, lanza una excepción SystemExit.
        # Esto detiene la ejecución del programa con un mensaje informativo.
        raise SystemExit(
            "No se encontraron modelos spaCy.\n"
            "Instala:\n"
            "  pip install spacy\n"
            "  python -m spacy download es_core_news_sm\n"
            "  (opcional) python -m spacy download en_core_web_sm\n"
            f"Detalle: {last_error}" # Muestra el último error ocurrido.
        )

    # Método heurístico para determinar si un texto parece código.
    def _looks_like_code(self, text):
        # Comprueba si alguna de las palabras clave en CODE_HINTS está presente en el texto.
        # 'any()' devuelve True si al menos una es encontrada.
        return any(h in text for h in self.CODE_HINTS)

    # --- Métodos Públicos ---

    # Realiza el análisis NLP de un texto dado.
    def analyze_text(self, text):
        if not self.nlp: # Verifica si se ha cargado un modelo NLP.
            print("[Error] No hay un modelo spaCy cargado.")
            return       # Si no hay modelo, no se puede analizar, así que sale.

        doc = self.nlp(text) # Procesa el texto con el pipeline de spaCy para crear un objeto 'Doc'.
        print(f"== spaCy (modelo: {self.model_name}) ==") # Imprime el encabezado con el modelo actual.
        print(f"Entrada: {text}\n") # Muestra el texto de entrada.

        # Si la salida breve no está activada, muestra el análisis detallado de los tokens.
        if not self.brief_output:
            print("1) Tokens (texto | lemma | POS | dep | cabeza)")
            for t in doc: # Itera sobre cada token en el objeto Doc.
                # Imprime el texto del token, su lema, su parte de la oración (POS),
                # su dependencia sintáctica (dep) y el texto de su "cabeza" (el token del que depende).
                print(f" - {t.text:15} | {t.lemma_:15} | {t.pos_:6} | {t.dep_:12} | {t.head.text}")

        print("\n2) Frases nominales (noun chunks):")
        # Intenta obtener los 'noun chunks' (frases nominales). Si 'noun_chunks' no existe (poco probable con modelos estándar),
        # devuelve una lista vacía para evitar errores.
        chunks = list(doc.noun_chunks) if hasattr(doc, 'noun_chunks') else []
        if chunks: # Si se encontraron frases nominales.
            for ch in chunks: # Itera y las imprime.
                print(f" - {ch.text}")
        else:
            print(" - (no detectadas)") # Si no se encontraron.

        print("\n3) Entidades nombradas (texto | etiqueta):")
        if doc.ents: # Si se encontraron entidades nombradas (personas, lugares, organizaciones, etc.).
            for ent in doc.ents: # Itera y las imprime.
                # Imprime el texto de la entidad y su etiqueta (tipo de entidad).
                print(f" - {ent.text:25} | {ent.label_}")
        else:
            print(" - (no se encontraron entidades)") # Si no se encontraron.

        print("\n4) Observaciones:")
        # Utiliza la heurística para determinar si el texto parece código.
        if self._looks_like_code(text):
            print(" - Parece código C/C++-like: NLP no está diseñado para extraer AST de código;")
            print("   tu parser descendente sí estructura este tipo de entrada.")
        else:
            print(" - Parece lenguaje natural: NLP aporta POS/dep/chunks/NER útiles;")
            print("   en cambio, el parser formal de C++ fallaría con estas frases.")

    # Ejecuta el bucle REPL (Read-Eval-Print Loop) interactivo.
    def run_repl(self):
        print(self.BANNER) # Muestra el banner al inicio del REPL.
        print(f"[OK] Modelo cargado: {self.model_name}") # Confirma el modelo cargado.

        while True: # Bucle infinito para el REPL.
            try:
                line = input("nlp> ") # Solicita entrada al usuario.
            except (EOFError, KeyboardInterrupt): # Captura Ctrl+D (EOF) o Ctrl+C (KeyboardInterrupt).
                print("\nSaliendo...") # Mensaje de salida.
                break # Sale del bucle REPL.

            if not line.strip(): # Si la línea está vacía o solo contiene espacios, la ignora y continúa.
                continue

            # --- Manejo de Comandos ---
            if line.strip() in (":q", ":quit", ":exit"): # Comando para salir.
                break # Sale del bucle REPL.
            elif line.strip() in (":h", ":help"): # Comando de ayuda.
                print(self.BANNER) # Muestra el banner de nuevo.
            elif line.startswith(":model"): # Comando para cambiar el modelo.
                parts = shlex.split(line) # Divide la línea en partes, manejando comillas.
                # Verifica que el comando tenga 2 partes y que el idioma sea válido.
                if len(parts) == 2 and parts[1] in self.MODELS:
                    self.prefer_es = (parts[1] == "es") # Actualiza la preferencia de idioma.
                    try:
                        self._load_spacy_model() # Intenta cargar el nuevo modelo.
                        print(f"[OK] Modelo cargado: {self.model_name}") # Confirma la carga.
                    except SystemExit as e: # Si la carga falla, imprime el error y permite continuar el REPL.
                        print(e)
                else:
                    print("Uso: :model es | :model en") # Mensaje de uso incorrecto.
            elif line.startswith(":brief"): # Comando para alternar la salida breve.
                parts = shlex.split(line) # Divide la línea en partes.
                # Verifica que el comando tenga 2 partes y que la opción sea válida.
                if len(parts) == 2 and parts[1] in ("on", "off"):
                    self.brief_output = (parts[1] == "on") # Actualiza la bandera de salida breve.
                    print(f"[OK] brief = {self.brief_output}") # Confirma el estado.
                else:
                    print("Uso: :brief on | :brief off") # Mensaje de uso incorrecto.
            else: # Si no es un comando, se asume que es texto para analizar.
                try:
                    self.analyze_text(line) # Llama al método de análisis.
                except Exception as e: # Captura cualquier error durante el análisis del texto.
                    print(f"[Error] {e}") # Imprime el error.

# --- Función Principal ---

# Punto de entrada principal del script cuando se ejecuta directamente.
def main(argv):
    # Crea una instancia de NLPDemo. Por defecto, intentará cargar el modelo español primero.
    demo = NLPDemo(prefer_es=True) 
    
    # Comprueba si el primer argumento es '--repl'.
    if len(argv) >= 2 and argv[1] == "--repl":
        demo.run_repl() # Si es '--repl', ejecuta el modo interactivo.
    # Comprueba si hay al menos un argumento además del nombre del script (es decir, texto para analizar).
    elif len(argv) >= 2:
        # Une todos los argumentos desde el segundo en adelante para formar el texto completo.
        demo.analyze_text(" ".join(argv[1:])) # Analiza el texto directamente.
    else:
        # Si no se proporcionan argumentos específicos, muestra el banner con las instrucciones.
        print(demo.BANNER)

# Bloque estándar para asegurar que 'main()' se llama solo cuando el script se ejecuta directamente.
if __name__ == "__main__":
    main(sys.argv) # Pasa los argumentos de la línea de comandos a la función main.