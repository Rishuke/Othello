#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    
    game.affiche(jeu)
    
    print("  Vous êtes le joueur {}".format(game.getJoueur(jeu)))

    coups_valides = game.getCoupsValides(jeu)
    print(" Coups valides:", coups_valides)
    
    coup_valide = False
    while(not coup_valide):
        print("  Saisir coup:")
        x = int(input("    ligne  ="))
        y = int(input("    colonne="))
        coup = (x,y)
        coup_valide = coup in coups_valides
        if not coup_valide:
            print("    coup invalide! rejouez...")
            
    return coup