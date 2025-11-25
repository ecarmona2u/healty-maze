import pygame
import sys 
import tutorial_level        

# --- CONSTANTES ---
# Nuevo tamaño por defecto (se usará si no se define uno individual)
NIVEL_IMG_SIZE_DEFAULT = (250, 200) 
COLOR_RESALTE = (255, 255, 0) 
AZUL_FONDO = (20, 20, 50)

# Constante para el efecto de escalado al pasar el ratón
LEVEL_HOVER_GROWTH = 20 # 20px de crecimiento total

BTN_REGRESAR_SIZE = (50, 50)
PATH_BTN_REGRESAR = "recursos/boton_regresar.png" 
COLOR_REGRESAR_FALLBACK = (200, 50, 50) 

# Paths de las imágenes de nivel con COORDENADAS FIJAS (x, y) y TAMAÑO INDIVIDUAL
NIVEL_PATHS = {
    # Tutorial: Usa el tamaño por defecto (250x200)
    'tutorial': {"path": "recursos/nivel_0_img.png", "pos_x": 502, "pos_y": 132, "width":273 , "height": 152}, 
    
    # Nivel 1: Tamaño grande (350x250)
    'nivel_1': {"path": "recursos/nivel_1_img.png", "pos_x": 24, "pos_y": 380, "width": 297, "height": 204}, 
    
    # Nivel 2: Tamaño pequeño (150x150)
    'nivel_2': {"path": "recursos/nivel_2_img.png", "pos_x": 474, "pos_y": 298, "width": 377, "height": 282}, # <-- OK
    
    # Nivel 3: Usa el tamaño por defecto (250x200)
    'nivel_3': {"path": "recursos/nivel_3_img.png", "pos_x": 943, "pos_y": 274, "width": 317, "height": 313}, # <-- OK
}
PATH_FONDO = "recursos/fondo_selector_nivel.png"

