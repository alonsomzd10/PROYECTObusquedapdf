import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, FuenteWeb, Documento
import Levenshtein

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_desarrollo'  # Requerido para usar alertas flash

# Configuración de la base de datos SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    os.makedirs('downloads', exist_ok=True)
    os.makedirs('markdown', exist_ok=True)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    """Página inicial (Home) con las estadísticas clave para Hiram."""
    total_docs = Documento.query.count()
    
    todos_los_docs = Documento.query.all()
    total_palabras = 0
    for doc in todos_los_docs:
        if doc.contenido_texto:
            total_palabras += len(doc.contenido_texto.split())
            
    conteo_por_anio = {}
    for doc in todos_los_docs:
        conteo_por_anio[doc.anio] = conteo_por_anio.get(doc.anio, 0) + 1
        
    return render_template('home.html', total_docs=total_docs, total_palabras=total_palabras, conteo_por_anio=conteo_por_anio)

@app.route('/scrapper')
def scrapper():
    """Muestra a Alan la lista de direcciones web configuradas y sus archivos."""
    fuentes = FuenteWeb.query.all()
    return render_template('scrapper.html', fuentes=fuentes)

@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    """Permite añadir nuevas URLs a la lista de escrapeo."""
    if request.method == 'POST':
        url_ingresada = request.form.get('url_fuente', '').strip()
        if url_ingresada:
            # Evitar duplicados en la base de datos
            existe = FuenteWeb.query.filter_by(url=url_ingresada).first()
            if not existe:
                nueva_fuente = FuenteWeb(url=url_ingresada)
                db.session.add(nueva_fuente)
                db.session.commit()
            return redirect(url_for('configuration'))
            
    fuentes = FuenteWeb.query.all()
    return render_template('config.html', fuentes=fuentes)

@app.route('/search')
def search():
    """Lógica de búsqueda con Levenshtein y filtro por slider."""
    texto_buscado = request.args.get('q', '').strip()
    umbral_slider = float(request.args.get('umbral', 0.5))  # Por defecto 0.5 (medio)
    
    resultados_encontrados = []
    
    if texto_buscado:
        documentos = Documento.query.all()
        texto_buscado_lower = texto_buscado.lower()
        
        for doc in documentos:
            if not doc.contenido_texto:
                continue
                
            content = doc.contenido_texto
            chunk_length = 100  # Longitud de bloques de texto para evaluar similitud
            
            for i in range(0, len(content), chunk_length):
                bloque_texto = content[i:i+chunk_length]
                bloque_lower = bloque_texto.lower()
                
                # Calcular ratio de Levenshtein (0.0 a 1.0)
                similitud_ratio = Levenshtein.ratio(bloque_lower, texto_buscado_lower)
                
                if similitud_ratio >= umbral_slider:
                    resultados_encontrados.append({
                        'url_original': doc.url_original_pdf,
                        'bloque_encontrado': bloque_texto,
                        'porcentaje_similitud': round(similitud_ratio * 100, 3)  # Requerido hasta 3 dígitos
                    })
                    
    return render_template('search.html', 
                           texto_buscado=texto_buscado, 
                           resultados=resultados_encontrados, 
                           umbral_actual=umbral_slider)

def registrar_documento_scrappeado(nombre, url_pdf, ruta_pdf, ruta_md, texto, anio, fuente_url):
    """Función de utilidad para que el scrapper registre PDFs en la BD."""
    fuente = FuenteWeb.query.filter_by(url=fuente_url).first()
    if not fuente:
        fuente = FuenteWeb(url=fuente_url, status="Escrapeada")
        db.session.add(fuente)

    fuente.status = "Escrapeada"

    nuevo_doc = Documento(
        nombre_archivo=nombre,
        url_original_pdf=url_pdf,
        ruta_local_pdf=ruta_pdf,
        ruta_local_markdown=ruta_md,
        contenido_texto=texto,
        anio=anio,
        fuente=fuente
    )
    db.session.add(nuevo_doc)
    db.session.commit()

@app.route('/seed-demo')
def seed_demo():
    """Ruta temporal para rellenar la base de datos con datos de prueba."""
    # Limpiar datos anteriores para pruebas limpias
    Documento.query.delete()
    FuenteWeb.query.delete()
    
    fuente = FuenteWeb(url="https://fi-ing.unison.mx/acuerdos-2026", status="Escrapeada")
    db.session.add(fuente)
    db.session.commit()
    
    doc1 = Documento(
        nombre_archivo="acuerdo_enero_2026.pdf",
        url_original_pdf="https://fi-ing.unison.mx/acuerdos-2026/enero.pdf",
        ruta_local_pdf="downloads/enero.pdf",
        ruta_local_markdown="markdown/enero.md",
        contenido_texto="En la Universidad de Sonora se acordó el presupuesto de ingeniería para el año dos mil veintiséis.",
        anio=2026,
        fuente_id=fuente.id
    )
    
    doc2 = Documento(
        nombre_archivo="minuta_octubre_2025.pdf",
        url_original_pdf="https://fi-ing.unison.mx/acuerdos-2025/octubre.pdf",
        ruta_local_pdf="downloads/octubre.pdf",
        ruta_local_markdown="markdown/octubre.md",
        contenido_texto="Reunión del consejo divisional sobre planes de estudio académicos del año dos mil veinticinco.",
        anio=2025,
        fuente_id=fuente.id
    )
    
    db.session.add_all([doc1, doc2])
    db.session.commit()
    return "¡Base de datos poblada con éxito! Ve al Home o a /search para probar."

if __name__ == '__main__':
    app.run(debug=True)