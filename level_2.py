# level_1.py (CÓDIGO COMPLETO Y CORREGIDO con lógica de tiempo y SFX)

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
from audio_manager import audio_manager # 💡 IMPORTACIÓN DE LA INSTANCIA GLOBAL

# --- CONSTANTES ---
PATH_FONDO_NIVEL_1 = "recursos/FondoNivel2.jpg" 
AZUL_FALLBACK = (50, 50, 150)
NUM_COLECCIONABLES_REQUERIDOS = 6 
TIEMPO_LIMITE_SEGUNDOS = 120
TIEMPO_PENALIZACION = 2
TIEMPO_BONIFICACION = 0 # 💡 NUEVA CONSTANTE
COLECCIONABLES_BUENOS_INDICES = [6, 7, 8] 

# --- CONSTANTES DE PAUSA ---
PATH_BTN_PAUSA = "recursos/btn_pausa.png"
PATH_BTN_PLAY = "recursos/btn_play.png"
PATH_BTN_MENU_PAUSA = "recursos/btn_menu.png"
PATH_BTN_REINICIAR = "recursos/btn_reiniciar.png"
PATH_FONDO_PAUSA = "recursos/fondo_menu_pausa.png" 

# Colores para la UI
VERDE_BARRA = (0, 200, 0)
ROJO_BARRA = (200, 0, 0)
GRIS_FONDO = (50, 50, 50)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
GRIS_OSCURO_PAUSA = (0,0,0,0) 


# --- CLASE BOTON SIMPLE (REINCLUIDA AQUÍ PARA SOLUCIONAR EL ERROR) ---
class BotonSimple:
    def __init__(self, x, y, width, height, path, action):
        self.action = action
        try:
            self.image_original = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image_original, (width, height))
        except pygame.error:
            # Crea un color si la imagen falla
            self.image = pygame.Surface((width, height)); self.image.fill((100, 100, 100))
        
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, AMARILLO, self.rect, 3, 5)
    
    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return self.action
        return None

# --- FUNCIÓN PARA CONFIGURAR EL NIVEL (sin cambios) ---
def setup_level(player):
    obstaculo_list = pygame.sprite.Group()
    meta_group = pygame.sprite.Group() 
    coleccionable_group = pygame.sprite.Group() 
    
    # DEFINICIÓN DE OBSTÁCULOS
    obstaculos_coords = [
        (1, 82, 1269, 19),
        (1269, 99, 17, 619),
        (1, 707, 1279, 13),
        (0, 119, 7, 586),
        #OBSTACULO MESAS
        (102, 142, 135, 49),#1
        (316, 142, 290, 46),#2
        (702, 142, 154, 42 ),#3
        (926, 155, 316, 34),#4
        (1199, 193, 60, 160),#5
        (1042, 295, 151, 48),#6
        (865, 286, 59, 152),#7
        (707, 399, 158, 49),#8
        (510, 401, 86, 42),#9
        (488, 281, 136, 41),#10 
        (256, 281, 135, 41),#11
        (92, 397, 148, 44),#12
        (48, 302, 65, 78),#13.1
        (53, 386, 40, 156),#13.2
        (196, 522, 86, 45),#14
        (365, 502, 63, 126),#15
        (511, 519, 87, 45),#16
        (712, 520, 87, 45),#17
        (895, 517, 137, 46),#18
        (1133, 435, 137, 45),#19
        (1134, 578, 145, 29),#20
        (1181, 562, 89, 15),#20.1
        (923, 644, 138, 41),#21
        (704, 644, 138, 41),#22
        (494, 645, 137, 40),#23
        (281, 644, 147, 44),#24
        (68, 644, 137, 40),#25
    ]
    
    for x, y, w, h in obstaculos_coords:
        obstaculo = Obstaculo(x, y, w, h)
        obstaculo_list.add(obstaculo)
        
    # DEFINICIÓN DE LA META
    meta = Meta(1241, 652, 27, 52)
    meta_group.add(meta)
    
    # COLECCIONABLES (Índices 0-2 BUENOS, 3-5 MALOS)
    coleccionables_coords = [
        (223, 233, 6), 
        (1062, 455, 6), 
        (132, 500, 7), 
        (639, 426, 7),
        (380, 445, 8), 
        (855, 600, 8), 
        # Malos
        (641, 173, 9), 
        (220, 622, 9), 
        (1200, 510, 10), 
        (795, 338, 10), 
        (465, 233, 11), 
        (1047, 242, 11) 
    ]

    for x, y, index in coleccionables_coords:
        coleccionable_group.add(Coleccionable(x, y, index=index))
        
    return obstaculo_list, meta_group, coleccionable_group 


