#!/usr/bin/env python
# -*- coding: utf-8 -*-
import othello
import sys
sys.path.append("..")
import game
game.game=othello
sys.path.append("./Joueurs")
import joueur_humain
game.joueur1=joueur_humain
game.joueur2=joueur_humain


def mainLoop() :
	jeu = game.initialiseJeu()
	it = 0
	while (it < 100) and (not game.finJeu(jeu)) :
		#game.afficheJeu(jeu)
		coup = game.saisieCoup(jeu)
		game.joueCoup(jeu, coup)
		it+=1
	game.affiche(jeu)
	print("gagnant :", game.getGagnant(jeu))

mainLoop()
