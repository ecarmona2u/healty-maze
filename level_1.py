# level_1.py 

import pygame
from player import Player 
from obstaculo import Obstaculo 
from meta import Meta 
from ganaste_entre_nivel import run_pantalla_ganaste 
from pantalla_derrota import run_pantalla_derrota, RETURN_REINTENTAR 
from coleccionable import Coleccionable 
import sys
import time 
import loading_screen 

# --- CONSTANTES ---
PATH_FONDO_NIVEL_1 = "recursos/FondoNivel1.jpg" 
AZUL_FALLBACK = (50, 50, 150)
NUM_COLECCIONABLES_REQUERIDOS = 6 
TIEMPO_LIMITE_SEGUNDOS = 30 
TIEMPO_PENALIZACION = 3

# --- CONSTANTES DE PAUSA ---
PATH_BTN_PAUSA = "recursos/btn_pausa.png"
PATH_BTN_PLAY = "recursos/btn_play.png"
PATH_BTN_MENU_PAUSA = "recursos/btn_menu_pausa.png"
PATH_BTN_REINICIAR = "recursos/btn_reiniciar.png"

# 🟢 NUEVA CONSTANTE PARA EL FONDO DEL MENÚ DE PAUSA
PATH_FONDO_PAUSA = "recursos/fondo_menu_pausa.png" 

# Colores para la UI
VERDE_BARRA = (0, 200, 0)
ROJO_BARRA = (200, 0, 0)
GRIS_FONDO = (50, 50, 50)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
GRIS_OSCURO_PAUSA = (0,0,0,0) # Semi-transparente para oscurecer el nivel (Actualmente transparente)


# --- CLASE BOTON SIMPLE (Sin cambios) ---
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

# --- FUNCIÓN PARA CONFIGURAR EL NIVEL (Sin cambios) ---
def setup_level(player):
    """Crea y posiciona los obstáculos, la meta y los coleccionables del nivel."""
    obstaculo_list = pygame.sprite.Group()
    meta_group = pygame.sprite.Group() 
    coleccionable_group = pygame.sprite.Group() 
    
    # DEFINICIÓN DE OBSTÁCULOS (Sin cambios) 
    obstaculos_coords = [
        (0, 110, 955, 20), 
        (1116, 110, 164, 20), 
        (0, 129, 13, 700), 
        (1262, 129, 16, 700), 
        (0, 700, 1280, 20), 
        (94, 213, 73, 72), 
        (94, 213, 229, 20), 
        (251, 213, 73, 178),
        (13, 371, 240, 20),
        (488, 128, 73, 309), 
        (551, 417, 246, 20), 
        (724, 417, 73, 174),
        (330, 519, 467, 20), 
        (330, 534, 73, 55), 
        (93, 571, 310, 20),
        (93, 467, 73, 124), 
        (488, 639, 73, 67),
        (1116, 127, 73, 105), 
        (646, 212, 472, 20), 
        (646, 225, 73, 110),
        (711, 315, 321, 20),
        (1116, 315, 73, 122), 
        (880, 417, 240, 20), 
        (880, 432, 73, 157),
        (1188, 571, 73, 20), 
        (1032, 572, 73, 132)
    ]
    
    for x, y, w, h in obstaculos_coords:
        obstaculo = Obstaculo(x, y, w, h)
        obstaculo_list.add(obstaculo)
        
    # DEFINICIÓN DE LA META
    meta = Meta(955, 100, 160, 17)
    meta_group.add(meta)
    
    # COLECCIONABLES NORMALES (12 objetos, 6 tipos x 2, índices 0 a 5)
    coleccionables_coords = [
        (24, 186, 0), 
        (347, 217, 3),
        (257, 644, 1),
        (595, 628, 5),
        (807, 391, 2),
        (574, 191, 4)
    ]

    # COLECCIONABLES DE PENALIZACIÓN (3 objetos, usando índices 6, 7 y 8)
    penalizacion_coords = [
        (430, 416, 6), 
        (186, 510, 7),  
        (974, 648, 8),
        (1192, 524, 7),
        (1021, 277, 6),
        (1207, 205, 8)
    ]

    todos_coleccionables = coleccionables_coords + penalizacion_coords
    
    for x, y, index in todos_coleccionables:
        coleccionable_group.add(Coleccionable(x, y, index=index))
        
    return obstaculo_list, meta_group, coleccionable_group 

