# player.py (FINAL - Colisión Laberinto y Velocidad Normalizada)

import pygame
import math 

class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos, character_data, screen_width, screen_height):
        super().__init__()
        
        self.animations = character_data['sprites'] 
        self.direction = 'front'
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # --- ESTADOS DEL JUGADOR ---
        self.is_moving = False
        self.frame_index = 0
        self.animation_speed = 0.1 
        
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=start_pos)
        
        self.speed = 2 # velocidad de personaje
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        move_vector = [0, 0] 
        self.is_moving = False 
        
        # --- Recoger Entrada y Construir el Vector ---
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_vector[1] -= 1
            self.direction = 'back'
            self.is_moving = True
            
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_vector[1] += 1
            self.direction = 'front'
            self.is_moving = True
            
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_vector[0] -= 1
            self.direction = 'left'
            self.is_moving = True
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_vector[0] += 1
            self.direction = 'right'
            self.is_moving = True
            
        return move_vector # Retorna el vector de dirección

    def mover_y_verificar_colision(self, move_vector, obstaculo_group):
        """Mueve al jugador separando los ejes X e Y para colisiones rígidas."""
        
        dx = move_vector[0]
        dy = move_vector[1]
        
        # 1. Normalización de la velocidad (evita el movimiento diagonal rápido)
        current_speed = self.speed
        if dx != 0 and dy != 0:
            current_speed = self.speed * (1 / math.sqrt(2))
            
        # 2. MOVER EN EL EJE X y verificar colisión
        self.rect.x += dx * current_speed
        self.verificar_colisiones_eje_x(obstaculo_group)

        # 3. MOVER EN EL EJE Y y verificar colisión
        self.rect.y += dy * current_speed
        self.verificar_colisiones_eje_y(obstaculo_group)


    def verificar_colisiones_eje_x(self, obstaculo_group):
        """Detiene el movimiento horizontal al colisionar."""
        colisiones = pygame.sprite.spritecollide(self, obstaculo_group, False)
        for obstaculo in colisiones:
            if self.rect.x > obstaculo.rect.x:
                # Colisión por la izquierda, empujar a la derecha del obstáculo
                self.rect.left = obstaculo.rect.right
            else:
                # Colisión por la derecha, empujar a la izquierda del obstáculo
                self.rect.right = obstaculo.rect.left


    def verificar_colisiones_eje_y(self, obstaculo_group):
        """Detiene el movimiento vertical al colisionar."""
        colisiones = pygame.sprite.spritecollide(self, obstaculo_group, False)
        for obstaculo in colisiones:
            if self.rect.y > obstaculo.rect.y:
                # Colisión por arriba, empujar debajo del obstáculo
                self.rect.top = obstaculo.rect.bottom
            else:
                # Colisión por abajo, empujar encima del obstáculo
                self.rect.bottom = obstaculo.rect.top

        
    def constrain(self):
        """Mantiene al jugador dentro de los límites de la pantalla."""
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        
    def update(self, obstaculo_group=None):
        
        move_vector = self.get_input()
        
        # Solo movemos y verificamos colisión si hay movimiento
        if self.is_moving and obstaculo_group is not None:
            self.mover_y_verificar_colision(move_vector, obstaculo_group)

        self.constrain() 
        self.animate()
        
    def animate(self):
        
        animation_list = self.animations[self.direction]
        
        if self.is_moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation_list):
                self.frame_index = 0
        else:
            self.frame_index = 0 
            
        self.image = animation_list[int(self.frame_index)]