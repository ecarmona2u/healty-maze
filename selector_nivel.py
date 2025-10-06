# selector_nivel.py (ACTUALIZADO)

import pygame
import sys
# 💡 Importamos el nuevo módulo
import nivel_en_proceso 

# --- CONSTANTES ---
NIVEL_IMG_SIZE = (250, 200) 
COLOR_RESALTE = (255, 255, 0) 
AZUL_FONDO = (20, 20, 50)

# CONSTANTES DEL BOTÓN DE RETROCESO
BTN_REGRESAR_SIZE = (50, 50)
PATH_BTN_REGRESAR = "recursos/botones/btn_regresar.png" 
COLOR_REGRESAR_FALLBACK = (200, 50, 50) 

# Paths de las imágenes de nivel
NIVEL_PATHS = {
    'nivel_1': {"path": "recursos/nivel_1_img.png"}, 
    'nivel_2': {"path": "recursos/nivel_2_img.png"},
    'nivel_3': {"path": "recursos/nivel_3_img.png"},
}
PATH_FONDO = "recursos/fondo_selector_nivel.png"

def run_selector_nivel(ventana, personaje_id):
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # Inicialización de la fuente
    pygame.font.init() # Aseguramos que la fuente esté lista
    
    # --- CARGA Y PREPARACIÓN DE IMÁGENES ---

    # 1. Cargar Fondo
    try:
        fondo_original = pygame.image.load(PATH_FONDO).convert()
        fondo_selector = pygame.transform.scale(fondo_original, (ANCHO, ALTO))
    except pygame.error:
        fondo_selector = pygame.Surface((ANCHO, ALTO)); fondo_selector.fill(AZUL_FONDO) 

    # 2. Cargar Imágenes de Nivel y calcular Rects
    imagenes_niveles = {}
    botones_nivel = []
    
    total_width = NIVEL_IMG_SIZE[0] * 3 + 50 * 2
    x_start = ANCHO // 2 - total_width // 2 
    spacing = 50 
    y_pos = ALTO // 2 - 50 
    current_x = x_start

    for id, data in NIVEL_PATHS.items():
        try:
            img = pygame.image.load(data["path"]).convert_alpha()
            img_scaled = pygame.transform.scale(img, NIVEL_IMG_SIZE)
        except pygame.error:
            img_scaled = pygame.Surface(NIVEL_IMG_SIZE); img_scaled.fill((100, 100, 100))
        
        rect = img_scaled.get_rect(topleft=(current_x, y_pos))
        
        imagenes_niveles[id] = img_scaled
        botones_nivel.append({'id': id, 'rect': rect})
        
        current_x += NIVEL_IMG_SIZE[0] + spacing 
        
    # 3. Cargar Botón de Regreso
    REGRESAR_RECT = pygame.Rect(10, 10, BTN_REGRESAR_SIZE[0], BTN_REGRESAR_SIZE[1])
    img_btn_regresar = pygame.Surface(BTN_REGRESAR_SIZE); img_btn_regresar.fill(COLOR_REGRESAR_FALLBACK)
    
    try:
        temp_regresar = pygame.image.load(PATH_BTN_REGRESAR).convert_alpha()
        img_btn_regresar = pygame.transform.scale(temp_regresar, BTN_REGRESAR_SIZE)
    except pygame.error as e:
        pass 

    # ----------------------------------------------------
    # --- BUCLE DE LA FUNCIÓN ---
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
                        
                        if nivel_id == 'nivel_1':
                            nivel_seleccionado = nivel_id
                            seleccion_activa = False # Termina y retorna 'nivel_1'
                        else:
                            # 💡 LLAMADA AL MÓDULO EXTERNO
                            nivel_en_proceso.run_nivel_en_proceso(ventana, img_btn_regresar, REGRESAR_RECT)
                        
                        break
        
        # --- DIBUJO ---
        ventana.blit(fondo_selector, (0, 0))
        
        ventana.blit(img_btn_regresar, REGRESAR_RECT)
        
        # Dibujar Botones (Imágenes de Nivel)
        for boton in botones_nivel:
            rect = boton['rect']
            ventana.blit(imagenes_niveles[boton['id']], rect)
            
            # Dibujar el borde de resaltado (hover)
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(ventana, COLOR_RESALTE, rect.inflate(10, 10), 5)
        
        # Dibujar el borde de resaltado (hover) para el botón Regresar
        if REGRESAR_RECT.collidepoint(mouse_pos):
            pygame.draw.rect(ventana, COLOR_RESALTE, REGRESAR_RECT.inflate(10, 10), 3)

        pygame.display.flip()
        clock.tick(60)
        
    return nivel_seleccionado