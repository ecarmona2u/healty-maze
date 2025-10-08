# audio_manager.py

import pygame

# --- INICIALIZACIÓN Y ESTADO GLOBAL ---
pygame.mixer.init() 

MUSICA_ACTUAL = None 
GLOBAL_VOLUME = 0.5 
IS_MUTED = False 
VOLUME_BEFORE_MUTE = GLOBAL_VOLUME 

# Rutas de Archivos de Música (Mapeo a tus 2 archivos)
MUSIC_PATHS = {
    # Mapeo de menús
    'menu_principal': 'recursos/musica/musica_menus.mp3', 
    'selector': 'recursos/musica/musica_menus.mp3', 
    
    # Mapeo de niveles
    'nivel_1': 'recursos/musica/musica_niveles.mp3',
    'tutorial': 'recursos/musica/musica_niveles.mp3', 
}

def set_global_volume(new_volume):
    """Actualiza el volumen global y lo aplica al mixer si no está muteado."""
    global GLOBAL_VOLUME, VOLUME_BEFORE_MUTE
    
    new_volume = max(0.0, min(1.0, new_volume))
    GLOBAL_VOLUME = new_volume
    VOLUME_BEFORE_MUTE = GLOBAL_VOLUME
    
    if not IS_MUTED:
        pygame.mixer.music.set_volume(GLOBAL_VOLUME)

def toggle_mute():
    """Alterna el estado de mute ON/OFF."""
    global IS_MUTED, VOLUME_BEFORE_MUTE
    
    IS_MUTED = not IS_MUTED
    
    if IS_MUTED:
        # Mute ON: Volumen del mixer a 0
        pygame.mixer.music.set_volume(0.0)
    else:
        # Mute OFF: Restaura el volumen del mixer al último valor deseado
        pygame.mixer.music.set_volume(VOLUME_BEFORE_MUTE)

def get_current_volume():
    """Devuelve el volumen global deseado por el usuario."""
    return GLOBAL_VOLUME

def is_muted():
    """Devuelve el estado de mute."""
    return IS_MUTED

def play_music(track_name, loops=-1):
    """Carga y reproduce una pista, respetando el estado de mute. (CORREGIDO)"""
    global MUSICA_ACTUAL
    
    #CORRECCIÓN: Usamos solo get_busy() en lugar de get_paused()
    if track_name == MUSICA_ACTUAL and pygame.mixer.music.get_busy(): 
        return

    pygame.mixer.music.stop()
    
    try:
        path = MUSIC_PATHS[track_name]
        pygame.mixer.music.load(path)
        
        volume_to_set = 0.0 if IS_MUTED else GLOBAL_VOLUME 
        pygame.mixer.music.set_volume(volume_to_set)
        
        pygame.mixer.music.play(loops)
        MUSICA_ACTUAL = track_name
    except KeyError:
        print(f"ERROR: Pista de música '{track_name}' no encontrada.")
    except pygame.error as e:
        print(f"ERROR al cargar/reproducir música: {e}")

def pause_music():
    """Pausa la reproducción de música."""
    if pygame.mixer.music.get_busy() and not pygame.mixer.music.get_paused():
        pygame.mixer.music.pause()

def unpause_music():
    """Reanuda la reproducción de música."""
    # Nota: Si get_paused() sigue dando error, deberías eliminar esta función
    # y simplemente dejar que play_music() reinicie la pista al volver al estado de juego.
    if pygame.mixer.music.get_paused():
        pygame.mixer.music.unpause()

def stop_music():
    """Detiene la reproducción de música completamente."""
    pygame.mixer.music.stop()
    global MUSICA_ACTUAL
    MUSICA_ACTUAL = None