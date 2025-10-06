# ganaste_entre_nivel.py (Pantalla de victoria con imagen de fondo y botones)

import pygame
import sys

# --- CONSTANTES ---
PATH_FONDO_VICTORIA = "recursos/fondo_victoria.png"
# Paths de las imágenes de botones
PATH_BTN_NEXT = "recursos/btn_siguiente.png" 
PATH_BTN_MENU = "recursos/botones/btn_menu.png"     

BLANCO = (255, 255, 255)

# --- VALORES DE RETORNO (para comunicación con juego_principal.py) ---
RETURN_NEXT_LEVEL = "NEXT_LEVEL"
RETURN_MENU = "MENU"


# =========================================================
# CLASE BOTON (Sin Cambios, ya acepta ancho y alto)
# =========================================================
class Boton:
    def __init__(self, x, y, ancho, alto, texto, accion, path_imagen):
        
        self.accion = accion
        
        # 1. Cargar y escalar la única imagen con el ancho y alto específicos
        try:
            img_base = pygame.image.load(path_imagen).convert_alpha()
            self.img_base = pygame.transform.scale(img_base, (ancho, alto))
        except pygame.error as e:
            # Fallback en caso de que la imagen no cargue
            print(f"Error cargando botón de imagen: {e}. Usando fallback.")
            self.img_base = pygame.Surface((ancho, alto)); self.img_base.fill((100, 100, 100))
            
        # 2. Definir el rectángulo de colisión y posición
        self.rect = self.img_base.get_rect(topleft=(x, y))
        

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        
        # 1. Detectar clic (la única lógica de interacción)
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # 2. Dibujar la imagen del botón
        surface.blit(self.img_base, self.rect) 
        
        if action:
            return self.accion

        return None


# =========================================================
# FUNCIÓN PRINCIPAL DE LA PANTALLA
# =========================================================
def run_pantalla_ganaste(ventana, img_btn_regresar=None, REGRESAR_RECT=None): 
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # 1. Cargar Fondo de Victoria
    try:
        fondo_victoria = pygame.image.load(PATH_FONDO_VICTORIA).convert()
        fondo_victoria = pygame.transform.scale(fondo_victoria, (ANCHO, ALTO))
    except pygame.error as e:
        print(f"Error cargando fondo de victoria: {e}")
        fondo_victoria = pygame.Surface((ANCHO, ALTO)); fondo_victoria.fill((50, 50, 50))

    # 2. Crear Botones con tamaños y posiciones individuales
    
    # ----------------------------------------------------
    # CONFIGURACIÓN DEL BOTÓN 1: SIGUIENTE NIVEL
    # ----------------------------------------------------
    #TAMAÑO ESPECÍFICO PARA EL BOTÓN DE SIGUIENTE NIVEL
    next_ancho = 300 
    next_alto = 90
    
    #POSICIÓN ESPECÍFICA (Centrado en X, 100 píxeles por encima del centro Y)
    next_x = (600)
    next_y = (500) 
    
    btn_siguiente = Boton(
        next_x, 
        next_y, 
        next_ancho, 
        next_alto, 
        "SIGUIENTE NIVEL", 
        RETURN_NEXT_LEVEL,
        PATH_BTN_NEXT 
    )
    
    # ----------------------------------------------------
    # CONFIGURACIÓN DEL BOTÓN 2: IR AL MENÚ
    # ----------------------------------------------------
    # ESPECÍFICO PARA EL BOTÓN DE MENÚ (más pequeño)
    menu_ancho = 90 
    menu_alto = 90
    
    #ESPECÍFICA (Centrado en X, 50 píxeles por debajo del centro Y)
    menu_x = (400)
    menu_y = (500) 
    
    btn_menu = Boton(
        menu_x, 
        menu_y, 
        menu_ancho, 
        menu_alto, 
        "MENÚ PRINCIPAL", 
        RETURN_MENU,
        PATH_BTN_MENU 
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
        ventana.blit(fondo_victoria, (0, 0))

        accion_siguiente = btn_siguiente.draw(ventana)
        accion_menu = btn_menu.draw(ventana)
        
        # 6. Devolver el resultado de la acción
        if accion_siguiente:
            running = False
            return RETURN_NEXT_LEVEL, img_btn_regresar, REGRESAR_RECT
        
        if accion_menu:
            running = False
            return RETURN_MENU, None, None 

        pygame.display.flip()
        clock.tick(60)
        
    return RETURN_MENU, None, None