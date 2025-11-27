# audio_manager.py (CÓDIGO COMPLETO CON CONTROL DE VOLUMEN DE SFX Y CORRECCIONES)

import pygame
import sys

# --- CONSTANTES DE RUTA ---
PATH_MUSICA_MENU = "recursos/musica/menu.mp3"
PATH_MUSICA_NIVEL_1 = "recursos/musica/level_1.mp3"
PATH_MUSICA_NIVEL_2 = "recursos/musica/level_2.mp3"
PATH_MUSICA_NIVEL_3 = "recursos/musica/level_3.mp3"
# 🚨 NOTA: Tanto el selector como el menú principal usan el mismo archivo MP3.
PATH_MUSICA_SELECTOR = "recursos/musica/menu.mp3" 
PATH_MUSICA_TUTORIAL = "recursos/musica/musica_niveles.mp3" 

# 🚨 CONSTANTES PARA LOS EFECTOS DE SONIDO DE COLECCIONABLES
PATH_SFX_GOOD = "recursos/audio/item_bueno.mp3"
PATH_SFX_BAD = "recursos/audio/item_malo.mp3"

# 🚨 VOLUMEN DE LOS EFECTOS DE SONIDO (0.0 a 1.0)
SFX_VOLUME = 0.5 # <--- AJUSTA ESTE VALOR PARA HACERLO MÁS FUERTE O SUAVE

class AudioManager:
    def __init__(self):
        # Inicializar el mixer
        if not pygame.mixer.get_init():
            try:
                # Se aumenta el buffer para mejor gestión de SFX cortos
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024) 
            except pygame.error as e:
                print(f"Error al inicializar el mixer de Pygame: {e}")
                sys.exit()

        self.music_paths = {
            'menu_principal': PATH_MUSICA_MENU,
            'nivel_1': PATH_MUSICA_NIVEL_1,
            'nivel_2': PATH_MUSICA_NIVEL_2,
            'nivel_3': PATH_MUSICA_NIVEL_3,
            'selector': PATH_MUSICA_SELECTOR,
            'tutorial': PATH_MUSICA_TUTORIAL,
        }
        self.MUSICA_ACTUAL = None
        self.is_music_paused = False
        
        # Gestor de volumen y mute (para MÚSICA)
        self._stored_volume = 0.3    
        self._is_muted = False
        pygame.mixer.music.set_volume(self._stored_volume)
        
        # 🚨 Carga de SFX de coleccionables
        try:
            self.sfx_good = pygame.mixer.Sound(PATH_SFX_GOOD)
            self.sfx_bad = pygame.mixer.Sound(PATH_SFX_BAD)
            
            # 👇 APLICAR VOLUMEN BAJO A CADA SFX
            self.sfx_good.set_volume(SFX_VOLUME)
            self.sfx_bad.set_volume(SFX_VOLUME)
            
        except pygame.error as e:
            print(f"Error al cargar SFX (bueno/malo): {e}. Asegúrese de que 'recursos/audio/item_bueno.mp3' y 'item_malo.mp3' existan.")
            # Fallback (para evitar AttributeError en play_collect_...)
            self.sfx_good = type('DummySound', (object,), {'play': lambda: None})()
            self.sfx_bad = type('DummySound', (object,), {'play': lambda: None})()

    # --- NUEVOS MÉTODOS PARA SFX ---
    def play_collect_good(self):
        """Reproduce el sonido al recoger un objeto bueno."""
        self.sfx_good.play()
        
    def play_collect_bad(self):
        """Reproduce el sonido al recoger un objeto malo."""
        self.sfx_bad.play()


    # --- CONTROL DE MÚSICA (Play/Pause/Stop) ---
    def play_music(self, track_name, loop=-1):
        """Reproduce la música especificada, respetando el estado de mute."""
        path = self.music_paths.get(track_name)
        if not path:
            print(f"ADVERTENCIA: Pista de música '{track_name}' no encontrada. Revisa las rutas.")
            return

        if track_name == self.MUSICA_ACTUAL and (pygame.mixer.music.get_busy() or self.is_music_paused):
            # Si la pista solicitada ya está sonando, no hacemos nada.
            return

        try:
            # 💡 NOTA: La condición 'track_name != self.MUSICA_ACTUAL' es lo que evita el reinicio
            # cuando la música es la misma. Si la pista solicitada es diferente, se recarga.
            if track_name != self.MUSICA_ACTUAL or not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(loop)
                self.MUSICA_ACTUAL = track_name
                self.is_music_paused = False
                
                if not self._is_muted:
                    pygame.mixer.music.set_volume(self._stored_volume)
                else:
                    pygame.mixer.music.set_volume(0.0)
                
        except pygame.error as e:
            print(f"Error CRÍTICO al reproducir la música: {e}. Asegúrate que el archivo sea un MP3 válido.") 

    def pause_music(self):
        """Pausa la música si está sonando. (Corregido el error de get_paused)"""
        # 💡 CORRECCIÓN: Usar self.is_music_paused
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


# Crea una única instancia global para usar en todo el juego (audio_manager en minúscula)
audio_manager = AudioManager()