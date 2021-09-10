#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import time

MOI = None
JEU = None

N = 2
WEIGHTS = [0.35, 0.10, 0.50, 0.04, 0.01]
#hand written: [0.35, 0.10, 0.50, 0.04, 0.01]

TIMEOUT = 1.0
START_TIME = None


def stadeJeu(jeu):
    plt = game.getPlateau(jeu)

    nb_pce = sum(sum(i) for i in plt)
    
    if nb_pce > 64/3:
        return 1 #mid game
        
    if nb_pce > 64*3/4:
        return 2 #late game
    
    return 0 #early game


def EScore(jeu):
    j = game.getJoueur(jeu)
    return game.getScore(jeu, j) - game.getScore(JEU, j) - (game.getScore(jeu, j%2+1) - game.getScore(JEU, j%2+1))

def ECoins(jeu):
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
            return 1
        elif gg == 0: #pas de gagnant
            return 0
        else:#adversaire
            return -1
    return 0

def EDiagonales(jeu):
    #seulement utile en mid et late game
    if stadeJeu(jeu) == 0:
        return 0
    
    plt = game.getPlateau(jeu)
    joueur = game.getJoueur(jeu)
    autre_joueur = joueur%2+1
    ret = 0
    
    for i in range(8):
        case = plt[i][i]
        if case == joueur:
            ret +=2
        elif case == autre_joueur:
            ret -=1
            
        case = plt[i][7-i]
        if case == joueur:
            ret +=2
        elif case == autre_joueur:
            ret -=1
    return ret/13

def EWalls(jeu):
    """On teste la continuité de lignes ou colonnes de pions d'un même joueur
    """
    plt = game.getPlateau(jeu)
    joueur = game.getJoueur(jeu)
    
    ret = 0
    
    for i in range(8):
        mur_ligne = 1
        mur_colonne = 1
        last_case_ligne = None
        last_case_colonne = None
        for j in range(8):
            case = plt[i][j]
            if case == last_case_ligne:
                if case == joueur:
                    mur_colonne /=2
                elif case == joueur%2+1:
                    mur_colonne +=1
            else:
                ret += mur_ligne - 1
                mur_ligne = 1
            last_case_ligne = case
                
            case = plt[j][i]
            if last_case_colonne == case:
                if case == joueur:
                    mur_ligne -=1
                elif case == joueur%2+1:
                    mur_ligne +=1
            else:
                ret += mur_colonne - 1
                mur_colonne = 1
            last_case_colonne = case
    
    return ret

#old eval
# def evaluation(jeu):
#     w=[0.7, 0.3]
#     f=[EScore(jeu), Ecoins(jeu)]
#     return np.dot(w,f)

def evaluation(jeu):
    w=WEIGHTS
    f=[EScore, ECoins, EGagne, EDiagonales, EWalls]
    return sum([fi(jeu)*wi for fi,wi in zip(f,w)])#dot

def estimation(jeu, coup, n=N, alpha=-float("inf"), beta=float("inf")): #negamax
    next_game = game.getCopieJeu(jeu)
    game.joueCoup(next_game, coup)
    
    cv = game.getCoupsValides(next_game)
    
    #profondeur d'arret ou plus de coup valides...
    if n <= 0 or not cv:
        return evaluation(next_game)
    
    score_coup = -float("inf")
    for cp in cv:
        score_coup = max(score_coup, -estimation(next_game, cp, n-1, -beta, -alpha))
        alpha = max(alpha, score_coup)
        
        if alpha >= beta:
            break
        
        #elagage si timeout
        if (time.time() - START_TIME) > TIMEOUT:
            break
    
    return score_coup

def decision(jeu):
    cv = game.getCoupsValides(jeu)
    estimations = []
    for cp in cv:
        estimations.append(-estimation(jeu, cp))
    
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