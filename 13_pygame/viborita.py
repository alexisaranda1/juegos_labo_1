import pygame
import random
import time

# Dimensiones de la ventana del juego
ANCHO = 800
ALTO = 500

# Colores
TURQUESA = (64, 224, 208)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Tamaño del cuerpo de la serpiente y velocidad
TAM_SEGMENTO = 20
VELOCIDAD = 5
VELOCIDAD_DECREMENTO = 1  # Valor para reducir la velocidad de decremento de las vidas

# Inicializar Pygame
pygame.init()
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("La Viborita")  # Nombre de la ventana

reloj = pygame.time.Clock()


def fin_juego(tiempo, comida_consumida):
    """
    Esta función muestra un mensaje en pantalla indicando que el juego ha terminado, junto con el tiempo
    transcurrido y la cantidad de comida consumida.
    
    :param tiempo: La cantidad de tiempo que el jugador duró en el juego antes de perder. Es un valor
    entero que representa el número de segundos
    :param comida_consumida: Es una variable que representa la cantidad de comida consumida por el
    jugador en el juego. Se utiliza para mostrar la cantidad total de alimentos consumidos en la
    pantalla Game Over
    """
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render("Perdiste. Tiempo: {}s".format(int(tiempo)), True, ROJO)
    rect_texto = texto.get_rect(center=(ANCHO/2, ALTO/2))
    PANTALLA.blit(texto, rect_texto)

    mostrar_comida_consumida(comida_consumida, 10, 60)

    pygame.display.flip()
    pygame.time.wait(2000)


def mostrar_vidas(vidas):
    """
    La función muestra el número de vidas en la pantalla usando Pygame.
    
    :param vidas: El número de vidas que le quedan al jugador en el juego. Esta función se utiliza para
    mostrar el número de vidas en la pantalla durante el juego
    """
    fuente = pygame.font.Font(None, 24)
    texto = fuente.render("Vidas: " + str(vidas), True, NEGRO)
    rect_texto = texto.get_rect(center=(ANCHO/2, 20))
    PANTALLA.blit(texto, rect_texto)


def mostrar_comida_consumida(comida_consumida, x, y):
    """
    Esta función muestra la cantidad de alimentos consumidos en la pantalla usando Pygame.
    
    :param comida_consumida: Este parámetro es una variable que contiene la cantidad de alimentos
    consumidos. Se utiliza para mostrar la cantidad de alimentos consumidos en la pantalla
    :param x: La coordenada x de la esquina superior derecha de la superficie de texto
    :param y: El parámetro y es la posición vertical donde se mostrará el texto en la pantalla
    """
    fuente = pygame.font.Font(None, 24)
    texto = fuente.render("Comida: " + str(comida_consumida), True, NEGRO)
    rect_texto = texto.get_rect(topright=(x, y))
    PANTALLA.blit(texto, rect_texto)


def dibujar_serpiente(segmentos):
    """
    Esta función dibuja una serpiente en una pantalla Pygame usando una lista de segmentos
    rectangulares.
    
    :param segmentos: una lista de rectángulos que representan los segmentos de una serpiente. Cada
    rectángulo tiene una posición (x, y) y un tamaño (ancho, alto). La función itera sobre la lista y
    dibuja cada rectángulo en la pantalla utilizando la biblioteca Pygame. El color de los rectángulos
    es negro (valor RGB
    """
    for segmento in segmentos:
        pygame.draw.rect(PANTALLA, NEGRO, segmento)


def mover_serpiente(segmentos, direccion):
    """
    Esta función mueve los segmentos de una serpiente en una dirección determinada.
    
    :param segmentos: Una lista de objetos pygame Rect que representan los segmentos del cuerpo de la
    serpiente
    :param direccion: La dirección en la que debe moverse la serpiente. Puede ser "derecha" (derecha),
    "izquierda" (izquierda), "arriba" (arriba) o "abajo" (abajo)
    """
    cabeza = segmentos[0].copy()
    if direccion == "derecha":
        cabeza.move_ip(TAM_SEGMENTO, 0)
    elif direccion == "izquierda":
        cabeza.move_ip(-TAM_SEGMENTO, 0)
    elif direccion == "arriba":
        cabeza.move_ip(0, -TAM_SEGMENTO)
    elif direccion == "abajo":
        cabeza.move_ip(0, TAM_SEGMENTO)
    segmentos.insert(0, cabeza)
    if len(segmentos) > 1:
        segmentos.pop()

