import pygame
import sys
import time 

# --- CONSTANTES ---
# Define la ruta a la imagen que quieres usar como fondo de carga (Nivel 2)
PATH_LOADING_BACKGROUND = "recursos/loading_nivel_2.png" 

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
# Coordenadas fijas para la imagen pequeña
SMALL_X_POS = 925
SMALL_Y_POS = 125
# ------------------------------------------------

def run_loading_screen(ventana):
    """
    Muestra la imagen de fondo de carga escalada en un cuadro pequeño (modal) 
    en el centro de la ventana, y la imagen pequeña (btn_X.png) en (925, 125).
    """
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # --- 1. Cargar y Escalar la Imagen Principal (Modal) ---
    try:
        fondo_original = pygame.image.load(PATH_LOADING_BACKGROUND).convert_alpha()
        imagen_modal = pygame.transform.scale(fondo_original, (MODAL_WIDTH, MODAL_HEIGHT))
    except pygame.error as e:
        print(f"Error cargando fondo de carga Nivel 2: {e}. Usando fallback para la imagen principal.")
        imagen_modal = pygame.Surface((MODAL_WIDTH, MODAL_HEIGHT), pygame.SRCALPHA); 
        imagen_modal.fill((50, 50, 200, 200)) # Fallback azul semi-transparente
        
    
    # Calculamos la posición de la imagen principal para centrarla
    MODAL_X = ANCHO // 2 - MODAL_WIDTH // 2
    MODAL_Y = ALTO // 2 - MODAL_HEIGHT // 2
    MODAL_POS = (MODAL_X, MODAL_Y)

    # --- 2. Cargar y Escalar la Imagen Pequeña (x.png) ---
    try:
        small_img_original = pygame.image.load(PATH_SMALL_IMAGE).convert_alpha()
        small_image = pygame.transform.scale(small_img_original, SMALL_IMAGE_SIZE)
    except pygame.error as e:
        print(f"Error cargando la imagen pequeña: {e}. Usando fallback para la imagen pequeña.")
        # Fallback: un cuadrado blanco
        small_image = pygame.Surface(SMALL_IMAGE_SIZE, pygame.SRCALPHA);
        pygame.draw.circle(small_image, (255, 255, 255), (SMALL_IMAGE_SIZE[0]//2, SMALL_IMAGE_SIZE[1]//2), 70) 

    # 3. Definir la posición fija de la imagen pequeña
    SMALL_POS = (SMALL_X_POS, SMALL_Y_POS)
    
    # Capa de oscurecimiento semi-transparente para el fondo
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 0)) # Negro con 150/255 de opacidad
        
    start_time = time.time()
    running = True
    
    while running:
        elapsed_time = time.time() - start_time
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            # Detectar clic
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True

        # --- Lógica de Salida ---
        if elapsed_time >= MIN_DISPLAY_TIME:
            running = False
            
        # Permitir saltar después de 0.5s para evitar clics accidentales
        if mouse_clicked and elapsed_time >= 0.5:
             running = False
            
        # --- Dibujo del Modal (Superpuesto) ---
        # 1. Aplica el oscurecimiento sobre el nivel que ya está dibujado
        ventana.blit(overlay, (0,0))
        
        # 2. Dibuja la imagen principal del modal en la posición central
        ventana.blit(imagen_modal, MODAL_POS)
        
        # 3. Dibuja la imagen pequeña (x.png) en la posición fija
        ventana.blit(small_image, SMALL_POS)

        pygame.display.flip()
        clock.tick(60)
        
    return True