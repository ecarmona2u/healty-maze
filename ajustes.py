# ajustes.py 
import pygame
import sys
from pathlib import Path 
# 🚨 Importa la INSTANCIA para acceder a sus métodos
from audio_manager import audio_manager 

# 📢 IMPORTAR LÓGICA DE TRADUCCIÓN
from traduccion import establecer_idioma, obtener_idioma_actual, obtener_ruta_imagen_traducida 

# --- CONSTANTES DE AJUSTES ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (50, 50, 200)
ROJO = (200, 50, 50)
VERDE = (50, 200, 50)
GRIS_BARRA = (100, 100, 100)
VERDE_BARRA = (0, 180, 0)
SLIDER_COLOR = (255, 255, 255)

# Dimensiones y posición de la ventana modal
MODAL_ANCHO, MODAL_ALTO = 600, 450
# Ruta base para el fondo de ajustes (la función de traducción añade el directorio /es/ o /in/)
PATH_FONDO_AJUSTES_BASE = "fondo_ajustes.png" 

# CONSTANTES DE AUDIO (🚨 RUTA CORREGIDA CON Path)
PATH_MUTE = str(Path("recursos") / "iconos" / "btn_mute.png")       
PATH_UNMUTE = str(Path("recursos") / "iconos" / "btn_unmute.png")   
MUTE_BTN_SIZE = 100 # Tamaño normal del botón Mute
SLIDER_HEIGHT = 15
SLIDER_WIDTH = 300

# 📢 RUTAS FIJAS PARA LOS BOTONES DE IDIOMA
PATH_BTN_ES = str(Path("recursos") / "es.png") 
PATH_BTN_IN = str(Path("recursos") / "in.png") 

# 🆕 CONSTANTE PARA EL BOTÓN DE CIERRE (Usando Path para asegurar compatibilidad)
PATH_BTN_CLOSE = str(Path("recursos") / "botones" / "btn_X.png") 
CLOSE_BTN_SIZE = 50 

# 📢 CONSTANTES DE DISEÑO GENERAL
LANG_BTN_WIDTH, LANG_BTN_HEIGHT = 100, 60
GROWTH_PX = 20 # Cuánto crece el botón al hacer hover o ser seleccionado


# 🚀 CONFIGURACIÓN DE POSICIÓN Y TAMAÑO DE ELEMENTOS (Relativo al modal_rect.topleft)

# --- SLIDER DE VOLUMEN y MUTE ---
# Posición X, Y del inicio de la barra del Slider
VOL_SLIDER_X = 150 
VOL_SLIDER_Y = 370 
VOL_SLIDER_POS = (VOL_SLIDER_X, VOL_SLIDER_Y) 

# Posición del botón Mute (calculado a la derecha del slider)
MUTE_BTN_X = 343
# MUTE_BTN_Y está centrado verticalmente con la barra del slider
MUTE_BTN_Y = 230
MUTE_BTN_POS = (MUTE_BTN_X, MUTE_BTN_Y)


# --- BOTONES DE IDIOMA ---
# X_center_modal = MODAL_ANCHO // 2 (300)
# Separación entre botones: 40px (20 a cada lado del centro)
# Posición Y de la fila de idioma
LANG_ROW_Y = 142

# Botón ESPAÑOL: X_center - Ancho - Sep_half 
ES_BTN_X = 285
ES_BTN_Y = LANG_ROW_Y
ES_BTN_CONFIG = {'x': ES_BTN_X, 'y': ES_BTN_Y, 'w': LANG_BTN_WIDTH, 'h': LANG_BTN_HEIGHT}

# Botón INGLÉS: X_center + Sep_half
IN_BTN_X = 420
IN_BTN_Y = LANG_ROW_Y
IN_BTN_CONFIG = {'x': IN_BTN_X, 'y': IN_BTN_Y, 'w': LANG_BTN_WIDTH, 'h': LANG_BTN_HEIGHT}


