import pygame
import sys
from pathlib import Path 
import os 

# 📢 IMPORTAR LÓGICA DE TRADUCCIÓN
# Nota: Asumo que esta lógica ('traduccion.py') está disponible en el entorno.
from traduccion import obtener_ruta_imagen_traducida 

# --- CONSTANTES DE RECURSOS (Rutas Base) ---
PATH_FONDO_BASE = "fondo_victoria3.png" # <<< RUTA BASE para traducción
# Los botones ya no se necesitan, pero se mantiene la ruta del sonido
PATH_SONIDO_NO_WIN = str(Path("recursos") / "audio" / "win.mp3") 

BLANCO = (255, 255, 255)

# --- VALORES DE RETORNO (ACTUALIZADO: RETURN_NEXT_LEVEL AHORA ES GAME_OVER) ---
# Se define RETURN_GAME_OVER para indicar el fin definitivo del juego después de la animación final.
RETURN_GAME_OVER = "GAME_OVER_VICTORY"
RETURN_SELECTOR_NIVEL = "SELECTOR_NIVEL" 
# RETURN_REINTENTAR = "REINTENTAR" (No usado aquí)

# --- CONFIGURACIÓN DE LA ANIMACIÓN FINAL (INTEGRADO) ---
# FIX: Usar Path object para mejor manejo de rutas.
INTRO_FRAMES_PATH = Path("recursos") / "videos" / "final" 
NUM_FRAMES = 131
FRAME_DISPLAY_TIME = 7
# FIX: Usar Path object para mejor manejo de rutas de audio.
INTRO_AUDIO_PATH = str(Path("recursos") / "videos" / "final.mp3") 

def load_intro_frames(ancho, alto):
    """Carga y escala todos los fotogramas de la introducción."""
    frames = []
    
    print("Cargando fotogramas de la intro desde:", INTRO_FRAMES_PATH)
    
    # Carga secuencial de Final_000.jpg a Final_130.jpg (NUM_FRAMES = 131)
    for i in range(NUM_FRAMES):
        filename = f"Final_{i:03d}.jpg"  # Formato: Final_000.jpg
        # FIX: Construir la ruta usando Path para mayor compatibilidad
        path = str(INTRO_FRAMES_PATH / filename)
        
        try:
            image = pygame.image.load(path).convert()
            # Escala la imagen al tamaño de la ventana (ANCHO, ALTO)
            image = pygame.transform.scale(image, (ancho, alto))
            frames.append(image)
        except pygame.error:
            # Fallback a un color sólido si la imagen no se carga
            print(f"Error al cargar el fotograma: {path}. Usando fallback.")
            fallback = pygame.Surface((ancho, alto))
            fallback.fill((255, 0, 0)) # Fallback visual: cuadrado rojo
            frames.append(fallback)
            
    if not frames:
        print("¡ADVERTENCIA! No se cargó ningún fotograma.")
    
    return frames