def run_selector_nivel(ventana, character_data): 
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    pygame.font.init() 
    
    # --- CARGA Y PREPARACIÓN DE IMÁGENES ---
    try:
        fondo_original = pygame.image.load(PATH_FONDO).convert()
        fondo_selector = pygame.transform.scale(fondo_original, (ANCHO, ALTO))
    except pygame.error:
        fondo_selector = pygame.Surface((ANCHO, ALTO)); fondo_selector.fill(AZUL_FONDO) 

    imagenes_niveles = {}
    botones_nivel = []
    
    # 1. Carga y preparación de Botones de Nivel (con estados Normal y Hover)
    for id, data in NIVEL_PATHS.items():
        # Obtiene el tamaño individual
        img_width = data.get("width", NIVEL_IMG_SIZE_DEFAULT[0])
        img_height = data.get("height", NIVEL_IMG_SIZE_DEFAULT[1])
        current_img_size = (img_width, img_height)

        # Calcular tamaño y posición de Hover
        size_hover = (img_width + LEVEL_HOVER_GROWTH, img_height + LEVEL_HOVER_GROWTH)
        pos_normal = (data["pos_x"], data["pos_y"])
        pos_hover = (pos_normal[0] - LEVEL_HOVER_GROWTH // 2, pos_normal[1] - LEVEL_HOVER_GROWTH // 2)

        try:
            img_base = pygame.image.load(data["path"]).convert_alpha()
            
            # Estado Normal
            img_normal = pygame.transform.scale(img_base, current_img_size)
            rect_normal = img_normal.get_rect(topleft=pos_normal)

            # Estado Hover
            img_hover = pygame.transform.scale(img_base, size_hover)
            rect_hover = img_hover.get_rect(topleft=pos_hover)
            
        except pygame.error:
            # Fallback (usa el mismo surface para normal y hover, sin escalado)
            img_normal = pygame.Surface(current_img_size); img_normal.fill((100, 100, 100))
            rect_normal = img_normal.get_rect(topleft=pos_normal)
            img_hover = img_normal 
            rect_hover = rect_normal
        
        botones_nivel.append({
            'id': id, 
            'normal_rect': rect_normal,
            'hover_rect': rect_hover,
            'normal_img': img_normal,
            'hover_img': img_hover
        })
        
    # 2. Carga y preparación del Botón Regresar (con estados Normal y Hover)
    BTN_REGRESAR_SIZE = (50, 50)
    REGRESAR_RECT = pygame.Rect(10, 10, BTN_REGRESAR_SIZE[0], BTN_REGRESAR_SIZE[1]) # Rect normal para clic

    # Calculamos el tamaño y posición del hover
    BTN_REGRESAR_SIZE_HOVER = (BTN_REGRESAR_SIZE[0] + LEVEL_HOVER_GROWTH, BTN_REGRESAR_SIZE[1] + LEVEL_HOVER_GROWTH)
    REGRESAR_POS_HOVER = (10 - LEVEL_HOVER_GROWTH // 2, 10 - LEVEL_HOVER_GROWTH // 2)
    REGRESAR_RECT_HOVER = pygame.Rect(REGRESAR_POS_HOVER[0], REGRESAR_POS_HOVER[1], BTN_REGRESAR_SIZE_HOVER[0], BTN_REGRESAR_SIZE_HOVER[1])
    
    try:
        img_regresar_base = pygame.image.load(PATH_BTN_REGRESAR).convert_alpha()
        img_btn_regresar_normal = pygame.transform.scale(img_regresar_base, BTN_REGRESAR_SIZE)
        img_btn_regresar_hover = pygame.transform.scale(img_regresar_base, BTN_REGRESAR_SIZE_HOVER)
    except pygame.error:
        # Fallback
        img_btn_regresar_normal = pygame.Surface(BTN_REGRESAR_SIZE); img_btn_regresar_normal.fill(COLOR_REGRESAR_FALLBACK)
        img_btn_regresar_hover = pygame.Surface(BTN_REGRESAR_SIZE_HOVER); img_btn_regresar_hover.fill(COLOR_REGRESAR_FALLBACK)

    # Variables para compatibilidad con la función run_tutorial_level
    img_btn_regresar = img_btn_regresar_normal 

    # ----------------------------------------------------
    # --- BUCLE PRINCIPAL (Selección) ---
    # ----------------------------------------------------
    nivel_seleccionado = None
    seleccion_activa = True

    while seleccion_activa:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Comprobación de clic en el botón Regresar (usando rect normal)
                if REGRESAR_RECT.collidepoint(mouse_pos):
                    return None
                    
                for boton in botones_nivel:
                    # Comprobación de clic en las miniaturas de nivel (usando rect normal)
                    if boton['normal_rect'].collidepoint(mouse_pos):
                        nivel_id = boton['id']
                        
                        # Manejo del Tutorial
                        if nivel_id == 'tutorial':
                            
                            tutorial_activo = True
                            while tutorial_activo:
                                # Ya no hay loading screen
                                precargados = tutorial_level.preload_tutorial_level(ventana, character_data)
                                # Se pasan las variables de compatibilidad
                                retorno, _, _ = tutorial_level.run_tutorial_level(ventana, precargados, img_btn_regresar, REGRESAR_RECT)
                                
                                if retorno == "SELECTOR_NIVEL":
                                    nivel_seleccionado = None 
                                    seleccion_activa = False
                                    tutorial_activo = False
                                    break 
                                
                                elif retorno == "nivel_1":
                                    nivel_seleccionado = "nivel_1"
                                    seleccion_activa = False
                                    tutorial_activo = False 
                                    break
                                elif retorno == "MENU":
                                    return None 
                                elif retorno == "REINTENTAR":
                                    continue 

                            if not seleccion_activa:
                                break
                            
                        # Manejo de Nivel 1, 2 y 3 (Niveles reales)
                        elif nivel_id in ('nivel_1', 'nivel_2', 'nivel_3'):
                            nivel_seleccionado = nivel_id
                            seleccion_activa = False 
                        
                        break
                
                if not seleccion_activa:
                    break
        
        # --- DIBUJO ---
        ventana.blit(fondo_selector, (0, 0))
        
        # 1. Dibujar Botón Regresar (con Hover)
        if REGRESAR_RECT.collidepoint(mouse_pos):
            ventana.blit(img_btn_regresar_hover, REGRESAR_RECT_HOVER)
        else:
            ventana.blit(img_btn_regresar_normal, REGRESAR_RECT)
        
        # 2. Dibujar Niveles (con Hover)
        for boton in botones_nivel:
            
            if boton['normal_rect'].collidepoint(mouse_pos):
                # Estado Hover: dibujar imagen escalada
                ventana.blit(boton['hover_img'], boton['hover_rect'])
            else:
                # Estado Normal: dibujar imagen normal
                ventana.blit(boton['normal_img'], boton['normal_rect'])
            
            # ELIMINADO: Se quita el resaltado amarillo del mouse
        
        pygame.display.flip()
        clock.tick(60)
        
    return nivel_seleccionado