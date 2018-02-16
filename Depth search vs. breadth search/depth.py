# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 16:43:41 2016

@author: Gorka
"""

import sys

sys.setrecursionlimit(1000000000)

#0, camino
#1, pared
#2, transitado


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
    return [hijo for hijo in posibles if laberinto[hijo[0]][hijo[1]]==0 or
            hijo==2*[len(laberinto)-1]]
            
    
    
    
def profundidad (x,y,laberinto) :
    
    if x==(len(laberinto[0])-1) and y==(len(laberinto)-1) :
        print(laberinto)
        
    else :
        for hijo in hijos(x,y,laberinto) :
            laberinto[hijo[0]][hijo[1]] = 2
            profundidad(hijo[0],hijo[1],laberinto)
            laberinto[hijo[0]][hijo[1]] = 0
