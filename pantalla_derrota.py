import pygame
import sys

# --- CONSTANTES DE RECURSOS ---
PATH_FONDO = "recursos/fondo_derrota.png" 
PATH_BTN_MENU = "recursos/btn_menu.png"
PATH_BTN_REINTENTAR = "recursos/btn_reintentar.png" 

# --- VALORES DE RETORNO ---
RETURN_REINTENTAR = "REINTENTAR"
# Acción estándar para salir al menú/selector de personaje
RETURN_MENU_PRINCIPAL = "MENU" 


# CLASE BOTON (Animada con escalado en hover, copiada de ganaste_entre_nivel_2.py)
class Boton:
    """
    Clase para crear botones con imagen y acción. Incluye efecto hover
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
            # Fallback a un color sólido si la imagen no se carga (Rojo para Derrota)
            self.img_normal = pygame.Surface(self.original_size, pygame.SRCALPHA)
            self.img_normal.fill((150, 0, 0, 180)) 
            self.img_hover = pygame.Surface(self.hover_size, pygame.SRCALPHA)
            self.img_hover.fill((200, 0, 0, 255)) 
        
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
        # Solo detectamos el clic si el ratón está sobre el rectángulo actual (escalado o normal)
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            action = self.accion

        # 4. Dibujar la imagen (grande o normal, centrada)
        surface.blit(current_image, self.rect) 
        
        return action


def run_pantalla_derrota(ventana):
    ANCHO, ALTO = ventana.get_size()
    clock = pygame.time.Clock()
    
    # 1. Cargar Fondo
    try:
        fondo = pygame.image.load(PATH_FONDO).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error:
        print(f"Error cargando fondo: {PATH_FONDO}. Usando color sólido.")
        fondo = pygame.Surface((ANCHO, ALTO)); fondo.fill((150, 0, 0))
        
    # 2. Configuración Común de Botones
    BTN_W_GRANDE, BTN_H_GRANDE = 300, 90 
    BTN_W_PEQUENO, BTN_H_PEQUENO = 90, 90 
    BTN_Y = 500
    
    # 3. Creación de Botones
    # Botón 1: REINTENTAR (Grande, Derecha)
    btn_reintentar = Boton(
        800, BTN_Y, BTN_W_GRANDE, BTN_H_GRANDE, 
        "REINTENTAR", 
        RETURN_REINTENTAR,
        PATH_BTN_REINTENTAR
    )
    # Botón 2: MENÚ (Pequeño, Izquierda)
    btn_menu = Boton(
        400, BTN_Y, BTN_W_PEQUENO, BTN_H_PEQUENO, 
        "PERSONAJE", 
        RETURN_MENU_PRINCIPAL, # <-- Usa "MENU"
        PATH_BTN_MENU
    )

    # 4. Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
        ventana.blit(fondo, (0, 0))
        
        # Dibujo y Lógica con la clase Boton animada
        accion_reintentar = btn_reintentar.draw(ventana)
        accion_menu = btn_menu.draw(ventana)
        
        if accion_reintentar:
            # Devuelve 3 valores (la acción, y dos None para consistencia)
            return RETURN_REINTENTAR, None, None 
        
        if accion_menu:
            # Devuelve 3 valores (la acción, y dos None para consistencia)
            return RETURN_MENU_PRINCIPAL, None, None 

        pygame.display.flip()
        clock.tick(30)
        
    # Fallback
    return RETURN_MENU_PRINCIPAL, None, None