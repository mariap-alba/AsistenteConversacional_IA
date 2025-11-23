# Asistente Conversacional RAG sobre “Guía de implementación de TailwindCSS”
Asistente conversacional IA capaz de responder preguntas basadas en información contenida en un documento, usando técnicas modernas.

---

## Documento Seleccionado

**Título:** *Guía de implementación de Tailwindcss en proyecto Web*   
**Tipo:** Documentación técnica framework de CSS  
**Formato:** PDF  

### ¿Por qué elegí este documento?

Elegí este documento porque:

- Es una **guía técnica**, clara y estructurada.
- Contiene definiciones, pasos, comandos y configuraciones relacionadas con TailwindCSS.

### ¿Qué tipo de prguntas pude responder?

El asistente puede responder preguntas sobre:

- **Definiciones básicas, por ejemplo:** qué es Tailwindcss y qué ventajas ofrece frente a los estilos por defecto del navegador.
- **Contextos de implementación de Tailwindcss:** CDN, entornos de desarrollo y uso por línea de comandos (CLI)
- **Los pasos para implementar Tailwindcss incluyendo:**
    - Estructura recomendada de carpetas (public y src) y ubicación del HTML y del CSS de entrada
    - Contenido mínimo del archivo styles.css con las directivas @tailwind base, @tailwind components y @tailwind utilities.
    - Creación y configuración básica de tailwind.config.js, especialmente la propiedad content y las rutas que se deben incluir.

### ¿Qué retos tiene el texto?

El documento presenta algunos retos desde la perspectiva de un sistema RAG:

- **Ruido de maquetación:** incluye portada, números de página y un índice que se repite al inicio, lo cual genera líneas como “2”, “3”, “4” o títulos aislados que no aportan contenido semántico pero sí aparecen en el texto extraído.

- **Saltos de línea y fragmentación:** el documento tiene muchos saltos de línea dentro de los párrafos (propios del formato PDF), lo que puede cortar frases a la mitad y afectar el chunking si no se hace una limpieza previa (unión de líneas y normalización de espacios).

- **Referencias externas:** la guía incluye URLs a la documentación oficial de Tailwindcss (por ejemplo, para el CDN y los frameworks), pero el contenido de esas páginas no forma parte del corpus, por lo que el asistente solo puede mencionar que existen esos enlaces, no explicar su contenido en detalle.

- **Imágenes no leíbles:** algunas partes (como ejemplos en consola o posibles capturas de pantalla) están embebidas como imágenes en el PDF. El proceso de extracción de texto no recupera esa información visual, por lo que el asistente no puede aprovecharla directamente.

- **Cobertura limitada del tema:** aunque la guía explica bien la instalación por CLI y la estructura básica del proyecto, no describe todas las características de Tailwindcss (clases utilitarias, responsive design avanzado, plugins, etc.). Esto implica que el asistente solo puede responder preguntas dentro del alcance concreto de la guía y no sobre todo el ecosistema de Tailwindcss.