import pygame
from player import Player 
from obstaculo import Obstaculo 
from meta import Meta 
from ganaste_entre_nivel3 import run_pantalla_ganaste 
from pantalla_derrota import run_pantalla_derrota
from coleccionable import Coleccionable 
import sys
import time 
import loading_screen3
from audio_manager import audio_manager 
import cortina 
# 📢 IMPORTAR LÓGICA DE TRADUCCIÓN (AÑADIDO obtener_texto_traducido)
from traduccion import obtener_ruta_imagen_traducida, obtener_texto_traducido 

# --- CONSTANTES ---
PATH_FONDO_NIVEL_1 = "recursos/FondoNivel3.png" 
AZUL_FALLBACK = (50, 50, 150)
NUM_COLECCIONABLES_REQUERIDOS = 9 
TIEMPO_LIMITE_SEGUNDOS = 60
TIEMPO_PENALIZACION = 2
TIEMPO_BONIFICACION = 0 
COLECCIONABLES_BUENOS_INDICES = [12, 13, 14, 15] 

# --- CONSTANTES DE PAUSA y UI ---
PATH_BTN_PAUSA = "recursos/botones/btn_pausa.png"
PATH_BTN_PLAY = "recursos/botones/btn_play.png"
PATH_BTN_MENU_PAUSA = "recursos/botones/btn_menu.png"
PATH_BTN_REINICIAR = "recursos/botones/btn_reiniciar.png"
PATH_FONDO_PAUSA_BASE = "fondo_menu_pausa.png" # <--- Ruta base para traducción

VERDE_BARRA = (0, 200, 0)
ROJO_BARRA = (200, 0, 0)
GRIS_FONDO = (50, 50, 50)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
GRIS_OSCURO_PAUSA = (0,0,0,0) 

# Nueva constante para el efecto de escalado al pasar el ratón en los botones de UI (Copiado de Nivel 2)
BUTTON_HOVER_GROWTH = 10 


# --- CLASE BOTON SIMPLE (Actualizada para animación de hover sin marco - Copiado de Nivel 2) ---
class BotonSimple:
    def __init__(self, x, y, width, height, path, action):
        self.action = action
        self.width = width
        self.height = height
        
        # Calcular dimensiones de Hover
        self.hover_width = width + BUTTON_HOVER_GROWTH
        self.hover_height = height + BUTTON_HOVER_GROWTH
        
        try:
            image_original = pygame.image.load(path).convert_alpha()
            
            # Estado Normal
            self.image_normal = pygame.transform.scale(image_original, (width, height))
            self.rect_normal = self.image_normal.get_rect(topleft=(x, y))
            
            # Estado Hover
            self.image_hover = pygame.transform.scale(image_original, (self.hover_width, self.hover_height))
            # Recalcular la posición para centrar el botón en hover
            pos_hover_x = x - BUTTON_HOVER_GROWTH // 2
            pos_hover_y = y - BUTTON_HOVER_GROWTH // 2
            self.rect_hover = self.image_hover.get_rect(topleft=(pos_hover_x, pos_hover_y))
            
        except pygame.error:
            # Fallback
            self.image_normal = pygame.Surface((width, height)); self.image_normal.fill((100, 100, 100))
            self.rect_normal = self.image_normal.get_rect(topleft=(x, y))
            self.image_hover = self.image_normal # Usar la normal como hover en fallback
            self.rect_hover = self.rect_normal
        
        # Se mantiene el rect para compatibilidad con llamadas externas
        self.rect = self.rect_normal 

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect_normal.collidepoint(mouse_pos):
            # Dibujar estado hover (imagen escalada, sin marco amarillo)
            surface.blit(self.image_hover, self.rect_hover)
        else:
            # Dibujar estado normal
            surface.blit(self.image_normal, self.rect_normal)
    
    def check_click(self, mouse_pos):
        # Se comprueba la colisión contra el rect normal (huella original)
        if self.rect_normal.collidepoint(mouse_pos):
            return self.action
        return None

