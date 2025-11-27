import pygame
import sys
from pathlib import Path 
# 🚨 Importar la lógica de traducción
from traduccion import obtener_ruta_imagen_traducida 

# --- CONSTANTES DE RECURSOS (Rutas Base) ---
# Ahora definimos las rutas BASE que serán traducidas.
# La función obtener_ruta_imagen_traducida se encargará de añadir 'recursos/<idioma>/' al inicio.
PATH_FONDO_BASE = "fondo_derrota.png" # <<< RUTA BASE para el fondo (SÍ se traduce, ej: recursos/es/fondo_derrota.png)
# El botón de reintentar está en la misma carpeta que el fondo.
PATH_BTN_REINTENTAR_BASE = "btn_reintentar.png" # <<< RUTA BASE para el botón de reintentar (SÍ se traduce)

# 🚨 CAMBIO APLICADO: Ruta FIJA (no traducida) para el botón de menú
# Este path debe ser la ruta completa, independientemente del idioma.
PATH_BTN_MENU_FIJO = "recursos/botones/btn_menu.png" 

# 🎧 RUTA DEL SONIDO AGREGADO
PATH_SONIDO_NO_WIN = str(Path("recursos") / "audio" / "no_win.mp3") 

# --- VALORES DE RETORNO ---
RETURN_REINTENTAR = "REINTENTAR"
RETURN_MENU_PRINCIPAL = "MENU" 


# CLASE BOTON (Animada con escalado en hover)
class Boton:
    """
    Clase para crear botones con imagen y acción. 
    Acepta una ruta de imagen completa.
    """
    # Recibe path_imagen_completa (la ruta ya traducida o la ruta fija)
    def __init__(self, x, y, ancho, alto, accion, path_imagen_completa): 
        
        self.accion = accion
        self.original_size = (ancho, alto)
        self.hover_size = (ancho + 10, alto + 10) # 10 píxeles más grande
        
        # Carga y escalado de la imagen base (usa la ruta COMPLETA)
        try:
            # Intentamos cargar la imagen
            img_original = pygame.image.load(path_imagen_completa).convert_alpha()
            # Almacenamos las dos versiones de la imagen para el hover
            self.img_normal = pygame.transform.scale(img_original, self.original_size)
            self.img_hover = pygame.transform.scale(img_original, self.hover_size)
        except pygame.error as e:
            # Fallback si el asset no se encuentra (FileNotFoundError o PygameError)
            
            # Adaptar mensaje de error para dar la pista correcta al usuario
            error_msg = f"Error CRÍTICO al cargar el botón {path_imagen_completa}: {e}. Asegúrate de que el archivo existe en la ruta especificada."
            if "btn_reintentar" in path_imagen_completa:
                error_msg += " (Para el botón Reintentar, revisa recursos/<idioma>/)."
            elif "btn_menu" in path_imagen_completa:
                error_msg += " (Para el botón Menú, revisa la ruta fija: recursos/botones/btn_menu.png)."
            print(error_msg + " Usando fallback de color sólido.")
            
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
    
    # 1. VERIFICAR E INICIALIZAR EL MIXER (AUDIO)
    if not pygame.mixer.get_init():
        pygame.mixer.init()
        
    # 2. CARGA DEL SONIDO
    sonido_no_win = None
    try:
        sonido_no_win = pygame.mixer.Sound(PATH_SONIDO_NO_WIN)
    except pygame.error as e:
        print(f"Error cargando el sonido: {e}. Asegúrate de que '{PATH_SONIDO_NO_WIN}' exista.")
        
    # 3. REPRODUCCIÓN DEL SONIDO
    if sonido_no_win:
        sonido_no_win.play()
        
    ANCHO, ALTO = ventana.get_size()
    clock = pygame.time.Clock()
    
    # 4. TRADUCCIÓN y Carga de Fondo (SÍ se traduce)
    # Obtiene la ruta correcta (ej: recursos/es/fondo_derrota.png)
    path_fondo_traducido = obtener_ruta_imagen_traducida(PATH_FONDO_BASE)
    try:
        fondo = pygame.image.load(path_fondo_traducido).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error:
        print(f"Error cargando fondo traducido: {path_fondo_traducido}. Usando color sólido.")
        fondo = pygame.Surface((ANCHO, ALTO)); fondo.fill((150, 0, 0)) # Fallback a color oscuro
        
    # 5. Configuración Común de Botones
    BTN_W_GRANDE, BTN_H_GRANDE = 300, 90 
    BTN_W_PEQUENO, BTN_H_PEQUENO = 90, 90 
    BTN_Y = 500
    
    # 6. Creación de Botones
    
    # TRADUCCIÓN del botón REINTENTAR (SÍ se traduce)
    path_btn_reintentar_traducido = obtener_ruta_imagen_traducida(PATH_BTN_REINTENTAR_BASE)
    
    # Botón 1: REINTENTAR (Grande, Derecha)
    btn_reintentar = Boton(
        # Posición: 150px a la derecha del centro, ajustada por el ancho del botón
        ANCHO // 2 + 300 - (BTN_W_GRANDE // 2), BTN_Y, 
        BTN_W_GRANDE, BTN_H_GRANDE, 
        RETURN_REINTENTAR,
        path_btn_reintentar_traducido # <<< Usa la ruta traducida (Correcto)
    )
    
    # Botón 2: MENÚ (Pequeño, Izquierda)
    btn_menu = Boton(
        # Posición: 150px a la izquierda del centro, ajustada por el ancho del botón
        ANCHO // 2 - 200 - (BTN_W_PEQUENO // 2), BTN_Y, 
        BTN_W_PEQUENO, BTN_H_PEQUENO, 
        RETURN_MENU_PRINCIPAL, 
        PATH_BTN_MENU_FIJO # <<< Usa la ruta fija (Correcto)
    )

    # 7. Bucle principal
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