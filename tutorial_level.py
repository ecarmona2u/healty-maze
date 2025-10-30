# tutorial_level.py

import pygame
from player import Player 
from obstaculo import Obstaculo 
from meta import Meta 
from tutorial_win_screen import run_pantalla_tutorial_win, RETURN_LEVEL_1, RETURN_MENU 
from coleccionable import Coleccionable 
import sys
import time 
from audio_manager import audio_manager # Importación correcta del gestor de audio

# --- CONSTANTES DE NIVEL ESPECÍFICAS DEL TUTORIAL ---
PATH_FONDO_TUTORIAL = "recursos/FondoTutorial.png" 
AZUL_FALLBACK = (50, 50, 150)
NUM_COLECCIONABLES_REQUERIDOS = 2 
TIEMPO_LIMITE_SEGUNDOS = 30
TIEMPO_PENALIZACION = 3 

# --- CONSTANTES DE PAUSA (Completas y Corregidas) ---
PATH_BTN_PAUSA = "recursos/btn_pausa.png"
PATH_BTN_PLAY = "recursos/btn_play.png"
PATH_BTN_MENU_PAUSA = "recursos/btn_menu.png"
PATH_BTN_REINICIAR = "recursos/btn_reiniciar.png"
PATH_FONDO_PAUSA = "recursos/fondo_menu_pausa.png" 
# Colores UI
VERDE_BARRA = (0, 200, 0)
ROJO_BARRA = (200, 0, 0)
GRIS_FONDO = (50, 50, 50)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
GRIS_OSCURO_PAUSA = (0,0,0,0) 

# --- CLASE BOTON SIMPLE (Copia de seguridad) ---
class BotonSimple:
    def __init__(self, x, y, width, height, path, action):
        self.action = action
        try:
            self.image_original = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image_original, (width, height))
        except pygame.error:
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

# --- FUNCIÓN PARA CONFIGURAR EL NIVEL TUTORIAL (sin cambios funcionales) ---
def setup_tutorial_level(player):
    obstaculo_list = pygame.sprite.Group()
    meta_group = pygame.sprite.Group() 
    coleccionable_group = pygame.sprite.Group() 
    
    obstaculos_coords = [
        (0, 110, 955, 20), (1116, 110, 164, 20), (0, 129, 13, 700), 
        (1262, 129, 16, 700), (0, 700, 1280, 20), (14, 207, 707, 20),
        (648, 224, 73, 310), (716, 514, 91, 20), (803, 119, 73, 415),
        (14, 322, 547, 20), (489, 337, 73, 363), (971, 222, 73, 478),
        (1036, 222, 227, 20)
    ]
    
    for x, y, w, h in obstaculos_coords:
        obstaculo = Obstaculo(x, y, w, h)
        obstaculo_list.add(obstaculo)
        
    meta = Meta(955, 100, 160, 17)
    meta_group.add(meta)
    
    coleccionables_coords = [
        (576, 295, 0),  (894, 219, 2),  # Buenos
        (725, 639, 3), # Malo
    ]

    for x, y, index in coleccionables_coords:
        coleccionable_group.add(Coleccionable(x, y, index=index))
        
    return obstaculo_list, meta_group, coleccionable_group 

# --- FUNCIÓN DE PRECÁRGALA (sin cambios funcionales) ---
def preload_tutorial_level(ventana, character_data):
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    
    try:
        fondo_nivel = pygame.image.load(PATH_FONDO_TUTORIAL).convert()
        fondo_nivel = pygame.transform.scale(fondo_nivel, (ANCHO, ALTO))
    except pygame.error as e:
        fondo_nivel = pygame.Surface((ANCHO, ALTO)); fondo_nivel.fill(AZUL_FALLBACK)
        
    start_position = (30, 250) 
    player = Player(start_position, character_data, ANCHO, ALTO) 
    player_group = pygame.sprite.Group(player)

    obstaculo_group, meta_group, coleccionable_group = setup_tutorial_level(player) 
    
    return fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group


