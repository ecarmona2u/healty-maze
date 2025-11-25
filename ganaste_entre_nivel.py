import pygame
import sys

# --- CONSTANTES DE RECURSOS ---
PATH_FONDO = "recursos/fondo_victoria1.png"
PATH_BTN_NEXT = "recursos/btn_siguiente.png" 
PATH_BTN_MENU = "recursos/btn_menu.png"     

BLANCO = (255, 255, 255)

# --- VALORES DE RETORNO ---
RETURN_NEXT_LEVEL = "NEXT_LEVEL"
RETURN_LEVEL_2 = "LEVEL_2" 
RETURN_REINTENTAR = "REINTENTAR" 


# CLASE BOTON (MODIFICADA para soportar animación y hover)
class Boton:
    """
    Clase para crear botones con imagen y acción, ahora incluye efecto hover
    de escalado (+10 píxeles) y detecta clics correctamente en el área del botón.
    """
    def __init__(self, x, y, ancho, alto, texto, accion, path_imagen):
        
        self.accion = accion
        self.original_size = (ancho, alto)
        self.hover_size = (ancho + 10, alto + 10) # 10 píxeles más grande
        
        # Carga y escalado de la imagen base
        try:
            img_original = pygame.image.load(path_imagen).convert_alpha()
            # Almacenamos las dos versiones de la imagen para el hover
            self.img_normal = pygame.transform.scale(img_original, self.original_size)
            self.img_hover = pygame.transform.scale(img_original, self.hover_size)
        except pygame.error as e:
            print(f"Error cargando imagen de botón {path_imagen}: {e}. Usando fallback.")
            # Fallback a un color sólido si la imagen no se carga
            self.img_normal = pygame.Surface(self.original_size, pygame.SRCALPHA)
            self.img_normal.fill((0, 150, 0, 180)) # Verde semi-transparente
            self.img_hover = pygame.Surface(self.hover_size, pygame.SRCALPHA)
            self.img_hover.fill((0, 200, 0, 255)) # Verde más brillante
        
        # Rectángulo base (usado para la detección de hover y posición original)
        self.rect_normal = self.img_normal.get_rect(topleft=(x, y))
        self.rect = self.rect_normal # Rectángulo actual
        
    def draw(self, surface):
        action = None
        pos = pygame.mouse.get_pos()
        
        is_hovering = self.rect_normal.collidepoint(pos)

        if is_hovering:
            # 1. Aplicar efecto hover: usar imagen y rectángulo más grande
            current_image = self.img_hover
            # Recalcular el rectángulo para centrar la imagen grande sobre la posición normal
            self.rect = current_image.get_rect(center=self.rect_normal.center)
        else:
            # 2. Estado normal: usar imagen y rectángulo normal
            current_image = self.img_normal
            self.rect = self.rect_normal
            
        # 3. Comprobar clic
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            action = self.accion

        # 4. Dibujar la imagen (grande o normal, centrada)
        surface.blit(current_image, self.rect) 
        
        return action


# FUNCIÓN PRINCIPAL DE LA PANTALLA
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

    # Botón 1: SIGUIENTE NIVEL (Grande, Derecha)
    btn_siguiente = Boton(
        830, BTN_Y, BTN_W_GRANDE, BTN_H_GRANDE, 
        "SIGUIENTE NIVEL", 
        RETURN_NEXT_LEVEL,
        PATH_BTN_NEXT 
    )
    
    # Botón 2: SELECTOR DE NIVEL (Pequeño, Izquierda)
    btn_menu = Boton(
        350, BTN_Y, BTN_W_PEQUENO, BTN_H_PEQUENO, 
        "LEVEL 2",
        RETURN_LEVEL_2, 
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
        # La función draw ahora maneja la detección de hover y el escalado
        accion_siguiente = btn_siguiente.draw(ventana)
        accion_menu = btn_menu.draw(ventana)
        
        if accion_siguiente:
            running = False
            return RETURN_NEXT_LEVEL, img_btn_regresar, REGRESAR_RECT 
        
        if accion_menu:
            running = False
            return RETURN_LEVEL_2, None, None 

        pygame.display.flip()
        clock.tick(60)
        
    # Fallback
    return RETURN_LEVEL_2, None, None