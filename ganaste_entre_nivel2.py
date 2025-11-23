import pygame
import sys

# --- CONSTANTES DE RECURSOS ---
PATH_FONDO = "recursos/fondo_victoria2.png"
PATH_BTN_NEXT = "recursos/btn_siguiente.png" 
PATH_BTN_MENU = "recursos/btn_menu.png"     

BLANCO = (255, 255, 255)

# --- VALORES DE RETORNO ---
RETURN_NEXT_LEVEL = "NEXT_LEVEL"
# 💡 RESTABLECEMOS a SELECTOR_NIVEL para el botón de menú
RETURN_SELECTOR_NIVEL = "SELECTOR_NIVEL" 
RETURN_REINTENTAR = "REINTENTAR" 


# CLASE BOTON (Necesaria para pantallas de Ganar y Perder)
class Boton:
    """Clase para crear botones con imagen y acción."""
    def __init__(self, x, y, ancho, alto, texto, accion, path_imagen):
        
        self.accion = accion
        
        # Carga de la imagen
        try:
            img_base = pygame.image.load(path_imagen).convert_alpha()
            self.img_base = pygame.transform.scale(img_base, (ancho, alto))
        except pygame.error:
            # Fallback a un color sólido si la imagen no se carga
            self.img_base = pygame.Surface((ancho, alto))
            self.img_base.fill((0, 150, 0)) # Verde para victoria

        self.rect = self.img_base.get_rect(topleft=(x, y))
        
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        
        # Comprobar colisión y clic
        if self.rect.collidepoint(pos):
            # Dibujar un borde o efecto de hover si es necesario
            
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        surface.blit(self.img_base, self.rect) 
        
        if action:
            return self.accion

        return None


# FUNCIÓN PRINCIPAL DE LA PANTALLA (run_pantalla_ganaste)
def run_pantalla_ganaste(ventana, img_btn_regresar=None, REGRESAR_RECT=None): 
    
    ANCHO, ALTO = ventana.get_size()
    clock = pygame.time.Clock()
    
    # 1. Cargar Fondo
    try:
        fondo = pygame.image.load(PATH_FONDO).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error:
        print(f"Error cargando fondo: {PATH_FONDO}. Usando color sólido.")
        fondo = pygame.Surface((ANCHO, ALTO)); fondo.fill((50, 50, 50))

    # 2. Configuración Común de Botones
    BTN_W_GRANDE, BTN_H_GRANDE = 300, 90 
    BTN_W_PEQUENO, BTN_H_PEQUENO = 90, 90 
    BTN_Y = 550
    
    # 3. Creación de Botones

    # Botón 1: SIGUIENTE NIVEL (Grande, Derecha) -> Mandará a Level 3
    btn_siguiente = Boton(
        830, BTN_Y, BTN_W_GRANDE, BTN_H_GRANDE, 
        "SIGUIENTE NIVEL", 
        RETURN_NEXT_LEVEL, # <-- Este valor hará que juego_principal cargue nivel 3
        PATH_BTN_NEXT 
    )
    
    # Botón 2: SELECTOR DE NIVEL (Pequeño, Izquierda)
    btn_menu = Boton(
        350, BTN_Y, BTN_W_PEQUENO, BTN_H_PEQUENO, 
        "NIVELES", 
        RETURN_SELECTOR_NIVEL, # <-- Devuelve al selector de nivel
        PATH_BTN_MENU 
    )

    # 4. Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
        ventana.blit(fondo, (0, 0))

        # Dibujo y Lógica
        accion_siguiente = btn_siguiente.draw(ventana)
        accion_menu = btn_menu.draw(ventana)
        
        if accion_siguiente:
            running = False
            # Devuelve 3 valores
            return RETURN_NEXT_LEVEL, img_btn_regresar, REGRESAR_RECT 
        
        if accion_menu:
            running = False
            # Devuelve 3 valores
            return RETURN_SELECTOR_NIVEL, None, None 

        pygame.display.flip()
        clock.tick(60)
        
    # Fallback
    return RETURN_SELECTOR_NIVEL, None, None