# FUNCIÓN DE LA ANIMACIÓN FINAL
def run_final_animation(surface, clock):
    """
    Ejecuta la animación final.
    Una vez terminada, se queda en el último frame hasta que el usuario 
    pulsa una tecla o toca la pantalla.
    
    Retorna True si finaliza/se salta o se pulsa para continuar, 
    o False si el usuario cierra el juego.
    """
    ANCHO, ALTO = surface.get_size()
    
    # 1. Cargar recursos
    intro_frames = load_intro_frames(ANCHO, ALTO)
    if not intro_frames:
        print("Saliendo de la animación final inmediatamente por falta de fotogramas.")
        return True 

    # 2. Inicializar variables
    frame_index = 0
    frame_counter = 0
    running = True
    paused_on_end = False # Nuevo estado para la pausa en el último fotograma
    
    # 3. Inicializar y reproducir el audio de la intro
    pygame.mixer.stop() # Asegura que se detenga cualquier sonido anterior (como el de victoria)
    
    intro_sound = None
    try:
        intro_sound = pygame.mixer.Sound(INTRO_AUDIO_PATH)
        intro_sound.play(loops=0)
    except pygame.error as e:
        print(f"Error al cargar o reproducir el audio de la intro: {e}")
        
    # Inicializar fuente para el mensaje de continuación
    font = None
    try:
        # Usar una fuente por defecto de Pygame para el mensaje de pausa
        font = pygame.font.Font(None, 40)
    except pygame.error as e:
        print(f"Advertencia: No se pudo cargar la fuente para el mensaje de pausa: {e}")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Detener el audio al salir
                if intro_sound:
                    intro_sound.stop()
                return False # Indica que el juego debe salir
            
            # Comportamiento de salto/continuación:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if paused_on_end:
                    # 5. Si ya está pausado en el último frame, cualquier input finaliza el bucle
                    running = False 
                    break 
                else:
                    # 6. Si no está pausado, cualquier input salta la animación
                    if intro_sound:
                        intro_sound.stop()
                    return True # Indica que la animación terminó y debe continuar

        # --- Lógica de avance de fotograma ---
        if not paused_on_end:
            frame_counter += 1
            
            if frame_counter >= FRAME_DISPLAY_TIME:
                frame_counter = 0
                frame_index += 1
                
                # 8. Finalizar la animación y entrar en estado de pausa
                if frame_index >= len(intro_frames):
                    frame_index = len(intro_frames) - 1 # Asegura que se muestre el último frame
                    paused_on_end = True                # Pausar en el último frame
                    # NOTA: El audio se detendrá al final del bucle al salir.
        
        # 9. Determinar el fotograma a dibujar
        current_frame = intro_frames[frame_index]
        surface.blit(current_frame, (0, 0))

        # 10. Mostrar indicación de continuación si está en pausa final
        if paused_on_end and font:
            text_surface = font.render("Toca la pantalla o presiona una tecla para continuar...", True, BLANCO)
            text_rect = text_surface.get_rect(center=(ANCHO // 2, ALTO - 50))
            surface.blit(text_surface, text_rect)

        # 11. Actualizar pantalla y reloj
        pygame.display.flip()
        clock.tick(60)

    # 12. Detener el audio al salir (después de terminar la animación o ser saltada/continuada)
    if intro_sound:
        intro_sound.stop()

    # 13. Retorno después de completar la intro y pulsar para continuar
    return True 


# FUNCIÓN PRINCIPAL DE LA PANTALLA
def run_pantalla_ganaste(ventana, img_btn_regresar=None, REGRESAR_RECT=None): 
    """
    Muestra la pantalla de 'Ganaste' por 5 segundos, ejecuta la animación final
    y luego espera la interacción del usuario en el último frame antes de 
    regresar con la señal de GAME_OVER.
    """
    
    # 1. VERIFICAR E INICIALIZAR EL MIXER (AUDIO)
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Advertencia: No se pudo inicializar el mezclador de audio: {e}")
        
    # 2. CARGA DEL SONIDO
    sonido_win = None
    try:
        sonido_win = pygame.mixer.Sound(PATH_SONIDO_NO_WIN)
    except pygame.error as e:
        print(f"Error cargando el sonido: {e}. Se intentará continuar sin audio.")
        
    # 3. REPRODUCCIÓN DEL SONIDO
    if sonido_win:
        sonido_win.play()
        
    ANCHO, ALTO = ventana.get_size()
    clock = pygame.time.Clock()
    
    # 4. TRADUCCIÓN Y CARGA DE FONDO
    path_fondo_traducido = obtener_ruta_imagen_traducida(PATH_FONDO_BASE)
    
    try:
        # Usa la ruta traducida y escala
        fondo = pygame.image.load(path_fondo_traducido).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error:
        print(f"Error cargando fondo traducido: {path_fondo_traducido}. Usando color sólido.")
        fondo = pygame.Surface((ANCHO, ALTO)); fondo.fill((50, 50, 50)) # Fallback a color gris oscuro

    # --- LÓGICA DE TIEMPO AÑADIDA ---
    # Tiempo en milisegundos que debe durar la pantalla (5 segundos)
    DURACION_PANTALLA_MS = 5000 
    start_time = pygame.time.get_ticks() # Obtener el tiempo de inicio
    
    # 7. Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            # Opcional: Permitir la salida inmediata con ESCAPE (se mantiene por utilidad)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if sonido_win: sonido_win.stop() 
                    running = False
                    return RETURN_SELECTOR_NIVEL, None, None 

        # --- VERIFICACIÓN DE TIEMPO ---
        elapsed_time = pygame.time.get_ticks() - start_time
        
        if elapsed_time >= DURACION_PANTALLA_MS:
            # 5 segundos han pasado. Paramos el sonido de victoria.
            if sonido_win:
                sonido_win.stop()

            # Ejecutar la animación final (incluye la pausa en el último frame)
            animacion_exitosa = run_final_animation(ventana, clock)
            
            running = False # Se fuerza la salida del bucle principal
            
            if animacion_exitosa:
                # Retorna GAME_OVER_VICTORY después de la animación y la pausa final
                return RETURN_GAME_OVER, img_btn_regresar, REGRESAR_RECT 
            else:
                # El usuario cerró la ventana durante la animación: salir del juego
                pygame.quit(); sys.exit() 

            
        ventana.blit(fondo, (0, 0))

        
        pygame.display.flip()
        clock.tick(60)
        
    # Fallback 
    return RETURN_SELECTOR_NIVEL, None, None