# --- FUNCIÓN PARA CONFIGURAR EL NIVEL (sin cambios) ---
def setup_level(player):
    obstaculo_list = pygame.sprite.Group()
    meta_group = pygame.sprite.Group() 
    coleccionable_group = pygame.sprite.Group() 
    
    # DEFINICIÓN DE OBSTÁCULOS
    obstaculos_coords = [
         (132, 136, 1016, 8), (136, 212, 8, 468), (136, 212, 128, 8), (256, 212, 8, 29),
        (220, 316, 8, 136), (220, 444, 40, 8), (252, 444, 8, 160), (252, 520, 52, 8),
        (136, 520, 52, 8), (220, 368, 40, 8), (136, 596, 124, 8), (136, 672, 1012, 8),
        (1140, 136, 8, 456), (1108, 584, 41, 8), (348, 136, 8, 164), (348, 292, 48, 8),
        (580, 136, 8, 88), (464, 216, 124, 8), (492, 216, 12, 236), (356, 384, 8, 68),
        (356, 444, 176, 8), (432, 444, 8, 44), (844, 136, 8, 60), (844, 188, 40, 8),
        (964, 136, 8, 92), (964, 220, 88, 8), (1000, 220, 12, 81), (980, 292, 32, 8),
        (1104, 292, 44, 8), (1104, 292, 8, 84), (1056, 368, 57, 8), (1056, 368, 8, 84),
        (960, 444, 104, 8), (1000, 544, 12, 140), (980, 544, 32, 8), (536, 560, 8, 125),
        (340, 600, 8, 84), (340, 600, 112, 8), (372, 564, 8, 44), (708, 516, 12, 168),
        (708, 604, 88, 8), (788, 444, 8, 168), (788, 520, 92, 8), (872, 520, 8, 72),
        (872, 580, 40, 12), (744, 444, 52, 8), (744, 372, 8, 80), (744, 372, 41, 8),
        (776, 292, 8, 88), (776, 292, 92, 8), (860, 292, 8, 120), (816, 364, 52, 8),
        (608, 516, 108, 8), (620, 596, 36, 8), (644, 368, 12, 236), (584, 368, 72, 12),
        (584, 292, 8, 88), (584, 292, 92, 8), (664, 216, 12, 84), (664, 216, 60, 8),
        (0, 48, 1280, 8)
    ]
    
    for x, y, w, h in obstaculos_coords:
        obstaculo = Obstaculo(x, y, w, h)
        obstaculo_list.add(obstaculo)
        
    # DEFINICIÓN DE LA META
    meta = Meta(1137, 591, 10, 85)
    meta_group.add(meta)
    
    # COLECCIONABLES
    coleccionables_coords = [
        (302, 166, 15), (364, 322, 13), (416, 544, 12), (612, 242, 12), (588, 428, 14), 
        (782, 154, 14), (942, 242, 13), (894, 460, 12), (1088, 520, 15), 
        (170, 242, 18), (216, 388, 16), (240, 618, 17), (510, 156, 16), (570, 576, 18), 
        (774, 364, 18), (814, 618, 16), (950, 576, 17), (1086, 170, 17), 
    ]

    for x, y, index in coleccionables_coords:
        coleccionable_group.add(Coleccionable(x, y, index=index))
        
    return obstaculo_list, meta_group, coleccionable_group 


# --- FUNCIÓN DE PRECÁRGALA (sin cambios) ---
def preload_level(ventana, character_data):
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    
    try:
        fondo_nivel = pygame.image.load(PATH_FONDO_NIVEL_1).convert()
        fondo_nivel = pygame.transform.scale(fondo_nivel, (ANCHO, ALTO))
    except pygame.error as e:
        fondo_nivel = pygame.Surface((ANCHO, ALTO)); fondo_nivel.fill(AZUL_FALLBACK)
        
    start_position = (158, 148) 
    from player import Player
    player = Player(start_position, character_data, ANCHO, ALTO) 
    player_group = pygame.sprite.Group(player)

    obstaculo_group, meta_group, coleccionable_group = setup_level(player) 
    
    return fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group


