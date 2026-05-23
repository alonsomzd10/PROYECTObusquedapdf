import os
import requests
from bs4 import BeautifulSoup
import pdfplumber
import pytesseract

def escanear_pagina_web(url_objetivo):
    """
    Busca todos los enlaces a archivos .pdf dentro de una URL dada.
    """
    enlaces_pdf = []
    try:
        respuesta = requests.get(url_objetivo, timeout=10)
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if href.endswith('.pdf'):
                    # Asegurar que la URL sea completa
                    if not href.startswith('http'):
                        href = os.path.join(url_objetivo, href)
                    enlaces_pdf.append(href)
    except Exception as e:
        print(f"Error al scrappear {url_objetivo}: {e}")
    return enlaces_pdf

def extraer_texto_pdf_u_ocr(pdf_path_o_url):
    """
    Descarga o abre un PDF, extrae su texto. Si viene vacío (render de imagen),
    aplica la técnica de OCR (Tesseract) página por página.
    """
    texto_total = ""
    
    # Si es una URL, debemos descargar el contenido temporalmente
    if pdf_path_o_url.startswith('http'):
        respuesta = requests.get(pdf_path_o_url)
        temp_pdf = "temporal_scraped.pdf"
        with open(temp_pdf, 'wb') as f:
            f.write(respuesta.content)
        ruta_archivo = temp_pdf
    else:
        ruta_archivo = pdf_path_o_url

    try:
        with pdfplumber.open(ruta_archivo) as pdf:
            for i, pagina in enumerate(pdf.pages):
                texto_pagina = pagina.extract_text()
                
                # Si el texto extraído es válido y no está vacío
                if texto_pagina and texto_pagina.strip():
                    texto_total += texto_pagina + "\n"
                else:
                    # EXTRA REQUERIDO: Si no hay texto nativo, es un render de imagen -> Aplicar OCR
                    print(f"Página {i+1} no contiene texto digital. Aplicando OCR...")
                    imagen_pagina = pagina.to_image(resolution=150).original
                    # Extraer texto usando Tesseract en español
                    texto_ocr = pytesseract.image_to_string(imagen_pagina, lang='spa')
                    texto_total += texto_ocr + "\n"
    except Exception as e:
        print(f"Error procesando el PDF: {e}")
    finally:
        # Limpiar el archivo temporal si se creó
        if pdf_path_o_url.startswith('http') and os.path.exists("temporal_scraped.pdf"):
            os.remove("temporal_scraped.pdf")
            
    return texto_total