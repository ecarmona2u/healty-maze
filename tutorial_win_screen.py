import pygame
import sys

# --- CONSTANTES ---
PATH_FONDO_TUTORIAL_WIN = "recursos/fondo_victoria0.png" 
PATH_BTN_LEVEL_1 = "recursos/btn_nivel_1.png" 
PATH_BTN_MENU = "recursos/btn_menu.png"     
PATH_IMAGEN_DECORATIVA = "recursos/sabes_jugar.png" # Asegúrate de tener esta imagen

# --- VALORES DE RETORNO ESPECÍFICOS ---
RETURN_LEVEL_1 = "nivel_1" 
RETURN_MENU = "MENU"


# CLASE BOTON
class Boton:
    def __init__(self, x, y, ancho, alto, accion, path_imagen):
        
        self.accion = accion
        
        try:
            img_base = pygame.image.load(path_imagen).convert_alpha()
            self.img_base = pygame.transform.scale(img_base, (ancho, alto))
        except pygame.error as e:
            # Fallback si la imagen no se encuentra
            self.img_base = pygame.Surface((ancho, alto)); self.img_base.fill((100, 100, 100))
            
        self.rect = self.img_base.get_rect(topleft=(x, y))
        

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            # Dibuja un borde resaltado
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 3, 5) 
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        surface.blit(self.img_base, self.rect) 
        
        if action:
            return self.accion

        return None

# CLASE IMAGEN DECORATIVA 
class ImagenDecorativa:
    def __init__(self, x, y, ancho, alto, path_imagen):
        try:
            img_base = pygame.image.load(path_imagen).convert_alpha()
            self.imagen = pygame.transform.scale(img_base, (ancho, alto))
        except pygame.error as e:
            # Fallback si la imagen no se encuentra
            self.imagen = pygame.Surface((ancho, alto)); self.imagen.fill((200, 50, 50))
            
        self.rect = self.imagen.get_rect(topleft=(x, y))
        
    def draw(self, surface):
        surface.blit(self.imagen, self.rect)


# FUNCIÓN PRINCIPAL DE LA PANTALLA DE VICTORIA DEL TUTORIAL
def run_pantalla_tutorial_win(ventana, img_btn_regresar=None, REGRESAR_RECT=None): 
    
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()
    clock = pygame.time.Clock()
    
    # 1. Cargar Fondo de Victoria
    try:
        fondo_victoria = pygame.image.load(PATH_FONDO_TUTORIAL_WIN).convert()
        fondo_victoria = pygame.transform.scale(fondo_victoria, (ANCHO, ALTO))
    except pygame.error:
        fondo_victoria = pygame.Surface((ANCHO, ALTO)); fondo_victoria.fill((0, 80, 0)) 

    # 2. Creación Individual de Elementos (COORDENADAS Y TAMAÑO INDIVIDUALES)

    # 2.1 Botón 1: Menú Principal (Personaliza estas variables)
    BTN_MENU_W, BTN_MENU_H = 90, 90 
    BTN_MENU_X = 350 # Posición X
    BTN_MENU_Y = 531 # Posición Y
    
    btn_menu = Boton(
        BTN_MENU_X, 
        BTN_MENU_Y, 
        BTN_MENU_W, 
        BTN_MENU_H, 
        RETURN_MENU,
        PATH_BTN_MENU 
    )
    
    # 2.2 Botón 2: Nivel 1 (Personaliza estas variables)
    BTN_NIVEL_1_W, BTN_NIVEL_1_H = 452, 90 
    BTN_NIVEL_1_X = 520 # Posición X
    BTN_NIVEL_1_Y = 531 # Posición Y
    
    btn_nivel_1 = Boton(
        BTN_NIVEL_1_X, 
        BTN_NIVEL_1_Y, 
        BTN_NIVEL_1_W, 
        BTN_NIVEL_1_H, 
        RETURN_LEVEL_1,
        PATH_BTN_LEVEL_1 
    )
    
    # mensaje
    IMG_DECO_W, IMG_DECO_H = 696, 394 
    IMG_DECO_X = 300 # Posición X
    IMG_DECO_Y = 100 # Posición Y
    
    imagen_decorativa = ImagenDecorativa(
        IMG_DECO_X,
        IMG_DECO_Y,
        IMG_DECO_W,
        IMG_DECO_H,
        PATH_IMAGEN_DECORATIVA
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
        ventana.blit(fondo_victoria, (0, 0))

        # 3. Dibujar Elementos
        imagen_decorativa.draw(ventana) # Imagen decorativa
        
        accion_menu = btn_menu.draw(ventana)
        accion_nivel_1 = btn_nivel_1.draw(ventana)

        # 4. Devolver el resultado de la acción
        if accion_menu:
            return RETURN_MENU, None, None 
        
        if accion_nivel_1:
            return RETURN_LEVEL_1, img_btn_regresar, REGRESAR_RECT 
        
        pygame.display.flip()
        clock.tick(60)
        
    return RETURN_MENU, None, None