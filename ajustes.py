# ajustes.py (MODIFICADO para NO tener bucle ni clock)

import pygame
import sys

# --- CONSTANTES DE AJUSTES ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (50, 50, 200)
ROJO = (200, 50, 50)
VERDE = (50, 200, 50)

# Dimensiones y posición de la ventana modal
MODAL_ANCHO, MODAL_ALTO = 600, 450
PATH_FONDO_AJUSTES = "recursos/fondo_ajustes.png" 

# Inicialización de fuentes
pygame.font.init()
font_opcion = pygame.font.Font(None, 40)
font_titulo = pygame.font.Font(None, 50)

# --- UTILIDADES DE DIBUJO Y CÁLCULO ---

def obtener_rect_modal(ancho_pantalla, alto_pantalla):
    """Calcula el rectángulo principal del modal centrado."""
    return pygame.Rect(
        ancho_pantalla // 2 - MODAL_ANCHO // 2, 
        alto_pantalla // 2 - MODAL_ALTO // 2, 
        MODAL_ANCHO, 
        MODAL_ALTO
    )

def cargar_fondo_modal(modal_rect):
    """Carga y escala la imagen de fondo del modal (Solo una vez)."""
    try:
        fondo_original = pygame.image.load(PATH_FONDO_AJUSTES).convert()
        fondo_escalado = pygame.transform.scale(fondo_original, (MODAL_ANCHO, MODAL_ALTO))
    except pygame.error:
        fondo_escalado = pygame.Surface((MODAL_ANCHO, MODAL_ALTO))
        fondo_escalado.fill((30, 30, 30))
    return fondo_escalado


def dibujar_ajustes_contenido(ventana, mouse_pos, fondo_modal, modal_rect):
    """Dibuja el contenido del modal y devuelve los rectángulos de los botones."""
    
    ventana.blit(fondo_modal, modal_rect.topleft)
    pygame.draw.rect(ventana, AZUL, modal_rect, 5)

    texto_titulo = font_titulo.render("AJUSTES DEL JUEGO", True, BLANCO)
    ventana.blit(texto_titulo, texto_titulo.get_rect(center=(modal_rect.centerx, modal_rect.top + 40)))
    
    # Botón GUARDAR
    rect_guardar = pygame.Rect(modal_rect.left + 50, modal_rect.bottom - 80, 200, 50)
    texto_guardar = font_opcion.render("GUARDAR", True, BLANCO)
    color_guardar = VERDE if rect_guardar.collidepoint(mouse_pos) else AZUL
    pygame.draw.rect(ventana, color_guardar, rect_guardar, border_radius=5)
    ventana.blit(texto_guardar, texto_guardar.get_rect(center=rect_guardar.center))

    # Botón CERRAR
    rect_cerrar = pygame.Rect(modal_rect.right - 250, modal_rect.bottom - 80, 200, 50)
    texto_cerrar = font_opcion.render("CERRAR", True, BLANCO)
    color_cerrar = ROJO if rect_cerrar.collidepoint(mouse_pos) else AZUL
    pygame.draw.rect(ventana, color_cerrar, rect_cerrar, border_radius=5)
    ventana.blit(texto_cerrar, texto_cerrar.get_rect(center=rect_cerrar.center))
    
    return {'guardar': rect_guardar, 'cerrar': rect_cerrar}


# Variable global para almacenar el fondo del modal una sola vez.
_fondo_modal_cache = None 

def gestionar_ajustes_modal(ventana, event_list, mouse_pos):
    """
    Dibuja el modal y maneja los eventos del botón en un solo frame.
    Retorna 'cerrar', 'guardar' o None.
    """
    global _fondo_modal_cache

    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    
    # 1. Inicializar cache la primera vez
    modal_rect = obtener_rect_modal(ANCHO, ALTO)
    if _fondo_modal_cache is None:
        _fondo_modal_cache = cargar_fondo_modal(modal_rect)
    
    # 2. DIBUJAR el contenido de ajustes
    botones = dibujar_ajustes_contenido(ventana, mouse_pos, _fondo_modal_cache, modal_rect)

    # 3. MANEJAR EVENTOS (Se pasa event_list del main loop)
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botones['cerrar'].collidepoint(mouse_pos):
                return 'cerrar'
            elif botones['guardar'].collidepoint(mouse_pos):
                print("Ajustes guardados (Acción en proceso).")
                return 'guardar'
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'cerrar'
            
    return None # No hubo acción que requiera cambio de estado