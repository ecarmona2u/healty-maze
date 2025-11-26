import pygame 
import sys  
import level_1  
import level_2 
import level_3 
import selector_personaje 
import selector_nivel 
import ajustes  
from ganaste_entre_nivel import run_pantalla_ganaste  
import tutorial_level  
# 🚨 CORRECCIÓN CLAVE: Importa la INSTANCIA para evitar el AttributeError 
from audio_manager import audio_manager  

# --- NUEVOS CAMBIOS PARA INTRO ---
import intro  
# --- FIN NUEVOS CAMBIOS PARA INTRO ---

# --- CONFIGURACIÓN GLOBAL --- 
pygame.init() 
pygame.font.init()  

ANCHO, ALTO = 1280, 720    
surface = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("HEALTY MAZE") 
clock = pygame.time.Clock() 

# --- CONSTANTES --- 
AZUL = (50, 50, 200) 
COLOR_FONDO_NEGRO = (0, 0, 0)  
# Constante para el efecto de crecimiento en HOVER  
GROWTH_PX = 20 
# Nuevo: Máximo crecimiento para la animación de reposo (solo para el botón de inicio) 
ANIMATION_MAX_PX = 10 
# Nuevo: Velocidad de la animación (cuánto cambia el tamaño por frame) 
ANIMATION_SPEED = 0.2 

# Paths de las imágenes (DEBEN existir) 
PATH_FONDO_MENU = "recursos/fondo_menu.png"  
PATH_INICIAR = "recursos/boton_iniciar.png" 
PATH_SALIR = "recursos/botones/btn_X.png" 
PATH_AJUSTES = "recursos/boton_ajustes.png"  
PATH_BTN_REGRESAR = "recursos/boton_regresar.png"  

# --- ESTADO DE JUEGO --- 
# estado_actual = 'menu'  # Original
# --- NUEVOS CAMBIOS PARA INTRO ---
estado_actual = 'intro'  # El juego comienza en la intro
# --- FIN NUEVOS CAMBIOS PARA INTRO ---
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
    {'action': 'iniciar_nivel', 'pos': (530, 280), 'path': PATH_INICIAR, 'size': (200, 100)},  
    {'action': 'ajustes', 'pos': (14, 9), 'path': PATH_AJUSTES, 'size': (60, 60)},  
    {'action': 'salir', 'pos': (1215, 10), 'path': PATH_SALIR, 'size': (60, 60)}, 
] 

