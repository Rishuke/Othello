#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import random as rnd

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
         
    return rnd.choice(game.getCoupsValides(jeu))