def generar_comida():
    """
    Esta función genera un objeto rectangular que representa comida en un lugar aleatorio dentro de la
    pantalla del juego.
    :return: La función `generar_comida()` devuelve un objeto `pygame.Rect` que representa la posición y
    el tamaño de un alimento generado aleatoriamente en la pantalla del juego.
    """
    x = random.randint(1, (ANCHO-TAM_SEGMENTO)//TAM_SEGMENTO) * TAM_SEGMENTO
    y = random.randint(1, (ALTO-TAM_SEGMENTO)//TAM_SEGMENTO) * TAM_SEGMENTO
    return pygame.Rect(x, y, TAM_SEGMENTO, TAM_SEGMENTO)

# Crear la serpiente
segmentos_serpiente = [pygame.Rect(100, 100, TAM_SEGMENTO, TAM_SEGMENTO)]
direccion_serpiente = "derecha"

# Generar primera pieza de comida
comida = generar_comida()

# Vidas
vidas = 3

# Contador de comida consumida
comida_consumida = 0

# Bandera para indicar si la serpiente colisionó
colision = False

# Contador de frames para reducir la velocidad de decremento de las vidas
contador_frames = 0

# Variables para almacenar la posición y dirección inicial de la serpiente
posicion_inicial = segmentos_serpiente[0].copy()
direccion_inicial = direccion_serpiente

# Variable para almacenar el tiempo de inicio del juego
tiempo_inicio = time.time()

# Bucle principal del juego
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT and direccion_serpiente != "izquierda":
                direccion_serpiente = "derecha"
            elif evento.key == pygame.K_LEFT and direccion_serpiente != "derecha":
                direccion_serpiente = "izquierda"
            elif evento.key == pygame.K_UP and direccion_serpiente != "abajo":
                direccion_serpiente = "arriba"
            elif evento.key == pygame.K_DOWN and direccion_serpiente != "arriba":
                direccion_serpiente = "abajo"

    PANTALLA.fill(TURQUESA)

    mover_serpiente(segmentos_serpiente, direccion_serpiente)
    dibujar_serpiente(segmentos_serpiente)

    if segmentos_serpiente[0].colliderect(comida):
        segmentos_serpiente.append(pygame.Rect(0, 0, TAM_SEGMENTO, TAM_SEGMENTO))
        comida = generar_comida()
        comida_consumida += 1

    for segmento in segmentos_serpiente[1:]:
        if segmentos_serpiente[0].colliderect(segmento):
            colision = True

    if segmentos_serpiente[0].left < 0 or segmentos_serpiente[0].right > ANCHO or segmentos_serpiente[0].top < 0 or segmentos_serpiente[0].bottom > ALTO:
        colision = True

    if colision:
        colision = False
        if contador_frames % VELOCIDAD_DECREMENTO == 0:
            vidas -= 1
            if vidas == 0:
                tiempo_transcurrido = time.time() - tiempo_inicio
                fin_juego(tiempo_transcurrido, comida_consumida)
                segmentos_serpiente = [posicion_inicial]
                direccion_serpiente = direccion_inicial
                vidas = 3
                comida_consumida = 0
            else:
                if len(segmentos_serpiente) > 1:
                    segmentos_serpiente.pop()  # Remover el último segmento
                segmentos_serpiente[0] = posicion_inicial  # Restaurar la posición inicial
                direccion_serpiente = direccion_inicial

    mostrar_vidas(vidas)
    mostrar_comida_consumida(comida_consumida, ANCHO - 10, 20)

    pygame.draw.circle(PANTALLA, ROJO, (comida.x + TAM_SEGMENTO//2, comida.y + TAM_SEGMENTO//2), TAM_SEGMENTO//2)

    # Mostrar tiempo transcurrido
    tiempo_transcurrido = int(time.time() - tiempo_inicio)
    fuente_tiempo = pygame.font.Font(None, 24)
    texto_tiempo = fuente_tiempo.render("Tiempo: {}s".format(tiempo_transcurrido), True, NEGRO)
    rect_tiempo = texto_tiempo.get_rect(topleft=(10, 20))
    PANTALLA.blit(texto_tiempo, rect_tiempo)

    pygame.display.flip()
    reloj.tick(VELOCIDAD)
    contador_frames += 1

pygame.quit()
