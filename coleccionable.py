# coleccionable.py (ACTUALIZADO para la nueva estructura /buenos/ y /malos/)

import pygame
import os 

# --- CONSTANTES DE ANIMACIÓN ---
# Tiempo entre cada frame de la animación (en milisegundos).
ANIMATION_SPEED = 100 
NUM_FRAMES = 12 # Todos los sets tienen 12 imágenes (1 a 12)

# --- MAPEO DE COLECCIONABLES A CARPETAS ---
# Definimos las carpetas base y el prefijo de archivo para cada índice.
# Asignamos índices 0-2 a los "buenos" y 3-5 a los "malos".
ANIMATION_SETS = {
    # COLECCIONABLES BUENOS (Índices 0, 1, 2) - Tienen animación
    0: {"base_path": "recursos/coleccionables/buenos/almoada", "prefix": "almoada_"}, 
    1: {"base_path": "recursos/coleccionables/buenos/libros", "prefix": "libros_"}, 
    2: {"base_path": "recursos/coleccionables/buenos/manzana", "prefix": "manzana_"}, 
    
    # COLECCIONABLES MALOS (PENALIZACIONES) (Índices 3, 4, 5) - Tienen animación
    3: {"base_path": "recursos/coleccionables/malos/celular", "prefix": "celular_"}, 
    4: {"base_path": "recursos/coleccionables/malos/paleta", "prefix": "paleta_"}, 
    5: {"base_path": "recursos/coleccionables/malos/refresco", "prefix": "refresco_"}, 
}

MAX_INDEX = 5 # El índice más alto usado en ANIMATION_SETS


# --- CONSTANTE DE TAMAÑOS ---
IMAGE_SIZES = {
    # Buenos
    0: (50, 50), # Almoada
    1: (50, 50), # Libros
    2: (50, 50), # Manzana
    
    # Malos (Penalizaciones)
    3: (40, 55), # Celular (Un poco más grande para ser llamativo)
    4: (55, 55), # Paleta
    5: (40, 55), # Refresco
}


# --- CLASE COLECCIONABLE ---

class Coleccionable(pygame.sprite.Sprite):
    
    def __init__(self, x, y, index, size=None):
        super().__init__()
        
        if index not in ANIMATION_SETS:
             raise ValueError(f"Índice de coleccionable {index} no es válido. Debe ser entre 0 y {MAX_INDEX}.")
             
        self.index = index
        self.is_animated = True # ¡Ahora todos se animan!
        
        # 1. Configuración de Animación
        self.images = []        
        self.frame_index = 0    
        self.animation_timer = 0 
        
        self.final_size = IMAGE_SIZES.get(index, (50, 50)) 
        
        # 2. Cargar imágenes
        self.load_images(index)
        
        # 3. Asignar imagen inicial y rect
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def load_images(self, index):
        
        config = ANIMATION_SETS[index]
        
        for i in range(1, NUM_FRAMES + 1):
            
            # Construye la ruta: 'base_path/prefix_i.png'
            # Ejemplo: recursos/coleccionables/buenos/almoada/almoada_1.png
            filename = f"{config['prefix']}{i}.png"
            path = os.path.join(config['base_path'], filename)
            
            try:
                original = pygame.image.load(path).convert_alpha()
                scaled = pygame.transform.scale(original, self.final_size)
                self.images.append(scaled)
            except pygame.error:
                print(f"Error cargando frame: {path}")
                
                # Fallback: Color según si es bueno (<=2) o malo (>=3)
                fallback_color = (0, 255, 0) if index <= 2 else (255, 0, 0)
                fallback = pygame.Surface(self.final_size)
                fallback.fill(fallback_color)
                self.images.append(fallback)
                
        # Asegurarse de que al menos hay una imagen (el fallback)
        if not self.images:
            fallback = pygame.Surface(self.final_size); fallback.fill((255, 0, 255))
            self.images.append(fallback)


    def update(self, dt):
        """Actualiza la animación de todos los coleccionables."""
        
        # Incrementa el temporizador con el tiempo transcurrido (dt)
        self.animation_timer += dt
        
        if self.animation_timer >= ANIMATION_SPEED:
            self.animation_timer = 0
            
            # Cicla el índice de frame
            self.frame_index = (self.frame_index + 1) % len(self.images)
            
            # Asigna la nueva imagen al sprite
            self.image = self.images[self.frame_index]
            
# --- RECUERDA ---
# Debes llamar a `coleccionables_group.update(dt)` en el bucle principal de tus niveles.