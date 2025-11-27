from pathlib import Path 

# ----------------------------------------------------------------
# CONFIGURACIÓN Y LÓGICA CENTRAL DE TRADUCCIÓN POR RECURSOS GRÁFICOS
# ----------------------------------------------------------------

# 📢 RUTA BASE: AJUSTA ESTO a "recursos/assets_traducidos" si esa es tu carpeta.
# Lo dejo como "recursos" por defecto.
RUTA_BASE_ASSETS = "recursos" 

# Idioma predeterminado
_idioma_actual = "es"

# --- DICCIONARIO DE TRADUCCIONES DE TEXTO ---
# Clave: Identificador del texto; Valor: Diccionario de traducciones por idioma.
TEXT_TRANSLATIONS = {
    # CLAVE PARA LOS CONTADORES DE COLECIONABLES (SOLICITADA)
    "ITEMS_COLLECTED": {
        "es": "Objetos",
        "in": "Objects" 
    },
    # Puedes añadir más claves de texto aquí (ej. "PAUSE_TITLE", "RESTART_BUTTON")
}

def obtener_idioma_actual():
    """Retorna el código del idioma activo ('es' o 'in')."""
    return _idioma_actual

def establecer_idioma(nuevo_idioma):
    """
    Establece el idioma global si es soportado.
    """
    global _idioma_actual
    
    if nuevo_idioma in ["es", "in"]:
        _idioma_actual = nuevo_idioma
        print(f"Idioma del juego establecido a: {_idioma_actual}")
        return True
    else:
        print(f"Error: Idioma '{nuevo_idioma}' no soportado.")
        return False

def obtener_ruta_imagen_traducida(nombre_archivo):
    """
    Construye la ruta completa al archivo de imagen traducido 
    basándose en el idioma actual, usando pathlib.
    
    Args:
        nombre_archivo (str): El nombre del archivo (e.g., "fondo_ajustes.png").
        
    Returns:
        str: La ruta completa (e.g., "recursos/es/fondo_ajustes.png").
    """
    idioma = obtener_idioma_actual()
    # USO DE PATHLIB: Construye la ruta de forma segura y retorna como string
    ruta_path = Path(RUTA_BASE_ASSETS) / idioma / nombre_archivo
    return str(ruta_path)

def obtener_texto_traducido(clave):
    """
    Retorna la cadena de texto traducida según el idioma activo.
    
    Args:
        clave (str): La clave de identificación del texto (ej. "ITEMS_COLLECTED").
        
    Returns:
        str: El texto traducido, o la clave si no se encuentra.
    """
    idioma = obtener_idioma_actual()
    
    # Busca la clave en el diccionario global
    if clave in TEXT_TRANSLATIONS:
        traducciones = TEXT_TRANSLATIONS[clave]
        
        # Retorna la traducción para el idioma actual, si existe.
        if idioma in traducciones:
            return traducciones[idioma]
        
        # Fallback a Español si el idioma existe pero la traducción falta.
        return traducciones.get("es", clave)
        
    return clave