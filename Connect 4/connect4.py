# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 15:14:10 2016

@author: Gorka
"""

import math
import os
import random as rd
import copy
#import numpy as np

ANCHURA = 7
ALTURA = 6

###
### ||||||||||| MAIN ||||||||||
###

def main() :
    print('Conecta 4')
    
    tablero = nuevotablero(ANCHURA,ALTURA) # Pedir tablero
    
    print()
    print('La máquina juega con X y la persona con O.')
    
    # Pedir dificultad (número de niveles de profundidad a comprobar en minimax)
    nivel = input('Elige dificultad (número de 1 al 5): ')
    while not(nivel.isnumeric()) or int(nivel) > 5 or int(nivel) < 1:
        print()
        print('El nivel ha de ser un número del 1 al 5.')
        nivel = input('Elige dificultad (número de 1 al 5): ')
    nivel = int(nivel)
    

    
    # Elegir quien va primero
    empieza = input('¿Quien va primero? (M = máquina, P = persona) ')
    while str(empieza) != 'M' and str(empieza) != 'P' :
        print()
        print('Introducir M o P.')
        empieza = input('¿Quien va primero? (M = máquina, P = persona) ')
    
    
    # Asignación de fichas según el primer turno
    if empieza == 'M' :
        ficha = 'X'
    elif empieza == 'P' :
        ficha = 'O'


    while True : # Loop de juego
    
        if ficha == 'X' : # Turno de la máquina
        
#            imprimir(tablero) # Imprimir tablero
            

            if nivel<=3 :
                # Conseguir y colocar movimiento
                print('La máquina está pensando...')
                movmaquina,evaluacion = alfabeta(tablero,nivel,True,-math.inf,math.inf,ficha)
                colocar(tablero,movmaquina,ficha)
                
            else :
                # Conseguir y colocar movimiento
                print('La máquina está pensando...')
                movmaquina = moviOrdenador(tablero,ficha)
                colocar(tablero,movmaquina,ficha)
                
            
            os.system('cls' if os.name == 'nt' else 'clear')
            imprimir(tablero) # Imprimir tablero

            
            if ganador(tablero,ficha) : # Comprobar si hay ganador
                print('Ha ganado la máquina...')
                break
            
            if empate(tablero) : # Comprobar si hay empate
                print('Empate.')
                break


            ficha = 'O'
            
        else : # Turno de la persona
                         
#            imprimir(tablero) # Mostrar tablero
            

            
            # Pedir movimiento a realizar
            columna = pedir()
            
            # Colocar movimiento en tablero e imprimir
            control = False
            while colocar(tablero,columna,ficha) :
                imprimir(tablero)
                print('No se puede realizar ese movimiento.')
                columna = pedir()
                control = True
                colocar(tablero,columna,ficha)
            
            ## En caso de entrar en el loop while, coloca la ficha dos veces
            ##(la primera dentro del while, después de imprimir el mensaje
            ##y la otra al comprobar la condición para no entrar al loop)
            ## Es necesario, pues, quitar el movimiento que sobra
            if control :
                for y in range(ALTURA) :
                    if tablero[y][columna] != ' ' :
                        tablero[y][columna] = ' '
                        control = False
                        break
            
            os.system('cls' if os.name == 'nt' else 'clear')
            imprimir(tablero)
                
            if ganador(tablero,ficha) : # Comprobar si hay ganador
                print('Has ganado!')
                break
            
            if empate(tablero) : # Comprobar si hay empate
                print('Empate.')
                break
            
            ficha = 'X'


    
    denuevo = input('¿Quieres jugar de nuevo? (S = si, N = no) ')
    while str(denuevo)!='S' and str(denuevo)!='N' :
        print()
        print('Introducir S (si) o N (no).')
        denuevo = input('¿Quieres jugar de nuevo? (S = si, N = no) ')
    
    if denuevo == 'S' :
        main()
        
    return





###
### |||||||||| MINIMAX ||||||||||
###

def minimax (tablero,profundidad,maximizar,ficha,nodo=-1) :
    
    # Caso base
    if (profundidad==0) or (not sucesores(tablero)) or (ganador(tablero,ficha)) :
        return nodo,evaluacion(tablero)
        
    if maximizar : # Maximixar jugador
        mejor = -math.inf
        for hijo in sucesores(tablero) :
            colocar(tablero,hijo,ficha)
            n,v = minimax(tablero,profundidad-1,False,'O',hijo)
            quitar(tablero,hijo,ficha)
            if v>mejor :
                mejor,mov = v,n
        return mov,mejor

    else : # Minimizar jugador
        peor = math.inf
        for hijo in sucesores(tablero) :
            colocar(tablero,hijo,ficha)
            n,v = minimax(tablero,profundidad-1,True,'X',hijo)
            quitar(tablero,hijo,ficha)
            if v<peor :
                peor,mov = v,n
        return mov,peor






###
### ||||||| MINIMAX + PODA ALFA BETA |||||||
###

def alfabeta (tablero,profundidad,maximizar,alfa,beta,ficha,nodo=-1) :
    
    # Caso base
    if (profundidad==0) or (not sucesores(tablero)) or (ganador(tablero,ficha)) :
        return nodo,evaluacion2(tablero,ficha)
        
    if maximizar : # Maximixar jugador
        v = -math.inf
        for hijo in sucesores(tablero) :
            colocar(tablero,hijo,ficha)
            movi,evalu = alfabeta(tablero,profundidad-1,False,alfa,beta,'O',hijo)
            quitar(tablero,hijo,ficha)            
            v = max(v,evalu)
            alfa = max(alfa,v)
            if beta<=alfa :
                break
        return movi,evalu

    else : # Minimizar jugador
        v = math.inf
        for hijo in sucesores(tablero) :
            colocar(tablero,hijo,ficha)
            movi,evalu = alfabeta(tablero,profundidad-1,alfa,beta,True,'X',hijo)
            quitar(tablero,hijo,ficha)
            v = min(v,evalu)
            beta = min(beta,v)
            if beta<=alfa :
                break
        return movi,evalu





###
### |||||||||| GANADOR ||||||||||
###

def ganador(tablero,ficha) : # Comprueba si hay algun cuatro en raya
    
    # Horizontal
    for y in range(ALTURA) :
        for x in range(ANCHURA-3) :
            if all(tablero[y][j]==ficha for j in range(x,x+4)) :
                return True

    # Vertical
    for x in range(ANCHURA):
        for y in range(ALTURA-3) :
            if all(tablero[j][x]==ficha for j in range(y,y+4)) :
                return True

    # Diagonal /
    for x in range(ANCHURA-3) :
        for y in range(3,ALTURA) :
            if all(tablero[y-j][x+j]==ficha for j in range(4)) :
                return True

    # Diagonal \
    for x in range(ANCHURA-3) :
        for y in range(ALTURA-3) :
            if all(tablero[y+j][x+j]==ficha for j in range(4)) :
                return True

    return False





###
### |||||||||| EMPATE |||||||||
###

def empate(tablero) :
    if ' ' not in tablero[0] :
        return True


###
### |||||||||| EVALUACION1 ||||||||||
###


def evaluacion (tablero) :
    
    maquina,persona = 0,0 # Contador de nº de cuatros en rayas posibles
    
    # Horizontal
    for y in range(ALTURA) :
        for x in range(ANCHURA-3) :
            if set([tablero[y][j] for j in range(x,x+4)])==set(['X',' ']) :
                maquina += 1
            if set([tablero[y][j] for j in range(x,x+4)])==set(['O',' ']) :
                persona += 1
    
    # Vertical
    for x in range(ANCHURA):
        for y in range(ALTURA-3) :
            if set([tablero[j][x] for j in range(y,y+4)])==set(['X',' ']) :
                maquina += 1
            if set([tablero[j][x] for j in range(y,y+4)])==set(['O',' ']) :
                persona += 1
    
    # Diagonal /
    for x in range(ANCHURA-3) :
        for y in range(3,ALTURA) :
            if set([tablero[y-j][x+j] for j in range(4)])==set(['X',' ']) :
                maquina += 1
            if set([tablero[y-j][x+j] for j in range(4)])==set(['O',' ']) :
                persona += 1
    
    # Diagonal \
    for x in range(ANCHURA-3) :
        for y in range(ALTURA-3) :
            if set([tablero[y+j][x+j] for j in range(4)])==set(['X',' ']) :
                maquina += 1
            if set([tablero[y+j][x+j] for j in range(4)])==set(['O',' ']) :
                persona += 1
                
    return persona-maquina







###
### |||||||||| EVALUACION2 ||||||||||
###

def evaluacion2 (tablero,ficha):
    puntuacion = 0
    for fila in range(ALTURA) :
        if fila <= (ALTURA-4) :
            for columna in range(ANCHURA) :
                puntuacion += score(fila,columna,tablero,ficha)
        else :
            for columna in range(ANCHURA-3) :
                puntuacion += score(fila,columna,tablero,ficha)
    return puntuacion



def score (fila,columna,tablero,ficha):
    puntuacion = 0
    desbloqueado = True
    cuenta = 0
    
    if fila < (ALTURA-3) :
        
        # Comprobar hacia arriba
        desbloqueado = True
        cuenta = 0
        
        for y in range(fila,fila+4) :
            if (tablero[y][columna]!=ficha) and (tablero[y][columna]!=' '):
                desbloqueado = False
            if (tablero[y][columna]==ficha) :
                cuenta += 1
        
        if desbloqueado :
            puntuacion = puntuacion + (cuenta*cuenta*cuenta*cuenta)

        if columna < ANCHURA-3 :
            # Arriba y a la izquierda
            desbloqueado = True
            cuenta = 0
            
            for x in range(columna,fila+4) :
                for y in range(fila,fila+4) :
                    if (tablero[y][x]!=ficha) and (tablero[y][x]!=' ') :
                        desbloqueado = False
                    if (tablero[y][x]==ficha) :
                        cuenta = 0
            
            if desbloqueado :
                puntuacion = puntuacion + (cuenta*cuenta*cuenta*cuenta)
            
    
    if columna < ANCHURA-3 :
        # Comprobar hacia la derecha
        desbloqueado = True
        cuenta = 0
        
        for x in range(columna,columna+4) :
            if (tablero[fila][x]!=ficha) and (tablero[fila][x]!=' ') :
                desbloqueado = False
            if (tablero[fila][x]==ficha) :
                cuenta += 1
        
        if desbloqueado :
            puntuacion = puntuacion + (cuenta*cuenta*cuenta*cuenta)
        
        if fila > 2 :
            # Mirar abajo y derecha
            desbloqueado = True
            cuenta = 0
            
            # Argiiiii
            f = fila
            c = columna
            while c<columna+4 :
                f -= 1
                c += 1
                        
            if desbloqueado :
                puntuacion = puntuacion + (cuenta*cuenta*cuenta*cuenta)
 
        
        


    return puntuacion




###
### |||||||||| NUEVOTABLERO ||||||||||
###

def nuevotablero (anchura,altura) :
    tablero = []
    for alt in range(altura) :
        tablero.append(anchura*[' '])
                
    return tablero




###
### |||||||||| IMPRIMIR ||||||||||
###
    
def imprimir(tablero) :
    print()
    print(' ', end='')
    for x in range(1, ANCHURA + 1):
        print(' %s  ' % x, end='')
    print()

    print('+---+' + ('---+' * (ANCHURA - 1)))

    for y in range(ALTURA):
        print('|   |' + ('   |' * (ANCHURA - 1)))

        print('|', end='')
        for x in range(ANCHURA):
            print(' %s |' % tablero[y][x], end='')
        print()

        print('|   |' + ('   |' * (ANCHURA - 1)))

        print('+---+' + ('---+' * (ANCHURA - 1)))
    
    print(' ', end='')
    for x in range(1, ANCHURA + 1):
        print(' %s  ' % x, end='')
    print()




###
### |||||||||| PEDIR ||||||||||
###

def pedir() :
    columna = input('¿Cuál es tu siguiente movimiento? (Introduce el número de la columna) ')
    while not(columna.isnumeric()) or int(columna)<1 or int(columna)>7 :
        print()
        print('El input ha de ser un número del 1 al 7.')
        columna = input('¿Cuál es tu siguiente movimiento? (Introduce el número de la columna) ')
    return int(columna)-1




###
### ||||||||| COLOCAR MOVIMIENTO ||||||||||
###

def colocar(tablero,columna,ficha) :
    # Recorrer la columna correspondiente y ver si es posible
    for y in range(ALTURA-1,-1,-1) :
        if tablero[y][columna] == ' ' :
            tablero[y][columna] = ficha
            return
    return True





###
### |||||||||| QUITAR ||||||||||
###

def quitar (tablero,columna,ficha) :
    for y in range(ALTURA) :
        if tablero[y][columna] == ficha :
            tablero[y][columna] = ' '
            return
    return True
                



###
### |||||||||| SUCESORES |||||||||
###

def sucesores (tablero) :
    sucesores = []

    for x in range(ANCHURA) :
        if any(tablero[y][x] == ' ' for y in range(ALTURA)) :
            sucesores.append(x)
        
#    for x in range(ANCHURA) :
#        if any(tablero[y][x] == ' ' for y in range(ALTURA)) and x not in sucesores :
#            sucesores.append(x)

    return sucesores
            



###
### |||||||||| GETPOTENTIALMOVES ETAB. ||||||||||
###

def moviValido(tablero, columna):
    if columna < 0 or columna >= (ANCHURA):
        return False

    if tablero[0][columna] != ' ':
        return False

    return True


def moviOrdenador(tablero, fichaOrdenador):
    movimientos = minimax2(tablero, fichaOrdenador, 2)
    print(sum(movimientos))
    evaluMejormovi = max([movimientos[i] for i in range(ANCHURA) if moviValido(tablero, i)])
    mejoresMovi = []
    for i in range(len(movimientos)):
        if movimientos[i] == evaluMejormovi:
            mejoresMovi.append(i)
    return rd.choice(mejoresMovi)


def minimax2(tablero, fichaUsuario, profundidad):

    if profundidad == 0:
        return [0] * ANCHURA

    moviPotenciales = []

    if fichaUsuario == 'X':
        fichaEnemiga = 'O'
    else:
        fichaEnemiga = 'X'

    # Returns (best move, average condition of this state)
    if empate(tablero):
        return [0] * ANCHURA

    # Figure out the best move to make.
    moviPotenciales = [0] * ANCHURA
    for moviJugador in range(ANCHURA):
        copyTablero = copy.deepcopy(tablero)
        if not moviValido(copyTablero, moviJugador):
            continue
        colocar(copyTablero,moviJugador,fichaUsuario)
        if ganador(copyTablero, fichaUsuario):
            moviPotenciales[moviJugador] = 1
            break
        
        else:
            # do other player's moves and determine best one
            if empate(copyTablero):
                moviPotenciales[moviJugador] = 0
            else:
                for moviEnemigo in range(ANCHURA):
                    copyTablero2 = copy.deepcopy(copyTablero)
                    if not moviValido(copyTablero2, moviEnemigo):
                        continue
                    colocar(copyTablero2,moviEnemigo,fichaEnemiga)
                    if ganador(copyTablero2, fichaEnemiga):
                        moviPotenciales[moviJugador] = -1
                        break
                    else:
                        resultados = minimax2(copyTablero2, fichaUsuario, profundidad - 1)
                        moviPotenciales[moviJugador] += (sum(resultados) / ANCHURA) / ANCHURA

    return moviPotenciales


if __name__ == '__main__':
    main()
