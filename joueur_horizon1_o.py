#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import numpy as np

MOI = None
JEU = None

def EScore(jeu):
    return game.getScore(jeu, MOI) - game.getScore(JEU, MOI) - (game.getScore(jeu, MOI%2+1) - game.getScore(JEU, MOI%2+1))
    
def Ecoins(jeu):
    plt = game.getPlateau(jeu)
    ret = 0
    
    for i in [7, 0]:
        for j in [7, 0]:
            case = plt[i][j]
            if case == MOI:
                ret +=1
            elif case == MOI%2+1:
                ret -=2
            
    return ret



def evaluation(jeu):
    w=[0.7, 0.3]
    f=[EScore(jeu), Ecoins(jeu)]
    return np.dot(w,f)

def estimation(jeu, coup):
    next_game = game.getCopieJeu(jeu)
    game.joueCoup(next_game, coup)
    return evaluation(next_game)

def decision(jeu):
    cv = game.getCoupsValides(jeu)
    estimations = []
    for cp in cv:
        estimations.append(estimation(jeu, cp))
    
    e = np.array(estimations)
    i_max = np.argmax(e)
    
    coup = cv[i_max]
    
    return coup



def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global MOI
    global JEU
    JEU = jeu
    MOI = game.getJoueur(JEU)
    
    coup = decision(jeu)
    
    return coup