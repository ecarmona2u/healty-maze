import pygame
import sys
import time

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego con tiempo y meta")

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (200, 50, 50)
VERDE = (50, 200, 50)
GRIS = (100, 100, 100)

try:
    background_image = pygame.image.load('assets/FondoFinal.jpg').convert()
    ball_image = pygame.image.load('assets/Redimensionado.png').convert_alpha()
    ball_image = pygame.transform.scale(ball_image, (50, 50)) #TAMAÑO DE LA BOLA
except pygame.error as message:
    print('No se pudieron cargar las imágenes:', message)
    pygame.quit()
    exit()

background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

ball_rect = ball_image.get_rect()
ball_rect.center = (56, 330)
ball_speed = 5

goal_rect = pygame.Rect(956, 78, 160, 50)

TIEMPO_MAX = 30
BARRA_ANCHO_MAX = 400

inicio = time.time()
tiempo_pausado_total = 0
pausa_inicio = None
tiempo_restante_final = TIEMPO_MAX
tiempo_restante = TIEMPO_MAX  # <<<< valor congelable

font = pygame.font.SysFont(None, 48)

running = True
game_over = False
ganaste = False
pausado = False
clock = pygame.time.Clock()

boton_pausa = pygame.Rect(screen_width - 60, 10, 50, 30)
boton_play = pygame.Rect(screen_width//2 - 50, screen_height//2 + 40, 100, 40)

walls = [
    pygame.Rect(14, 100, 946, 65),
    pygame.Rect(255, 215, 65, 180),
    pygame.Rect(492, 150, 65, 310),
    pygame.Rect(98, 215, 65, 100),
    pygame.Rect(98, 215, 222, 40),
    pygame.Rect(18, 374, 300, 40),
    pygame.Rect(96, 570, 306, 60),
    pygame.Rect(98, 470, 65, 100),
    pygame.Rect(492, 420, 302, 40),
]

def mover_bola(rect, dx, dy):
    rect.x += dx
    for wall in walls:
        if rect.colliderect(wall):
            if dx > 0: rect.right = wall.left
            if dx < 0: rect.left = wall.right

    rect.y += dy
    for wall in walls:
        if rect.colliderect(wall):
            if dy > 0: rect.bottom = wall.top
            if dy < 0: rect.top = wall.bottom
    return rect

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if boton_pausa.collidepoint(event.pos) and not pausado:
                pausado = True
                pausa_inicio = time.time()
            elif pausado and boton_play.collidepoint(event.pos):
                pausado = False
                tiempo_pausado_total += time.time() - pausa_inicio
                pausa_inicio = None

    if not game_over and not ganaste and not pausado:
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -ball_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = ball_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -ball_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = ball_speed

        ball_rect = mover_bola(ball_rect, dx, dy)

        if ball_rect.left < 0: ball_rect.left = 0
        if ball_rect.right > screen_width: ball_rect.right = screen_width
        if ball_rect.top < 0: ball_rect.top = 0
        if ball_rect.bottom > screen_height: ball_rect.bottom = screen_height

        if ball_rect.colliderect(goal_rect):
            ganaste = True
            tiempo_restante_final = max(0, TIEMPO_MAX - ((time.time() - inicio) - tiempo_pausado_total))

        if (time.time() - inicio) - tiempo_pausado_total >= TIEMPO_MAX:
            game_over = True

        tiempo_restante = max(0, TIEMPO_MAX - ((time.time() - inicio) - tiempo_pausado_total))

    screen.blit(background_image, (0, 0))
    screen.blit(ball_image, ball_rect)

    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 255), wall, 2)

    ancho_barra = int((tiempo_restante / TIEMPO_MAX) * BARRA_ANCHO_MAX)
    pygame.draw.rect(screen, ROJO, (10, 10, ancho_barra, 20))

    texto_tiempo = font.render(f"Tiempo: {int(tiempo_restante)}s", True, BLANCO)
    screen.blit(texto_tiempo, (10, 40))

    pygame.draw.rect(screen, GRIS, boton_pausa)
    texto_pausa = font.render("II", True, BLANCO)
    screen.blit(texto_pausa, (screen_width - 50, 10))

    if pausado:
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill(GRIS)
        screen.blit(overlay, (0, 0))

        texto = font.render("Juego Pausado", True, BLANCO)
        screen.blit(texto, (screen_width//2 - 150, screen_height//2 - 40))

        pygame.draw.rect(screen, VERDE, boton_play)
        texto_play = font.render("Play", True, BLANCO)
        screen.blit(texto_play, (screen_width//2 - 35, screen_height//2 + 40))

    if game_over:
        texto = font.render("¡Tiempo agotado! Fallaste", True, ROJO)
        screen.blit(texto, (screen_width // 2 - 200, screen_height // 2))
    elif ganaste:
        texto = font.render("¡Ganaste el laberinto!", True, VERDE)
        screen.blit(texto, (screen_width // 2 - 200, screen_height // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
