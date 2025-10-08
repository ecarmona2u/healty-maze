# juego_principal.py (MODIFICADO para integrar audio_manager)

import pygame
import sys 
import level_1 
import selector_personaje
import selector_nivel
import ajustes 
import nivel_en_proceso 
from ganaste_entre_nivel import run_pantalla_ganaste 
import loading_screen 
import tutorial_level 
import audio_manager 

# --- CONFIGURACIÓN GLOBAL ---
pygame.init()
pygame.font.init() 

ANCHO, ALTO = 1280, 720  
surface = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Pygame")
clock = pygame.time.Clock()

# --- CONSTANTES ---
AZUL = (50, 50, 200)
COLOR_FONDO_NEGRO = (0, 0, 0) 

# Paths de las imágenes (DEBEN existir)
PATH_FONDO_MENU = "recursos/fondo_menu.png" 
PATH_INICIAR = "recursos/boton_iniciar.png"
PATH_SALIR = "recursos/boton_salir.png"
PATH_AJUSTES = "recursos/boton_ajustes.png" 
PATH_BTN_REGRESAR = "recursos/boton_regresar.png" 

# --- ESTADO DE JUEGO ---
estado_actual = 'menu' 
personaje_seleccionado = None
nivel_actual = None
nivel_recursos_precargados = None 

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

# Carga del botón de regreso 
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

# FUNCIONES DE LÓGICA Y DIBUJO
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

# BUCLE PRINCIPAL DEL JUEGO (Máquina de Estados)
while True:
    mouse_pos = pygame.mouse.get_pos()
    event_list = pygame.event.get() 

    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if estado_actual == 'menu' and event.type == pygame.MOUSEBUTTONDOWN:
            manejar_clic_menu(mouse_pos, button_assets)

