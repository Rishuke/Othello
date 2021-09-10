#!/usr/bin/env python
# -*- coding: utf-8 -*-
import othello
import matplotlib.pyplot as plt
import sys
import random
from math import *

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
import joueur_alphabeta_old_o
import joueur_alphabeta_o

player_list = [joueur_humain, 
			joueur_aleatoire_u, 
			joueur_premier_coup_valide_u, 
			joueur_dernier_coup_valide_u, 
			joueur_horizon1_o, 	#4
			joueur_horizonN_o, 	#5
			joueur_minimax_o, 	#6
			joueur_alphabeta_old_o,#7
			joueur_alphabeta_o]	#8

def partie(j1, j2, wj1=None):
	game.joueur1 = joueur_aleatoire_u
	game.joueur2 = joueur_aleatoire_u
	jeu = game.initialiseJeu()
	for _ in range(4) :
		#game.afficheJeu(jeu)
		coup = game.saisieCoup(jeu)
		game.joueCoup(jeu, coup)
		
		
	game.joueur1 = player_list[j1]
	if wj1:
		game.joueur1.WEIGHTS = wj1
	game.joueur2 = player_list[j2]
	it = 4
	while (it < 100) and (not game.finJeu(jeu)) :
		#game.afficheJeu(jeu)
		coup = game.saisieCoup(jeu)
		game.joueCoup(jeu, coup)
		it+=1
	#game.affiche(jeu)
	print("*", end='')
	sys.stdout.flush()
	return game.getGagnant(jeu)


def UltraE(j1, j2, w=None):
	"""E mais avec du multiprocessing"""
	n = 15 
	#avant n=10 => 27 mins de processing
	# n = 40 -> 1h04 de processing avec H1
	
	score = n
	
	print("measuring score... for n=",n)
	resj1 = pool.starmap_async(partie, [(j1, j2, w) for _ in range(n//2)])
	resj2 = pool.starmap_async(partie, [(j2, j1, w) for _ in range(n - n//2)])
	vj1 = resj1.get()
	vj2 = resj2.get()
	
	for gagnant in vj1:
		if gagnant == 1:
			score-=1
		if gagnant == 2:
			score+=1
			
	for gagnant in vj2:
		if gagnant == 2:
			score-=1
		if gagnant == 1:
			score+=1
	
	print(" complete!\nscore=",score)	
	return score
		
def E(j1, j2, w=None) :
	"""calcul un score à minimiser pour augmenter les perfs du j1,
	le score produit est d'autant plus haut que j2 gagne où que des match nuls sont produits"""
	
	if w:
		j1.WEIGHTS = w
	n = 20
	
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
					
				#print("partie {}/{};\tgg pour j{}".format(i+1, n, gagnant))
			else:
				gagnant = partie(j2, j1)
				if gagnant == 2:
					j1_cpt_vic[1]+=1
				if gagnant == 1:
					j2_cpt_vic[1]+=1
					
				#print("partie {}/{};\tgg pour j{}".format(i+1, n, 1+gagnant%2))
	except KeyboardInterrupt:
		pass
		
	#print("\n victoires p1 \nj1: {}%\nj2: {}%\n".format( (j1_cpt_vic[0]/(n/2))*100, (j2_cpt_vic[0]/(n/2))*100),
	#	"victoires p2 \nj1: {}%\nj2: {}%\n\n".format((j1_cpt_vic[1]/(n/2))*100, (j2_cpt_vic[1]/(n/2))*100),
	#	"victoires tot\nj1: {}%\nj2: {}%\n".format((sum(j1_cpt_vic)/n)*100, (sum(j2_cpt_vic)/n)*100))
	return sum(j2_cpt_vic) - sum(j1_cpt_vic) + n #quand grand, j2 a l'avantage. on cherche à minimiser ce score

#inspiré par:
## programme de résolution du problème du voyaguer de commerce
## par l'algorithme du recuit simulé
## Dominique Lefebvre pour TangenteX.com
## 14 mars 2017
# et
## https://fr.wikipedia.org/wiki/Recuit_simul%C3%A9

def voisin(w, j):
	nw_plus = [e for e in w]
	nw_moins = [e for e in w]
	
	delta = random.random()
	
	nw_plus[j]  += delta
	nw_moins[j] -= delta
	
	return nw_plus, nw_moins

def P(dE, T):
	return exp(-dE/T)

def recuitSim(player_to_adjust, player_to_reinforce_against):
	import copy
	
	kmax = 20	#nombre d'étapes max
	emax = 1	#température min
	
	s0 = copy.copy(player_list[player_to_adjust].WEIGHTS)
	
	etat = s0
	meilleur = s0
	
	energie = UltraE(player_to_adjust, player_to_reinforce_against, etat)
	energie_meilleur = energie
	energie_start = energie
	
	# initialisation des listes d'historique
	Henergie = []		# énergie
	Htemps = []			# temps
	HT = []				# température
	Hvar = []			# paramètres
	
	k = 1
	num_params = len(meilleur)
	print(energie, " -> ", emax)
	
	try:
		for j in range(num_params):
			Hvar.append([])
			energie = energie_start
			k = 1
			while( k < kmax and energie > emax):
				sn_plus, sn_moins = voisin(etat, j)
				en_plus = UltraE(player_to_adjust, player_to_reinforce_against, sn_plus)
				en_moins = UltraE(player_to_adjust, player_to_reinforce_against, sn_moins)
				
				T = -log(k/kmax)
				
				if en_plus > en_moins:
					en = en_moins
					sn = sn_moins
				else:
					en = en_plus
					sn = sn_plus
				
				if en < energie or random.random() < P(en - energie, T):
					etat = sn
					energie = en
					
					#on conserve le meilleur résultat:
					if energie < energie_meilleur :
						meilleur = copy.copy(etat)
						energie_meilleur = energie
						
				if True:#k % 10 == 0:
					Henergie.append(energie)
					Htemps.append(k)
					HT.append(T)
					Hvar[-1].append(etat[j])
				
				print("Param ", j, ", my k: ", k, ", my E: ", energie, 
					"\nstate: ", etat,
					"\nsn:    ", sn[j])
				k += 1
			
	except KeyboardInterrupt:
		pool.terminate()
		pool.join()
	
	print(meilleur)
	
	# affichage des courbes d'évolution
	if Hvar:
		for i in range(len(Hvar)):
			plt.plot(Hvar[i], label="w{}".format(i))
		plt.title("Evolution des poids au cours du recuit simulé")
		plt.legend()
		plt.show()
		
	
	return meilleur

if __name__ ==  '__main__':
	from multiprocessing import Pool
	import time
	
	pool = Pool()
	START_TIME = time.time()
	
	recuitSim(8, 7)
	
	print("time elapsed: ", time.time() - START_TIME)
	pool.close()
	pool.join()
