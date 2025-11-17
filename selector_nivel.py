# selector_nivel.py (CÓDIGO COMPLETO Y CORREGIDO para Nivel 2 y 3)

import pygame
import sys
import nivel_en_proceso 
import tutorial_level          
import tutorial_win_screen     
import loading_screen          

# --- CONSTANTES ---
# Nuevo tamaño por defecto (se usará si no se define uno individual)
NIVEL_IMG_SIZE_DEFAULT = (250, 200) 
COLOR_RESALTE = (255, 255, 0) 
AZUL_FONDO = (20, 20, 50)
BTN_REGRESAR_SIZE = (50, 50)
PATH_BTN_REGRESAR = "recursos/boton_regresar.png" 
COLOR_REGRESAR_FALLBACK = (200, 50, 50) 

# Paths de las imágenes de nivel con COORDENADAS FIJAS (x, y) y TAMAÑO INDIVIDUAL
NIVEL_PATHS = {
    # Tutorial: Usa el tamaño por defecto (250x200)
    'tutorial': {"path": "recursos/nivel_0_img.png", "pos_x": 502, "pos_y": 132, "width":273 , "height": 152}, 
    
    # Nivel 1: Tamaño grande (350x250)
    'nivel_1': {"path": "recursos/nivel_1_img.png", "pos_x": 24, "pos_y": 386, "width": 297, "height": 204}, 
    
    # Nivel 2: Tamaño pequeño (150x150)
    'nivel_2': {"path": "recursos/nivel_2_img.png", "pos_x": 474, "pos_y": 308, "width": 377, "height": 282}, # <-- OK
    
    # Nivel 3: Usa el tamaño por defecto (250x200)
    'nivel_3': {"path": "recursos/nivel_3_img.png", "pos_x": 943, "pos_y": 284, "width": 317, "height": 313}, # <-- OK
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
    
    for id, data in NIVEL_PATHS.items():
        # Obtiene el tamaño individual, si no existe usa el por defecto
        img_width = data.get("width", NIVEL_IMG_SIZE_DEFAULT[0])
        img_height = data.get("height", NIVEL_IMG_SIZE_DEFAULT[1])
        current_img_size = (img_width, img_height)

        try:
            img = pygame.image.load(data["path"]).convert_alpha()
            img_scaled = pygame.transform.scale(img, current_img_size)
        except pygame.error:
            img_scaled = pygame.Surface(current_img_size); img_scaled.fill((100, 100, 100))
        
        rect = img_scaled.get_rect(topleft=(data["pos_x"], data["pos_y"])) 
        
        imagenes_niveles[id] = img_scaled
        botones_nivel.append({'id': id, 'rect': rect})
        
    REGRESAR_RECT = pygame.Rect(10, 10, BTN_REGRESAR_SIZE[0], BTN_REGRESAR_SIZE[1])
    img_btn_regresar = pygame.Surface(BTN_REGRESAR_SIZE); img_btn_regresar.fill(COLOR_REGRESAR_FALLBACK)
    
    try:
        temp_regresar = pygame.image.load(PATH_BTN_REGRESAR).convert_alpha()
        img_btn_regresar = pygame.transform.scale(temp_regresar, BTN_REGRESAR_SIZE)
    except pygame.error as e:
        pass 

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
                if REGRESAR_RECT.collidepoint(mouse_pos):
                    return None
                    
                for boton in botones_nivel:
                    if boton['rect'].collidepoint(mouse_pos):
                        nivel_id = boton['id']
                        
                        # Manejo del Tutorial
                        if nivel_id == 'tutorial':
                            
                            tutorial_activo = True
                            while tutorial_activo:
                                # Ya no hay loading screen
                                precargados = tutorial_level.preload_tutorial_level(ventana, character_data)
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
                        # Todos devuelven el ID para que juego_principal se encargue de la precarga
                        elif nivel_id in ('nivel_1', 'nivel_2', 'nivel_3'): # <-- LÓGICA UNIFICADA
                            nivel_seleccionado = nivel_id
                            seleccion_activa = False 
                        
                        # Si deseas bloquear niveles, usa un 'else:' aquí para llamar a nivel_en_proceso.
                        
                        break
                
                if not seleccion_activa:
                    break
        
        # --- DIBUJO ---
        ventana.blit(fondo_selector, (0, 0))
        ventana.blit(img_btn_regresar, REGRESAR_RECT)
        
        for boton in botones_nivel:
            rect = boton['rect']
            ventana.blit(imagenes_niveles[boton['id']], rect)
            
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(ventana, COLOR_RESALTE, rect.inflate(10, 10), 5)
        
        if REGRESAR_RECT.collidepoint(mouse_pos):
            pygame.draw.rect(ventana, COLOR_RESALTE, REGRESAR_RECT.inflate(10, 10), 3)

        pygame.display.flip()
        clock.tick(60)
        
    return nivel_seleccionado