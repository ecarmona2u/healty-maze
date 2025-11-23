# pantalla_derrota.py (FINAL CORREGIDO)

import pygame
import sys
# Asumimos que la clase Boton está definida en 'ganaste_entre_nivel.py' o es accesible.
from ganaste_entre_nivel import Boton 

# --- CONSTANTES DE RECURSOS ---
PATH_FONDO = "recursos/fondo_derrota.png" 
PATH_BTN_MENU = "recursos/btn_menu.png"
PATH_BTN_REINTENTAR = "recursos/btn_reintentar.png" 

# --- VALORES DE RETORNO ---
RETURN_REINTENTAR = "REINTENTAR"
#Acción estándar para salir al menú/selector de personaje
RETURN_MENU_PRINCIPAL = "MENU" 

def run_pantalla_derrota(ventana):
    ANCHO, ALTO = ventana.get_size()
    clock = pygame.time.Clock()
    
    # 1. Cargar Fondo
    try:
        fondo = pygame.image.load(PATH_FONDO).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error:
        fondo = pygame.Surface((ANCHO, ALTO)); fondo.fill((150, 0, 0))
        
    # 2. Configuración Común de Botones
    BTN_W_GRANDE, BTN_H_GRANDE = 300, 90 
    BTN_W_PEQUENO, BTN_H_PEQUENO = 90, 90 
    BTN_Y = 500
    
    # 3. Creación de Botones
    btn_reintentar = Boton(
        800, BTN_Y, BTN_W_GRANDE, BTN_H_GRANDE, 
        "REINTENTAR", 
        RETURN_REINTENTAR,
        PATH_BTN_REINTENTAR
    )
    # Botón de menú
    btn_menu = Boton(
        400, BTN_Y, BTN_W_PEQUENO, BTN_H_PEQUENO, 
        "PERSONAJE", 
        RETURN_MENU_PRINCIPAL, # <-- Usa "MENU"
        PATH_BTN_MENU
    )

    # 4. Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
        ventana.blit(fondo, (0, 0))
        
        accion_reintentar = btn_reintentar.draw(ventana)
        accion_menu = btn_menu.draw(ventana)
        
        if accion_reintentar:
            return RETURN_REINTENTAR, None, None 
        
        if accion_menu:
            return RETURN_MENU_PRINCIPAL, None, None 

        pygame.display.flip()
        clock.tick(30)
        
    return RETURN_MENU_PRINCIPAL, None, None