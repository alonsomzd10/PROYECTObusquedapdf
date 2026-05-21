from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FuenteWeb(db.Model):
    """Representa las URLs base que se configuran para escrapear."""
    __tablename__ = 'fuente_web'  # Simplificado para evitar errores de enlace

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    status = db.Column(db.String(50), default="No escrapeada")

    # Esta relación apunta a la clase 'Documento' y crea el backref 'fuente'
    documentos = db.relationship('Documento', backref='fuente', lazy=True)

class Documento(db.Model):
    """Representa cada archivo PDF descargado, procesado e indexado."""
    __tablename__ = 'documento'  # Simplificado

    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    url_original_pdf = db.Column(db.String(500), nullable=False)
    ruta_local_pdf = db.Column(db.String(255), nullable=False)
    ruta_local_markdown = db.Column(db.String(255), nullable=False)
    contenido_texto = db.Column(db.Text, nullable=True)
    anio = db.Column(db.Integer, nullable=False)

    # Clave foránea apuntando exactamente a 'fuente_web.id'
    fuente_id = db.Column(db.Integer, db.ForeignKey('fuente_web.id'), nullable=False)