# --- FUNCIÓN DE DIBUJO DE UI (MODIFICADA PARA TRADUCCIÓN DE TEXTO) ---
def draw_ui(ventana, remaining_time, max_time, collected, required):
    ANCHO, ALTO = ventana.get_size()
    
    BAR_WIDTH = 300
    BAR_HEIGHT = 20
    BAR_X = 20
    BAR_Y = 20
    
    time_ratio = remaining_time / max_time
    current_width = int(BAR_WIDTH * time_ratio)
    
    bar_color = VERDE_BARRA if remaining_time > 5 else ROJO_BARRA

    pygame.draw.rect(ventana, GRIS_FONDO, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 0, 5)
    pygame.draw.rect(ventana, bar_color, (BAR_X, BAR_Y, current_width, BAR_HEIGHT), 0, 5)
    pygame.draw.rect(ventana, BLANCO, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 2, 5)

    font_timer = pygame.font.SysFont('Arial', 20, bold=True)
    time_text = f"{int(remaining_time)}"
    timer_surface = font_timer.render(time_text, True, BLANCO)
    ventana.blit(timer_surface, (BAR_X + BAR_WIDTH + 10, BAR_Y))
    
    # --- Lógica de Traducción Aplicada Aquí (Copiado de Nivel 1) ---
    item_label = obtener_texto_traducido("ITEMS_COLLECTED") 

    font_items = pygame.font.SysFont('Arial', 30, bold=True)
    item_text = f"{item_label}: {collected} / {required}" # Usa la etiqueta traducida
    
    item_color = AMARILLO if collected < required else VERDE_BARRA
    
    item_surface = font_items.render(item_text, True, item_color)
    
    ventana.blit(item_surface, (BAR_X, BAR_Y + BAR_HEIGHT + 10))

