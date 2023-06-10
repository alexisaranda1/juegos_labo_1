import pygame

ANCHO = 800
ALTO = 500
CIR_POSICION_X = ANCHO // 2
CIR_POSICION_Y = ALTO // 2
POSICION_X = 2
POSICION_Y = 450
VELOCIDAD_MOVIMIENTO = 10



BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 244, 0)
AMARILLO = (255, 255, 0)
CELESTE = (132, 185, 254)
VERDE_CLARO = (97, 205, 53)

pygame.init()

PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("programa")



def mover_cuadrado(keys):
    global POSICION_X, POSICION_Y
    if keys[pygame.K_w]:
        POSICION_Y -= VELOCIDAD_MOVIMIENTO
    if keys[pygame.K_s]:
        POSICION_Y += VELOCIDAD_MOVIMIENTO
    if keys[pygame.K_a]:
        POSICION_X -= VELOCIDAD_MOVIMIENTO
    if keys[pygame.K_d]:
        POSICION_X += VELOCIDAD_MOVIMIENTO


reloj = pygame.time.Clock()
FPS = 60

TICK_1S = pygame.USEREVENT + 0
pygame.time.set_timer(TICK_1S, 1000)

contador = 0
running = True

SONIC = pygame.image.load("imagenes\sonic.png")
FONDO = pygame.image.load("imagenes/sfondo.jpg")
fondo_rect = FONDO.get_rect(center=(ANCHO // 2, ALTO // 2))


while running:
    PANTALLA.fill(CELESTE)
    PANTALLA.blit(FONDO,fondo_rect)
    PANTALLA.blit(SONIC, (POSICION_X, POSICION_Y))

    teclas = pygame.key.get_pressed()
    mover_cuadrado(teclas)

    pygame.display.set_caption("Programa")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == TICK_1S:
            contador += 1

    font = pygame.font.SysFont("Arial", 15)
    contador_texto = font.render("Tiempo: {0}".format(str(contador)), True, NEGRO)
    PANTALLA.blit(contador_texto, (10, 10))

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
