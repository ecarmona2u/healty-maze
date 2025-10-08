# selector_personaje.py

import pygame
import sys
# Asegúrate de tener la clase Player disponible
from player import Player 

# --- CONSTANTES ---
IMG_SIZE_DISPLAY = (500, 400) # Tamaño para la vista previa
IMG_SIZE_GAME = (60, 60)     # Tamaño para el juego real (player.py)
COLOR_RESALTE = (255, 255, 0)

# Rutas
PATH_FONDO_SELECTOR_PERSONAJE = "recursos/fondo_seleccionar_personaje.png"
PATH_BTN_CONFIRMAR_NORMAL = "recursos/botones/btn_confirmar.png"
PATH_BTN_REGRESAR = "recursos/botones/btn_regresar.png" 
PATH_ANIMACIONES = "recursos/animaciones/"
#Nueva constante para las imágenes de menú
PATH_IMAGENES_MENU = "recursos/imagenes_menu_perso/"

# Datos de Personajes (MODIFICADO para incluir la ruta de la imagen de menú)
PERSONAJES_DATA = {
    "chica": {
        "name": "Chica",
        #Ruta de la imagen para el menú de selección
        "menu_img": f"{PATH_IMAGENES_MENU}chica_menu.png",
        "anim": {
            "front": [f"{PATH_ANIMACIONES}chica/idle_front_{i:02d}.png" for i in range(1, 5)], 
            "back": [f"{PATH_ANIMACIONES}chica/idle_back_{i:02d}.png" for i in range(1, 5)],
            "left": [f"{PATH_ANIMACIONES}chica/idle_left_{i:02d}.png" for i in range(1, 5)],
            "right": [f"{PATH_ANIMACIONES}chica/idle_right_{i:02d}.png" for i in range(1, 5)],
        }
    },
    "chico": {
        "name": "Chico",
        #Ruta de la imagen para el menú de selección
        "menu_img": f"{PATH_IMAGENES_MENU}chico_menu.png",
        "anim": {
            "front": [f"{PATH_ANIMACIONES}chico/idle_front_{i:02d}.png" for i in range(1, 5)], 
            "back": [f"{PATH_ANIMACIONES}chico/idle_back_{i:02d}.png" for i in range(1, 5)],
            "left": [f"{PATH_ANIMACIONES}chico/idle_left_{i:02d}.png" for i in range(1, 5)],
            "right": [f"{PATH_ANIMACIONES}chico/idle_right_{i:02d}.png" for i in range(1, 5)],
        }
    }
}

# --- FUNCIONES ---

def cargar_sprites_movimiento(personaje_id, size):
    """Carga y escala todos los frames de las animaciones de un personaje.
       (Se mantiene igual, sigue cargando animaciones para el juego)."""
    sprites = {}
    data = PERSONAJES_DATA[personaje_id]
    
    for direction, paths in data['anim'].items():
        sprites[direction] = []
        for path in paths:
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, size)
                sprites[direction].append(img)
            except pygame.error as e:
                # Fallback sin texto de debug
                fallback_img = pygame.Surface(size, pygame.SRCALPHA)
                fallback_img.fill((255, 0, 0, 150))
                sprites[direction].append(fallback_img)
    return sprites


