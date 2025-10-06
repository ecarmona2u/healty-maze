# nivel_en_proceso.py

import pygame
import sys

# --- CONSTANTES ---
COLOR_TEXTO = (255, 255, 255)
COLOR_RESALTE = (255, 255, 0) # Amarillo para el hover
COLOR_FONDO_PROCESO = (10, 50, 80) # Fondo azul oscuro

def run_nivel_en_proceso(ventana, img_btn_regresar, REGRESAR_RECT):
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # Inicialización de la fuente (Asumimos que font.init() ya se hizo en el principal)
    FONT = pygame.font.Font(None, 40)
    
    # Prepara el fondo y el mensaje
    fondo_temporal = pygame.Surface((ANCHO, ALTO)); fondo_temporal.fill(COLOR_FONDO_PROCESO) 
    mensaje = FONT.render("Nivel en Desarrollo - ¡Pronto disponible!", True, COLOR_TEXTO)
    mensaje_rect = mensaje.get_rect(center=(ANCHO // 2, ALTO // 2))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return # Vuelve al selector de nivel
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REGRESAR_RECT.collidepoint(mouse_pos):
                    return # Vuelve al selector de nivel

        # DIBUJO
        ventana.blit(fondo_temporal, (0, 0))
        ventana.blit(mensaje, mensaje_rect)
        
        # Dibujar Botón de Regreso (Usamos las imágenes y rects pasados como argumento)
        ventana.blit(img_btn_regresar, REGRESAR_RECT)
        if REGRESAR_RECT.collidepoint(mouse_pos):
            pygame.draw.rect(ventana, COLOR_RESALTE, REGRESAR_RECT.inflate(10, 10), 3)

        pygame.display.flip()
        clock.tick(60)