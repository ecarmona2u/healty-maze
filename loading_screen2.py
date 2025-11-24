import pygame
import sys
import time 

# --- CONSTANTES ---
# Define la ruta a la imagen que quieres usar como fondo de carga (Nivel 2)
PATH_LOADING_BACKGROUND = "recursos/loading_nivel_2.png" 

# Duración mínima en segundos que la pantalla estará visible
MIN_DISPLAY_TIME = 5 

# --- CONSTANTES VISUALES PARA LA MODAL ---
# Define el tamaño que quieres para la imagen dentro del modal
MODAL_WIDTH = 700
MODAL_HEIGHT = 500 

def run_loading_screen(ventana):
    """
    Muestra la imagen de fondo de carga escalada en un cuadro pequeño (modal) 
    en el centro de la ventana, de forma transparente, sobre el contenido ya dibujado 
    (el nivel 2). NO MUESTRA NINGÚN TEXTO.
    """
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # 1. Cargar y Escalar la Imagen de Carga (al tamaño del modal)
    try:
        # Usamos convert_alpha para asegurar transparencia si la imagen lo tiene
        fondo_original = pygame.image.load(PATH_LOADING_BACKGROUND).convert_alpha()
        imagen_modal = pygame.transform.scale(fondo_original, (MODAL_WIDTH, MODAL_HEIGHT))
    except pygame.error as e:
        # Fallback si la imagen no se encuentra (cuadro azul semi-transparente)
        print(f"Error cargando fondo de carga: {e}. Usando fallback.")
        imagen_modal = pygame.Surface((MODAL_WIDTH, MODAL_HEIGHT), pygame.SRCALPHA); 
        imagen_modal.fill((50, 50, 200, 200)) # Azul semi-transparente de fallback
        
    
    # Calculamos la posición de la imagen para centrarla
    MODAL_X = ANCHO // 2 - MODAL_WIDTH // 2
    MODAL_Y = ALTO // 2 - MODAL_HEIGHT // 2
    MODAL_POS = (MODAL_X, MODAL_Y)
    
    # ❌ CÓDIGO ELIMINADO: Se ha quitado la inicialización de fuente y texto.
    
    # Capa de oscurecimiento semi-transparente para el fondo
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 0)) # Negro con 150/255 de opacidad (se ve el nivel debajo)
        
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
        
        # 2. Dibuja la imagen modal en la posición central
        ventana.blit(imagen_modal, MODAL_POS)
        
        # ❌ CÓDIGO ELIMINADO: Se ha quitado la línea para dibujar el texto.

        pygame.display.flip()
        clock.tick(60)
        
    return True