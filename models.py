from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FuenteWeb(db.Model):
    """Representa las URLs base que se configuran para escrapear."""
    __tablename__ = 'fuentes_web'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    status = db.Column(db.String(50), default="No escrapeada")
    
    documentos = db.relationship('Documento', backref='fuente', lazy=True)

class Documento(db.Model):
    """Representa cada archivo PDF descargado, procesado e indexado."""
    __tablename__ = 'documentos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    url_original_pdf = db.Column(db.String(500), nullable=False)
    ruta_local_pdf = db.Column(db.String(255), nullable=False)
    ruta_local_markdown = db.Column(db.String(255), nullable=False)
    contenido_texto = db.Column(db.Text, nullable=True)
    anio = db.Column(db.Integer, nullable=False)
    
    fuente_id = db.Column(db.Integer, db.ForeignKey('fuentes_web.id'), nullable=False)