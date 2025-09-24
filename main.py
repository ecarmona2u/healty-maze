import pygame
import sys
import time

# Inicializa Pygame
pygame.init()

# --- Configuración de la pantalla ---
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego con tiempo y meta")

# --- Colores ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (200, 50, 50)
VERDE = (50, 200, 50)

# --- Carga de imágenes ---
try:
    background_image = pygame.image.load('assets/nivel1.jpg').convert()
    ball_image = pygame.image.load('assets/bola_temp.png').convert_alpha()
except pygame.error as message:
    print('No se pudieron cargar las imágenes:', message)
    pygame.quit()
    exit()

# Redimensiona la imagen de fondo
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# --- Variables del personaje (la bolita) ---
ball_rect = ball_image.get_rect()
ball_rect.center = (56, 330)  # Posición inicial
ball_speed = 5

# --- Meta ---
goal_rect = pygame.Rect(956, 78, 160, 50)  # Rectángulo como meta

# --- Tiempo configurable ---
TIEMPO_MAX = 15  # en segundos
inicio = time.time()
tiempo_restante_final = TIEMPO_MAX  # Para guardar el tiempo al ganar

# --- Fuente ---
font = pygame.font.SysFont(None, 48)

# --- Control de estado ---
running = True
game_over = False
ganaste = False
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over and not ganaste:
        # --- Movimiento del personaje ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ball_rect.x -= ball_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ball_rect.x += ball_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            ball_rect.y -= ball_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            ball_rect.y += ball_speed

        # Limita el movimiento a la pantalla
        if ball_rect.left < 0:
            ball_rect.left = 0
        if ball_rect.right > screen_width:
            ball_rect.right = screen_width
        if ball_rect.top < 0:
            ball_rect.top = 0
        if ball_rect.bottom > screen_height:
            ball_rect.bottom = screen_height

        # --- Verificar meta ---
        if ball_rect.colliderect(goal_rect):
            ganaste = True
            # Guardar el tiempo restante al momento de ganar
            tiempo_restante_final = max(0, TIEMPO_MAX - (time.time() - inicio))

        # --- Verificar tiempo ---
        if time.time() - inicio >= TIEMPO_MAX:
            game_over = True

    # --- Dibujar en pantalla ---
    screen.blit(background_image, (0, 0))  # Fondo
    screen.blit(ball_image, ball_rect)     # Personaje

    # para mostrar la meta, quitar el "# de la lina de abajo"
    # pygame.draw.rect(screen, VERDE, goal_rect)

    # --- Barra y tiempo ---
    if ganaste:
        tiempo_restante = tiempo_restante_final  # Se congela al ganar
    else:
        tiempo_restante = max(0, TIEMPO_MAX - (time.time() - inicio))

    ancho_barra = int((tiempo_restante / TIEMPO_MAX) * screen_width)
    pygame.draw.rect(screen, ROJO, (0, 0, ancho_barra, 20))

    # Texto tiempo
    texto_tiempo = font.render(f"Tiempo: {int(tiempo_restante)}s", True, BLANCO)
    screen.blit(texto_tiempo, (10, 25))

    # Mensajes de ganar/perder
    if game_over:
        texto = font.render("¡Tiempo agotado! Fallaste", True, ROJO)
        screen.blit(texto, (screen_width // 2 - 200, screen_height // 2))
    elif ganaste:
        texto = font.render("¡Ganaste el laberinto!", True, VERDE)
        screen.blit(texto, (screen_width // 2 - 200, screen_height // 2))

    pygame.display.flip()

# Cierra Pygame
pygame.quit()
sys.exit()
