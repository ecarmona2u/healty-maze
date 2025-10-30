# audio_manager.py (CÓDIGO COMPLETO Y CORREGIDO para Nivel 2 y 3)

import pygame
import sys

# --- CONSTANTES DE RUTA ---
# IMPORTANTE: Asegúrate de que los archivos .mp3 estén en una carpeta llamada 'recursos'
PATH_MUSICA_MENU = "recursos/musica/musica_menus.mp3"
PATH_MUSICA_NIVEL_1 = "recursos/musica/musica_niveles.mp3"
PATH_MUSICA_NIVEL_2 = "recursos/musica/musica_niveles.mp3" # <-- NUEVA CONSTANTE
PATH_MUSICA_NIVEL_3 = "recursos/musica/musica_niveles.mp3" # <-- NUEVA CONSTANTE
PATH_MUSICA_SELECTOR = "recursos/musica/musica_menus.mp3" 
PATH_MUSICA_TUTORIAL = "recursos/musica/musica_niveles.mp3" 

class AudioManager:
    def __init__(self):
        # Inicializar el mixer
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except pygame.error as e:
                print(f"Error al inicializar el mixer de Pygame: {e}")
                sys.exit()

        self.music_paths = {
            'menu_principal': PATH_MUSICA_MENU,
            'nivel_1': PATH_MUSICA_NIVEL_1,
            'nivel_2': PATH_MUSICA_NIVEL_2, # <-- NUEVA CLAVE
            'nivel_3': PATH_MUSICA_NIVEL_3, # <-- NUEVA CLAVE
            'selector': PATH_MUSICA_SELECTOR,
            'tutorial': PATH_MUSICA_TUTORIAL,
        }
        self.MUSICA_ACTUAL = None
        self.is_music_paused = False # Bandera interna (soluciona error get_paused)
        
        # Gestor de volumen y mute (soluciona error get_current_volume y set_global_volume)
        self._stored_volume = 0.5    
        self._is_muted = False
        pygame.mixer.music.set_volume(self._stored_volume)


    # --- CONTROL DE MÚSICA (Play/Pause/Stop) ---
    def play_music(self, track_name, loop=-1):
        """Reproduce la música especificada, respetando el estado de mute."""
        path = self.music_paths.get(track_name)
        if not path:
            print(f"ADVERTENCIA: Pista de música '{track_name}' no encontrada. Revisa las rutas.")
            return

        if track_name == self.MUSICA_ACTUAL and (pygame.mixer.music.get_busy() or self.is_music_paused):
            return

        try:
            if track_name != self.MUSICA_ACTUAL or not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(loop)
                self.MUSICA_ACTUAL = track_name
                self.is_music_paused = False
                
                # Aplica el volumen inicial o 0.0 si está muteado
                if not self._is_muted:
                    pygame.mixer.music.set_volume(self._stored_volume)
                else:
                    pygame.mixer.music.set_volume(0.0)
                
        except pygame.error as e:
            # Esto se dispara si el archivo existe pero no se puede cargar (formato incorrecto, corrupto, etc.)
            print(f"Error CRÍTICO al reproducir la música: {e}. Asegúrate que el archivo sea un MP3 válido.") 

    def pause_music(self):
        """Pausa la música si está sonando."""
        if pygame.mixer.music.get_busy() and not self.is_music_paused:
            pygame.mixer.music.pause()
            self.is_music_paused = True

    def unpause_music(self):
        """Reanuda la música si estaba en pausa."""
        if self.is_music_paused:
            pygame.mixer.music.unpause()
            self.is_music_paused = False

    def stop_music(self):
        """Detiene completamente la música."""
        if pygame.mixer.music.get_busy() or self.is_music_paused:
            pygame.mixer.music.stop()
            self.MUSICA_ACTUAL = None
            self.is_music_paused = False
            
    # --- CONTROL DE VOLUMEN Y MUTE ---
    def set_volume(self, volume):
        """Establece el volumen de la música (0.0 a 1.0)."""
        self._stored_volume = max(0.0, min(1.0, volume)) 
        if not self._is_muted:
            pygame.mixer.music.set_volume(self._stored_volume)

    def get_current_volume(self):
        """Devuelve el volumen almacenado (0.0 a 1.0)."""
        return self._stored_volume

    def is_muted(self):
        """Devuelve True si el audio está en silencio."""
        return self._is_muted
        
    def toggle_mute(self):
        """Alterna el estado de mute."""
        self._is_muted = not self._is_muted
        if self._is_muted:
            pygame.mixer.music.set_volume(0.0)
        else:
            pygame.mixer.music.set_volume(self._stored_volume)


# Crea una única instancia global para usar en todo el juego
audio_manager = AudioManager()