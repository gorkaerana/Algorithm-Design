# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:35:44 2016

@author: Gorka
"""

from collections import deque
import sys

sys.setrecursionlimit(1000000)

#0 camino
#1 pared
#2 transitado

#Laberinto a grafo
def agrafo(laberinto):
    profundidad = len(laberinto)
    anchura = len(laberinto[0]) if profundidad else 0
    grafo = {(i, j): [] for j in range(anchura) for i in range(profundidad) 
            if not laberinto[i][j]}
    for fila, col in grafo.keys():
        if fila < profundidad - 1 and not laberinto[fila + 1][col] :
            grafo[(fila, col)].append(("v", (fila + 1, col)))
            grafo[(fila + 1, col)].append(("^", (fila, col)))
        if col < anchura - 1 and not laberinto[fila][col + 1] :
            grafo[(fila, col)].append((">", (fila, col + 1)))
            grafo[(fila, col + 1)].append(("<", (fila, col)))
    return grafo


#Busqueda en anchura
def anchura(laberinto):
    inicio, fin = (0,0), (len(laberinto)-1,len(laberinto[0])-1)
    cola = deque([("", inicio)])
    visitados = set()
    grafo = agrafo(laberinto)
    while cola:
        camino, actual = cola.popleft()
        if actual == fin:
            return camino
        if actual in visitados :
            continue
        visitados.add(actual)
        for direccion, vecino in grafo[actual]:
            cola.append((camino + direccion, vecino))
    print("NO HAY SOLUCION!")
