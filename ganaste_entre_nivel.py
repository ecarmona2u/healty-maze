import pygame
import sys
from pathlib import Path 

# 📢 IMPORTAR LÓGICA DE TRADUCCIÓN
# Necesitas una implementación de este archivo en tu proyecto:
from traduccion import obtener_ruta_imagen_traducida 

# --- CONSTANTES DE RECURSOS (Rutas Base) ---
# Ahora definimos las rutas BASE y la función de traducción añadirá el idioma
PATH_FONDO_BASE = "fondo_victoria1.png" # <<< RUTA BASE
PATH_BTN_NEXT_BASE = "btn_siguiente.png" # <<< RUTA BASE
PATH_BTN_MENU = str(Path("recursos") / "botones" / "btn_menu.png") # RUTA FIJA
# 🎧 RUTA DEL SONIDO AGREGADO
PATH_SONIDO_NO_WIN = str(Path("recursos") / "audio" / "win.mp3") 

BLANCO = (255, 255, 255)

# --- VALORES DE RETORNO ---
RETURN_NEXT_LEVEL = "NEXT_LEVEL"
RETURN_SELECTOR_NIVEL = "SELECTOR_NIVEL" 
RETURN_REINTENTAR = "REINTENTAR" 


# CLASE BOTON (Animada con escalado en hover)
class Boton:
    """
    Clase para crear botones con imagen y acción. 
    Se modificó para aceptar una ruta de imagen ya traducida.
    """
    def __init__(self, x, y, ancho, alto, accion, path_imagen_completa): # Eliminé 'texto'
        
        self.accion = accion
        self.original_size = (ancho, alto)
        self.hover_size = (ancho + 10, alto + 10) # 10 píxeles más grande
        
        # Carga y escalado de la imagen base (usa la ruta COMPLETA y traducida)
        try:
            img_original = pygame.image.load(path_imagen_completa).convert_alpha()
            # Almacenamos las dos versiones de la imagen para el hover
            self.img_normal = pygame.transform.scale(img_original, self.original_size)
            self.img_hover = pygame.transform.scale(img_original, self.hover_size)
        except pygame.error as e:
            print(f"Error cargando imagen de botón {path_imagen_completa}: {e}. Usando fallback.")
            # Fallback a un color sólido si la imagen no se carga
            self.img_normal = pygame.Surface(self.original_size, pygame.SRCALPHA)
            self.img_normal.fill((0, 150, 0, 180)) 
            self.img_hover = pygame.Surface(self.hover_size, pygame.SRCALPHA)
            self.img_hover.fill((0, 200, 0, 255)) 
        
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


# FUNCIÓN PRINCIPAL DE LA PANTALLA
def run_pantalla_ganaste(ventana, img_btn_regresar=None, REGRESAR_RECT=None): 
    
    # ⚠️ ASEGÚRATE DE QUE EL MÓDULO MIXER ESTÉ INICIALIZADO AL PRINCIPIO DE TU JUEGO 
    # (ej. después de pygame.init()). 
    # Lo inicializamos aquí por si acaso, pero es mejor hacerlo una vez al inicio del juego.
    if not pygame.mixer.get_init():
        pygame.mixer.init()
        
    # --- CARGA DEL SONIDO ---
    sonido_no_win = None
    try:
        sonido_no_win = pygame.mixer.Sound(PATH_SONIDO_NO_WIN)
    except pygame.error as e:
        print(f"Error cargando el sonido: {e}. Asegúrate de que '{PATH_SONIDO_NO_WIN}' exista y sea un archivo de sonido válido.")


    ANCHO, ALTO = ventana.get_size()
    clock = pygame.time.Clock()
    
    # 1. TRADUCCIÓN Y CARGA DE FONDO
    # Obtiene la ruta correcta (ej: recursos/es/fondo_victoria1.png)
    path_fondo_traducido = obtener_ruta_imagen_traducida(PATH_FONDO_BASE)
    try:
        fondo = pygame.image.load(path_fondo_traducido).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error:
        print(f"Error cargando fondo traducido: {path_fondo_traducido}. Usando color sólido.")
        fondo = pygame.Surface((ANCHO, ALTO)); fondo.fill((50, 50, 50))
        
    # 🚀 REPRODUCCIÓN DEL SONIDO AL INICIO DE LA PANTALLA
    if sonido_no_win:
        sonido_no_win.play()

    # 2. Configuración Común de Botones
    BTN_W_GRANDE, BTN_H_GRANDE = 300, 90 
    BTN_W_PEQUENO, BTN_H_PEQUENO = 90, 90 
    BTN_Y = 550
    
    # 3. Creación de Botones

    # Botón 1: SIGUIENTE NIVEL (Grande, Derecha)
    # TRADUCCIÓN del botón Siguiente
    path_btn_siguiente_traducido = obtener_ruta_imagen_traducida(PATH_BTN_NEXT_BASE)

    btn_siguiente = Boton(
        830, BTN_Y, BTN_W_GRANDE, BTN_H_GRANDE, 
        RETURN_NEXT_LEVEL, 
        path_btn_siguiente_traducido # <<< Usa la ruta traducida
    )
    
    # Botón 2: SELECTOR DE NIVEL (Pequeño, Izquierda) - Imagen FIJA, no traducida.
    btn_menu = Boton(
        350, BTN_Y, BTN_W_PEQUENO, BTN_H_PEQUENO, 
        RETURN_SELECTOR_NIVEL, 
        PATH_BTN_MENU # <<< Usa la ruta fija
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