# ajustes.py (MODIFICADO: Se eliminan los botones GUARDAR y CERRAR)
import pygame
import sys
import audio_manager 

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
PATH_FONDO_AJUSTES = "recursos/fondo_ajustes.png" 

# NUEVAS CONSTANTES DE AUDIO
PATH_MUTE = "recursos/iconos/btn_mute.png"       
PATH_UNMUTE = "recursos/iconos/btn_unmute.png"   
MUTE_BTN_SIZE = 40
SLIDER_HEIGHT = 15
SLIDER_WIDTH = 300


# Inicialización de fuentes
pygame.font.init()
font_opcion = pygame.font.Font(None, 40)
font_titulo = pygame.font.Font(None, 50)
font_label = pygame.font.Font(None, 30)


# --- CLASE VolumeSlider ---

class VolumeSlider:
    def __init__(self, x, y, w, h, initial_volume):
        self.bar_rect = pygame.Rect(x, y, w, h)
        self.slider_rect = pygame.Rect(0, 0, h * 2, h * 2) 
        self.volume = initial_volume
        self.dragging = False
        self._update_slider_position(initial_volume)

    def _update_slider_position(self, volume):
        """Calcula la posición del control basándose en el volumen."""
        self.slider_rect.centerx = int(self.bar_rect.left + self.bar_rect.width * volume)
        self.slider_rect.centery = self.bar_rect.centery

    def handle_event(self, event, mouse_pos):
        """Maneja el arrastre del slider."""
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
                audio_manager.set_global_volume(self.volume)
                self._update_slider_position(self.volume)

    def draw(self, surface):
        # Sincronizar posición visual si no estamos arrastrando
        if not self.dragging:
            display_volume = 0.0 if audio_manager.is_muted() else audio_manager.get_current_volume()
            self._update_slider_position(display_volume)
        
        # Fondo de la barra
        pygame.draw.rect(surface, GRIS_BARRA, self.bar_rect, border_radius=self.bar_rect.height // 2)
        
        # Barra de progreso (Verde)
        current_width = int(self.bar_rect.width * self.volume)
        progress_rect = pygame.Rect(self.bar_rect.topleft, (current_width, self.bar_rect.height))
        pygame.draw.rect(surface, VERDE_BARRA, progress_rect, border_radius=self.bar_rect.height // 2)
        
        # Botón deslizador
        pygame.draw.circle(surface, SLIDER_COLOR, self.slider_rect.center, self.slider_rect.height // 2)
        pygame.draw.circle(surface, AZUL, self.slider_rect.center, self.slider_rect.height // 2, 2)


# --- UTILIDADES DE DIBUJO Y CÁLCULO (Existentes) ---

def obtener_rect_modal(ancho_pantalla, alto_pantalla):
    """Calcula el rectángulo principal del modal centrado."""
    return pygame.Rect(
        ancho_pantalla // 2 - MODAL_ANCHO // 2, 
        alto_pantalla // 2 - MODAL_ALTO // 2, 
        MODAL_ANCHO, 
        MODAL_ALTO
    )

def cargar_fondo_modal(modal_rect):
    """Carga y escala la imagen de fondo del modal (Solo una vez)."""
    try:
        fondo_original = pygame.image.load(PATH_FONDO_AJUSTES).convert()
        fondo_escalado = pygame.transform.scale(fondo_original, (MODAL_ANCHO, MODAL_ALTO))
    except pygame.error:
        fondo_escalado = pygame.Surface((MODAL_ANCHO, MODAL_ALTO))
        fondo_escalado.fill((30, 30, 30))
    return fondo_escalado

# --- CACHE Y VARIABLES GLOBALES DE AJUSTES ---
_fondo_modal_cache = None 
_slider_cache = None
_mute_btn_assets_cache = None


def _get_mute_btn_assets():
    """Carga y devuelve las imágenes de mute/unmute."""
    global _mute_btn_assets_cache
    if _mute_btn_assets_cache:
        return _mute_btn_assets_cache
        
    try:
        img_mute_orig = pygame.image.load(PATH_MUTE).convert_alpha()
        img_unmute_orig = pygame.image.load(PATH_UNMUTE).convert_alpha()
        img_mute = pygame.transform.scale(img_mute_orig, (MUTE_BTN_SIZE, MUTE_BTN_SIZE))
        img_unmute = pygame.transform.scale(img_unmute_orig, (MUTE_BTN_SIZE, MUTE_BTN_SIZE))
    except pygame.error:
        img_mute = pygame.Surface((MUTE_BTN_SIZE, MUTE_BTN_SIZE)); img_mute.fill(ROJO) 
        img_unmute = pygame.Surface((MUTE_BTN_SIZE, MUTE_BTN_SIZE)); img_unmute.fill(VERDE)
        
    _mute_btn_assets_cache = {'mute': img_mute, 'unmute': img_unmute}
    return _mute_btn_assets_cache


def dibujar_ajustes_contenido(ventana, mouse_pos, fondo_modal, modal_rect):
    """Dibuja el contenido del modal, SÓLO el control de volumen."""
    
    global _slider_cache
    
    ventana.blit(fondo_modal, modal_rect.topleft)
    pygame.draw.rect(ventana, AZUL, modal_rect, 5)
    
    # --- CONTROL DE VOLUMEN ---
    
    # 1. Etiqueta
    texto_volumen = font_label.render("Volumen de Música", True, BLANCO)
    ventana.blit(texto_volumen, (modal_rect.left + 50, modal_rect.top + 120))
    
    # 2. Slider (Inicialización en la primera llamada)
    if _slider_cache is None:
        slider_x = modal_rect.left + 50
        slider_y = modal_rect.top + 160
        _slider_cache = VolumeSlider(slider_x, slider_y, SLIDER_WIDTH, SLIDER_HEIGHT, audio_manager.get_current_volume())
        
    _slider_cache.draw(ventana)
    
    # 3. Botón de Mute
    mute_assets = _get_mute_btn_assets()
    # Posición del botón de mute junto al slider
    btn_rect = pygame.Rect(_slider_cache.bar_rect.right + 20, _slider_cache.bar_rect.centery - MUTE_BTN_SIZE // 2, MUTE_BTN_SIZE, MUTE_BTN_SIZE)
    
    # Selecciona la imagen correcta
    current_img = mute_assets['mute'] if audio_manager.is_muted() else mute_assets['unmute']
    
    # Dibujar el botón
    ventana.blit(current_img, btn_rect.topleft)
    if btn_rect.collidepoint(mouse_pos):
        pygame.draw.rect(ventana, AZUL, btn_rect, 3) 
    
    # Solo devolvemos el rect del botón de mute para manejar su clic
    return {'mute_btn': btn_rect}


# --- FUNCIÓN PRINCIPAL (Modificada para la salida simple) ---

def gestionar_ajustes_modal(ventana, event_list, mouse_pos):
    """
    Dibuja el modal y maneja los eventos del slider y el botón de mute.
    Retorna 'cerrar' si se presiona ESC o None.
    """
    global _fondo_modal_cache, _slider_cache

    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    
    # 1. Inicializar cache
    modal_rect = obtener_rect_modal(ANCHO, ALTO)
    if _fondo_modal_cache is None:
        _fondo_modal_cache = cargar_fondo_modal(modal_rect)
    
    # 2. DIBUJAR el contenido de ajustes
    botones = dibujar_ajustes_contenido(ventana, mouse_pos, _fondo_modal_cache, modal_rect)

    # 3. MANEJAR EVENTOS
    for event in event_list:
        
        # Manejar Slider (arrastre)
        if _slider_cache:
            _slider_cache.handle_event(event, mouse_pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Botón MUTE
            if botones['mute_btn'].collidepoint(mouse_pos):
                audio_manager.toggle_mute()
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'cerrar' # <-- Única forma de salir
            
    return None # No hubo acción que requiera cambio de estado