import pygame
import sys
import os

# --- CONFIGURACIÓN DE LA INTRO ---
INTRO_FRAMES_PATH = "recursos/videos/intro/"  
NUM_FRAMES = 81  
FRAME_DISPLAY_TIME = 7

# --- CONFIGURACIÓN DE AUDIO (NUEVO) ---
INTRO_AUDIO_PATH = "recursos/videos/intro.mp3" 

def load_intro_frames(ancho, alto):
    """Carga y escala todos los fotogramas de la introducción."""
    frames = []
    
    print("Cargando fotogramas de la intro...")
    
    # Carga secuencial de intro_000.jpg a intro_080.jpg
    for i in range(NUM_FRAMES):
        filename = f"intro_{i:03d}.jpg"  # Formato: intro_000.jpg
        path = os.path.join(INTRO_FRAMES_PATH, filename)
        
        try:
            image = pygame.image.load(path).convert()
            # Escala la imagen al tamaño de la ventana (ANCHO, ALTO)
            image = pygame.transform.scale(image, (ancho, alto))
            frames.append(image)
        except pygame.error:
            print(f"Error al cargar el fotograma: {path}. Usando fallback.")
            fallback = pygame.Surface((ancho, alto))
            fallback.fill((255, 0, 0)) # Fallback visual: cuadrado rojo
            frames.append(fallback)
            
    if not frames:
        print("¡ADVERTENCIA! No se cargó ningún fotograma.")
    
    return frames

def run_intro(surface, clock, audio_manager):
    """
    Ejecuta la animación de introducción con su audio.
    Retorna 'menu' si finaliza/se salta, o 'quit' si el usuario cierra el juego.
    """
    ANCHO, ALTO = surface.get_size()
    
    # 1. Cargar recursos
    intro_frames = load_intro_frames(ANCHO, ALTO)
    if not intro_frames:
        return 'menu' 

    # 2. Inicializar variables
    frame_index = 0
    frame_counter = 0
    running = True

    # 3. Inicializar y reproducir el audio de la intro (NUEVO)
    # Detenemos cualquier música que esté sonando a través del audio_manager
    audio_manager.stop_music() 
    
    intro_sound = None
    try:
        # Cargamos el archivo MP3 directamente. Usamos pygame.mixer.Sound
        intro_sound = pygame.mixer.Sound(INTRO_AUDIO_PATH)
        # Reproducimos el sonido una vez (loops=0)
        intro_sound.play(loops=0)
    except pygame.error as e:
        print(f"Error al cargar o reproducir el audio de la intro: {e}")
        # La intro continuará sin audio si hay un error.

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 4. Detener el audio al salir (NUEVO)
                if intro_sound:
                    intro_sound.stop()
                return 'quit' 
            
            # 5. Permitir saltar la intro con cualquier tecla o clic
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # 6. Detener el audio al saltar (NUEVO)
                if intro_sound:
                    intro_sound.stop()
                return 'menu' 

        # 7. Lógica de avance de fotograma
        frame_counter += 1
        
        if frame_counter >= FRAME_DISPLAY_TIME:
            frame_counter = 0
            frame_index += 1
            
            # 8. Finalizar la intro
            if frame_index >= len(intro_frames):
                running = False
                break
        
        # 9. Dibujar el fotograma actual
        current_frame = intro_frames[frame_index]
        surface.blit(current_frame, (0, 0))

        # 10. Actualizar pantalla y reloj
        pygame.display.flip()
        clock.tick(60)

    # 11. Detener el audio después de que la intro finalice (NUEVO)
    if intro_sound:
        intro_sound.stop()

    # 12. Retorno después de completar la intro
    return 'menu'