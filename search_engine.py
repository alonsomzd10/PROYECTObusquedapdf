import Levenshtein

def ejecutar_busqueda_difusa(palabra_buscada, lista_documentos_bd, valor_slider=0.0):
    resultados_finales = []
    
    for doc in lista_documentos_bd:
        texto_doc = doc.get('texto', '')
        
        porcentaje_similitud = Levenshtein.ratio(palabra_buscada.lower(), texto_doc.lower())
        
        if porcentaje_similitud >= valor_slider:
            resultados_finales.append({
                "url": doc.get('url', 'Sin URL'),
                "bloque": texto_doc[:350] + "...", 
                "porcentaje": round(porcentaje_similitud * 100, 3) 
            })
            
    return sorted(resultados_finales, key=lambda x: x['porcentaje'], reverse=True)