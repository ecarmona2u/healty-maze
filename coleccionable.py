# coleccionable.py

import pygame

# --- RUTAS DE IMÁGENES (AJUSTA ESTO A TUS ARCHIVOS) ---

# Rutas de los 6 coleccionables buenos (índices 0 a 5)
PATH_COLECTABLE_1 = "recursos/coleccionables/colectable_1.png" 
PATH_COLECTABLE_2 = "recursos/coleccionables/colectable_2.png" 
PATH_COLECTABLE_3 = "recursos/coleccionables/colectable_3.png"
PATH_COLECTABLE_4 = "recursos/coleccionables/colectable_4.png"
PATH_COLECTABLE_5 = "recursos/coleccionables/colectable_5.png"
PATH_COLECTABLE_6 = "recursos/coleccionables/colectable_6.png"

# Rutas de las 3 imágenes de penalización (índices 6 a 8)
PATH_PENALIZACION_1 = "recursos/malus/malus_1.png" 
PATH_PENALIZACION_2 = "recursos/malus/malus_2.png" 
PATH_PENALIZACION_3 = "recursos/malus/malus_3.png" 

# --- CONSTANTE DE TAMAÑOS (Nueva adición para personalizar tamaños por índice) ---
# Puedes cambiar los tamaños predeterminados aquí. Si un índice no está listado, usará (50, 50).
IMAGE_SIZES = {
    # Coleccionables buenos (índices 0-5)
    0: (50, 50), # Ejemplo: Más pequeño
    1: (50, 50), 
    2: (50, 50),
    3: (50, 50),
    4: (50, 50),
    5: (50, 50),
    
    # Penalizaciones (índices 6-8)
    6: (40, 20), # Ejemplo: Más grande para que destaque
    7: (40, 50),
    8: (40, 50),
}
# --- CLASE COLECCIONABLE ---

class Coleccionable(pygame.sprite.Sprite):
    
    # Lista maestra de paths de imágenes para todos los coleccionables
    IMAGE_PATHS = [
        PATH_COLECTABLE_1, PATH_COLECTABLE_2, PATH_COLECTABLE_3, 
        PATH_COLECTABLE_4, PATH_COLECTABLE_5, PATH_COLECTABLE_6,
        PATH_PENALIZACION_1, # Index 6
        PATH_PENALIZACION_2, # Index 7
        PATH_PENALIZACION_3  # Index 8
    ]
    
    def __init__(self, x, y, index, size=None):
        super().__init__()
        self.index = index
        
        # ✅ Lógica para obtener el tamaño: usa el dict, o (50, 50) por defecto si no está listado
        final_size = IMAGE_SIZES.get(index, (50, 50)) 
        
        self.image = self.load_image(index, final_size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def load_image(self, index, size):
        try:
            path = Coleccionable.IMAGE_PATHS[index]
            original = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(original, size) 
        except (pygame.error, IndexError):
            # Fallback en caso de que una imagen no se cargue.
            fallback = pygame.Surface(size)
            # Rojo para penalización (6+) y Verde para buenos (0-5)
            fallback_color = (255, 0, 0) if index >= 6 else (0, 255, 0)
            fallback.fill(fallback_color)
            return fallback