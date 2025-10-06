# loading_screen.py

import pygame
import sys
import time 

# --- CONSTANTES ---
#Define la ruta a la imagen que quieres usar como fondo de carga
PATH_LOADING_BACKGROUND = "recursos/fondo_loading.png" 

# Duración mínima en segundos que la pantalla estará visible
MIN_DISPLAY_TIME = 5 

def run_loading_screen(ventana):
    """
    Muestra una pantalla de carga con una imagen de fondo por un tiempo mínimo.
    """
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # 1. Cargar el Fondo de Carga
    try:
        fondo_original = pygame.image.load(PATH_LOADING_BACKGROUND).convert()
        fondo_loading = pygame.transform.scale(fondo_original, (ANCHO, ALTO))
    except pygame.error as e:
        # Fallback si la imagen no se encuentra
        print(f"Error cargando fondo de carga: {e}. Usando fallback.")
        fondo_loading = pygame.Surface((ANCHO, ALTO)); fondo_loading.fill((0, 0, 0))
        
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
        # 1. Si ha pasado el tiempo mínimo (1.5s), salimos.
        if elapsed_time >= MIN_DISPLAY_TIME:
            running = False
            
        # 2. Si el usuario hace clic Y ya pasaron 0.5s para evitar cierres accidentales.
        if mouse_clicked and elapsed_time >= 0.5:
             running = False
            
        # --- Dibujo ---
        ventana.blit(fondo_loading, (0, 0))

        pygame.display.flip()
        clock.tick(60)
        
    return True