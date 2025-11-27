import pygame
from player import Player 
from obstaculo import Obstaculo 
from meta import Meta 
from ganaste_entre_nivel import run_pantalla_ganaste 
from pantalla_derrota import run_pantalla_derrota
from coleccionable import Coleccionable 
import sys
import time 
import loading_screen 
from audio_manager import audio_manager 
import cortina 
from pathlib import Path

# 📢 IMPORTAR LÓGICA DE TRADUCCIÓN
from traduccion import obtener_ruta_imagen_traducida 

# --- CONSTANTES ---
PATH_FONDO_NIVEL_1 = "recursos/FondoNivel1.jpg" 
AZUL_FALLBACK = (50, 50, 150)
NUM_COLECCIONABLES_REQUERIDOS = 6 
TIEMPO_LIMITE_SEGUNDOS = 45
TIEMPO_PENALIZACION = 2
TIEMPO_BONIFICACION = 0 
COLECCIONABLES_BUENOS_INDICES = [0, 1, 2] 

# --- CONSTANTES DE PAUSA ---
PATH_BTN_PAUSA = "recursos/botones/btn_pausa.png"
PATH_BTN_PLAY = "recursos/botones/btn_play.png"
PATH_BTN_MENU_PAUSA = "recursos/botones/btn_menu.png"
PATH_BTN_REINICIAR = "recursos/botones/btn_reiniciar.png"
# 🚨 RUTA BASE para la traducción del fondo de pausa
PATH_FONDO_PAUSA_BASE = "fondo_menu_pausa.png" 

# Colores para la UI
VERDE_BARRA = (0, 200, 0)
ROJO_BARRA = (200, 0, 0)
GRIS_FONDO = (50, 50, 50)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
GRIS_OSCURO_PAUSA = (0,0,0,0) 

# Nueva constante para el efecto de escalado al pasar el ratón en los botones de UI
BUTTON_HOVER_GROWTH = 10 

# --- CLASE BOTON SIMPLE (Actualizada para animación de hover sin marco) ---
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

# --- FUNCIÓN PARA CONFIGURAR EL NIVEL ---
def setup_level():
    obstaculo_list = pygame.sprite.Group()
    meta_group = pygame.sprite.Group() 
    coleccionable_group = pygame.sprite.Group() 
    
    # DEFINICIÓN DE OBSTÁCULOS
    obstaculos_coords = [
        (0, 110, 955, 20), (1116, 110, 164, 20), (0, 129, 13, 700), 
        (1262, 129, 16, 700), (0, 700, 1280, 20), (94, 213, 73, 72), 
        (94, 213, 229, 20), (251, 213, 73, 178), (13, 371, 240, 20),
        (488, 128, 73, 309), (551, 417, 246, 20), (724, 417, 73, 174),
        (330, 519, 467, 20), (330, 534, 73, 55), (93, 571, 310, 20),
        (93, 467, 73, 124), (488, 639, 73, 67), (1116, 127, 73, 105), 
        (646, 212, 472, 20), (646, 225, 73, 110), (711, 315, 321, 20),
        (1116, 315, 73, 122), (880, 417, 240, 20), (880, 432, 73, 157),
        (1188, 571, 73, 20), (1032, 572, 73, 132)
    ]
    
    for x, y, w, h in obstaculos_coords:
        obstaculo = Obstaculo(x, y, w, h)
        obstaculo_list.add(obstaculo)
        
    # DEFINICIÓN DE LA META
    meta = Meta(955, 100, 160, 17)
    meta_group.add(meta)
    
    # COLECCIONABLES (Índices 0-2 BUENOS, 3-5 MALOS)
    coleccionables_coords = [
        (24, 186, 0), (347, 217, 2), (257, 630, 1), (595, 628, 2), 
        (807, 391, 0), (574, 191, 1), 
        # Malos
        (430, 416, 3), (186, 510, 4), (974, 648, 5), (1192, 510, 3), 
        (1021, 265, 4), (1207, 205, 5) 
    ]

    for x, y, index in coleccionables_coords:
        coleccionable_group.add(Coleccionable(x, y, index=index))
        
    return obstaculo_list, meta_group, coleccionable_group 


# --- FUNCIÓN DE PRECÁRGALA ---
def preload_level(ventana, character_dict):
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    
    # 1. Cargar Fondo
    try:
        fondo_nivel = pygame.image.load(PATH_FONDO_NIVEL_1).convert()
        fondo_nivel = pygame.transform.scale(fondo_nivel, (ANCHO, ALTO))
    except pygame.error as e:
        fondo_nivel = pygame.Surface((ANCHO, ALTO)); fondo_nivel.fill(AZUL_FALLBACK)
        
    # 2. Inicializar Personaje
    start_position = (175, 250) 
    from player import Player
    player = Player(start_position, character_dict, ANCHO, ALTO) 
    player_group = pygame.sprite.Group(player)

    # 3. Carga de obstáculos y coleccionables
    obstaculo_group, meta_group, coleccionable_group = setup_level() 
    
    return fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group