# GESTIÓN DE ESTADOS Y DIBUJO    
    # Manejo de AJUSTES
    if estado_actual == 'ajustes':
        # La música sigue sonando ya que solo se abre un modal (no hay cambio de pista)
        accion = ajustes.gestionar_ajustes_modal(surface, event_list, mouse_pos)
        
        if accion == 'cerrar' or accion == 'guardar': # El modal ya solo usa 'cerrar'
            estado_actual = 'menu'
        
        pygame.display.flip()
        clock.tick(60)
        continue 

    elif estado_actual == 'menu':
        audio_manager.play_music('menu_principal') #INICIA MÚSICA DEL MENÚ
        dibujar_menu(surface, mouse_pos, button_assets, menu_background_image)
        
    # 1. ESTADO: SELECCIÓN DE PERSONAJE
    elif estado_actual == 'seleccionar_personaje':
        audio_manager.play_music('selector') #INICIA MÚSICA DEL SELECTOR
        personaje_data_result = selector_personaje.run_selector_personaje(surface) 
        
        if personaje_data_result:
            personaje_seleccionado = personaje_data_result
            estado_actual = 'seleccionar_nivel'
        else:
            estado_actual = 'menu' #Vuelve al menú principal
            audio_manager.play_music('menu_principal') # Cambia la pista de nuevo

    # 2. ESTADO: SELECCIÓN DE NIVEL
    elif estado_actual == 'seleccionar_nivel':
        audio_manager.play_music('selector') #MÚSICA DE SELECTOR CONTINÚA
        nivel_id = selector_nivel.run_selector_nivel(surface, personaje_seleccionado) 
        
        if nivel_id:
            nivel_actual = nivel_id
            if nivel_actual == 'nivel_1':
                estado_actual = 'precarga_nivel' 
            elif nivel_actual == 'tutorial':
                estado_actual = 'precarga_tutorial'
        else:
            estado_actual = 'seleccionar_personaje'

    #ESTADO: Precarga NIVEL 1
    elif estado_actual == 'precarga_nivel':
        audio_manager.play_music('nivel_1') #NICIA MÚSICA DEL NIVEL
        
        # 1. Precarga los recursos
        nivel_recursos_precargados = level_1.preload_level(surface, personaje_seleccionado)
        
        # 2. Dibuja el fondo y la pantalla de carga
        try:
            fondo_nivel_1 = nivel_recursos_precargados[0]
            surface.blit(fondo_nivel_1, (0, 0)) 
            pygame.display.flip()
        except (TypeError, IndexError):
            surface.fill(COLOR_FONDO_NEGRO)
            pygame.display.flip()
        
        loading_screen.run_loading_screen(surface)
        
        estado_actual = 'jugando'

    #ESTADO: Precarga TUTORIAL
    elif estado_actual == 'precarga_tutorial':
        audio_manager.play_music('tutorial') #INICIA MÚSICA DEL TUTORIAL
        
        # 1. Precarga los recursos
        nivel_recursos_precargados = tutorial_level.preload_tutorial_level(surface, personaje_seleccionado)
        
        # 2. Muestra la pantalla de carga 
        loading_screen.run_loading_screen(surface)
        
        estado_actual = 'jugando_tutorial'
            
    # 3. ESTADO: JUGANDO (NIVEL 1)
    elif estado_actual == 'jugando':
        # La música ya fue iniciada en 'precarga_nivel'
        
        resultado, img_retorno, rect_retorno = level_1.run_level(
            surface, 
            nivel_recursos_precargados, 
            img_btn_regresar, 
            REGRESAR_RECT
        )
        
        if resultado not in ('REINTENTAR', 'NEXT_LEVEL'):
            nivel_recursos_precargados = None
            
        if resultado == 'MENU':
            audio_manager.stop_music() #DETENER AL SALIR
            estado_actual = 'menu' 
            
        elif resultado == 'REINTENTAR':
            audio_manager.stop_music() #DETENER ANTES DE RECARGAR
            estado_actual = 'precarga_nivel'
            
        elif resultado == 'NEXT_LEVEL':
            audio_manager.stop_music() #DETENER ANTES DE LA PANTALLA DE GANASTE
            nivel_en_proceso.run_nivel_en_proceso(surface, img_retorno, rect_retorno)
            estado_actual = 'seleccionar_nivel' 
        
        elif resultado == 'SELECT_CHARACTER': 
            audio_manager.stop_music() #DETENER AL CAMBIAR DE ESTADO
            personaje_seleccionado = None
            nivel_actual = None
            estado_actual = 'seleccionar_personaje'
            
        elif resultado == 'SELECTOR_NIVEL':
            audio_manager.stop_music() #DETENER AL CAMBIAR DE ESTADO
            estado_actual = 'seleccionar_nivel'


    #ESTADO: JUGANDO (TUTORIAL) 
    elif estado_actual == 'jugando_tutorial':
        # La música ya fue iniciada en 'precarga_tutorial'
        
        resultado, img_retorno, rect_retorno = tutorial_level.run_tutorial_level(
            surface, 
            nivel_recursos_precargados, 
            img_btn_regresar, 
            REGRESAR_RECT
        )
        
        if resultado != 'REINTENTAR':
            nivel_recursos_precargados = None
        
        if resultado == 'SELECTOR_PERSONAJE' or resultado == 'SELECTOR_NIVEL': 
            audio_manager.stop_music() #DETENER AL SALIR
            estado_actual = 'seleccionar_nivel' 
            
        elif resultado == 'REINTENTAR':
            audio_manager.stop_music() #DETENER ANTES DE RECARGAR
            estado_actual = 'precarga_tutorial'

        elif resultado == 'MENU':
            audio_manager.stop_music() #DETENER AL SALIR
            estado_actual = 'menu' 

        else:
            audio_manager.stop_music() #DETENER COMO FALLBACK
            estado_actual = 'menu'


    # Solo hacemos flip si no estamos en un estado bloqueante que ya lo hizo
    if estado_actual not in ['precarga_nivel', 'precarga_tutorial']:
        pygame.display.flip()
        
    clock.tick(60)