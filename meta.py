# meta.py

import pygame

class Meta(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, color=(0, 255, 0)):
        super().__init__()
        
        # Crear superficie transparente (como lo hiciste con Obstaculo)
        self.image = pygame.Surface([ancho, alto], pygame.SRCALPHA)
        self.image.fill((color)) #COLOCAR 0,0,0,0 PARA NO VEL / COLOCA color PARA VER
        
        # Rectángulo de colisión
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        # La meta es estática
        pass