# --------------------------------------------------------------------------
# FUNCIÓN DEL MENÚ DE PAUSA (Actualizada para usar la nueva clase BotonSimple)
# --------------------------------------------------------------------------
def run_pause_menu(ventana):
    ANCHO, ALTO = ventana.get_size()
    
    fondo_oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    # Rellenar con opacidad (0, 0, 0, 150) para oscurecer el fondo del juego
    fondo_oscuro.fill((0, 0, 0, 0)) 
    
    PANEL_W, PANEL_H = 500, 250 
    CENTER_X = ANCHO // 2
    PANEL_X = CENTER_X - PANEL_W // 2
    PANEL_Y = ALTO // 2 - PANEL_H // 2
    
    fondo_pausa_img = None
    
    # Obtener la ruta traducida del fondo del menú de pausa
    path_fondo_traducido = obtener_ruta_imagen_traducida(PATH_FONDO_PAUSA_BASE) # <--- Uso de la función de traducción

    try:
        # Cargar la imagen usando la ruta traducida
        fondo_pausa_img_orig = pygame.image.load(path_fondo_traducido).convert_alpha()
        fondo_pausa_img = pygame.transform.scale(fondo_pausa_img_orig, (PANEL_W, PANEL_H))
    except pygame.error as e:
        print(f"Error cargando fondo traducido: {path_fondo_traducido}. Usando color sólido.")
        fondo_pausa_img = pygame.Surface((PANEL_W, PANEL_H)); 
        fondo_pausa_img.fill((80, 80, 80)) 
    
    BTN_W, BTN_H = 100, 100 
    GAP = 20 
    TOTAL_MENU_WIDTH = (BTN_W * 3) + (GAP * 2)
    
    START_X = CENTER_X - (TOTAL_MENU_WIDTH // 2) 
    BUTTON_Y = PANEL_Y + PANEL_H - BTN_H - 30 

    # Botones (Usando la clase BotonSimple con hover)
    btn_menu = BotonSimple(START_X, BUTTON_Y, BTN_W, BTN_H, PATH_BTN_MENU_PAUSA, "SELECTOR_NIVEL")
    btn_restart = BotonSimple(START_X + BTN_W + GAP, BUTTON_Y, BTN_W, BTN_H, PATH_BTN_REINICIAR, "REINTENTAR")
    btn_play = BotonSimple(START_X + (BTN_W + GAP) * 2, BUTTON_Y, BTN_W, BTN_H, PATH_BTN_PLAY, "CONTINUE")
    
    botones = [btn_play, btn_restart, btn_menu]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for btn in botones:
                    accion = btn.check_click(mouse_pos)
                    if accion:
                        return accion
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "CONTINUE"

        ventana.blit(fondo_oscuro, (0, 0)) # Dibujar el oscurecimiento
        ventana.blit(fondo_pausa_img, (PANEL_X, PANEL_Y))
        
        for btn in botones:
            btn.draw(ventana)

        pygame.display.flip()
        pygame.time.Clock().tick(30) 


# --- FUNCIÓN PRINCIPAL DEL NIVEL 3 (MODIFICADA) ---
def run_level(ventana, precargados, img_btn_regresar, REGRESAR_RECT):
    
    # --- Solución para TypeError: cannot unpack non-iterable NoneType object ---
    # Verifica si la precarga falló (devolvió None) antes de intentar desempaquetar.
    if precargados is None:
        print("Error: Precarga de nivel fallida (precargados es None). Devolviendo a SELECTOR_NIVEL.")
        fondo_nivel = None 
        player_group = pygame.sprite.Group() 
        obstaculo_group = pygame.sprite.Group()
        meta_group = pygame.sprite.Group()
        coleccionable_group = pygame.sprite.Group()
        
        # MODIFICACIÓN CLAVE: Devolver "SELECTOR_NIVEL" para ir al menú principal
        return "SELECTOR_NIVEL", None, None 

    else:
        # Desempaquetado normal si precargados es una tupla de 5 elementos
        fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group = precargados
    # ---------------------------------------------------------------------------

    ANCHO = ventana.get_width()
    clock = pygame.time.Clock()
    
    # Botón de Pausa (Usando la clase BotonSimple con hover)
    btn_pausa = BotonSimple(ANCHO - 60, 20, 40, 40, PATH_BTN_PAUSA, "PAUSE") 
    
    start_time = time.time() 
    is_paused = False 
    pause_start_time = 0 

    coleccionables_recogidos = 0 
    penalizacion_total = 0 

    # --------------------------------------------------------------------------------
    # PASO DE CARGA INICIAL
    # --------------------------------------------------------------------------------
    
    # Verificar si el fondo fue cargado correctamente 
    if fondo_nivel:
        ventana.blit(fondo_nivel, (0, 0)) 
    else:
        # Fallback de color sólido 
        ventana.fill(AZUL_FALLBACK) 
        
    player_group.draw(ventana)
    obstaculo_group.draw(ventana) 
    coleccionable_group.draw(ventana) 
    meta_group.draw(ventana)
    pygame.display.flip() 
    
    loading_screen3.run_loading_screen(ventana) 
    
    start_time = time.time() 
    # --------------------------------------------------------------------------------
    
    running = True
    while running:
        
        dt = clock.tick(60) 
        
        elapsed_time = time.time() - start_time + penalizacion_total
        remaining_time = max(0, TIEMPO_LIMITE_SEGUNDOS - elapsed_time)
        
        # 1. MANEJO DE EVENTOS
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not is_paused: 
                is_paused = True
                pause_start_time = time.time()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 💡 Uso del nuevo BotonSimple que comprueba la acción de pausa
                if btn_pausa.check_click(mouse_pos) == "PAUSE" and not is_paused:
                    is_paused = True
                    pause_start_time = time.time()

        # 2. LÓGICA DE PAUSA
        if is_paused:
            audio_manager.pause_music()
            
            if fondo_nivel:
                ventana.blit(fondo_nivel, (0, 0)) 
            player_group.draw(ventana)
            obstaculo_group.draw(ventana) 
            coleccionable_group.draw(ventana) 
            meta_group.draw(ventana)
            draw_ui(ventana, remaining_time, TIEMPO_LIMITE_SEGUNDOS, coleccionables_recogidos, NUM_COLECCIONABLES_REQUERIDOS)
            btn_pausa.draw(ventana) # 💡 Dibujar el botón para que se vea antes del menú
            pygame.display.flip()
            
            accion_pausa = run_pause_menu(ventana) 

            if accion_pausa == "CONTINUE":
                is_paused = False
                pause_duration = time.time() - pause_start_time
                start_time += pause_duration 
                audio_manager.unpause_music()
            elif accion_pausa == "REINTENTAR":
                audio_manager.stop_music()
                return "REINTENTAR", None, None
            elif accion_pausa == "SELECTOR_NIVEL": 
                audio_manager.stop_music()
                return "SELECTOR_NIVEL", None, None 
                
            continue 

        # 3. LÓGICA DEL JUEGO 
        
        # CONDICIÓN DE DERROTA POR TIEMPO
        if remaining_time <= 0:
            running = False
            audio_manager.stop_music() 
            
            # LLAMADA A LA ANIMACIÓN DE CORTINA
            cortina.run_cortina_animation(ventana)
            
            # 🐞 FIX: Asegurar que run_pantalla_derrota devuelva una tupla y manejar None
            accion_derrota = run_pantalla_derrota(ventana)
            if accion_derrota is None: return "SELECTOR_NIVEL", None, None # Retorno seguro en caso de error
            
            if accion_derrota[0] == "MENU": return "SELECTOR_NIVEL", None, None 
            return accion_derrota
        
        # ACTUALIZAR Y COLISIONES
        # Comprobar que haya al menos un sprite antes de acceder a [0]
        if not player_group.sprites():
            # Si el grupo de jugadores está vacío (p. ej., por fallo de precarga), salimos del bucle.
            return "SELECTOR_NIVEL", None, None
            
        player = player_group.sprites()[0] 
        player_group.update(obstaculo_group) 
        coleccionable_group.update(dt) 
        
        collected_items = pygame.sprite.spritecollide(player, coleccionable_group, True)
        
        # LÓGICA CLAVE DE COLECCIONABLES
        for item in collected_items:
            
            bonus_speed = item.get_effect_value()
            
            if bonus_speed > 0:
                audio_manager.play_collect_good() 
                
                player.increase_speed(bonus_speed) 
                penalizacion_total = max(0, penalizacion_total - TIEMPO_BONIFICACION)
                
                coleccionables_recogidos += 1
                
            else: 
                audio_manager.play_collect_bad() 
                
                penalizacion_total += TIEMPO_PENALIZACION
            
        # DETECCIÓN DE META CONDICIONAL
        if pygame.sprite.spritecollide(player, meta_group, False):
            running = False 
            audio_manager.stop_music()
            
            # LLAMADA A LA ANIMACIÓN DE CORTINA
            cortina.run_cortina_animation(ventana)
            
            if coleccionables_recogidos >= NUM_COLECCIONABLES_REQUERIDOS:
                # 🐞 FIX: Asegurar que run_pantalla_ganaste devuelva una tupla y manejar None
                resultado_final = run_pantalla_ganaste(ventana, img_btn_regresar, REGRESAR_RECT)
                if resultado_final is None: return "SELECTOR_NIVEL", None, None # Retorno seguro en caso de error
                return resultado_final
            else:
                # 🐞 FIX: Asegurar que run_pantalla_derrota devuelva una tupla y manejar None
                accion_derrota = run_pantalla_derrota(ventana) 
                if accion_derrota is None: return "SELECTOR_NIVEL", None, None # Retorno seguro en caso de error
                
                if accion_derrota[0] == "MENU": return "SELECTOR_NIVEL", None, None 
                return accion_derrota
                
        # 4. Dibujar
        if fondo_nivel:
            ventana.blit(fondo_nivel, (0, 0)) 
        else:
             ventana.fill(AZUL_FALLBACK) # Fallback si el fondo es None
             
        player_group.draw(ventana)
        obstaculo_group.draw(ventana) 
        coleccionable_group.draw(ventana) 
        meta_group.draw(ventana)

        draw_ui(ventana, remaining_time, TIEMPO_LIMITE_SEGUNDOS, coleccionables_recogidos, NUM_COLECCIONABLES_REQUERIDOS)
        btn_pausa.draw(ventana)
        pygame.display.flip()

    audio_manager.stop_music()
    # Retorno por defecto al salir del bucle (también cambiado de "MENU" a "SELECTOR_NIVEL" para consistencia)
    return "SELECTOR_NIVEL", None, None