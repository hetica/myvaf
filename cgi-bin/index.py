#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

"""
Liens :
	http://webpython.codepoint.net/cgi_file_upload
	//// la réponse faites est très intérressante (WSGIScriptAlias)
	http://stackoverflow.com/questions/882430/how-to-hide-cgi-bin-py-etc-from-my-urls
"""

import os
import cgi
import cgitb; cgitb.enable() 		# Pour afficher les erreurs dans le browser

form = cgi.FieldStorage()

def file_check_ok(texte):
	"""
	En entrée : le texte à controller
	En sortie : vrai ou faux
	"""
	if texte == "":
		return False
	return True

def parse_file(texte):
	
	texte = texte.split("\n")								# Séparer la chaine en liste de lignes

	if "Gene" or "gene" in texte[0]:						# supprimer la ligne d'entete si nécessaire
		del texte[0]
	for i,line in enumerate(texte):							# supprimer les lignes non conformes
		if not "\t" in line:
			del texte[i]
		if line == '' or line == "\n":
			del texte[i]
	for i,line in enumerate(texte):							# séparer les lignes en champs 
		texte[i] = line.split("\t")
		
	return texte

def calcule_svg1(texte):
	# les abcisses
	abc1 = 100 ; abc2 = 560									# longueur utile de la barre des abcisses
	abc_t = abc2 - abc1										# longueur utile pour les abcisses
	eb = (abc2-abc1) / len(texte) 							# espace entre chaque barre (1/2 espace au début et à la fin)
	# les ordonnées
	ord1 = 330 ; ord2 = 60									# ord1 : base ; ord2 : hauteur max
	ord_t = ord1 - ord2										# longueur utile pour les ordonnées
	# plus_grand + grande valeur de variant
	plus_grand = max([ int(v) for w,x,y,z,v in texte])		# plus_grande valeur trouvée
	# vsup : valeur max du graphique
	nb_dec = len(str(plus_grand))							# nombre de décimale de plus_grand
	if nb_dec == 1:											# si une seule décimale : vsup = 10
		vsup = 10
	elif plus_grand % 10 == 0:								# si valeur maxi est multiple de 10 alors
		vsup = plus_grand									# 	vsup = valeur maxi
	#elif int(str(plus_grand)[0]) == 1:						# si valeur max a sa unité de poids fort = 1
	#	 vsup = plus_grand - (plus_grand % 10)				# 	vsup = dizaine inférieure de la plus grande valeur
	else:													# dans les autres cas
		vsup = plus_grand - (plus_grand % 10) + 10			# 	vsup = dizaine supérieure de la plus grande valeur
	# déterminer les autres valeurs d'ordonnées du graphiques
	val_dec = int(str(vsup)[0])
	if vsup % 70 == 0:
		vsup = 8 * 10**(len(str(vsup))-1)					# on arrondi à 8 si on était à 7 (ex 70 --> 80)
	if vsup == 10:
		val_ord = (5, 10)
	elif vsup % 30 == 0:
		val_ord = (vsup // 3 , (vsup // 3) * 2 , vsup)
	elif vsup % 20 == 0 or vsup % 50 == 0:
		val_ord = (vsup // 2, vsup)
	# calculer l'espace entre les lignes des abcisses
	ea = (ord1 - ord2) / len(val_ord)	
	
	# print("<p>",plus_grand," ", vsup, " " , val_dec, " " , val_ord,"</p>")
	# print("<p>",ord1," ", ord2, " ", len(val_ord), " " , ea ,"</p>")

	# Cadre exterieur (en fonction de la définition de l'écran, avec un max et min)
	pos = '<rect x="0" y="0" width="620" height="420" fill="white" opacity="0.7"/>'
	# Position du liseré exterieur 
	pos += '<path d="M 100,10 L 10,10 L 10,410 L 610,410 L 610,10 L 180,10" style="fill:none; stroke:grey;"/>'
	# texte du liseré
	pos += '<text id="lisere1" x="110" y="15">My VAF</text>'
	# ligne des abcisses
	pos += '<line x1=' + str(abc1-5) +' y1="330" x2=' + str(abc2+5) + ' y2="330" stroke="grey"/>'
	# ligne de base des ordonnées
	pos += '<line x1='+str(abc1)+' y1='+ str(ord1+5)+' x2='+str(abc1)+' y2='+str(ord2-5)+' stroke="grey"/>'
	pos += '<text x='+str(abc1-10) + ' y='+str(ord1+5) + ' style="text-anchor:end;">0</text>'
	# lignes intermédiaires des ordonnées
	Y = ord1
	for a in val_ord:
		Y -= ea
		pos += '<line x1='+str(abc1-5) + ' y1='+str(Y) + ' x2=' + str(abc2+5) + ' y2='+str(Y) + ' stroke="#B3B3B3"/>'
		pos += '<text x='+str(abc1-10) + ' y='+str(Y+5) + ' style="text-anchor:end; baseline-shift:5;">'+ str(a) +'</text>'
	# Position des barres
	X = abc1
	for a in (texte):
		if X == abc1:									# compter 1/2 décalage pour la première barre 
			X = X + eb / 2
		else:											# sinon on décale de eb (ecart entre barre)
			X = X + eb
		Y2 = ord1 - (ord_t * int(a[4]) / vsup)
		pos += '<line x1='+str(X) + ' y1='+str(ord1)+' x2='+str(X) + ' y2='+ str(Y2) + ' style=" stroke:grey; stroke-width:15 "/>'
		pos += '<text x='+str(X) + ' y=' + str(ord1 + 20) + ' style="text-anchor:middle">' + a[0] + '</text>'
		pos += '<circle cx='+str(X+30)+' cy='+str(Y2)+' r="15" style="fill:white;opacity:0.8;stroke-width:1;stroke:grey"/>'
		pos += '<g fill="grey"><text x='+str(X+30) + ' y=' + str(Y2+6) + ' style="text-anchor:middle" >' + a[4] + '</text></g>' 

	return pos

def affiche_svg1(positions):
	print("""
	<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
	"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
	<svg width="620px" height="420px" xml:lang="fr"
	xmlns="http://www.w3.org/2000/svg"
	xmlns:xlink="http://www.w3.org/1999/xlink">

	<title>My VAF</title>
	{}
	</svg>
	""".format(positions))

def debug(texte):
	print('<br/><h3>--- DEBUG ---</h3>')
	# print(texte)										# Afficher la liste 'texte'
	for i,line in enumerate(texte):						# afficher les éléments des éléments de 'texte'
		for j,field in enumerate(line):
			print("ligne {} - champs {} : {}<br/>".format(i, j, field))


def affiche_env():
	print("<br/><h3>--- VARIABLES D'ENVIRONNEMENT ---</h3>")
	for a,b in os.environ.items():
		print("{} -> {}<br/>".format(a,b))

#####################################################
#####         AFFICHAGE DE LA PAGE 				#####
#####################################################

print("""content-type: text/html\n
<!--#include virtual="/head.html" -->
<!--#include virtual="/header.html" -->
<!--#include virtual="/form1.html" -->
""")

try:										# on essaie d'affficher le contenu du fichier, sinon on passe
	fileitem = form['fichier_csv']
	#print(fileitem)
	print("<h4>{}</h4>".format(fileitem.filename))	# on affiche le nom du fichier
	
	texte = fileitem.file.read()			# on passe dans la variable texte la partie texte
	texte = texte.decode("utf-8")			# passer le contenu au format texte utf-8 (il est au format bytes)
	if file_check_ok(texte):				# Si le controle du format de fichier est OK
		texte = parse_file(texte)				# on analyse on fichier
		positions = calcule_svg1(texte)			# on crée le fichier svg1
		affiche_svg1(positions)					# afficher svg1
		#debug(texte)							# pour debugguer
		#affiche_env()							# affiche les variables d'environnement renvoyée par Apache
	
except:
	pass
	
print("""
<!--#include virtual="/footer.html" -->
""")