# cortina.py

import pygame
import sys

# Rutas de las imágenes de la cortina (asume que están en el directorio raíz o Pygame las encuentra)
CORTINA_PATHS = [
    "recursos/animaciones/cortina/cortina0.png",
    "recursos/animaciones/cortina/cortina1.1.png", 
    "recursos/animaciones/cortina/cortina1.2.png", 
    "recursos/animaciones/cortina/cortina1.3.png", 
    "recursos/animaciones/cortina/cortina2.png", 
    "recursos/animaciones/cortina/cortina3.png", 
    "recursos/animaciones/cortina/cortina4.png", 
    "recursos/animaciones/cortina/cortina5.png", 
    "recursos/animaciones/cortina/cortina6.png", 
    "recursos/animaciones/cortina/cortina7.png", 
    "recursos/animaciones/cortina/cortina8.png",
    "recursos/animaciones/cortina/cortina9.png",
    "recursos/animaciones/cortina/cortina10.png",
    "recursos/animaciones/cortina/cortina11.png",
    "recursos/animaciones/cortina/cortina12.png",
    "recursos/animaciones/cortina/cortina13.png",
    "recursos/animaciones/cortina/cortina14.png",
    "recursos/animaciones/cortina/cortina15.png",


]

# Tasa de fotogramas de la animación (velocidad de la cortina)
FPS_ANIMACION = 10 

def preload_cortina_frames(ANCHO, ALTO):
    """Carga y escala todos los frames de la animación de cortina."""
    frames = []
    for path in CORTINA_PATHS:
        try:
            # Es importante usar .convert_alpha() para transparencia
            image_orig = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(image_orig, (ANCHO, ALTO))
            frames.append(frame)
        except pygame.error as e:
            print(f"Error cargando frame de cortina {path}: {e}")
            # Fallback si una imagen falla: un frame transparente
            frame = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            frame.fill((0, 0, 0, 0)) 
            frames.append(frame)
            
    if not frames:
        # Fallback si no se pudo cargar NADA: un frame negro sólido para cubrir la pantalla
        frame = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        frame.fill((0, 0, 0, 255))
        frames.append(frame)
        
    return frames

def run_cortina_animation(ventana):
    """
    Ejecuta la animación de la cortina sobre la ventana actual,
    bloqueando la ejecución hasta que la cortina se haya cerrado (último frame).
    """
    ANCHO, ALTO = ventana.get_size()
    clock = pygame.time.Clock()
    
    frames = preload_cortina_frames(ANCHO, ALTO)
    num_frames = len(frames)
    
    if num_frames == 0:
        return 
        
    running = True
    current_frame_index = 0

    while running:
        clock.tick(FPS_ANIMACION)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # 1. Dibujar el frame actual de la cortina
        # La cortina se superpone al estado final del nivel.
        ventana.blit(frames[current_frame_index], (0, 0))
        
        # 2. Avanzar al siguiente frame
        current_frame_index += 1
        
        # 3. Finalizar la animación
        if current_frame_index >= num_frames:
            running = False
            
        pygame.display.flip()
        
    return True