# --- FUNCIÓN DE PRECÁRGALA (Sin cambios) ---
def preload_level(ventana, character_data):
    """Carga y devuelve todos los recursos necesarios para run_level, excepto el bucle de juego."""
    # ... (código preload_level sin cambios) ...
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
    # NOTA: Player debe ser importado (ya lo está)
    from player import Player
    player = Player(start_position, character_data, ANCHO, ALTO) 
    player_group = pygame.sprite.Group(player)

    # 3. Carga de obstáculos y coleccionables
    obstaculo_group, meta_group, coleccionable_group = setup_level(player) 
    
    # 4. Devolver todos los elementos
    return fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group


# --- FUNCIÓN DE DIBUJO DE UI (Sin cambios) ---
def draw_ui(ventana, remaining_time, max_time, collected, required):
    # ... (código draw_ui sin cambios) ...
    ANCHO, ALTO = ventana.get_size()
    
    # 1. BARRA DE TIEMPO
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
    
    # 2. CONTADOR DE OBJETOS
    font_items = pygame.font.SysFont('Arial', 30, bold=True)
    item_text = f"Objetos: {collected} / {required}"
    
    item_color = AMARILLO if collected < required else VERDE_BARRA
    
    item_surface = font_items.render(item_text, True, item_color)
    
    ventana.blit(item_surface, (BAR_X, BAR_Y + BAR_HEIGHT + 10))