def run_selector_personaje(ventana):
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    pygame.font.init()
    
    # --- CARGA DE RECURSOS ---
    
    # 1. Cargar Fondo
    try:
        fondo_original = pygame.image.load(PATH_FONDO_SELECTOR_PERSONAJE).convert()
        fondo_selector = pygame.transform.scale(fondo_original, (ANCHO, ALTO))
    except pygame.error:
        fondo_selector = pygame.Surface((ANCHO, ALTO)); fondo_selector.fill((10, 10, 50)) 

    # 2. Imágenes de personajes (MODIFICADO para usar la nueva ruta 'menu_img')
    imagenes_personajes_normal = {}
    for id, data in PERSONAJES_DATA.items():
        #CAMBIO AQUÍ: Usamos la nueva clave 'menu_img' en lugar del primer frame de la animación.
        path_menu_img = data["menu_img"] 
        try:
            img_normal = pygame.image.load(path_menu_img).convert_alpha()
            imagenes_personajes_normal[id] = pygame.transform.scale(img_normal, IMG_SIZE_DISPLAY)
        except pygame.error as e:
            # Fallback si la imagen estática no se encuentra
            fallback_normal = pygame.Surface(IMG_SIZE_DISPLAY); fallback_normal.fill((255, 100, 100)) 
            imagenes_personajes_normal[id] = fallback_normal
            
    # 3. Botones (Regresar y Confirmar)
    # Botón Regresar (arriba izquierda)
    BTN_REGRESAR_SIZE = (50, 50)
    REGRESAR_RECT = pygame.Rect(10, 10, BTN_REGRESAR_SIZE[0], BTN_REGRESAR_SIZE[1])
    try:
        img_regresar = pygame.image.load(PATH_BTN_REGRESAR).convert_alpha()
        img_regresar = pygame.transform.scale(img_regresar, BTN_REGRESAR_SIZE)
    except pygame.error:
        img_regresar = pygame.Surface(BTN_REGRESAR_SIZE); img_regresar.fill((150, 0, 0))

    # Botón Confirmar (abajo derecha)
    BTN_CONFIRMAR_SIZE = (150, 50)
    CONFIRMAR_RECT = pygame.Rect(ANCHO - 160, ALTO - 60, BTN_CONFIRMAR_SIZE[0], BTN_CONFIRMAR_SIZE[1])
    try:
        img_confirmar = pygame.image.load(PATH_BTN_CONFIRMAR_NORMAL).convert_alpha()
        img_confirmar = pygame.transform.scale(img_confirmar, BTN_CONFIRMAR_SIZE)
    except pygame.error:
        img_confirmar = pygame.Surface(BTN_CONFIRMAR_SIZE); img_confirmar.fill((0, 150, 0))


    # 4. Coordenadas de los personajes
    personaje_rects = {}
    pos_chica = (ANCHO // 2 - IMG_SIZE_DISPLAY[0] - 50, ALTO // 2 - IMG_SIZE_DISPLAY[1] // 2 + 50)
    pos_chico = (ANCHO // 2 + 50, ALTO // 2 - IMG_SIZE_DISPLAY[1] // 2 + 50)
    
    personaje_rects['chica'] = imagenes_personajes_normal['chica'].get_rect(topleft=pos_chica)
    personaje_rects['chico'] = imagenes_personajes_normal['chico'].get_rect(topleft=pos_chico)
    
    # 5. Estado de selección
    personaje_seleccionado = 'chica' # Inicial por defecto
    
    # --- BUCLE PRINCIPAL ---
    seleccion_activa = True
    while seleccion_activa:
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # Clic en REGRESAR
                if REGRESAR_RECT.collidepoint(mouse_pos):
                    return None 
                
                # Clic en CONFIRMAR
                if CONFIRMAR_RECT.collidepoint(mouse_pos):
                    seleccion_activa = False 
                    
                # Clic en personajes
                for id, rect in personaje_rects.items():
                    if rect.collidepoint(mouse_pos):
                        personaje_seleccionado = id

        # --- DIBUJO ---
        ventana.blit(fondo_selector, (0, 0))

        # Dibujar personajes
        for id, img in imagenes_personajes_normal.items():
            rect = personaje_rects[id]
            
            # Resaltado del seleccionado
            if id == personaje_seleccionado:
                pygame.draw.rect(ventana, COLOR_RESALTE, rect.inflate(10, 10), 3) 
            
            ventana.blit(img, rect)
            
        # Dibujar botones estáticos
        ventana.blit(img_regresar, REGRESAR_RECT)
        ventana.blit(img_confirmar, CONFIRMAR_RECT)
        
        # Resaltado de botones (hover)
        if CONFIRMAR_RECT.collidepoint(mouse_pos):
            pygame.draw.rect(ventana, COLOR_RESALTE, CONFIRMAR_RECT.inflate(10, 10), 3)

        pygame.display.flip()
        clock.tick(60)
        
    # --- SALIDA DEL BUCLE ---
    # Esto sigue cargando las animaciones (sprites) para el juego.
    sprites_movimiento = cargar_sprites_movimiento(personaje_seleccionado, IMG_SIZE_GAME)
    
    return {
        "id": personaje_seleccionado, 
        "sprites": sprites_movimiento
    }