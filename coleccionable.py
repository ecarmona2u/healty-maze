# coleccionable.py (Mantiene la lógica de movimiento y el constructor simple)

import pygame
import os 
import math 

# --- CONSTANTES DE MOVIMIENTO ---
# Distancia MÁXIMA que se moverá hacia arriba (30 píxeles)
ALTURA_MOVIMIENTO = 5
# Velocidad con la que se mueve (mayor valor = movimiento más rápido)
VELOCIDAD_VERTICAL = 3 

# --- VALORES DE EFECTO (sin cambios) ---
VELOCIDAD_BONUS = 0.2

# --- MAPEO DE COLECCIONABLES A ARCHIVOS (ACTUALIZADO y AMPLIADO) ---
# Usamos nuevos índices para los nuevos coleccionables.
# NOTA: Los nombres de archivo asumen que ahora están directamente en la carpeta 'buenos' o 'malos'.
ANIMATION_SETS = {
    # COLECCIONABLES BUENOS (LEVEL 1)
    0: {"base_path": "recursos/coleccionables/buenos/level_1", "filename": "AGUA.PNG", "is_good": True, "effect": VELOCIDAD_BONUS}, 
    1: {"base_path": "recursos/coleccionables/buenos/level_1", "filename": "ALMOHADA.PNG", "is_good": True, "effect": VELOCIDAD_BONUS}, 
    2: {"base_path": "recursos/coleccionables/buenos/level_1", "filename": "LIBRO.PNG", "is_good": True, "effect": VELOCIDAD_BONUS}, 
    
    # COLECCIONABLES MALOS (LEVEL 1)
    3: {"base_path": "recursos/coleccionables/malos/level_1", "filename": "CELULAR.PNG", "is_good": False}, 
    4: {"base_path": "recursos/coleccionables/malos/level_1", "filename": "DULCE.PNG", "is_good": False}, 
    5: {"base_path": "recursos/coleccionables/malos/level_1", "filename": "REFRESCO.PNG", "is_good": False}, 

    # COLECCIONABLES BUENOS (LEVEL 2)
    6: {"base_path": "recursos/coleccionables/buenos/level_2", "filename": "CEPILLO DE DIENTES.PNG", "is_good": True, "effect": VELOCIDAD_BONUS}, 
    7: {"base_path": "recursos/coleccionables/buenos/level_2", "filename": "LAVARSE MANOS.PNG", "is_good": True, "effect": VELOCIDAD_BONUS}, 
    8: {"base_path": "recursos/coleccionables/buenos/level_2", "filename": "MANZANA.PNG", "is_good": True, "effect": VELOCIDAD_BONUS}, 

    # COLECCIONABLES MALOS (LEVEL 2)
    9: {"base_path": "recursos/coleccionables/malos/level_2", "filename": "BASURA.PNG", "is_good": False}, 
    10: {"base_path": "recursos/coleccionables/malos/level_2", "filename": "CHOCOLATE.PNG", "is_good": False}, 
    11: {"base_path": "recursos/coleccionables/malos/level_2", "filename": "HAMBURGUESA.PNG", "is_good": False}, 
    
    # Nota: Los coleccionables de level_3 pueden continuar la numeración si los agregas.
}

MAX_INDEX = 11 # El índice máximo ahora es 11

# --- CONSTANTE DE TAMAÑOS (Añadiendo el resto, asumiendo 50x50 para la simplicidad) ---
IMAGE_SIZES = {
    0: (50, 50), 1: (50, 70), 2: (60, 60),
    3: (50, 50), 4: (70, 70), 5: (50, 50),
    6: (70, 50), 7: (50, 50), 8: (70, 70),
    9: (50, 50), 10: (50, 50), 11: (50, 50),
}


# --- CLASE COLECCIONABLE ---

class Coleccionable(pygame.sprite.Sprite):
    
    def __init__(self, x, y, index, size=None):
        super().__init__()
        
        if index not in ANIMATION_SETS:
             # Se actualiza el mensaje de error con el nuevo MAX_INDEX
             raise ValueError(f"Índice de coleccionable {index} no es válido. Debe ser entre 0 y {MAX_INDEX}.")
             
        self.index = index
        
        self.images = []        
        self.final_size = IMAGE_SIZES.get(index, (50, 50)) 
        
        self.load_images(index)
        
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # --- VARIABLES DE MOVIMIENTO ---
        self.start_y = y 
        self.movement_time = 0.0 
        
        self.frame_index = 0 

    def load_images(self, index):
        """
        Carga la imagen única PNG para el coleccionable.
        """
        config = ANIMATION_SETS[index]
        
        # Construye la ruta: 'base_path/filename'
        path = os.path.join(config['base_path'], config['filename'])
        
        try:
            # Añade una advertencia si el archivo no existe
            if not os.path.exists(path):
                 print(f"ADVERTENCIA: Archivo no encontrado en {path}. Usando fallback.")
                 raise pygame.error("File not found")

            original = pygame.image.load(path).convert_alpha()
            scaled = pygame.transform.scale(original, self.final_size)
            self.images.append(scaled)
        except pygame.error:
            # Fallback
            fallback_color = (0, 255, 0) if config['is_good'] else (255, 0, 0)
            fallback = pygame.Surface(self.final_size)
            fallback.fill(fallback_color)
            self.images.append(fallback)
            
        if not self.images:
            fallback = pygame.Surface(self.final_size); fallback.fill((255, 0, 255))
            self.images.append(fallback)


    def update(self, dt):
        """
        Mueve el coleccionable 30 píxeles hacia arriba y regresa a su posición inicial (start_y).
        """
        dt_seconds = dt / 1000.0 
        
        self.movement_time += dt_seconds * VELOCIDAD_VERTICAL
        
        # Fórmula para el movimiento de rebote suave de 0 a ALTURA_MOVIMIENTO
        offset_up = abs(math.sin(self.movement_time)) * ALTURA_MOVIMIENTO
        
        # Mueve hacia arriba (restamos Y)
        self.rect.y = self.start_y - offset_up
            
    def get_effect_value(self):
        """
        Devuelve el valor del efecto del coleccionable.
        """
        config = ANIMATION_SETS[self.index]
        if config.get("is_good"):
            return config.get("effect", 0.0)
        return 0.0