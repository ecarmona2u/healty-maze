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
# 🟢 NUEVA VARIABLE para almacenar los recursos precargados
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
                # 🟢 CAMBIO: Transiciona a precarga
                estado_actual = 'precarga_nivel' 
        else:
            estado_actual = 'seleccionar_personaje'

    # 🚨 NUEVO ESTADO CLAVE: Precarga el nivel y muestra la carga modal sobre él
    elif estado_actual == 'precarga_nivel':
        
        # 1. 🟢 PRECÁRGA DEL NIVEL y almacenamiento de recursos
        nivel_recursos_precargados = level_1.preload_level(surface, personaje_seleccionado)
        
        # 2. 🟢 DIBUJAR EL NIVEL COMPLETO (Esto será el fondo de la pantalla de carga)
        fondo_nivel, player_group, obstaculo_group, meta_group, coleccionable_group = nivel_recursos_precargados
        
        surface.blit(fondo_nivel, (0, 0)) 
        obstaculo_group.draw(surface)
        coleccionable_group.draw(surface)
        meta_group.draw(surface)
        player_group.draw(surface)
        
        # 3. 🟢 LLAMADA ÚNICA Y OFICIAL A LA PANTALLA DE CARGA MODAL
        loading_screen.run_loading_screen(surface)
        
        # 4. Pasa al estado de juego real después de la carga
        estado_actual = 'jugando'
            
    # 3. ESTADO: JUGANDO (NIVEL 1)
    elif estado_actual == 'jugando':
        
        # 🟢 CAMBIO: Pasamos los recursos precargados a run_level
        resultado, img_retorno, rect_retorno = level_1.run_level(
            surface, 
            nivel_recursos_precargados, 
            img_btn_regresar, 
            REGRESAR_RECT
        )
        
        # 🟢 LIMPIAR LOS RECURSOS después de terminar (buena práctica)
        if resultado != 'REINTENTAR':
            nivel_recursos_precargados = None
        
        if resultado == 'MENU':
            estado_actual = 'menu' 
            
        elif resultado == 'REINTENTAR':
            # Si reintenta, volvemos a precargar para un nuevo inicio limpio (el estado 'precarga_nivel' se encarga)
            estado_actual = 'precarga_nivel'
            
        elif resultado == 'NEXT_LEVEL':
            nivel_en_proceso.run_nivel_en_proceso(surface, img_retorno, rect_retorno)
            estado_actual = 'seleccionar_nivel' 

    pygame.display.flip()
    clock.tick(60)