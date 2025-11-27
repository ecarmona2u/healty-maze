# traduccion.py

from pathlib import Path 

# ----------------------------------------------------------------
# CONFIGURACIÓN Y LÓGICA CENTRAL DE TRADUCCIÓN POR RECURSOS GRÁFICOS
# ----------------------------------------------------------------

# 📢 RUTA BASE: AJUSTA ESTO a "recursos/assets_traducidos" si esa es tu carpeta.
# Lo dejo como "recursos" por defecto.
RUTA_BASE_ASSETS = "recursos" 

# Idioma predeterminado
_idioma_actual = "es"

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
    # 🚨 USO DE PATHLIB: Construye la ruta de forma segura y retorna como string
    ruta_path = Path(RUTA_BASE_ASSETS) / idioma / nombre_archivo
    return str(ruta_path)