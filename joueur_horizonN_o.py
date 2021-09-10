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


def EGagne(jeu):
    if not game.getCoupsValides(jeu): #plus de coup valides...
        gg = game.getGagnant(jeu)
        if gg == MOI:
            return 1000
        elif gg == 0: #pas de gagnant
            return 1
        else:#adversaire
            return -1000
    return 1

#old eval
# def evaluation(jeu):
#     w=[0.7, 0.3]
#     f=[EScore(jeu), Ecoins(jeu)]
#     return np.dot(w,f)

def evaluation(jeu):
    w=[0.35, 0.15, 0.5]
    f=[EScore(jeu), Ecoins(jeu), EGagne(jeu)]
    return sum([fi*wi for fi,wi in zip(f,w)])#dot


def estimation(jeu, coup, n):
    next_game = game.getCopieJeu(jeu)
    game.joueCoup(next_game, coup)
    
    #profondeur d'arret
    if n == 0:
        return evaluation(next_game)
    
    #on continue d'explorer l'arbre
    cv = game.getCoupsValides(next_game)
    
    if not cv: #plus de coup valides...
        return evaluation(next_game)
    
    score_coup = 0
    for cp in cv:
        score_coup += estimation(next_game, cp, n-1)
        #coupure temps max atteint: élaguage
        if (time.time() - START_TIME) > TIMEOUT:
            score_coup = evaluation(next_game)
            break
        
    return score_coup

def decision(jeu):
    cv = game.getCoupsValides(jeu)
    estimations = []
    for cp in cv:
        estimations.append(estimation(jeu, cp, N))
    
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