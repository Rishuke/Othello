#!/usr/bin/env python
# -*- coding: utf-8 -*-
import othello
import sys
from symbol import except_clause
sys.path.append("..")
import game
game.game=othello
sys.path.append("./Joueurs")
import joueur_humain
import joueur_aleatoire_u
import joueur_premier_coup_valide_u
import joueur_dernier_coup_valide_u
import joueur_horizon1_o
import joueur_horizonN_o
import joueur_minimax_o
import joueur_alphabeta_o

def partie(j1, j2):
	game.joueur1 = joueur_aleatoire_u
	game.joueur2 = joueur_aleatoire_u
	jeu = game.initialiseJeu()
	for _ in range(4) :
		#game.afficheJeu(jeu)
		coup = game.saisieCoup(jeu)
		game.joueCoup(jeu, coup)
		
		
	game.joueur1 = j1
	game.joueur2 = j2
	it = 4
	while (it < 100) and (not game.finJeu(jeu)) :
		#game.afficheJeu(jeu)
		coup = game.saisieCoup(jeu)
		game.joueCoup(jeu, coup)
		it+=1
	#game.affiche(jeu)
	return game.getGagnant(jeu)

def mainLoop(j1, j2, n) :
	j1_cpt_vic = [0, 0]
	j2_cpt_vic = [0, 0]
	
	try:
		for i in range(n):
			gagnant = 0
			if i < n//2:
				gagnant = partie(j1, j2)
				if gagnant == 1:
					j1_cpt_vic[0]+=1
				if gagnant == 2:
					j2_cpt_vic[0]+=1
					
				print("partie {}/{};\tgg pour j{}".format(i+1, n, gagnant))
			else:
				gagnant = partie(j2, j1)
				if gagnant == 2:
					j1_cpt_vic[1]+=1
				if gagnant == 1:
					j2_cpt_vic[1]+=1
					
				print("partie {}/{};\tgg pour j{}".format(i+1, n, 1+gagnant%2))
	except KeyboardInterrupt:
		pass
		
	print("\n victoires p1 \nj1: {}%\nj2: {}%\n".format( (j1_cpt_vic[0]/(n/2))*100, (j2_cpt_vic[0]/(n/2))*100),
		"victoires p2 \nj1: {}%\nj2: {}%\n\n".format((j1_cpt_vic[1]/(n/2))*100, (j2_cpt_vic[1]/(n/2))*100),
		"victoires tot\nj1: {}%\nj2: {}%\n".format((sum(j1_cpt_vic)/n)*100, (sum(j2_cpt_vic)/n)*100))

mainLoop(joueur_alphabeta_o, joueur_horizonN_o, 50)
