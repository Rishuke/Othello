#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import time

MOI = None
JEU = None

N = 2

TIMEOUT = 1.0
START_TIME = None

def EScore(jeu):
    j = game.getJoueur(jeu)
    return game.getScore(jeu, j) - game.getScore(JEU, j) - (game.getScore(jeu, j%2+1) - game.getScore(JEU, j%2+1))

def Ecoins(jeu):
    plt = game.getPlateau(jeu)
    joueur = game.getJoueur(jeu)
    ret = 0
    
    for i in [7, 0]:
        for j in [7, 0]:
            case = plt[i][j]
            if case == joueur:
                ret +=1
            elif case == joueur%2+1:
                ret -=2
            
    return ret


def EGagne(jeu):
    if game.finJeu(jeu): #plus de coup valides...
        gg = game.getGagnant(jeu)
        if gg == game.getJoueur(jeu):
            return 1000
        elif gg == 0: #pas de gagnant
            return 0
        else:#adversaire
            return -1000
    return 0

#old eval
# def evaluation(jeu):
#     w=[0.7, 0.3]
#     f=[EScore(jeu), Ecoins(jeu)]
#     return np.dot(w,f)

def evaluation(jeu):
    w=[0.35, 0.15, 0.5]
    f=[EScore(jeu), Ecoins(jeu), EGagne(jeu)]
    return sum([fi*wi for fi,wi in zip(f,w)])#dot

def estimation(jeu, coup, n=N):
    next_game = game.getCopieJeu(jeu)
    game.joueCoup(next_game, coup)
    
    invert_joueur = 1
    if game.getJoueur(next_game) != MOI:
        invert_joueur = -1
    
    cv = game.getCoupsValides(next_game)
    
    #profondeur d'arret ou plus de coup valides...
    if n <= 0 or not cv:
        return evaluation(next_game)*invert_joueur
    
    score_coup = -float("inf") * invert_joueur
    for cp in cv:
        score_coup = max(score_coup*invert_joueur, estimation(next_game, cp, n-1)*invert_joueur)*invert_joueur
        
        #elagage si timeout
        if (time.time() - START_TIME) > TIMEOUT:
            break
    
    return score_coup

def decision(jeu):
    cv = game.getCoupsValides(jeu)
    estimations = []
    for cp in cv:
        estimations.append(estimation(jeu, cp))
    
    i_max = estimations.index(max(estimations))
    
    coup = cv[i_max]
    
    return coup



def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global MOI
    global JEU
    global START_TIME
    JEU = jeu
    MOI = game.getJoueur(JEU)
    START_TIME = time.time()
    
    coup = decision(jeu)
    
    return coup