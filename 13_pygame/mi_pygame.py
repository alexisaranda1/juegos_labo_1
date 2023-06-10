import pygame
import random

ancho_ventana = 800
alto_ventana = 500

def mover_circulo(keys, velocidad_movimiento):
    global posicion_x, posicion_y

    if keys[pygame.K_UP]:
        posicion_y -= velocidad_movimiento
    if keys[pygame.K_DOWN]:
        posicion_y += velocidad_movimiento
    if keys[pygame.K_LEFT]:
        posicion_x -= velocidad_movimiento
    if keys[pygame.K_RIGHT]:
        posicion_x += velocidad_movimiento

pygame.init()
# Ventana
PANTALLA = pygame.display.set_mode(size=(ancho_ventana, alto_ventana))
pygame.display.set_caption("Juego")

clock = pygame.time.Clock()
posicion_x = 250
posicion_y = 250
radio = 10
color_circulo = (189, 255, 1)
velocidad_movimiento = 5

obstáculos = []
radio_obstáculo = 5
color_obstáculo = (1, 12, 122)

def generar_obstaculo():
    obstáculo_x = random.randint(radio_obstáculo, 800 - radio_obstáculo)
    obstáculo_y = random.randint(radio_obstáculo, 500 - radio_obstáculo)
    return (obstáculo_x, obstáculo_y)

obstáculo_actual = generar_obstaculo()

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mover_circulo(keys, velocidad_movimiento)
    
    circle_rect = pygame.Rect(posicion_x - radio, posicion_y - radio,
                               radio * 2, radio * 2)

    PANTALLA.fill((122, 61, 176))

    # Dibujar obstáculos (manzanas)
    for obstacle in obstáculos:
        obstacle_x, obstacle_y = obstacle
        obstacle_rect = pygame.Rect(obstacle_x - radio_obstáculo,
                                    obstacle_y - radio_obstáculo, radio_obstáculo * 2, radio_obstáculo * 2)
        pygame.draw.circle(PANTALLA, color_obstáculo, (obstacle_x, obstacle_y),
                            radio_obstáculo)

        # Verificar colisión con el círculo
        if obstacle_rect.colliderect(circle_rect):
            obstáculos.remove(obstacle)
    
    # Dibujar obstáculo actual
    obstacle_x, obstacle_y = obstáculo_actual
    pygame.draw.circle(PANTALLA, color_obstáculo, (obstacle_x, obstacle_y),
                        radio_obstáculo)

    # Verificar colisión con el círculo
    obstacle_rect = pygame.Rect(obstacle_x - radio_obstáculo,
                                obstacle_y - radio_obstáculo, radio_obstáculo * 2, radio_obstáculo * 2)
    if obstacle_rect.colliderect(circle_rect):
        obstáculos.append(obstáculo_actual)
        obstáculo_actual = generar_obstaculo()
    
    pygame.draw.circle(PANTALLA, color_circulo, (posicion_x, posicion_y), radio)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
