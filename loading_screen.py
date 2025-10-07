# loading_screen.py

import pygame
import sys
import time 

# --- CONSTANTES ---
# Define la ruta a la imagen que quieres usar como fondo de carga
PATH_LOADING_BACKGROUND = "recursos/fondo_loading.png" 

# Duración mínima en segundos que la pantalla estará visible
MIN_DISPLAY_TIME = 5 

# --- CONSTANTES VISUALES PARA LA MODAL ---
# Define el tamaño que quieres para la imagen dentro del modal
MODAL_WIDTH = 700
MODAL_HEIGHT = 500 

def run_loading_screen(ventana):
    """
    Muestra la imagen de fondo de carga escalada en un cuadro pequeño (modal) 
    en el centro de la ventana, sobre el nivel ya dibujado.
    """
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # 1. Cargar y Escalar la Imagen de Carga (al tamaño del modal)
    try:
        fondo_original = pygame.image.load(PATH_LOADING_BACKGROUND).convert_alpha()
        # Escala la imagen al tamaño de la ventana modal
        imagen_modal = pygame.transform.scale(fondo_original, (MODAL_WIDTH, MODAL_HEIGHT))
    except pygame.error as e:
        # Fallback si la imagen no se encuentra (cuadro rojo sólido)
        print(f"Error cargando fondo de carga: {e}. Usando fallback.")
        imagen_modal = pygame.Surface((MODAL_WIDTH, MODAL_HEIGHT), pygame.SRCALPHA); 
        imagen_modal.fill((255, 0, 0, 200)) # Rojo semi-transparente
        
    
    # Calculamos la posición de la imagen para centrarla
    MODAL_X = ANCHO // 2 - MODAL_WIDTH // 2
    MODAL_Y = ALTO // 2 - MODAL_HEIGHT // 2
    MODAL_POS = (MODAL_X, MODAL_Y)
        
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
        # 1. Si ha pasado el tiempo mínimo, salimos.
        if elapsed_time >= MIN_DISPLAY_TIME:
            running = False
            
        # 2. Si el usuario hace clic Y ya pasaron 0.5s para evitar cierres accidentales.
        if mouse_clicked and elapsed_time >= 0.5:
             running = False
            
        # --- Dibujo del Modal ---
        # Dibuja la imagen modal en la posición central
        ventana.blit(imagen_modal, MODAL_POS)

        pygame.display.flip()
        clock.tick(60)
        
    return True 