import pygame
import sys
# Asegúrate de que esta importación sea correcta para tu función de traducción
from traduccion import obtener_ruta_imagen_traducida 

# --- CONSTANTES ---
PATH_FONDO_TUTORIAL_WIN = "recursos/fondo_victoria0.png" 
PATH_BTN_LEVEL_1_BASE = "btn_siguiente.png"      # Ruta Base para traducción
PATH_BTN_MENU = "recursos/botones/btn_menu.png"     # Ruta completa, NO se traduce
PATH_IMAGEN_DECORATIVA_BASE = "sabes_jugar.png"  # Ruta Base para traducción

# --- VALORES DE RETORNO ESPECÍFICOS ---
RETURN_LEVEL_1 = "nivel_1" 
RETURN_MENU = "MENU"


# CLASE BOTON (Actualizada para usar traducción condicional)
class Boton:
    """
    Clase para crear botones con imagen y acción. 
    Usa el parámetro 'traducir' para decidir si usa la función de traducción.
    """
    def __init__(self, x, y, ancho, alto, accion, path_imagen, traducir=True): 
        
        self.accion = accion
        self.original_size = (ancho, alto)
        self.hover_size = (ancho + 10, alto + 10) 
        
        try:
            # LÓGICA DE CARGA: Si traducir es True, usa la función de traducción
            if traducir:
                path_a_cargar = obtener_ruta_imagen_traducida(path_imagen)
            else:
                # Si traducir es False, carga la ruta completa directamente
                path_a_cargar = path_imagen
                
            img_original = pygame.image.load(path_a_cargar).convert_alpha()
            
            # Almacenamos las dos versiones de la imagen para el hover
            self.img_normal = pygame.transform.scale(img_original, self.original_size)
            self.img_hover = pygame.transform.scale(img_original, self.hover_size)
        except pygame.error as e:
            print(f"Error cargando imagen de botón {path_imagen}: {e}. Usando fallback.")
            # Fallback a un color sólido si la imagen no se carga
            self.img_normal = pygame.Surface(self.original_size, pygame.SRCALPHA)
            self.img_normal.fill((0, 150, 0, 180)) 
            self.img_hover = pygame.Surface(self.hover_size, pygame.SRCALPHA)
            self.img_hover.fill((0, 200, 0, 255)) 
        
        self.rect_normal = self.img_normal.get_rect(topleft=(x, y))
        self.rect = self.rect_normal
        
    def draw(self, surface):
        action = None
        pos = pygame.mouse.get_pos()
        
        is_hovering = self.rect_normal.collidepoint(pos)

        if is_hovering:
            current_image = self.img_hover
            self.rect = current_image.get_rect(center=self.rect_normal.center)
        else:
            current_image = self.img_normal
            self.rect = self.rect_normal
            
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            action = self.accion

        surface.blit(current_image, self.rect) 
        
        return action

# CLASE IMAGEN DECORATIVA (Actualizada para usar traducción condicional)
class ImagenDecorativa:
    def __init__(self, x, y, ancho, alto, path_imagen_base, traducir=True): 
        try:
            # LÓGICA DE CARGA: Si traducir es True, usa la función de traducción
            if traducir:
                path_a_cargar = obtener_ruta_imagen_traducida(path_imagen_base)
            else:
                # Si traducir es False, carga la ruta completa directamente
                path_a_cargar = path_imagen_base
                
            img_base = pygame.image.load(path_a_cargar).convert_alpha()
            self.imagen = pygame.transform.scale(img_base, (ancho, alto))
        except pygame.error as e:
            print(f"Error cargando imagen decorativa {path_imagen_base}: {e}. Usando fallback.")
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
        print(f"Error cargando fondo: {PATH_FONDO_TUTORIAL_WIN}. Usando color sólido.")
        fondo_victoria = pygame.Surface((ANCHO, ALTO)); fondo_victoria.fill((0, 80, 0)) 

    # 2. Creación Individual de Elementos

    # 2.1 Botón 1: Menú Principal (NO TRADUCIR, usa ruta completa)
    BTN_MENU_W, BTN_MENU_H = 90, 90 
    BTN_MENU_X = 350 
    BTN_MENU_Y = 531 
    
    btn_menu = Boton(
        BTN_MENU_X, 
        BTN_MENU_Y, 
        BTN_MENU_W, 
        BTN_MENU_H, 
        RETURN_MENU,
        PATH_BTN_MENU,
        traducir=False # <--- CLAVE: Carga la ruta directa para evitar el error
    )
    
    # 2.2 Botón 2: Nivel 1 (SÍ TRADUCIR, usa ruta base)
    BTN_NIVEL_1_W, BTN_NIVEL_1_H = 452, 90 
    BTN_NIVEL_1_X = 520 
    BTN_NIVEL_1_Y = 531 
    
    btn_nivel_1 = Boton(
        BTN_NIVEL_1_X, 
        BTN_NIVEL_1_Y, 
        BTN_NIVEL_1_W, 
        BTN_NIVEL_1_H, 
        RETURN_LEVEL_1,
        PATH_BTN_LEVEL_1_BASE # Se traduce por defecto
    )
    
    # Imagen decorativa (SÍ TRADUCIR, usa ruta base)
    IMG_DECO_W, IMG_DECO_H = 696, 394 
    IMG_DECO_X = 300 
    IMG_DECO_Y = 100 
    
    imagen_decorativa = ImagenDecorativa(
        IMG_DECO_X,
        IMG_DECO_Y,
        IMG_DECO_W,
        IMG_DECO_H,
        PATH_IMAGEN_DECORATIVA_BASE # Se traduce por defecto
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
        ventana.blit(fondo_victoria, (0, 0))

        # 3. Dibujar Elementos
        imagen_decorativa.draw(ventana) 
        
        # Dibujo y Lógica con la clase Boton animada
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