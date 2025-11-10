# player.py (MODIFICADO: Añadido increase_speed)

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
        
        # --- ATRIBUTO DE VELOCIDAD CLAVE ---
        self.speed = 3.0 # velocidad de personaje (Aseguramos que sea float para las sumas)
    
    def get_input(self):
        # ... (Método get_input sin cambios) ...
        keys = pygame.key.get_pressed()
        
        move_vector = [0, 0] 
        self.is_moving = False 
        
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
            
        return move_vector 

    def mover_y_verificar_colision(self, move_vector, obstaculo_group):
        # ... (Método de movimiento sin cambios) ...
        dx = move_vector[0]
        dy = move_vector[1]
        
        current_speed = self.speed
        if dx != 0 and dy != 0:
            current_speed = self.speed * (1 / math.sqrt(2))
            
        self.rect.x += dx * current_speed
        self.verificar_colisiones_eje_x(obstaculo_group)

        self.rect.y += dy * current_speed
        self.verificar_colisiones_eje_y(obstaculo_group)


    def verificar_colisiones_eje_x(self, obstaculo_group):
        # ... (Método de colisión X sin cambios) ...
        colisiones = pygame.sprite.spritecollide(self, obstaculo_group, False)
        for obstaculo in colisiones:
            if self.rect.x > obstaculo.rect.x:
                self.rect.left = obstaculo.rect.right
            else:
                self.rect.right = obstaculo.rect.left


    def verificar_colisiones_eje_y(self, obstaculo_group):
        # ... (Método de colisión Y sin cambios) ...
        colisiones = pygame.sprite.spritecollide(self, obstaculo_group, False)
        for obstaculo in colisiones:
            if self.rect.y > obstaculo.rect.y:
                self.rect.top = obstaculo.rect.bottom
            else:
                self.rect.bottom = obstaculo.rect.top

        
    def constrain(self):
        # ... (Método constrain sin cambios) ...
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        
    def update(self, obstaculo_group=None):
        # ... (Método update sin cambios) ...
        move_vector = self.get_input()
        
        if self.is_moving and obstaculo_group is not None:
            self.mover_y_verificar_colision(move_vector, obstaculo_group)

        self.constrain() 
        self.animate()
        
    def animate(self):
        # ... (Método animate sin cambios) ...
        animation_list = self.animations[self.direction]
        
        if self.is_moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation_list):
                self.frame_index = 0
        else:
            self.frame_index = 0 
            
        self.image = animation_list[int(self.frame_index)]

    # --- NUEVO MÉTODO DE MODIFICACIÓN DE VELOCIDAD ---
    def increase_speed(self, amount):
        """Aumenta la velocidad del personaje."""
        self.speed += amount
        print(f"Velocidad aumentada a: {self.speed:.2f}")