#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import os, sys
import cgi
import cgitb; cgitb.enable() 								# Affiche les erreurs dans le browser
import common

form = cgi.FieldStorage()

def file_check_ok(texte):
	"""
	Vérifier si la syntaxe du fichier est correcte
	En entrée : le texte à controller
	En sortie : vrai ou faux
	"""
	if texte == "":
		return False
	return True

def formulaire():
	print("""
	<form id="upload_form" enctype="multipart/form-data" method="post" action="/cgi-bin/index.py">
		<label for="image_file">Sélectionner un fichier</label><br />
		<input type="file" name="fichier_csv" id="fichier_csv" onchange="fileSelected();"/>
		<p>
			<input type="submit" name="Submit" value="Télécharger" />
		</p>
	</form>
	""")

def calcule_svg1(texte):
	"""
	Crée le fichier svg
	input : liste [ [ligne1, champs1], [ligne2, champs2], etc. ]
	output : String représentant le fichier SVG
	"""
	n_abc = len(texte) -1										# nombre de points d'abcisses
	################# ICI ON DEFINIT LES POSITIONS MODULABLES DU GRAPHIQUE #####################
	#ecart_abc = 70											# écart entre les points d'abcisses
	#lrg_max = 600											# largeur max des abscisses
	largeur = 550											# largeur du graphique
	hauteur = 440											# hauteur du graphique
	x1 = 0													# position gauche
	y1 = 0													# position haute
	#x2 = x1 + min(160 + ecart_abc * n_abc, lrg_max+150)	# position droite
	x2 = x1 + largeur										# position droite
	y2 = y1 + hauteur										# position basse
	x_mid = (x2-x1)/2 + x1									# position axe vertical du graphique
	y_abc = y1 + hauteur - 90								# position verticale de la barre des abcisses
	x_ord = x1 + 100										# position horizontale de la barre des ordonnées
	
	################# ICI ON DEFINIT LES DIMENSIONS DES PARTIES DU SVG #####################
	#l_abc = min(ecart__abc * n_abc, lrg_max)				# longueur de la barre utile des abcisses
	l_abc = largeur - 150									# longueur de la barre utile des abcisses
	e_abc = l_abc / n_abc 	 								# espaces entre les abcisses des points
	l_ord = hauteur - 140									# longueur de la barre utile des ordonnées
	grad = l_ord / 10										# ecart entre graduation des ordonnées
	
	################# ICI ON DEFINIT LES POINTS DU SVG #####################
	lis = [ str(x1+10), str(y1+10), str(x2-10), str(y2-10) ] 			# points extremes du liseré
	abc = [ str(x_ord-5), str(y_abc), str(x_ord+l_abc), str(y_abc) ]	# ligne des abcisses
	ords = [ str(x_ord), str(y_abc+5), str(x_ord), str(y_abc-l_ord-5) ]	# ligne des ordonnées
	### Déterminer la position des abcisses
	x_ech = x_ord
	pos_abc = []
	col = 0
	for i,a in enumerate(texte):
		col +=1
		line = 0
		for j,b in enumerate(a):
			line +=1
			if j == 0 and col != 1:
				if col == 2:
					x_ech += e_abc / 2
					pos_abc.append(x_ech)
				else:
					x_ech += e_abc
					pos_abc.append(x_ech)
	
	################# ICI ON COMMENCE LA DEFINITION DU SVG #####################
	svg = '<?xml version="1.0" encoding="utf-8"?> '
	svg += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" '
	svg += '"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"> '
	svg += '<svg width="'+str(x2)+'px" height="'+str(y2)+'px" xml:lang="fr" '
	svg += 'xmlns="http://www.w3.org/2000/svg" '
	svg += 'xmlns:xlink="http://www.w3.org/1999/xlink">'
	svg += '<title>Kinetic</title>'

	# Cadre exterieur (en fonction de la définition de l'écran, avec un max et min)
	svg += '<rect x="'+str(x1)+'" y="'+str(y1)+'" width="'+str(x2)+'" height="'+str(y2)+'" fill="white" opacity="0.7"/>'
	# liseré et son texte
	svg += '<path d="M '+str(x_mid-len(texte[0][0])*6)+','+lis[1]+' L '+lis[0]+','+lis[1]+' L '+lis[0]+','+lis[3]+' L '+lis[2]+','+lis[3]+' L '+lis[2]+','+lis[1]+' L '+str(x_mid+len(texte[0][0])*6)+','+lis[1]+'" style="fill:none; stroke:grey;"/>'
	svg += '<text id="lisere" x="'+str(x_mid)+'" y="'+lis[1]+'" dominant-baseline="middle" text-anchor="middle">' + texte[0][0] + '</text>'
	# ligne des abcisses
	svg += '<line x1="'+abc[0]+'" y1="'+abc[1]+'" x2="'+abc[2]+'" y2="'+abc[3]+'" stroke="grey"/>'
	# ligne de base des ordonnées
	svg += '<line x1="'+ords[0]+'" y1="'+ords[1]+'" x2="'+ords[2]+'" y2="'+ords[3]+'" stroke="grey"/>'
	svg += '<text x="'+str(x_ord-10) + '" y="'+str(y_abc) + '" style="text-anchor:end;dominant-baseline:middle">0</text>'
	# lignes intermédiaires des ordonnées
	y_ech = y_abc
	for a in range(10,101,10):
		y_ech -= grad 
		svg += '<line x1="'+abc[0]+ '" y1="'+str(y_ech) + '" x2="' +abc[2]+ '" y2="'+str(y_ech) + '" stroke="#D9D9D9"/>'
		svg += '<text x="'+str(x_ord-10) + '" y="'+str(y_ech) + '" style="text-anchor:end; dominant-baseline:middle;">'+ str(a) +'</text>'
	# Position des abcisses
	for a in pos_abc:
		svg += '<line x1="'+str(a) + '" y1="'+ords[1]+'" x2="'+str(a) + '" y2="'+ ords[3] + '" style=" stroke:#D9D9D9"/>'
		#print("<br/>pos a : ", a)
	#print(pos_abc)
	#print("ecart entre abcsisses : " , e_abc)
	#print(col)	
	#print(line)
	#print(texte[col-1][line-1])
	
	"""
	X = abc1
	for a in (texte):
		if X == abc1:									# compter 1/2 décalage pour la première barre 
			X = X + eb / 2
		else:											# sinon on décale de eb (ecart entre barre)
			X = X + eb
		Y2 = ord1 - (ord_t * int(a[4]) / vsup)
		svg += '<line x1="'+str(X) + '" y1="'+str(ord1)+'" x2="'+str(X) + '" y2="'+ str(Y2) + '" style=" stroke:grey; stroke-width:15 ">'
		svg += '<animate attributeName="y2" from="'+str(ord1)+'" to="'+str(Y2)+ '" begin="0s" dur="2s" />'
		svg += '</line>'
		svg += '<text x="'+str(X) + '" y="' + str(ord1 + 20) + '" style="text-anchor:middle">' + a[0] + '</text>'
		#svg += '<ellipse cx="'+str(X+36)+'" cy="'+str(Y2-12)+'" rx="32" ry="17" style="fill:white; opacity:0.8; stroke-width:1; stroke:grey"/>'
		#svg += '<set attributeName="fill" to="white" begin="2" />'
		#svg += '<set attributeName="stroke" to="grey" begin="2" /></ellipse>'
		svg += '<text x="'+str(X+36) + '" y="' + str(Y2-6) + '" style="text-anchor:middle" fill="grey">' + a[3]
		svg += '</text>'
		#svg += '<set attributeName="fill" to="grey" begin="2" /></text>'
	"""
	################# ICI ON TERMINE LA DEFINITION DU SVG #####################
	svg += '</svg>'									# la fin du fichier SVG
	return svg										# il ne reste plus qu'à retourner le fichier