# Carga del botón de regreso (no se le aplica la lógica de hover en este caso) 
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
    """ 
    Carga y prepara las imágenes de los botones en estado normal y hover. 
    También inicializa el estado de animación de reposo. 
    """ 
    assets = {} 
    ROJO = (255, 0, 0) 

    for boton in data: 
        path = boton['path'] 
        size = boton['size'] 
        pos = boton['pos'] 
        action = boton['action'] 
         
        try: 
            imagen = pygame.image.load(path).convert_alpha() 

            # 1. Estado Normal (Tamaño base) 
            image_normal = pygame.transform.scale(imagen, size) 
            rect_normal = image_normal.get_rect(topleft=pos) 

            # 2. Estado Hover (GROWTH_PX más grande) 
            new_size_hover = (size[0] + GROWTH_PX, size[1] + GROWTH_PX) 
            image_hover = pygame.transform.scale(imagen, new_size_hover) 
             
            # Recalcular la posición para centrar el botón en hover 
            new_pos_hover = (pos[0] - GROWTH_PX // 2, pos[1] - GROWTH_PX // 2) 
            rect_hover = image_hover.get_rect(topleft=new_pos_hover) 

            assets[action] = { 
                'normal_image': image_normal, 
                'normal_rect': rect_normal, 
                'hover_image': image_hover, 
                'hover_rect': rect_hover, 
                # ESTADOS DE ANIMACIÓN 
                'anim_offset': 0.0,       
                'anim_direction': 1,      
                'base_image': imagen,     
            } 
        except pygame.error: 
            # Fallback (sin cambios) 
            fallback_normal = pygame.Surface(size) 
            fallback_normal.fill(ROJO)  
            rect_normal = fallback_normal.get_rect(topleft=pos) 
             
            new_size_hover = (size[0] + GROWTH_PX, size[1] + GROWTH_PX) 
            fallback_hover = pygame.Surface(new_size_hover) 
            fallback_hover.fill(ROJO)  
            new_pos_hover = (pos[0] - GROWTH_PX // 2, pos[1] - GROWTH_PX // 2) 
            rect_hover = fallback_hover.get_rect(topleft=new_pos_hover) 

            assets[action] = { 
                'normal_image': fallback_normal, 
                'normal_rect': rect_normal, 
                'hover_image': fallback_hover, 
                'hover_rect': rect_hover, 
                # ESTADOS DE ANIMACIÓN 
                'anim_offset': 0.0, 
                'anim_direction': 1, 
                'base_image': fallback_normal,  
            } 
    return assets 

# --- INICIALIZACIÓN DE ASSETS DEL MENÚ --- 
button_assets = cargar_y_preparar_botones(botones_data) 

def actualizar_animacion_botones(assets, mouse_pos): 
    """ 
    Actualiza el estado de animación SÓLO para el botón 'iniciar_nivel' 
    si NO está en hover. 
    """ 
    for action, asset in assets.items(): 
        # *** RESTRICCIÓN: SOLO ANIMAR EL BOTÓN DE INICIO *** if action == 'iniciar_nivel': 
            rect_normal = asset['normal_rect'] 
             
            # Solo animar si el mouse NO está encima 
            if not rect_normal.collidepoint(mouse_pos): 
                offset = asset['anim_offset'] + asset['anim_direction'] * ANIMATION_SPEED 
                 
                # Invertir dirección si llega al límite superior (ANIMATION_MAX_PX) 
                if offset >= ANIMATION_MAX_PX: 
                    offset = ANIMATION_MAX_PX 
                    asset['anim_direction'] = -1 
                 
                # Invertir dirección si llega al límite inferior (0px, tamaño normal) 
                elif offset <= 0: 
                    offset = 0 
                    asset['anim_direction'] = 1 
                     
                asset['anim_offset'] = offset 


# FUNCIONES DE LÓGICA Y DIBUJO 
def dibujar_menu(ventana, mouse_pos, assets, background_image): 
    """Dibuja el menú y aplica el efecto de hover o animación.""" 
    ventana.blit(background_image, (0, 0))  
    for action, asset in assets.items(): 
        rect_normal = asset['normal_rect'] 
         
        if rect_normal.collidepoint(mouse_pos): 
            # ESTADO HOVER (Crecimiento de 20px - Aplica a todos) 
            imagen = asset['hover_image']  
            rect = asset['hover_rect'] 
             
        else: 
            # Si el mouse NO está encima: 
            if action == 'iniciar_nivel': 
                # ESTADO ANIMADO (0 a 10px de crecimiento - Pulsante) 
                current_offset = asset['anim_offset'] # Offset actual (e.g., 0.0 a 10.0) 
                 
                # 1. Calcular el nuevo tamaño 
                size_normal = rect_normal.size 
                new_w = size_normal[0] + current_offset 
                new_h = size_normal[1] + current_offset 
                 
                # 2. Reescalar la imagen  
                # Nota: Usamos normal_image como base para evitar reescalar la imagen base original constantemente 
                imagen = pygame.transform.scale(asset['normal_image'], (int(new_w), int(new_h))) 

                # 3. Calcular la nueva posición para centrar 
                pos_normal = rect_normal.topleft 
                # El desplazamiento es la mitad del offset para centrar el botón 
                new_x = pos_normal[0] - current_offset / 2 
                new_y = pos_normal[1] - current_offset / 2 
                 
                rect = imagen.get_rect(topleft=(new_x, new_y)) 

            else: 
                # ESTADO NORMAL (ajustes y salir, sin animación de reposo) 
                asset['anim_offset'] = 0.0 # Asegurar que estén en 0 
                imagen = asset['normal_image'] 
                rect = asset['normal_rect'] 
             
        ventana.blit(imagen, rect) 

def manejar_clic_menu(mouse_pos, assets): 
    """Maneja los clics en el menú, usando el área normal del botón.""" 
    global estado_actual 
    for action, asset in assets.items(): 
        # Usamos el rect normal para el área de clic funcional 
        rect = asset['normal_rect'] 
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
            audio_manager.stop_music()  
            pygame.quit() 
            sys.exit() 
         
        # Solo manejar clics en el menú (la intro se maneja en el bloque de estado 'intro')
        if estado_actual == 'menu' and event.type == pygame.MOUSEBUTTONDOWN: 
            # Se usa la posición del mouse y los assets actualizados 
            manejar_clic_menu(mouse_pos, button_assets) 

# GESTIÓN DE ESTADOS Y DIBUJO     
    # --- NUEVOS CAMBIOS PARA INTRO ---
    # 0. ESTADO: INTRODUCCIÓN
    if estado_actual == 'intro':
        
        # Ejecutar la secuencia de la intro
        accion = intro.run_intro(surface, clock, audio_manager)
        
        if accion == 'menu':
            estado_actual = 'menu'
            audio_manager.play_music('menu_principal') # Iniciar la música del menú
        elif accion == 'quit':
            pygame.quit()
            sys.exit()
        
        continue # Ir al inicio del bucle while para el siguiente estado

    # --- FIN NUEVOS CAMBIOS PARA INTRO ---
    
    # Manejo de AJUSTES 
    if estado_actual == 'ajustes': 
        accion = ajustes.gestionar_ajustes_modal(surface, event_list, mouse_pos) 
         
        if accion == 'cerrar' or accion == 'guardar':  
            estado_actual = 'menu' 
         
        pygame.display.flip() 
        clock.tick(60) 
        continue  

    elif estado_actual == 'menu': 
        audio_manager.play_music('menu_principal')  
        # NUEVO: Actualizar el estado de animación antes de dibujar 
        actualizar_animacion_botones(button_assets, mouse_pos) 
        # Se llama a la función de dibujo actualizada 
        dibujar_menu(surface, mouse_pos, button_assets, menu_background_image) 
         
    # 1. ESTADO: SELECCIÓN DE PERSONAJE 
    elif estado_actual == 'seleccionar_personaje': 
        # FIX: Cambiamos 'selector' por 'menu_principal' para evitar el reinicio de música 
        # ya que ambas pistas apuntan al mismo archivo MP3. 
        audio_manager.play_music('menu_principal')  
        personaje_data_result = selector_personaje.run_selector_personaje(surface)  
         
        if personaje_data_result: 
            personaje_seleccionado = personaje_data_result 
            estado_actual = 'seleccionar_nivel' 
        else: 
            estado_actual = 'menu'  
            audio_manager.play_music('menu_principal')  

    # 2. ESTADO: SELECCIÓN DE NIVEL 
    elif estado_actual == 'seleccionar_nivel': 
        # FIX: Cambiamos 'selector' por 'menu_principal' para evitar el reinicio de música 
        # ya que ambas pistas apuntan al mismo archivo MP3. 
        audio_manager.play_music('menu_principal')  
        nivel_id = selector_nivel.run_selector_nivel(surface, personaje_seleccionado)  
         
        if nivel_id: 
            nivel_actual = nivel_id 
            if nivel_actual == 'nivel_1': 
                estado_actual = 'precarga_nivel_1' 
            elif nivel_actual == 'nivel_2': 
                estado_actual = 'precarga_nivel_2' 
            elif nivel_actual == 'nivel_3': 
                estado_actual = 'precarga_nivel_3' 
            elif nivel_actual == 'tutorial': 
                estado_actual = 'precarga_tutorial' 
        else: 
            estado_actual = 'seleccionar_personaje' 

    # ESTADO: Precarga NIVEL 1 
    elif estado_actual == 'precarga_nivel_1': 
        audio_manager.play_music('nivel_1')  
         
        # 1. Precarga los recursos (esto puede tardar) 
        nivel_recursos_precargados = level_1.preload_level(surface, personaje_seleccionado) 
         
        estado_actual = 'jugando_nivel_1' 

    # ESTADO: Precarga NIVEL 2 
    elif estado_actual == 'precarga_nivel_2': 
        audio_manager.play_music('nivel_2')  
        # 1. Precarga los recursos 
        nivel_recursos_precargados = level_2.preload_level(surface, personaje_seleccionado) 
         
        estado_actual = 'jugando_nivel_2' 

    # ESTADO: Precarga NIVEL 3 
    elif estado_actual == 'precarga_nivel_3': 
        audio_manager.play_music('nivel_3')  
        # 1. Precarga los recursos 
        nivel_recursos_precargados = level_3.preload_level(surface, personaje_seleccionado) 
         
        estado_actual = 'jugando_nivel_3' 

    # ESTADO: Precarga TUTORIAL 
    elif estado_actual == 'precarga_tutorial': 
        audio_manager.play_music('tutorial')  
         
        # 1. Precarga los recursos 
        nivel_recursos_precargados = tutorial_level.preload_tutorial_level(surface, personaje_seleccionado) 
         
        estado_actual = 'jugando_tutorial' 
             
    # 3. ESTADO: JUGANDO (NIVEL 1) 
    elif estado_actual == 'jugando_nivel_1': 
         
        # level_1.run_level DEBE empezar llamando a loading_screen.run_loading_screen() 
        resultado, img_retorno, rect_retorno = level_1.run_level( 
            surface,  
            nivel_recursos_precargados,  
            img_btn_regresar,  
            REGRESAR_RECT 
        ) 
         
        if resultado not in ('REINTENTAR', 'NEXT_LEVEL', 'LEVEL_2'):  
            nivel_recursos_precargados = None 
             
        if resultado == 'MENU': 
            audio_manager.stop_music()  
            estado_actual = 'menu'  
             
        elif resultado == 'REINTENTAR': 
            audio_manager.stop_music()  
            estado_actual = 'precarga_nivel_1' 
             
        elif resultado == 'NEXT_LEVEL': 
            audio_manager.stop_music()  
            nivel_actual = 'nivel_2'  
            estado_actual = 'precarga_nivel_2'  
             
        elif resultado == 'LEVEL_2': 
            audio_manager.stop_music()  
            nivel_actual = 'nivel_2' 
            estado_actual = 'precarga_nivel_2' 
         
        elif resultado == 'SELECT_CHARACTER':  
            audio_manager.stop_music()  
            personaje_seleccionado = None 
            nivel_actual = None 
            estado_actual = 'seleccionar_personaje' 
             
        elif resultado == 'SELECTOR_NIVEL': 
            audio_manager.stop_music()  
            estado_actual = 'seleccionar_nivel' 

    # ESTADO: JUGANDO (NIVEL 2) 
    elif estado_actual == 'jugando_nivel_2': 
         
        # level_2.run_level DEBE empezar llamando a loading_screen2.run_loading_screen() 
        resultado, img_retorno, rect_retorno = level_2.run_level( 
            surface,  
            nivel_recursos_precargados,  
            img_btn_regresar,  
            REGRESAR_RECT 
        ) 
         
        if resultado not in ('REINTENTAR', 'NEXT_LEVEL'): 
            nivel_recursos_precargados = None 
             
        if resultado == 'MENU': estado_actual = 'menu' 
        elif resultado == 'REINTENTAR': estado_actual = 'precarga_nivel_2' 
        elif resultado == 'NEXT_LEVEL':  
            audio_manager.stop_music() 
            nivel_actual = 'nivel_3' 
            estado_actual = 'precarga_nivel_3'  
        elif resultado == 'SELECT_CHARACTER': estado_actual = 'seleccionar_personaje' 
        elif resultado == 'SELECTOR_NIVEL': estado_actual = 'seleccionar_nivel' 
     
    # ESTADO: JUGANDO (NIVEL 3) 
    elif estado_actual == 'jugando_nivel_3': 
         
        # level_3.run_level DEBE empezar llamando a loading_screen2.run_loading_screen() 
        resultado, img_retorno, rect_retorno = level_3.run_level( 
            surface,  
            nivel_recursos_precargados,  
            img_btn_regresar,  
            REGRESAR_RECT 
        ) 
         
        if resultado not in ('REINTENTAR', 'NEXT_LEVEL'): 
            nivel_recursos_precargados = None 
             
        if resultado == 'MENU': estado_actual = 'menu' 
        elif resultado == 'REINTENTAR': estado_actual = 'precarga_nivel_3' 
        elif resultado == 'NEXT_LEVEL':  
            audio_manager.stop_music()  
            run_pantalla_ganaste(surface)  
            estado_actual = 'seleccionar_nivel'  
        elif resultado == 'SELECT_CHARACTER': estado_actual = 'seleccionar_personaje' 
        elif resultado == 'SELECTOR_NIVEL': estado_actual = 'seleccionar_nivel' 


    # ESTADO: JUGANDO (TUTORIAL)  
    elif estado_actual == 'jugando_tutorial': 
         
        # tutorial_level.run_tutorial_level DEBE empezar llamando a loading_screen.run_loading_screen() 
        resultado, img_retorno, rect_retorno = tutorial_level.run_tutorial_level( 
            surface,  
            nivel_recursos_precargados,  
            img_btn_regresar,  
            REGRESAR_RECT 
        ) 
         
        if resultado != 'REINTENTAR': 
            nivel_recursos_precargados = None 
         
        if resultado == 'SELECTOR_PERSONAJE' or resultado == 'SELECTOR_NIVEL':  
            audio_manager.stop_music()  
            estado_actual = 'seleccionar_nivel'  
             
        elif resultado == 'REINTENTAR': 
            audio_manager.stop_music()  
            estado_actual = 'precarga_tutorial' 

        elif resultado == 'MENU': 
            audio_manager.stop_music()  
            estado_actual = 'menu'  

        else: 
            audio_manager.stop_music()  
            estado_actual = 'menu' 


    # Solo hacemos flip si no estamos en un estado bloqueante (como la pantalla de carga misma) 
    if estado_actual not in ['precarga_nivel_1', 'precarga_nivel_2', 'precarga_nivel_3', 'precarga_tutorial', 'intro']: 
        pygame.display.flip() 
         
    clock.tick(60)