import pygame
import sys
import time 
from pathlib import Path # Importado para manejo seguro de rutas
from traduccion import obtener_ruta_imagen_traducida # Importar lógica de traducción

# --- CONSTANTES ---
# Define la ruta BASE para la imagen que quieres usar como fondo de carga (el modal)
PATH_LOADING_BACKGROUND_BASE = "loading_nivel_1.png" 

# Duración mínima en segundos que la pantalla estará visible
MIN_DISPLAY_TIME = 5 

# --- CONSTANTES VISUALES PARA LA MODAL ---
# Define el tamaño que quieres para la imagen principal (el modal)
MODAL_WIDTH = 700
MODAL_HEIGHT = 500 

# --- CONSTANTES PARA LA IMAGEN PEQUEÑA (x.png) ---
# 💡 Define la ruta a la imagen pequeña
PATH_SMALL_IMAGE = "recursos/botones/btn_X.png" 
# Tamaño deseado para la imagen pequeña
SMALL_IMAGE_SIZE = (50, 50) 
# Coordenadas fijas para la imagen pequeña (igual que Nivel 2 y 3)
SMALL_X_POS = 925
SMALL_Y_POS = 125
# ------------------------------------------------

def run_loading_screen(ventana):
    """
    Muestra la imagen de fondo de carga escalada en un cuadro pequeño (modal) 
    en el centro de la ventana, y la imagen pequeña (x.png) en (150, 180).
    Se ha añadido la lógica de animación (escalado en hover) al botón 'X'.
    """
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # 1. Obtener la ruta traducida para el fondo del modal
    path_fondo_traducido = obtener_ruta_imagen_traducida(PATH_LOADING_BACKGROUND_BASE)
    
    # --- 1. Cargar y Escalar la Imagen Principal (Modal) ---
    try:
        # Usa la ruta traducida para cargar el fondo
        fondo_original = pygame.image.load(path_fondo_traducido).convert_alpha()
        imagen_modal = pygame.transform.scale(fondo_original, (MODAL_WIDTH, MODAL_HEIGHT))
    except pygame.error as e:
        print(f"Error cargando fondo de carga: {e}. Usando fallback para la imagen principal.")
        imagen_modal = pygame.Surface((MODAL_WIDTH, MODAL_HEIGHT), pygame.SRCALPHA); 
        imagen_modal.fill((40, 40, 40, 200)) # Fondo oscuro semi-transparente
        
    # Calculamos la posición de la imagen principal para centrarla
    MODAL_X = ANCHO // 2 - MODAL_WIDTH // 2
    MODAL_Y = ALTO // 2 - MODAL_HEIGHT // 2
    MODAL_POS = (MODAL_X, MODAL_Y)

    # --- 2. Cargar y Preparar Imágenes del Botón 'X' ---
    try:
        small_img_original = pygame.image.load(PATH_SMALL_IMAGE).convert_alpha()
    except pygame.error as e:
        print(f"Error cargando la imagen pequeña: {e}. Usando fallback para la imagen pequeña.")
        # Fallback: un cuadrado blanco
        small_img_original = pygame.Surface(SMALL_IMAGE_SIZE, pygame.SRCALPHA);
        small_img_original.fill((255, 255, 255)) 

    # Tamaño normal (50x50)
    original_size = SMALL_IMAGE_SIZE
    small_image_normal = pygame.transform.scale(small_img_original, original_size)
    
    # Tamaño al pasar el ratón (+10 píxeles, 60x60)
    hover_size = (original_size[0] + 10, original_size[1] + 10)
    small_image_hover = pygame.transform.scale(small_img_original, hover_size)

    # Rectángulo base (para detección de hover) en la posición fija
    small_rect_base = small_image_normal.get_rect(topleft=(SMALL_X_POS, SMALL_Y_POS))
    
    start_time = time.time()
    running = True
    
    # Crea una superficie oscura para el fondo del modal (el oscurecimiento)
    fondo_oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    # Usamos un relleno negro semi-transparente
    fondo_oscuro.fill((0, 0, 0, 0)) 

    while running:
        elapsed_time = time.time() - start_time
        mouse_clicked = False
        
        # --- Detección de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        # --- Lógica de Hover y Escalado del Botón 'X' ---
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = small_rect_base.collidepoint(mouse_pos)
        
        if is_hovering:
            # Si el ratón está encima, usa la imagen más grande
            current_image = small_image_hover
            # Calcula la posición del nuevo rectángulo para que su CENTRO
            # coincida con el centro del rectángulo base (para centrar la animación)
            current_rect = current_image.get_rect(center=small_rect_base.center)
        else:
            # Si el ratón NO está encima, usa la imagen normal
            current_image = small_image_normal
            # Mantiene la posición del rectángulo base
            current_rect = small_rect_base

        # --- Lógica de Salida ---
        # El tiempo mínimo debe cumplirse O debe haber pasado el tiempo mínimo y haber un clic
        # También se cierra si se hace clic en el botón 'X'
        if elapsed_time >= MIN_DISPLAY_TIME:
            running = False
            
        # Si hay clic, salimos si ya pasó el tiempo de gracia (0.5s) O si el clic fue en el botón 'X'
        if mouse_clicked and (elapsed_time >= 0.5 or current_rect.collidepoint(mouse_pos)):
             running = False
            
        # --- Dibujo del Modal ---
        # 1. Dibuja el oscurecimiento sobre el nivel
        ventana.blit(fondo_oscuro, (0, 0))
        
        # 2. Dibuja la imagen principal del modal en la posición central
        ventana.blit(imagen_modal, MODAL_POS)

        # 3. Dibuja la imagen pequeña (x.png) usando el tamaño y la posición calculada
        ventana.blit(current_image, current_rect.topleft)
        
        pygame.display.flip()
        clock.tick(60)
        
    return True