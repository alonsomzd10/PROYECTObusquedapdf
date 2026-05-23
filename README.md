# Sistema de Búsqueda de PDFs — Flask & Levenshtein

## Introducción
El **Sistema de Búsqueda de PDFs** es una aplicación web que desarrollamos en Python con el framework Flask. Su objetivo es automatizar la indexación, procesamiento y búsqueda inteligente de documentos oficiales en formato PDF 

El sistema integra un rastreador web automático Web Scraper que localiza y descarga archivos PDF desde enlaces semilla configurados, procesa su contenido textual  y almacena la información de forma estructurada en una base de datos relacional. Finalmente, ofrece una interfaz de usuario limpia e interactiva para realizar búsquedas difusas basadas en el algoritmo de **similitud de Levenshtein**, permitiendo encontrar términos exactos o aproximados de manera eficiente.

---

## Integrantes del Equipo
* **Diego Alonso Canales Meza** — Backend, Modelos de Datos y Base de Datos
* **Hiram** — Frontend, Diseño de Interfaz y Bootstrap
* **Alan** — Web Scraper, Extracción de Texto y Procesamiento OCR

## Cómo ejecutar el proyecto de forma local
1. Clonar el repositorio.
2. Activar el entorno virtual: `venv\Scripts\activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar el servidor: `python app.py`
