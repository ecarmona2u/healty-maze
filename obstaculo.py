# obstaculo.py (ACTUALIZADO para Transparencia)

import pygame

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, color=(150, 75, 0)):
        super().__init__()
        
        # 1. Crear la superficie con soporte para canal alfa (transparencia)
        # Esto permite que la imagen sea invisible mientras su .rect sigue funcionando.
        self.image = pygame.Surface([ancho, alto], pygame.SRCALPHA)
        
        # 2. Rellenar con un color completamente transparente (canal alfa 0)
        # El formato es (R, G, B, A), donde A=0 significa invisible.
        self.image.fill((color)) #COLOCAR 0,0,0,0 PARA NO VEL / COLOCA color PARA VER 
        
        # 3. Obtener el rectángulo (zona de colisión)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        pass