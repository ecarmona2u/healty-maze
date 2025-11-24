import pygame
import sys
import time 

# --- CONSTANTES ---
# Define la ruta a la imagen que quieres usar como fondo de carga (el modal)
PATH_LOADING_BACKGROUND = "recursos/loading_nivel_1.png" 

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
    """
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # --- 1. Cargar y Escalar la Imagen Principal (Modal) ---
    try:
        fondo_original = pygame.image.load(PATH_LOADING_BACKGROUND).convert_alpha()
        imagen_modal = pygame.transform.scale(fondo_original, (MODAL_WIDTH, MODAL_HEIGHT))
    except pygame.error as e:
        print(f"Error cargando fondo de carga: {e}. Usando fallback para la imagen principal.")
        imagen_modal = pygame.Surface((MODAL_WIDTH, MODAL_HEIGHT), pygame.SRCALPHA); 
        imagen_modal.fill((40, 40, 40, 200)) # Fondo oscuro semi-transparente
        
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
        # Fallback: un cuadrado animado
        small_image = pygame.Surface(SMALL_IMAGE_SIZE, pygame.SRCALPHA);
        pygame.draw.circle(small_image, (255, 255, 255), (SMALL_IMAGE_SIZE[0]//2, SMALL_IMAGE_SIZE[1]//2), 70) 

    # 3. Definir la posición fija de la imagen pequeña usando las constantes
    SMALL_POS = (SMALL_X_POS, SMALL_Y_POS)
        
    start_time = time.time()
    running = True
    
    # Crea una superficie oscura para el fondo del modal (el oscurecimiento)
    # CORRECCIÓN: Usamos opacidad (180) para oscurecer el nivel de fondo
    fondo_oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    fondo_oscuro.fill((0, 0, 0, 0)) 

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
        # El tiempo mínimo debe cumplirse O debe haber pasado el tiempo mínimo y haber un clic
        if elapsed_time >= MIN_DISPLAY_TIME:
            running = False
            
        if mouse_clicked and elapsed_time >= 0.5:
             running = False
            
        # --- Dibujo del Modal ---
        # 1. Dibuja el oscurecimiento sobre el nivel
        ventana.blit(fondo_oscuro, (0, 0))
        
        # 2. Dibuja la imagen principal del modal en la posición central
        ventana.blit(imagen_modal, MODAL_POS)

        # 3. Dibuja la imagen pequeña (x.png) en la posición fija (150, 180)
        ventana.blit(small_image, SMALL_POS)
        
        # 💡 Opcional: Rotar un poco la imagen pequeña para darle un efecto de carga
        # small_image_rotated = pygame.transform.rotate(small_image, (elapsed_time * 100) % 360)
        # rotated_rect = small_image_rotated.get_rect(center=(ANCHO // 2, ALTO // 2))
        # ventana.blit(small_image_rotated, rotated_rect.topleft)

        pygame.display.flip()
        clock.tick(60)
        
    return True