def debug(texte):
	"""
	Pour le debug
	"""
	print('<br/><h3>--- DEBUG ---</h3>')

	# print(texte)										# Afficher la liste 'texte'
	for i,line in enumerate(texte):						# afficher les éléments des éléments de 'texte'
		for j,field in enumerate(line):
			print("ligne {} - champs {} : {}<br/>".format(i, j, field))

#####################################################
#####         AFFICHAGE DE LA PAGE 				#####
#####################################################

print("""content-type: text/html\n
<!--#include virtual="/head.html" -->
<!--#include virtual="/header.html" -->
""")

print("""
<section>
<article>
<h1>Kinetic</h1>
<p>
	Représente des fréquences alléliques variantes détectées  par patient, dans plusieurs échantillons séquentiels,
	sous forme de graphique d'évolution clonale.<br/> 
	Un fichier d'exemple est téléchargeable : <a href="/static/sample_kinetic.csv" download="kinetic.csv" id="upload_file" >sample.txt</a>
</p>
<br />
""")

common.formulaire("kinetic.py")

if os.environ['REQUEST_METHOD'] == 'POST':			# si la méthode est 'POST'
	fileitem = form['fichier_csv']
	# définie le nom du fichier sans son extension	
	fichier = fileitem.filename
	for i,a in enumerate(fichier):
		if a == ".": ind = i
	fichier = fichier[:ind]
	# définit le nom et emplacement du graphique png
	png_path = "../graphics/" + fichier + ".png"
	png_file = fichier + ".png"
	# définie le nom et emplacement du graphique png
	svg_path = "../graphics/" + fichier + ".svg"
	svg_file = fichier + ".svg"	
	print("<h4>{}</h4>".format(fileitem.filename))	# on affiche le nom du fichier

	texte = fileitem.file.read()					# on passe dans la variable texte la partie texte
	texte = texte.decode("utf-8")					# passer le contenu au format texte utf-8 (il est au format bytes)
	if file_check_ok(texte):						# Si le controle du format de fichier est OK
		texte = common.parse_kinetic(texte)			# on analyse le fichier
		svg = calcule_svg1(texte)					# on crée le fichier svg1
		print(svg)									# AFFICHER LE SVG
		
		debug(texte)								# pour debugguer

		
print("""
</article>
</section>
<!--#include virtual="/footer.html" -->
""")
