import pygame
import sys
# Asegúrate de tener la clase Player disponible
from player import Player 

# --- CONSTANTES ---
IMG_SIZE_DISPLAY = (507, 300) # Tamaño para la vista previa
IMG_SIZE_GAME = (60, 60)     # Tamaño para el juego real (player.py)
# COLOR_RESALTE (Ya no es necesario, pero lo mantenemos por si se quiere un 'hover')
COLOR_RESALTE = (255, 255, 0)

# Constantes para la animación del selector
GROWTH_PX_HOVER = 20    # Crecimiento total al pasar el mouse (hover)
ANIMATION_MAX_PX = 0   # Máximo crecimiento para la animación de reposo (pulsante)
ANIMATION_SPEED = 0.2   # Velocidad de la animación

# Rutas
PATH_FONDO_SELECTOR_PERSONAJE = "recursos/fondo_seleccionar_personaje.png"
PATH_BTN_REGRESAR = "recursos/botones/btn_regresar.png" 
PATH_ANIMACIONES = "recursos/animaciones/"
PATH_IMAGENES_MENU = "recursos/imagenes_menu_perso/"

# Datos de Personajes (Mantenemos igual)
PERSONAJES_DATA = {
    "chica": {
        "name": "Chica",
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
       (Se mantiene igual)"""
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

def actualizar_animacion_personajes(personajes_data, mouse_pos):
    """Actualiza el estado de animación de los personajes que NO están en hover."""
    for id, data in personajes_data.items():
        rect_normal = data['normal_rect']
        
        # Solo animar si el mouse NO está encima
        if not rect_normal.collidepoint(mouse_pos):
            offset = data['anim_offset'] + data['anim_direction'] * ANIMATION_SPEED
            
            # Invertir dirección si llega al límite superior
            if offset >= ANIMATION_MAX_PX:
                offset = ANIMATION_MAX_PX
                data['anim_direction'] = -1
            
            # Invertir dirección si llega al límite inferior (0px, tamaño normal)
            elif offset <= 0:
                offset = 0
                data['anim_direction'] = 1
                
            data['anim_offset'] = offset


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

    # 2. Inicialización de Personajes (Incluye estados de Animación/Hover)
    personaje_data_state = {}
    
    pos_chica = (ANCHO // 2 - IMG_SIZE_DISPLAY[0] - 50, ALTO // 2 - IMG_SIZE_DISPLAY[1] // 2 + 10)
    pos_chico = (ANCHO // 2 + 50, ALTO // 2 - IMG_SIZE_DISPLAY[1] // 2 + 10)
    posiciones = {'chica': pos_chica, 'chico': pos_chico}

    for id, data in PERSONAJES_DATA.items():
        path_menu_img = data["menu_img"] 
        pos = posiciones[id]
        
        try:
            imagen = pygame.image.load(path_menu_img).convert_alpha()

            # 2.1. Estado Normal
            image_normal = pygame.transform.scale(imagen, IMG_SIZE_DISPLAY)
            rect_normal = image_normal.get_rect(topleft=pos)

            # 2.2. Estado Hover (GROWTH_PX_HOVER más grande)
            size_hover = (IMG_SIZE_DISPLAY[0] + GROWTH_PX_HOVER, IMG_SIZE_DISPLAY[1] + GROWTH_PX_HOVER)
            image_hover = pygame.transform.scale(imagen, size_hover)
            
            # Recalcular la posición para centrar el botón en hover
            pos_hover = (pos[0] - GROWTH_PX_HOVER // 2, pos[1] - GROWTH_PX_HOVER // 2)
            rect_hover = image_hover.get_rect(topleft=pos_hover)

            personaje_data_state[id] = {
                'normal_image': image_normal,
                'normal_rect': rect_normal,
                'hover_image': image_hover,
                'hover_rect': rect_hover,
                # ESTADOS DE ANIMACIÓN
                'anim_offset': 0.0,      
                'anim_direction': 1,     
            }
        except pygame.error:
             # Fallback (sin cambios en la imagen, solo el rect normal para clics)
            fallback_normal = pygame.Surface(IMG_SIZE_DISPLAY); fallback_normal.fill((255, 100, 100)) 
            rect_normal = fallback_normal.get_rect(topleft=pos)
            
            personaje_data_state[id] = {
                'normal_image': fallback_normal,
                'normal_rect': rect_normal,
                'hover_image': fallback_normal, # Usar normal como hover en fallback
                'hover_rect': rect_normal,
                'anim_offset': 0.0,      
                'anim_direction': 1, 
            }
            
    # 3. Botón Regresar (Preparamos los estados Normal y Hover)
    BTN_REGRESAR_SIZE = (50, 50)
    REGRESAR_RECT_NORMAL = pygame.Rect(10, 10, BTN_REGRESAR_SIZE[0], BTN_REGRESAR_SIZE[1])
    
    # Calculamos el tamaño y posición del hover
    BTN_REGRESAR_SIZE_HOVER = (BTN_REGRESAR_SIZE[0] + GROWTH_PX_HOVER, BTN_REGRESAR_SIZE[1] + GROWTH_PX_HOVER)
    REGRESAR_POS_HOVER = (10 - GROWTH_PX_HOVER // 2, 10 - GROWTH_PX_HOVER // 2)
    REGRESAR_RECT_HOVER = pygame.Rect(REGRESAR_POS_HOVER[0], REGRESAR_POS_HOVER[1], BTN_REGRESAR_SIZE_HOVER[0], BTN_REGRESAR_SIZE_HOVER[1])
    
    try:
        img_regresar_base = pygame.image.load(PATH_BTN_REGRESAR).convert_alpha()
        img_regresar_normal = pygame.transform.scale(img_regresar_base, BTN_REGRESAR_SIZE)
        img_regresar_hover = pygame.transform.scale(img_regresar_base, BTN_REGRESAR_SIZE_HOVER)
    except pygame.error:
        img_regresar_normal = pygame.Surface(BTN_REGRESAR_SIZE); img_regresar_normal.fill((150, 0, 0))
        img_regresar_hover = pygame.Surface(BTN_REGRESAR_SIZE_HOVER); img_regresar_hover.fill((150, 0, 0))

    # 4. Estado de selección
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
                if REGRESAR_RECT_NORMAL.collidepoint(mouse_pos):
                    # Retorna None para volver al menú anterior
                    return None 
                
                # Clic en personajes: SELECCIÓN INMEDIATA
                for id, data in personaje_data_state.items():
                    # Usamos el rect normal para el área de clic
                    if data['normal_rect'].collidepoint(mouse_pos):
                        personaje_seleccionado = id
                        seleccion_activa = False 
                        break 
                
        # --- LÓGICA DE ANIMACIÓN ---
        actualizar_animacion_personajes(personaje_data_state, mouse_pos)

        # --- DIBUJO ---
        ventana.blit(fondo_selector, (0, 0))

        # Dibujar personajes (con Animación o Hover)
        personaje_actualmente_seleccionado = None

        for id, data in personaje_data_state.items():
            rect_normal = data['normal_rect']
            
            if rect_normal.collidepoint(mouse_pos):
                # 1. ESTADO HOVER (Crecimiento estático)
                imagen = data['hover_image'] 
                rect = data['hover_rect']
            else:
                # 2. ESTADO ANIMADO (Pulso suave)
                current_offset = data['anim_offset']
                
                # 2.1. Calcular el nuevo tamaño
                size_normal = rect_normal.size
                new_w = size_normal[0] + current_offset
                new_h = size_normal[1] + current_offset
                
                # 2.2. Reescalar la imagen
                imagen = pygame.transform.scale(data['normal_image'], (int(new_w), int(new_h)))

                # 2.3. Calcular la nueva posición para centrar
                pos_normal = rect_normal.topleft
                new_x = pos_normal[0] - current_offset / 2
                new_y = pos_normal[1] - current_offset / 2
                
                rect = imagen.get_rect(topleft=(new_x, new_y))

            ventana.blit(imagen, rect)
            
            # ELIMINADO: Guardamos el rectángulo del seleccionado, ya sea normal o animado/hover
            # if id == personaje_seleccionado:
            #     personaje_actualmente_seleccionado = rect
        
        # ELIMINADO: Resaltado del seleccionado (marco fijo alrededor de la versión dibujada)
        # if personaje_actualmente_seleccionado:
        #     pygame.draw.rect(ventana, COLOR_RESALTE, personaje_actualmente_seleccionado.inflate(10, 10), 3) 
            
        # Dibujar botón REGRESAR (Solo Hover, sin animación de reposo)
        if REGRESAR_RECT_NORMAL.collidepoint(mouse_pos):
            # Estado Hover
            ventana.blit(img_regresar_hover, REGRESAR_RECT_HOVER)
            # ELIMINADO: Resaltado de botón REGRESAR (hover)
            # pygame.draw.rect(ventana, COLOR_RESALTE, REGRESAR_RECT_HOVER, 3) # Se dibuja con el rect de hover
        else:
            # Estado Normal
            ventana.blit(img_regresar_normal, REGRESAR_RECT_NORMAL)

        pygame.display.flip()
        clock.tick(60)
        
    # --- SALIDA DEL BUCLE ---
    
    # Cargamos los sprites del personaje seleccionado para el juego.
    sprites_movimiento = cargar_sprites_movimiento(personaje_seleccionado, IMG_SIZE_GAME)
    
    return {
        "id": personaje_seleccionado, 
        "sprites": sprites_movimiento
    }