#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import game  # @UnresolvedImport

T = 8
MV_DIRS = ((1,0),(0,1),(1,1),(-1,1),(-1,0),(0,-1),(-1,-1),(1,-1))

def nouveauPlateau():
    """ void -> plateau
        Retourne un nouveau plateau du jeu
    """
    
    #plateau vide
    p = [[0]*T for _ in range(T)]
    
    #on pose les 4 premières pièces
    p[T//2-1][T//2-1] = 1
    p[T//2][T//2]     = 1
    p[T//2-1][T//2]   = 2
    p[T//2][T//2-1]   = 2
    
    return p

def calcScore(jeu):
    sj1 = 0
    sj2 = 0
    for l in jeu[0]:
        for c in l:
            if c == 1:
                sj1 += 1
            elif c == 2:
                sj2 += 1
                
    jeu[4] = (sj1, sj2)
    return sj1, sj2

def coupValides(jeu):
    """jeu -> list[coup]
        Retourne vrai si le coup est valide dans jeu
    """
    cv = set()
    joueur = game.getJoueur(jeu)
    advers = 1+joueur%2
    plt = game.getPlateau(jeu)
    
    for i in range(T):
        for j in range(T):
            if plt[i][j] == joueur:
                for direction in MV_DIRS:
                    x = i + direction[0]
                    y = j + direction[1]
                    while((0 <= x < T) and (0 <= y < T) and (plt[x][y] == advers)):
                        x += direction[0]
                        y += direction[1]
                        if ((0 <= x < T) and (0 <= y < T) and (plt[x][y] == 0)):
                            cv.add((x,y))
    
    return list(cv)

def joueCoup(jeu,coup):
    """jeu*coup -> void
        Joue un coup
        Hypothese:le coup est valide
        Met à jour le plateau
    """
    ln, cl = coup
    plt = jeu[0]
    
    joueur = game.getJoueur(jeu)
    advers = 1+joueur%2
    #score = list(game.getScores(jeu))
    
    plt[ln][cl] = joueur
    #score[joueur-1] += 1
    
    for direction in MV_DIRS:
        #on cherche les directions où retourner les pions
        x = ln + direction[0]
        y = cl + direction[1]
        while((0 <= x < T) and (0 <= y < T) and (plt[x][y] == advers)):
            x += direction[0]
            y += direction[1]
            if ((0 <= x < T) and (0 <= y < T) and (plt[x][y] == joueur)):
                #direction valide! on retourne les pions
                x = ln + direction[0]
                y = cl + direction[1]
                while((0 <= x < T) and (0 <= y < T) and (plt[x][y] == advers)):
                    plt[x][y] = joueur
                    
                    #score[joueur-1] += 1
                    #score[advers-1] -= 1
                    
                    x += direction[0]
                    y += direction[1]

    #jeu[4] = tuple(score)
    
    _ = calcScore(jeu)
    
    game.changeJoueur(jeu)
    jeu[2] = None
    game.getCoupsJoues(jeu).append(coup)

def finJeu(jeu):
    """ jeu -> bool
        Retourne vrai si c'est la fin du jeu
    """
    return len(game.getCoupsValides(jeu)) == 0

def getGagnant(jeu):
    """jeu->nat
    Retourne le numero du joueur gagnant apres avoir finalise la partie. Retourne 0 si match nul
    """
    #on compte...
    sj1, sj2 = calcScore(jeu)

    #on regarde le winner 
    if sj1 > sj2:
        return 1
    if sj2 > sj1:
        return 2
    return 0
