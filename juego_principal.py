import pygame
import sys 
import level_1 
import selector_personaje
import selector_nivel
import ajustes 
import nivel_en_proceso 
from ganaste_entre_nivel import run_pantalla_ganaste 
import loading_screen 

# --- CONFIGURACIÓN GLOBAL ---
pygame.init()
pygame.font.init() 

ANCHO, ALTO = 1280, 720  
surface = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Pygame")
clock = pygame.time.Clock()

# --- CONSTANTES ---
AZUL = (50, 50, 200)

# Paths de las imágenes
PATH_FONDO_MENU = "recursos/fondo_menu.png" 
PATH_INICIAR = "recursos/boton_iniciar.png"
PATH_SALIR = "recursos/boton_salir.png"
PATH_AJUSTES = "recursos/boton_ajustes.png" 

# 💡 AÑADE LA CARGA DE RECURSOS PARA EL BOTÓN DE REGRESO
PATH_BTN_REGRESAR = "recursos/boton_regresar.png" 

# --- ESTADO DE JUEGO ---
estado_actual = 'menu' 
personaje_seleccionado = None
nivel_actual = None

# --- CARGAR IMAGEN DE FONDO DEL MENÚ ---
menu_background_image = None
try:
    fondo_original = pygame.image.load(PATH_FONDO_MENU).convert()
    menu_background_image = pygame.transform.scale(fondo_original, (ANCHO, ALTO))
except pygame.error:
    menu_background_image = pygame.Surface((ANCHO, ALTO))
    menu_background_image.fill((50, 50, 50)) 

# --- DEFINICIÓN Y CARGA DE BOTONES ---
botones_data = [
    {'action': 'iniciar_nivel', 'pos': (590, 260), 'path': PATH_INICIAR, 'size': (100, 100)}, 
    {'action': 'ajustes', 'pos': (14, 9), 'path': PATH_AJUSTES, 'size': (60, 60)}, 
    {'action': 'salir', 'pos': (1215, 10), 'path': PATH_SALIR, 'size': (60, 60)},
]

# Carga del botón de regreso (Necesario para pasar a run_level)
img_btn_regresar = None
REGRESAR_RECT = None
try:
    img_btn_regresar = pygame.image.load(PATH_BTN_REGRESAR).convert_alpha()
    img_btn_regresar = pygame.transform.scale(img_btn_regresar, (50, 50))
    REGRESAR_RECT = img_btn_regresar.get_rect(topleft=(20, 20))
except pygame.error:
    img_btn_regresar = pygame.Surface((50, 50)); img_btn_regresar.fill((200, 50, 50))
    REGRESAR_RECT = img_btn_regresar.get_rect(topleft=(20, 20))


def cargar_y_preparar_botones(data):
    assets = {}
    ROJO = (255, 0, 0)
    for boton in data:
        try:
            imagen = pygame.image.load(boton['path']).convert_alpha()
            imagen_escalada = pygame.transform.scale(imagen, boton['size'])
            rect = imagen_escalada.get_rect(topleft=boton['pos'])
            assets[boton['action']] = {'image': imagen_escalada, 'rect': rect}
        except pygame.error:
            fallback = pygame.Surface(boton['size'])
            fallback.fill(ROJO) 
            assets[boton['action']] = {'image': fallback, 'rect': fallback.get_rect(topleft=boton['pos'])}
    return assets

button_assets = cargar_y_preparar_botones(botones_data)

# -------------------------------------------------------------------------
# FUNCIONES DE LÓGICA Y DIBUJO
# -------------------------------------------------------------------------

def dibujar_menu(ventana, mouse_pos, assets, background_image):
    ventana.blit(background_image, (0, 0)) 
    for action, asset in assets.items():
        rect = asset['rect']
        imagen = asset['image']
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(ventana, AZUL, rect, 3) 
        ventana.blit(imagen, rect)

def manejar_clic_menu(mouse_pos, assets):
    global estado_actual
    for action, asset in assets.items():
        rect = asset['rect']
        if rect.collidepoint(mouse_pos):
            if action == 'iniciar_nivel':
                estado_actual = 'seleccionar_personaje'
                return 
            elif action == 'ajustes':
                estado_actual = 'ajustes'
                return
            elif action == 'salir':
                pygame.quit()
                sys.exit()

# -------------------------------------------------------------------------
# BUCLE PRINCIPAL DEL JUEGO (Máquina de Estados)
# -------------------------------------------------------------------------

while True:
    mouse_pos = pygame.mouse.get_pos()
    event_list = pygame.event.get() # Se obtienen todos los eventos una sola vez por frame

    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #MANEJO DE EVENTOS ESPECÍFICO POR ESTADO
        if estado_actual == 'menu' and event.type == pygame.MOUSEBUTTONDOWN:
            manejar_clic_menu(mouse_pos, button_assets)

# -------------------------------------------------------------------------
# GESTIÓN DE ESTADOS Y DIBUJO
# -------------------------------------------------------------------------

    if estado_actual == 'menu':
        dibujar_menu(surface, mouse_pos, button_assets, menu_background_image)
        
    elif estado_actual == 'ajustes':
        dibujar_menu(surface, mouse_pos, button_assets, menu_background_image) 
        
        accion = ajustes.gestionar_ajustes_modal(surface, event_list, mouse_pos)
        
        if accion == 'cerrar':
            estado_actual = 'menu'

    # 1. ESTADO: SELECCIÓN DE PERSONAJE
    elif estado_actual == 'seleccionar_personaje':
        personaje_data_result = selector_personaje.run_selector_personaje(surface) 
        
        if personaje_data_result:
            personaje_seleccionado = personaje_data_result
            estado_actual = 'seleccionar_nivel'
        else:
            estado_actual = 'menu'

    # 2. ESTADO: SELECCIÓN DE NIVEL
    elif estado_actual == 'seleccionar_nivel':
        nivel_id = selector_nivel.run_selector_nivel(surface, personaje_seleccionado['id'])
        
        if nivel_id:
            nivel_actual = nivel_id
            if nivel_actual == 'nivel_1':
                estado_actual = 'jugando'
        else:
            estado_actual = 'seleccionar_personaje'
            
    # 3. ESTADO: JUGANDO (NIVEL 1)
    elif estado_actual == 'jugando':
        
        #PANTALLA DE CARGA IMPLEMENTADA: Se ejecuta una sola vez.
        loading_screen.run_loading_screen(surface)
        
        # level_1.run_level puede devolver "MENU", "NEXT_LEVEL" o "REINTENTAR"
        resultado, img_retorno, rect_retorno = level_1.run_level(
            surface, 
            personaje_seleccionado, 
            nivel_actual, 
            img_btn_regresar, 
            REGRESAR_RECT
        )
        
        if resultado == 'MENU':
            estado_actual = 'menu' # Regresar al menú principal
            
        elif resultado == 'REINTENTAR': #LÓGICA DE REINTENTO
            pass 
            
        elif resultado == 'NEXT_LEVEL':
            nivel_en_proceso.run_nivel_en_proceso(surface, img_retorno, rect_retorno)
            estado_actual = 'seleccionar_nivel' 

    pygame.display.flip()
    clock.tick(60)