# --- FUNCIÓN DE PRECÁRGALA (sin cambios) ---
def preload_level(ventana, character_data):
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    
    # 1. Cargar Fondo
    try:
        fondo_nivel = pygame.image.load(PATH_FONDO_NIVEL_1).convert()
        fondo_nivel = pygame.transform.scale(fondo_nivel, (ANCHO, ALTO))
    except pygame.error as e:
        fondo_nivel = pygame.Surface((ANCHO, ALTO)); fondo_nivel.fill(AZUL_FALLBACK)
        
    # 2. Inicializar Personaje
    start_position = (24, 224) 
    from player import Player
    player = Player(start_position, character_data, ANCHO, ALTO) 
    player_group = pygame.sprite.Group(player)

    # 3. Carga de obstáculos y coleccionables
    obstaculo_group, meta_group, coleccionable_group = setup_level(player) 
    
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
# FUNCIÓN DEL MENÚ DE PAUSA (sin cambios)
# --------------------------------------------------------------------------
def run_pause_menu(ventana):
    ANCHO, ALTO = ventana.get_size()
    
    fondo_oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    fondo_oscuro.fill(GRIS_OSCURO_PAUSA)
    
    PANEL_W, PANEL_H = 500, 250 
    CENTER_X = ANCHO // 2
    PANEL_X = CENTER_X - PANEL_W // 2
    PANEL_Y = ALTO // 2 - PANEL_H // 2
    
    fondo_pausa_img = None
    try:
        fondo_pausa_img_orig = pygame.image.load(PATH_FONDO_PAUSA).convert_alpha()
        fondo_pausa_img = pygame.transform.scale(fondo_pausa_img_orig, (PANEL_W, PANEL_H))
    except pygame.error as e:
        fondo_pausa_img = pygame.Surface((PANEL_W, PANEL_H)); 
        fondo_pausa_img.fill((80, 80, 80)) 
    
    BTN_W, BTN_H = 100, 100 
    GAP = 20 
    TOTAL_MENU_WIDTH = (BTN_W * 3) + (GAP * 2)
    
    START_X = CENTER_X - (TOTAL_MENU_WIDTH // 2) 
    BUTTON_Y = PANEL_Y + PANEL_H - BTN_H - 30 

    # Botones (usa la clase BotonSimple que ahora está definida)
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
            btn.draw(ventana)

        pygame.display.flip()
        pygame.time.Clock().tick(30) 

# --- FUNCIÓN PRINCIPAL DEL NIVEL 1 (MODIFICADA) ---
def run_level(ventana, precargados, img_btn_regresar, REGRESAR_RECT):
    
    fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group = precargados
    
    ANCHO = ventana.get_width()
    clock = pygame.time.Clock()
    
    btn_pausa = BotonSimple(ANCHO - 60, 20, 40, 40, PATH_BTN_PAUSA, "PAUSE") # Ahora BotonSimple está definido
    
    start_time = time.time() 
    is_paused = False 
    pause_start_time = 0 

    coleccionables_recogidos = 0 
    penalizacion_total = 0 

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
            accion_derrota = run_pantalla_derrota(ventana)
            if accion_derrota[0] == "MENU": return "SELECTOR_NIVEL", None, None 
            return accion_derrota
        
        # ACTUALIZAR Y COLISIONES
        player = player_group.sprites()[0] 
        player_group.update(obstaculo_group) 
        coleccionable_group.update(dt) 
        
        collected_items = pygame.sprite.spritecollide(player, coleccionable_group, True)
        
        # 🚨 LÓGICA CLAVE DE COLECCIONABLES (CORREGIDA para Bonificación de Tiempo y SFX)
        for item in collected_items:
            
            # Usamos get_effect_value() para determinar si es bueno (devuelve > 0.0)
            bonus_speed = item.get_effect_value()
            
            if bonus_speed > 0:
                # 🎊 ¡COLECCIONABLE BUENO! 🎊
                audio_manager.play_collect_good() # 👈 Reproducir SFX bueno
                
                player.increase_speed(bonus_speed) 
                # Ganar tiempo (reducir la penalización total)
                penalizacion_total = max(0, penalizacion_total - TIEMPO_BONIFICACION)
                
                coleccionables_recogidos += 1
                
            else: 
                # 💥 COLECCIONABLE MALO! 💥 (get_effect_value devuelve 0.0)
                audio_manager.play_collect_bad() # 👈 Reproducir SFX malo
                
                penalizacion_total += TIEMPO_PENALIZACION
            
        # DETECCIÓN DE META CONDICIONAL
        if pygame.sprite.spritecollide(player, meta_group, False):
            running = False 
            audio_manager.stop_music()
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