# --- BOTÓN DE CIERRE ---
# Usamos un padding desde el borde derecho y superior del modal
CLOSE_BTN_PADDING = 20 
CLOSE_BTN_CONFIG = {'size': CLOSE_BTN_SIZE, 'padding': CLOSE_BTN_PADDING}


# Inicialización de fuentes (Se mantienen por si se necesitan más adelante)
pygame.font.init()
font_opcion = pygame.font.Font(None, 40)
font_titulo = pygame.font.Font(None, 50)
font_label = pygame.font.Font(None, 30)


# --- CLASE VolumeSlider (Sin Cambios) ---

class VolumeSlider:
    def __init__(self, x, y, w, h, initial_volume):
        self.bar_rect = pygame.Rect(x, y, w, h)
        self.slider_rect = pygame.Rect(0, 0, h * 2, h * 2) 
        self.volume = initial_volume
        self.dragging = False
        self._update_slider_position(initial_volume)

    def _update_slider_position(self, volume):
        self.slider_rect.centerx = int(self.bar_rect.left + self.bar_rect.width * volume)
        self.slider_rect.centery = self.bar_rect.centery

    def handle_event(self, event, mouse_pos):
        if audio_manager.is_muted():
            return
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(mouse_pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                pos_x = mouse_pos[0]
                pos_x = max(self.bar_rect.left, min(self.bar_rect.right, pos_x))
                
                self.volume = (pos_x - self.bar_rect.left) / self.bar_rect.width
                audio_manager.set_volume(self.volume)
                self._update_slider_position(self.volume)

    def draw(self, surface):
        if not self.dragging:
            display_volume = 0.0 if audio_manager.is_muted() else audio_manager.get_current_volume()
            self.volume = display_volume 
            self._update_slider_position(display_volume)
        
        pygame.draw.rect(surface, GRIS_BARRA, self.bar_rect, border_radius=self.bar_rect.height // 2)
        
        current_width = int(self.bar_rect.width * self.volume)
        progress_rect = pygame.Rect(self.bar_rect.topleft, (current_width, self.bar_rect.height))
        pygame.draw.rect(surface, VERDE_BARRA, progress_rect, border_radius=self.bar_rect.height // 2)
        
        pygame.draw.circle(surface, SLIDER_COLOR, self.slider_rect.center, self.slider_rect.height // 2)
        pygame.draw.circle(surface, AZUL, self.slider_rect.center, self.slider_rect.height // 2, 2)


# --- UTILIDADES DE DIBUJO Y CÁLCULO (Sin Cambios Relevantes) ---

def obtener_rect_modal(ancho_pantalla, alto_pantalla):
    """Calcula el rectángulo principal del modal centrado."""
    return pygame.Rect(
        ancho_pantalla // 2 - MODAL_ANCHO // 2, 
        alto_pantalla // 2 - MODAL_ALTO // 2, 
        MODAL_ANCHO, 
        MODAL_ALTO
    )

def cargar_fondo_modal(modal_rect):
    """
    Carga y escala la imagen de fondo del modal. 
    Usa la función de traducción para obtener la imagen correcta (fondo_ajustes.png).
    """
    path_traducido = obtener_ruta_imagen_traducida(PATH_FONDO_AJUSTES_BASE) 
    
    try:
        fondo_original = pygame.image.load(path_traducido).convert()
        fondo_escalado = pygame.transform.scale(fondo_original, (MODAL_ANCHO, MODAL_ALTO))
    except pygame.error as e:
        print(f"Error cargando fondo traducido en {path_traducido}: {e}. Usando fondo genérico.")
        fondo_escalado = pygame.Surface((MODAL_ANCHO, MODAL_ALTO))
        fondo_escalado.fill((30, 30, 30))
    return fondo_escalado

# --- CACHE Y VARIABLES GLOBALES DE AJUSTES (Sin Cambios Relevantes) ---
_fondo_modal_cache = None 
_slider_cache = None
_mute_btn_assets_cache = None
_lang_btn_assets_cache = None 
_idioma_cache_check = None 
_close_btn_asset_cache = None

# 🌟 NUEVA FUNCIÓN: Carga y escala los botones Mute/Unmute para el estado Normal y Hover
def _get_mute_btn_assets():
    """Carga y devuelve las imágenes de mute/unmute en estado normal y hover."""
    global _mute_btn_assets_cache
    if _mute_btn_assets_cache:
        return _mute_btn_assets_cache
    
    MUTE_HOVER_SIZE = MUTE_BTN_SIZE + GROWTH_PX
        
    try:
        img_mute_orig = pygame.image.load(PATH_MUTE).convert_alpha()
        img_unmute_orig = pygame.image.load(PATH_UNMUTE).convert_alpha()
        
        # Imágenes Normales
        img_mute_normal = pygame.transform.scale(img_mute_orig, (MUTE_BTN_SIZE, MUTE_BTN_SIZE))
        img_unmute_normal = pygame.transform.scale(img_unmute_orig, (MUTE_BTN_SIZE, MUTE_BTN_SIZE))
        
        # Imágenes Hover
        img_mute_hover = pygame.transform.scale(img_mute_orig, (MUTE_HOVER_SIZE, MUTE_HOVER_SIZE))
        img_unmute_hover = pygame.transform.scale(img_unmute_orig, (MUTE_HOVER_SIZE, MUTE_HOVER_SIZE))
        
    except pygame.error:
        # Fallback (sin animación)
        img_mute_normal = pygame.Surface((MUTE_BTN_SIZE, MUTE_BTN_SIZE)); img_mute_normal.fill(ROJO) 
        img_unmute_normal = pygame.Surface((MUTE_BTN_SIZE, MUTE_BTN_SIZE)); img_unmute_normal.fill(VERDE)
        img_mute_hover = img_mute_normal
        img_unmute_hover = img_unmute_normal
        
    _mute_btn_assets_cache = {
        'mute_normal': img_mute_normal, 
        'unmute_normal': img_unmute_normal,
        'mute_hover': img_mute_hover,
        'unmute_hover': img_unmute_hover,
        'normal_size': MUTE_BTN_SIZE,
        'hover_size': MUTE_HOVER_SIZE
    }
    return _mute_btn_assets_cache

# 🌟 FUNCIÓN DE CACHE PARA BOTONES DE IDIOMA (CON ESTADOS NORMAL Y HOVER)
def _get_lang_btn_assets():
    """
    Carga y devuelve las imágenes de los botones de idioma en estado normal y hover.
    El estado hover es GROWTH_PX más grande y centrado.
    """
    global _lang_btn_assets_cache
    if _lang_btn_assets_cache:
        return _lang_btn_assets_cache
        
    assets = {}
    langs = {'es': PATH_BTN_ES, 'in': PATH_BTN_IN}
    
    # 🌟 Definimos el tamaño hover
    LANG_BTN_HOVER_WIDTH = LANG_BTN_WIDTH + GROWTH_PX
    LANG_BTN_HOVER_HEIGHT = LANG_BTN_HEIGHT + GROWTH_PX
    
    try:
        for lang_code, path in langs.items():
            img_orig = pygame.image.load(path).convert_alpha()
            
            # 1. Imagen Normal
            img_normal = pygame.transform.scale(img_orig, (LANG_BTN_WIDTH, LANG_BTN_HEIGHT))
            
            # 2. Imagen Hover (para usar cuando está seleccionado o en hover)
            img_hover = pygame.transform.scale(img_orig, (LANG_BTN_HOVER_WIDTH, LANG_BTN_HOVER_HEIGHT))
            
            assets[lang_code] = {
                'normal': img_normal,
                'hover': img_hover,
                'width_normal': LANG_BTN_WIDTH,
                'height_normal': LANG_BTN_HEIGHT,
                'width_hover': LANG_BTN_HOVER_WIDTH,
                'height_hover': LANG_BTN_HOVER_HEIGHT
            }
            
    except pygame.error as e:
        print(f"Error cargando botones de idioma desde recursos/ [es.png/in.png]: {e}. Usando botones genéricos.")
        # Fallback (sin cambios)
        for lang_code in langs:
            img_normal = pygame.Surface((LANG_BTN_WIDTH, LANG_BTN_HEIGHT)); img_normal.fill(AZUL) 
            text = font_titulo.render(lang_code.upper(), True, BLANCO); img_normal.blit(text, (40, 15))
            
            img_hover = pygame.Surface((LANG_BTN_HOVER_WIDTH, LANG_BTN_HOVER_HEIGHT)); img_hover.fill(ROJO) 

            assets[lang_code] = {
                'normal': img_normal,
                'hover': img_hover,
                'width_normal': LANG_BTN_WIDTH,
                'height_normal': LANG_BTN_HEIGHT,
                'width_hover': LANG_BTN_HOVER_WIDTH,
                'height_hover': LANG_BTN_HOVER_HEIGHT
            }
        
    _lang_btn_assets_cache = assets
    return assets

# 🆕 FUNCIÓN DE CACHE PARA EL BOTÓN DE CIERRE (CON ESTADOS NORMAL Y HOVER)
def _get_close_btn_asset():
    """Carga y devuelve la imagen del botón de cierre 'x.png' en estado normal y hover."""
    global _close_btn_asset_cache
    if isinstance(_close_btn_asset_cache, dict):
        return _close_btn_asset_cache
        
    assets = {}
    CLOSE_HOVER_SIZE = CLOSE_BTN_SIZE + GROWTH_PX // 2 
    
    try:
        img_orig = pygame.image.load(PATH_BTN_CLOSE).convert_alpha()
        
        # 1. Imagen Normal
        assets['normal'] = pygame.transform.scale(img_orig, (CLOSE_BTN_SIZE, CLOSE_BTN_SIZE))
        
        # 2. Imagen Hover
        assets['hover'] = pygame.transform.scale(img_orig, (CLOSE_HOVER_SIZE, CLOSE_HOVER_SIZE))
        
    except pygame.error as e:
        print(f"Error cargando botón de cierre 'x.png': {e}. Usando botón genérico.")
        # Fallback Normal
        assets['normal'] = pygame.Surface((CLOSE_BTN_SIZE, CLOSE_BTN_SIZE)); assets['normal'].fill(ROJO)
        # Fallback Hover
        assets['hover'] = pygame.Surface((CLOSE_HOVER_SIZE, CLOSE_HOVER_SIZE)); assets['hover'].fill(AZUL)
        
    _close_btn_asset_cache = assets
    return assets


# 🌟 MODIFICADA: Se eliminan las líneas que dibujan el recuadro AZUL o VERDE
def _draw_lang_button(ventana, modal_rect, lang_code, is_selected, is_hovered, lang_assets, mouse_pos):
    """Dibuja un botón de idioma con lógica de tamaño para selección y hover. SIN RECUADRO DE RESALTADO."""
    
    # 1. Obtener la posición base del botón (desde la configuración global)
    config = ES_BTN_CONFIG if lang_code == 'es' else IN_BTN_CONFIG
    
    # x_base y y_base son relativos a la esquina superior izquierda del modal (modal_rect.topleft)
    x_base = modal_rect.left + config['x']
    y_base = modal_rect.top + config['y']
    
    asset = lang_assets[lang_code]
    
    # 2. Determinar el tamaño y la imagen a usar
    # Si está seleccionado O en hover, usamos la imagen más grande (hover)
    if is_selected or is_hovered:
        img_to_draw = asset['hover']
        width = asset['width_hover']
        height = asset['height_hover']
    else:
        img_to_draw = asset['normal']
        width = asset['width_normal']
        height = asset['height_normal']
        
    # 3. Calcular el desplazamiento para centrar la imagen
    width_diff = width - LANG_BTN_WIDTH
    height_diff = height - LANG_BTN_HEIGHT
    
    x_draw = x_base - width_diff // 2
    y_draw = y_base - height_diff // 2
    
    # 4. Crear el Rect para dibujar y colisionar
    draw_rect = pygame.Rect(x_draw, y_draw, width, height)
    
    ventana.blit(img_to_draw, draw_rect.topleft)
    
    # 5. Dibuja un círculo verde solo si está seleccionado (opcional, para indicar estado)
    if is_selected:
        # Dibuja un pequeño círculo o marcador para indicar selección, sin el recuadro grande
        pygame.draw.circle(ventana, VERDE, (draw_rect.right - 10, draw_rect.top + 10), 5) 
        
    # ELIMINADO: pygame.draw.rect(ventana, VERDE/AZUL, draw_rect, 3)
        
    return draw_rect


# 🌟 MODIFICADA: Implementa animación (crecimiento) para el botón Mute y quita su recuadro.
def dibujar_ajustes_contenido(ventana, mouse_pos, fondo_modal, modal_rect):
    """Dibuja el contenido del modal (solo elementos, sin textos hardcodeados)."""
    
    global _slider_cache
    
    ventana.blit(fondo_modal, modal_rect.topleft)
    pygame.draw.rect(ventana, AZUL, modal_rect, 5) # Recuadro exterior del modal
    
    # --- CONTROL DE VOLUMEN ---
    
    # 1. Slider: Usando VOL_SLIDER_POS
    slider_x = modal_rect.left + VOL_SLIDER_POS[0]
    slider_y = modal_rect.top + VOL_SLIDER_POS[1]
    
    if _slider_cache is None:
        _slider_cache = VolumeSlider(slider_x, slider_y, SLIDER_WIDTH, SLIDER_HEIGHT, audio_manager.get_current_volume())
        
    _slider_cache.draw(ventana)
    
    # 2. Botón de Mute: Implementando animación y eliminando recuadro
    mute_assets = _get_mute_btn_assets()
    
    # Rectángulo base (Normal) para colisión
    btn_mute_base_rect = pygame.Rect(
        modal_rect.left + MUTE_BTN_POS[0], 
        modal_rect.top + MUTE_BTN_POS[1], 
        MUTE_BTN_SIZE, 
        MUTE_BTN_SIZE
    )
    
    is_muted = audio_manager.is_muted()
    is_hovered = btn_mute_base_rect.collidepoint(mouse_pos)
    
    # Determinar imagen y tamaño
    if is_muted:
        if is_hovered:
            img_to_draw = mute_assets['mute_hover']
        else:
            img_to_draw = mute_assets['mute_normal']
    else:
        if is_hovered:
            img_to_draw = mute_assets['unmute_hover']
        else:
            img_to_draw = mute_assets['unmute_normal']

    # Calcular la posición para centrar el ícono escalado
    current_size = mute_assets['hover_size'] if is_hovered else mute_assets['normal_size']
    size_diff = current_size - MUTE_BTN_SIZE
    
    x_draw = btn_mute_base_rect.left - size_diff // 2
    y_draw = btn_mute_base_rect.top - size_diff // 2
    
    btn_mute_rect = pygame.Rect(x_draw, y_draw, current_size, current_size)
    
    ventana.blit(img_to_draw, btn_mute_rect.topleft)
    
    # ELIMINADO: if btn_mute_base_rect.collidepoint(mouse_pos): pygame.draw.rect(ventana, AZUL, btn_mute_base_rect, 3) 
    
    # --- CONTROL DE IDIOMA --- 
    
    lang_assets = _get_lang_btn_assets()
    idioma_actual = obtener_idioma_actual()
    
    # Dibujar Botón Español
    es_is_selected = idioma_actual == 'es'
    es_is_hovered = not es_is_selected and _get_lang_btn_rect_base('es', modal_rect).collidepoint(mouse_pos)
    es_rect = _draw_lang_button(ventana, modal_rect, 'es', es_is_selected, es_is_hovered, lang_assets, mouse_pos)
    
    # Dibujar Botón Inglés
    in_is_selected = idioma_actual == 'in'
    in_is_hovered = not in_is_selected and _get_lang_btn_rect_base('in', modal_rect).collidepoint(mouse_pos)
    in_rect = _draw_lang_button(ventana, modal_rect, 'in', in_is_selected, in_is_hovered, lang_assets, mouse_pos)
    
    # 🆕 BOTÓN DE CIERRE "X" 
    close_assets = _get_close_btn_asset()
    close_is_hovered = False
    
    padding = CLOSE_BTN_CONFIG['padding']
    size = CLOSE_BTN_CONFIG['size']
    
    # Rectángulo base (normal): Ahora usa el padding desde la configuración
    base_rect = close_assets['normal'].get_rect(
        topright=(modal_rect.right - padding, modal_rect.top + padding)
    )
    if base_rect.collidepoint(mouse_pos):
        close_is_hovered = True
    
    if close_is_hovered:
        img_to_draw = close_assets['hover']
        center_x = base_rect.centerx
        center_y = base_rect.centery
        close_rect = img_to_draw.get_rect(center=(center_x, center_y))
        # ELIMINADO: pygame.draw.rect(ventana, ROJO, close_rect, 2)
    else:
        img_to_draw = close_assets['normal']
        close_rect = base_rect
        
    ventana.blit(img_to_draw, close_rect.topleft)

    return {'mute_btn': btn_mute_base_rect, 'es_btn': es_rect, 'in_btn': in_rect, 'close_btn': close_rect}

# 🌟 MODIFICADA: Ahora lee las coordenadas base de la configuración global
def _get_lang_btn_rect_base(lang_code, modal_rect):
    """Devuelve el rectángulo del botón en su tamaño normal (base) para la detección de colisión."""
    
    config = ES_BTN_CONFIG if lang_code == 'es' else IN_BTN_CONFIG
    
    x_base = modal_rect.left + config['x']
    y_base = modal_rect.top + config['y']
    
    return pygame.Rect(x_base, y_base, config['w'], config['h'])

# --- FUNCIÓN PRINCIPAL (Sin Cambios) ---

def gestionar_ajustes_modal(ventana, event_list, mouse_pos):
    """
    Dibuja el modal y maneja los eventos del slider, mute, botones de idioma y cierre.
    Retorna 'cerrar' si se presiona ESC o el botón X, o None.
    """
    global _fondo_modal_cache, _slider_cache, _idioma_cache_check

    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    
    current_lang = obtener_idioma_actual()
    modal_rect = obtener_rect_modal(ANCHO, ALTO)
    
    # Lógica de recarga: Si el idioma cambió, recargar el fondo traducido y los assets de idioma
    if current_lang != _idioma_cache_check or _fondo_modal_cache is None:
        _fondo_modal_cache = cargar_fondo_modal(modal_rect)
        
        global _lang_btn_assets_cache, _close_btn_asset_cache
        _lang_btn_assets_cache = None 
        _close_btn_asset_cache = None 
        
        _idioma_cache_check = current_lang
    
    # DIBUJAR el contenido de ajustes
    botones = dibujar_ajustes_contenido(ventana, mouse_pos, _fondo_modal_cache, modal_rect)

    # MANEJAR EVENTOS
    for event in event_list:
        
        # Manejar Slider (arrastre)
        if _slider_cache:
            _slider_cache.handle_event(event, mouse_pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Botón de CIERRE
            if botones['close_btn'].collidepoint(mouse_pos):
                return 'cerrar'
                
            # Botón MUTE
            if botones['mute_btn'].collidepoint(mouse_pos):
                audio_manager.toggle_mute()
                
            # Botón ESPAÑOL: Cambia el idioma
            elif botones['es_btn'].collidepoint(mouse_pos):
                establecer_idioma("es")
                
            # Botón INGLÉS: Cambia el idioma
            elif botones['in_btn'].collidepoint(mouse_pos):
                establecer_idioma("in")
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'cerrar' 
            
    return None