# --- FUNCIÓN DE DIBUJO DE UI (sin cambios) ---
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
    
    font_items = pygame.font.SysFont('Arial', 30, bold=True)
    item_text = f"Objetos: {collected} / {required}"
    
    item_color = AMARILLO if collected < required else VERDE_BARRA
    
    item_surface = font_items.render(item_text, True, item_color)
    
    ventana.blit(item_surface, (BAR_X, BAR_Y + BAR_HEIGHT + 10))

# --------------------------------------------------------------------------
# FUNCIÓN DEL MENÚ DE PAUSA (CON FONDO TRADUCIDO)
# --------------------------------------------------------------------------
def run_pause_menu(ventana):
    ANCHO, ALTO = ventana.get_size()
    
    fondo_oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    fondo_oscuro.fill((0, 0, 0, 0))
    
    PANEL_W, PANEL_H = 500, 250 
    CENTER_X = ANCHO // 2
    PANEL_X = CENTER_X - PANEL_W // 2
    PANEL_Y = ALTO // 2 - PANEL_H // 2
    
    fondo_pausa_img = None
    
    # 🚨 Cargar fondo de pausa traducido
    path_fondo_pausa_traducido = obtener_ruta_imagen_traducida(PATH_FONDO_PAUSA_BASE)
    
    try:
        fondo_pausa_img_orig = pygame.image.load(path_fondo_pausa_traducido).convert_alpha()
        fondo_pausa_img = pygame.transform.scale(fondo_pausa_img_orig, (PANEL_W, PANEL_H))
    except pygame.error as e:
        print(f"Error cargando fondo de pausa traducido: {path_fondo_pausa_traducido}. Usando color sólido.")
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

        ventana.blit(fondo_oscuro, (0, 0))
        ventana.blit(fondo_pausa_img, (PANEL_X, PANEL_Y))
        
        for btn in botones:
            btn.draw(ventana) # Dibuja con efecto hover

        pygame.display.flip()
        pygame.time.Clock().tick(30) 

# --- FUNCIÓN PRINCIPAL DEL NIVEL 1 (CORREGIDA) ---
def run_level(ventana, precargados_assets, img_btn_regresar, REGRESAR_RECT): 
    
    fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group = precargados_assets
    
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
    
    # 1. Dibuja el nivel completo para que se vea detrás del modal de carga.
    ventana.blit(fondo_nivel, (0, 0)) 
    player_group.draw(ventana)
    obstaculo_group.draw(ventana) 
    coleccionable_group.draw(ventana) 
    meta_group.draw(ventana)
    pygame.display.flip() 
    
    # 2. Llama a la pantalla de carga.
    loading_screen.run_loading_screen(ventana) 
    
    # Reinicia el tiempo de inicio
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
                # Comprobar clic usando el nuevo método check_click
                if btn_pausa.check_click(mouse_pos) == "PAUSE" and not is_paused:
                    is_paused = True
                    pause_start_time = time.time()

        # 2. LÓGICA DE PAUSA
        if is_paused:
            audio_manager.pause_music()
            
            ventana.blit(fondo_nivel, (0, 0)) 
            player_group.draw(ventana)
            obstaculo_group.draw(ventana) 
            coleccionable_group.draw(ventana) 
            meta_group.draw(ventana)
            draw_ui(ventana, remaining_time, TIEMPO_LIMITE_SEGUNDOS, coleccionables_recogidos, NUM_COLECCIONABLES_REQUERIDOS)
            btn_pausa.draw(ventana)
            pygame.display.flip()
            
            accion_pausa = run_pause_menu(ventana) 

            # Lógica post-menú
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
            
            # LLAMADA A LA ANIMACIÓN DE CORTINA (DERROTA POR TIEMPO)
            cortina.run_cortina_animation(ventana)
            
            accion_derrota = run_pantalla_derrota(ventana)
            if accion_derrota[0] == "MENU": return "SELECTOR_NIVEL", None, None 
            return accion_derrota
        
        # ACTUALIZAR Y COLISIONES
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
            
            # LLAMADA A LA ANIMACIÓN DE CORTINA (VICTORIA O DERROTA POR META)
            cortina.run_cortina_animation(ventana)

            if coleccionables_recogidos >= NUM_COLECCIONABLES_REQUERIDOS:
                return run_pantalla_ganaste(ventana, img_btn_regresar, REGRESAR_RECT) 
            else:
                accion_derrota = run_pantalla_derrota(ventana) 
                if accion_derrota[0] == "MENU": return "SELECTOR_NIVEL", None, None 
                return accion_derrota
                
        # 4. Dibujar
        ventana.blit(fondo_nivel, (0, 0)) 
        player_group.draw(ventana)
        obstaculo_group.draw(ventana) 
        coleccionable_group.draw(ventana) 
        meta_group.draw(ventana)

        draw_ui(ventana, remaining_time, TIEMPO_LIMITE_SEGUNDOS, coleccionables_recogidos, NUM_COLECCIONABLES_REQUERIDOS)
        btn_pausa.draw(ventana)
        pygame.display.flip()

    audio_manager.stop_music()
    return "MENU", None, None