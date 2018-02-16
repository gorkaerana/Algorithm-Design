# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 17:44:01 2016

@author: Gorka
"""


def hijos (x,y,laberinto) : 
    
    posibles = [[x-1,y],[x+1,y],[x,y+1],[x,y-1]] #Norte, sur, este, oeste
    
    if x==0 : #Limite izquierdo
        posibles.remove([x-1,y])
    if y==0 : #Limite superior
        posibles.remove([x,y-1])
    if x==(len(laberinto[0])-1) : #Limite derecho
        posibles.remove([x+1,y])
    if y==(len(laberinto)-1) : #Limite inferior
        posibles.remove([x,y+1])
        
    #Devolver las intransitadas
    return [hijo for hijo in posibles if laberinto[hijo[0]]
    [hijo[1]]==0 or hijo==2*[len(laberinto)-1]]


def agrafo(laberinto):
    profundidad = len(laberinto)
    anchura = len(laberinto[0]) if profundidad else 0
    grafo = {(i, j): [] for j in range(anchura) for i in 
            range(profundidad) 
            if not laberinto[i][j]} # inicializar grafo
    for key in grafo.keys(): # marcar conexiones
        grafo[key] = hijos(key[0],key[1],laberinto)
    return grafo




def anchura (laberinto) :
    
    grafo = agrafo(laberinto)
    
    inicio = [0,0]
    fin = 2*[len(laberinto)-1] 
    
    cola = list([[inicio]]) # cola de elementos a explorar
    laberinto[inicio[0]][inicio[1]] = 2 # marcar inicio como transitado
    
    while cola :
        
        camino = cola.pop(0)
        
        activo = camino[-1]
        
        if activo == fin :
            break
            
        for anexo in grafo.get((activo[0],activo[1]),[]) :
            caminonuevo = list(camino)
            caminonuevo.append(anexo)
            cola.append(caminonuevo)
    
    if fin not in camino :
        return 'NO HAY SOLUCION'
    
    for elemento in camino :
        laberinto[elemento[0]][elemento[1]] = 2
        
    return laberinto