# --------------------------------------------------------------------------
# 🟢 FUNCIÓN DEL MENÚ DE PAUSA MODIFICADA (Botones intercambiados y BTN_H corregido)
# --------------------------------------------------------------------------
def run_pause_menu(ventana):
    ANCHO, ALTO = ventana.get_size()
    
    # 1. Fondo Oscuro (para oscurecer el nivel detrás del menú)
    fondo_oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    fondo_oscuro.fill(GRIS_OSCURO_PAUSA)
    
    # 2. Parámetros del Panel del Menú (La caja donde va la imagen)
    PANEL_W, PANEL_H = 500, 250 
    CENTER_X = ANCHO // 2
    PANEL_X = CENTER_X - PANEL_W // 2
    PANEL_Y = ALTO // 2 - PANEL_H // 2
    
    # 3. Cargar y escalar la Imagen de Fondo de Pausa
    fondo_pausa_img = None
    try:
        fondo_pausa_img_orig = pygame.image.load(PATH_FONDO_PAUSA).convert_alpha()
        fondo_pausa_img = pygame.transform.scale(fondo_pausa_img_orig, (PANEL_W, PANEL_H))
    except pygame.error as e:
        print(f"Error cargando fondo de pausa: {e}")
        fondo_pausa_img = pygame.Surface((PANEL_W, PANEL_H)); 
        fondo_pausa_img.fill((80, 80, 80)) 
    
    # 4. Posicionamiento de Botones (Centrados en el panel)
    # 🟢 CORRECCIÓN: BTN_H se establece en 50 para que el botón sea visible y funcional.
    BTN_W, BTN_H = 100, 100 
    GAP = 20 
    TOTAL_MENU_WIDTH = (BTN_W * 3) + (GAP * 2)
    
    START_X = CENTER_X - (TOTAL_MENU_WIDTH // 2) 
    
    # Posición Y de los botones (Cerca del fondo del panel, ajusta el 30 si es necesario)
    BUTTON_Y = PANEL_Y + PANEL_H - BTN_H - 30 

    # 🟢 SWAP: El botón MENU ahora está en START_X (izquierda)
    btn_menu = BotonSimple(START_X, BUTTON_Y, BTN_W, BTN_H, PATH_BTN_MENU_PAUSA, "MENU")
    
    # RESTART (se mantiene en el centro)
    btn_restart = BotonSimple(START_X + BTN_W + GAP, BUTTON_Y, BTN_W, BTN_H, PATH_BTN_REINICIAR, "REINTENTAR")
    
    # 🟢 SWAP: El botón CONTINUE ahora está en START_X + (BTN_W + GAP) * 2 (derecha)
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

        # Dibuja: 1. Oscuridad 2. Imagen del Menú 3. Botones
        ventana.blit(fondo_oscuro, (0, 0))
        ventana.blit(fondo_pausa_img, (PANEL_X, PANEL_Y))
        
        for btn in botones:
            btn.draw(ventana)

        pygame.display.flip()
        pygame.time.Clock().tick(30) 

# --- FUNCIÓN PRINCIPAL DEL NIVEL MODIFICADA (Sin cambios en lógica) ---
def run_level(ventana, precargados, img_btn_regresar, REGRESAR_RECT):
    """Recibe recursos precargados e inicia el bucle del juego."""
    
    # Desempaquetar los recursos precargados
    fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group = precargados
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    btn_pausa = BotonSimple(ANCHO - 60, 20, 40, 40, PATH_BTN_PAUSA, "PAUSE")
    
    # --- 1. INICIO DEL JUEGO REAL ---
    start_time = time.time() 
    is_paused = False 
    pause_start_time = 0 # 🟢 Inicializa el contador de inicio de pausa

    coleccionables_recogidos = 0 
    elapsed_time = 0 
    penalizacion_total = 0 

    running = True
    while running:
        
        elapsed_time = time.time() - start_time + penalizacion_total
        remaining_time = max(0, TIEMPO_LIMITE_SEGUNDOS - elapsed_time)
        
        # 1. MANEJO DE EVENTOS
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            # 🟢 Captura el inicio de la pausa
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
            
            # Dibuja el estado congelado del nivel
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
                
                # ARREGLO DEL TIEMPO: Congela el cronómetro ajustando el tiempo de inicio
                pause_duration = time.time() - pause_start_time
                start_time += pause_duration 
                
            elif accion_pausa == "REINTENTAR":
                return "REINTENTAR", None, None
            elif accion_pausa == "MENU":
                return "MENU", None, None 
                
            continue 

        # 3. LÓGICA DEL JUEGO 
        
        #CONDICIÓN DE DERROTA POR TIEMPO
        if remaining_time <= 0:
            running = False
            accion = run_pantalla_derrota(ventana)
            if accion == "MENU":
                return "MENU", None, None 
            elif accion == "REINTENTAR":
                return "REINTENTAR", None, None
        
        # ACTUALIZAR Y COLISIONES CON COLECCIONABLES
        player = player_group.sprites()[0] 
        player_group.update(obstaculo_group) 
        
        collected_items = pygame.sprite.spritecollide(player, coleccionable_group, True)
        for item in collected_items:
            
            #Lógica de penalización: Índices 6, 7 y 8
            if hasattr(item, 'index') and item.index in [6, 7, 8]:
                penalizacion_total += TIEMPO_PENALIZACION
            else:
                # Coleccionables normales (Índices 0 a 5)
                coleccionables_recogidos += 1
            
        # DETECCIÓN DE META CONDICIONAL
        if pygame.sprite.spritecollide(player, meta_group, False):
            if coleccionables_recogidos >= NUM_COLECCIONABLES_REQUERIDOS:
                running = False 
                return run_pantalla_ganaste(ventana, img_btn_regresar, REGRESAR_RECT) 
            else:
                running = False 
                accion = run_pantalla_derrota(ventana)
                if accion == "MENU":
                    return "MENU", None, None 
                elif accion == "REINTENTAR":
                    return "REINTENTAR", None, None
                
        # 4. Dibujar
        ventana.blit(fondo_nivel, (0, 0)) 
        player_group.draw(ventana)
        obstaculo_group.draw(ventana) 
        coleccionable_group.draw(ventana) 
        meta_group.draw(ventana)

        draw_ui(ventana, remaining_time, TIEMPO_LIMITE_SEGUNDOS, coleccionables_recogidos, NUM_COLECCIONABLES_REQUERIDOS)
        
        btn_pausa.draw(ventana)
        
        pygame.display.flip()
        clock.tick(60)

    return "MENU", None, None