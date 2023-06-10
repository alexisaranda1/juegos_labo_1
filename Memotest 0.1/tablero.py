import pygame
import time
import random
import tarjeta
from tarjeta import *
from constantes import *

def crear_tablero():
    '''
    Crea una lista de tarjetas
    Retorna un diccionario tablero
    '''
    tablero = {}
    tablero['tarjetas'] = generar_lista_tarjetas()
    tablero['tiempo_ultimo_destape'] = 0
    tablero['primer_tarjeta_seleccionada'] = None
    tablero['segunda_tarjeta_seleccionada'] = None

    return tablero


def generar_lista_tarjetas()->list:
    '''
    Función que se encarga de generar una lista de tarjetas ordenada aleatoriamente
    El for x me recorre todas las posiciones de x usando de step el ancho de la tarjeta
    El for y me recorre todas las posiciones de x usando de step el alto de la tarjeta
    Por ende me va a generar la cantidad de tarjetas que le especifique anteriormente 
    ajustandose a la resolución de mi pantalla de manera dinámica
    Usa la función random.shuffle para generar de manera aleatoria los identificadores. Genera una lista de identificadores
    en donde se repiten dos veces el mismo ya que en un memotest se repiten dos veces la misma carta
    Retorna la lista de las tarjetas generadas
    '''
    lista_tarjetas = []
    indice = 0
    lista_id = generar_lista_ids_tarjetas() 
    print(lista_id)

    for x in range(0, CANTIDAD_TARJETAS_H * ANCHO_TARJETA, ANCHO_TARJETA):
        for y in range(0, CANTIDAD_TARJETAS_V * ALTO_TARJETA, ALTO_TARJETA):
            imagen = "0{0}.png".format(lista_id[indice])
            imagen_escondida = "00.png"
            id = lista_id[indice]

            tarjeta =crear_tarjeta(imagen, id, imagen_escondida, x, y)
            lista_tarjetas.append(tarjeta)
            indice += 1
            pass
            # COMPLETAR
    
    return lista_tarjetas

def generar_lista_ids_tarjetas():
    lista_id = list(range(1,CANTIDAD_TARJETAS_UNICAS+1)) #Creo una lista con todos los identificadores posibles
    lista_id.extend(list(range(1,CANTIDAD_TARJETAS_UNICAS+1))) #Extiendo esa lista con otra lista identica ya que hay dos tarjetas iguales en cada tablero (mismo identificador)
    random.seed(time.time())
    random.shuffle(lista_id) #Esos identificadores los desordeno de forma al azar
    return lista_id
    
def detectar_colision(tablero: dict, pos_xy: tuple) -> int  :
    '''
    verifica si existe una colision alguna tarjetas del tablero y la coordenada recibida como parametro
    Recibe como parametro el tablero y una tupla (X,Y)
    Retorna el identificador de la tarjeta que colisiono con el mouse y sino retorna None
    '''

    tarjetas = tablero['tarjetas']
    primer_tarjeta_seleccionada = tablero['primer_tarjeta_seleccionada']
    segunda_tarjeta_seleccionada = tablero['segunda_tarjeta_seleccionada']

    if primer_tarjeta_seleccionada is not None and segunda_tarjeta_seleccionada is not None:
        # Ya se seleccionaron dos tarjetas en este turno, no hacer nada
        return

    for indice, tarjeta in enumerate(tarjetas):
        if tarjeta['rectangulo'].collidepoint(pos_xy):
            tarjeta['visible'] = True
            if primer_tarjeta_seleccionada is None:
                tablero['primer_tarjeta_seleccionada'] = indice
            else:
                tablero['segunda_tarjeta_seleccionada'] = indice
            tablero['tiempo_ultimo_destape'] = pygame.time.get_ticks()
            break

    # COMPLETAR

def actualizar_tablero(tablero: dict) -> None:
    '''
    Verifica si es necesario actualizar el estado de alguna tarjeta, en funcion de su propio estado y el de las otras
    Recibe como parametro el tablero
    '''

    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = tiempo_actual - tablero["tiempo_ultimo_destape"]
    
    if tiempo_transcurrido > TIEMPO_MOVIMIENTO:
        tablero["tiempo_ultimo_destape"] = 0
        
        for tarjeta in tablero["tarjetas"]:
            if not tarjeta["descubierto"]:
                tarjeta["visible"] = False
        
        tablero["primer_tarjeta_seleccionada"] = None
        tablero["segunda_tarjeta_seleccionada"] = None
    
    if tablero["primer_tarjeta_seleccionada"] is not None and tablero["segunda_tarjeta_seleccionada"] is not None:
        primer_tarjeta_indice = tablero["primer_tarjeta_seleccionada"]
        segunda_tarjeta_indice = tablero["segunda_tarjeta_seleccionada"]
        
        primer_tarjeta = tablero["tarjetas"][int(primer_tarjeta_indice)]
        segunda_tarjeta = tablero["tarjetas"][int(segunda_tarjeta_indice)]
        
        if primer_tarjeta["identificador"] == segunda_tarjeta["identificador"]:
            primer_tarjeta["visible"] = True
            primer_tarjeta["descubierto"] = True
            segunda_tarjeta["visible"] = True
            segunda_tarjeta["descubierto"] = True

    # COMPLETAR

def comprarar_tarjetas(tablero: dict) -> bool | None:
    '''
    Funcion que se encarga de encontrar un match en la selección de las tarjetas del usuario.
    Si el usuario selecciono dos tarjetas está función se encargara de verificar si el identificador 
    de las mismas corresponde si es así retorna True, sino False. 
    En caso de que no hayan dos tarjetas seleccionadas retorna None
    '''
    retorno = None
    if tablero["primer_tarjeta_seleccionada"] != None and tablero["segunda_tarjeta_seleccionada"] != None:
        retorno = False
        if tablero["primer_tarjeta_seleccionada"]["identificador"] == tablero["segunda_tarjeta_seleccionada"]["identificador"]:
            tarjeta.descubrir_tarjetas(tablero["tarjetas"], tablero["primer_tarjeta_seleccionada"]["identificador"])
            retorno = True

    return retorno

def dibujar_tablero(tablero: dict, pantalla_juego: pygame.Surface):
    '''
    Dibuja todos los elementos del tablero en la superficie recibida como parametro
    Recibe como parametro el tablero y la ventana principal
    '''
    tarjetas = tablero['tarjetas']

    for tarjeta in tarjetas:
        if tarjeta['visible']:
            superficie_tarjeta = tarjeta['superficie']
        else:
            superficie_tarjeta = tarjeta['superficie_escondida']

        pantalla_juego.blit(superficie_tarjeta, tarjeta['rectangulo'])


    # COMPLETAR
   