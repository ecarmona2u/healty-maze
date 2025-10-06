# pantalla_derrota.py (MODIFICADO: Posiciones específicas de los botones)

import pygame
import sys
# Asumimos que tienes una clase Boton en ganaste_entre_nivel.py
from ganaste_entre_nivel import Boton 

# --- CONSTANTES DE RECURSOS ---
PATH_FONDO_DERROTA = "recursos/fondo_derrota.png" 
PATH_BTN_MENU = "recursos/botones/btn_menu.png"
PATH_BTN_REINTENTAR = "recursos/btn_reintentar.png" 

# --- VALORES DE RETORNO ---
RETURN_MENU = "MENU"
RETURN_REINTENTAR = "REINTENTAR"

def run_pantalla_derrota(ventana):
    ANCHO, ALTO = ventana.get_size()
    clock = pygame.time.Clock()
    
    # 1. Cargar Fondo de Derrota
    try:
        fondo_derrota = pygame.image.load(PATH_FONDO_DERROTA).convert()
        fondo_derrota = pygame.transform.scale(fondo_derrota, (ANCHO, ALTO))
    except pygame.error as e:
        # Fallback si la imagen no se encuentra
        fondo_derrota = pygame.Surface((ANCHO, ALTO)); fondo_derrota.fill((150, 0, 0))
        
    # 2. Crear Botones con TAMAÑO y POSICIÓN FIJA
    
    #Botón 1: REINTENTAR
    reintentar_ancho, reintentar_alto = 300, 90 
    
    #POSICIÓN SOLICITADA: (600, 500)
    # NOTA: Pygame usa la esquina superior izquierda (topleft)
    btn_reintentar = Boton(
        600,                           # X = 600
        500,                           # Y = 500
        reintentar_ancho, 
        reintentar_alto, 
        "REINTENTAR", 
        RETURN_REINTENTAR,
        PATH_BTN_REINTENTAR
    )

    #Botón 2: VOLVER AL MENÚ
    menu_ancho, menu_alto = 90, 90 # Usando los valores de tu código anterior.
    
    #POSICIÓN SOLICITADA: (400, 500)
    # NOTA: Pygame usa la esquina superior izquierda (topleft)
    btn_menu = Boton(
        400,                           # X = 400
        500,                           # Y = 500
        menu_ancho, 
        menu_alto, 
        "MENÚ PRINCIPAL", 
        RETURN_MENU,
        PATH_BTN_MENU
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
        ventana.blit(fondo_derrota, (0, 0))
        
        accion_reintentar = btn_reintentar.draw(ventana)
        accion_menu = btn_menu.draw(ventana)
        
        if accion_reintentar:
            return RETURN_REINTENTAR 
        
        if accion_menu:
            return RETURN_MENU 

        pygame.display.flip()
        clock.tick(30)
        
    return RETURN_MENU