# --- FUNCIÓN DE DIBUJO DE UI (sin cambios) ---
def draw_ui(ventana, remaining_time, max_time, collected, required):
    ANCHO, ALTO = ventana.get_size()
    
    BAR_WIDTH = 300; BAR_HEIGHT = 20; BAR_X = 20; BAR_Y = 20
    time_ratio = remaining_time / max_time
    current_width = int(BAR_WIDTH * time_ratio)
    bar_color = VERDE_BARRA if remaining_time > 10 else ROJO_BARRA

    pygame.draw.rect(ventana, GRIS_FONDO, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 0, 5)
    pygame.draw.rect(ventana, bar_color, (BAR_X, BAR_Y, current_width, BAR_HEIGHT), 0, 5)

    font_timer = pygame.font.SysFont('Arial', 20, bold=True)
    time_text = f"{int(remaining_time)}"
    timer_surface = font_timer.render(time_text, True, BLANCO)
    ventana.blit(timer_surface, (BAR_X + BAR_WIDTH + 10, BAR_Y))
    
    font_items = pygame.font.SysFont('Arial', 30, bold=True)
    item_text = f"Objetos: {collected} / {required}"
    item_color = AMARILLO if collected < required else VERDE_BARRA
    item_surface = font_items.render(item_text, True, item_color)
    
    ventana.blit(item_surface, (BAR_X, BAR_Y + BAR_HEIGHT + 10))

# --- FUNCIÓN DEL MENÚ DE PAUSA ---
def run_pause_menu(ventana):
    ANCHO, ALTO = ventana.get_size()
    fondo_oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    fondo_oscuro.fill(GRIS_OSCURO_PAUSA) 
    
    PANEL_W, PANEL_H = 500, 250 
    CENTER_X = ANCHO // 2; PANEL_X = CENTER_X - PANEL_W // 2; PANEL_Y = ALTO // 2 - PANEL_H // 2
    
    COLOR_FIJO_PAUSA = (120, 120, 120) 
    
    try:
        fondo_pausa_img_orig = pygame.image.load(PATH_FONDO_PAUSA).convert_alpha()
        fondo_pausa_img = pygame.transform.scale(fondo_pausa_img_orig, (PANEL_W, PANEL_H))
    except pygame.error:
        fondo_pausa_img = pygame.Surface((PANEL_W, PANEL_H)); fondo_pausa_img.fill(COLOR_FIJO_PAUSA)
        
    BTN_W, BTN_H = 100, 100 
    GAP = 20 
    TOTAL_MENU_WIDTH = (BTN_W * 3) + (GAP * 2)
    START_X = CENTER_X - (TOTAL_MENU_WIDTH // 2) 
    BUTTON_Y = PANEL_Y + PANEL_H - BTN_H - 30 

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
            # 🚨 CORRECCIÓN CLAVE: ESC en el menú solo retorna "CONTINUE"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "CONTINUE"

        ventana.blit(fondo_oscuro, (0, 0))
        ventana.blit(fondo_pausa_img, (PANEL_X, PANEL_Y))
        
        for btn in botones:
            btn.draw(ventana)

        pygame.display.flip()
        pygame.time.Clock().tick(30) 

# --- FUNCIÓN PRINCIPAL DEL NIVEL TUTORIAL (CORREGIDA) ---
def run_tutorial_level(ventana, precargados, img_btn_regresar, REGRESAR_RECT):
    
    fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group = precargados
    
    ANCHO = ventana.get_width()
    clock = pygame.time.Clock()
    
    btn_pausa = BotonSimple(ANCHO - 60, 20, 40, 40, PATH_BTN_PAUSA, "PAUSE")
    
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
            # 🚨 CORRECCIÓN DE PAUSA: Solo pausa si NO está ya en pausa
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not is_paused: 
                is_paused = True
                pause_start_time = time.time()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if btn_pausa.check_click(mouse_pos) == "PAUSE" and not is_paused:
                    is_paused = True
                    pause_start_time = time.time()

        # 2. LÓGICA DE PAUSA (CON AUDIO)
        if is_paused:
            audio_manager.pause_music() # PAUSA la música (corregido en audio_manager.py)
            
            # Dibujar estado congelado
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
                audio_manager.unpause_music() # REANUDAR la música
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
            return "SELECTOR_NIVEL", None, None
        
        player = player_group.sprites()[0] 
        player_group.update(obstaculo_group) 
        coleccionable_group.update(dt) # Actualización de animación

        collected_items = pygame.sprite.spritecollide(player, coleccionable_group, True)
        for item in collected_items:
            if hasattr(item, 'index') and item.index in [3, 4, 5]:
                penalizacion_total += TIEMPO_PENALIZACION
            else:
                coleccionables_recogidos += 1
            
        # CONDICIÓN DE META
        if pygame.sprite.spritecollide(player, meta_group, False):
            running = False 
            audio_manager.stop_music()
            if coleccionables_recogidos >= NUM_COLECCIONABLES_REQUERIDOS:
                return run_pantalla_tutorial_win(ventana, img_btn_regresar, REGRESAR_RECT) 
            else:
                return "SELECTOR_NIVEL", None, None
                
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