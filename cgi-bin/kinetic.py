#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import os, sys
import cgi
import cgitb; cgitb.enable() 								# Affiche les erreurs dans le browser
import common

form = cgi.FieldStorage()

# variables globales
dash = [ "0", "22,2", "20,2,4,2,4,2,4,2", "4,2", "20,2,4,2"]		# définition des tirets des chemins
color = [ "#D9D9D9", "#8F8F8F", "#808080", "#707070", "#979797" ]	# définition des couleurs des chemins
	
def file_check_ok(texte):
	"""
	Vérifier si la syntaxe du fichier est correcte
	En entrée : le texte à controller
	En sortie : vrai ou faux
	"""
	if texte == "":
		return False
	return True

def calcule_svg1(texte):
	"""
	Crée le fichier svg
	input : liste [ [ligne1, champs1], [ligne2, champs2], etc. ]
	output : String représentant le fichier SVG
	"""
	n_abc = len(texte) -1									# nombre de points d'abcisses
	n_chemins = len(texte[0]) -1							# nombre de chemins (patients)
	################# ICI ON DEFINIT LES POSITIONS MODULABLES DU GRAPHIQUE #####################
	#ecart_abc = 70											# écart entre les points d'abcisses
	#lrg_max = 600											# largeur max des abscisses
	largeur = 550											# largeur du graphique
	hauteur = 460											# hauteur du graphique
	x1 = 0													# position gauche
	y1 = 0													# position haute
	#x2 = x1 + min(160 + ecart_abc * n_abc, lrg_max+150)	# position droite
	x2 = x1 + largeur										# position droite
	y2 = y1 + hauteur										# position basse
	x_mid = (x2-x1)/2 + x1									# position axe vertical du graphique
	y_abc = y1 + hauteur - 100								# position verticale de la barre des abcisses
	x_ord = x1 + 100										# position horizontale de la barre des ordonnées
	
	################# ICI ON DEFINIT LES DIMENSIONS DES PARTIES DU SVG #####################
	#l_abc = min(ecart__abc * n_abc, lrg_max)				# longueur de la barre utile des abcisses
	l_abc = largeur - 150									# longueur de la barre utile des abcisses
	e_abc = l_abc / n_abc 	 								# espaces entre les abcisses des points
	l_ord = hauteur - 150									# longueur de la barre utile des ordonnées
	grad = l_ord / 10										# ecart entre graduation des ordonnées
	ratio = l_ord / 100
	
	################# ICI ON DEFINIT LES POINTS DU SVG #####################
	lis = [ str(x1+10), str(y1+10), str(x2-10), str(y2-10) ] 			# points extremes du liseré
	abc = [ str(x_ord-5), str(y_abc), str(x_ord+l_abc), str(y_abc) ]	# ligne des abcisses
	ords = [ str(x_ord), str(y_abc+5), str(x_ord), str(y_abc-l_ord-5) ]	# ligne des ordonnées
	### Déterminer la position des abcisses
	x_ech = x_ord														# abcisse a un instant T
	pos_abc = []														# liste des abcisses utilisées
	x_text = []															# le texte des abcisses
	nom_path = []														# le nom de chaque path, ou patient
	col = 0																# numéro de colonne, la première colonne vaut 1
	chemins = []														# définit la liste de tous les chemins
	for i in range(n_chemins):											# définit chaque chemin
		chemin = []
		chemins.append(chemin)											# et l'ajoute dans la liste des chemins
	for i,a in enumerate(texte):										# pour chaque ligne du texte
		col +=1	
		line = 0
		for j,b in enumerate(a):										# pour chaque champs de la ligne
			line +=1
			### PREMIERE LIGNE MOINS LA PREMIÈRE COLONNE
			if i == 0 and j != 0:										# pour les champs de la ligne d'entête - 1ere colonne
				nom_path.append(b)										# on récupère le nom du champs (nom du patient)
			### DEUXIÈME LIGNE MOINS LE PREMIER CHAMPS
			if line == 1 and col != 1:									# Sur la première ligne moins le premier champs
				if col == 2:											# si on est sur le deuxième champs
					x_ech += e_abc / 2									# la première abcisse est situé à un demi écart type
					pos_abc.append(x_ech)								# on stocke la valeur dans pos_abc[]
				else:													# pour les autres champs (de la première ligne)
					x_ech += e_abc										# on augmente la valeur de la position
					pos_abc.append(x_ech)								# et on stocke la valeur dans pos_abc[]
				x_text.append(b) 										# on stocke le contenu des en-tete dans x_text[]
			### TOUTES LES AUTRES LIGNES
			else:														# pour les autres lignes
				for k in range(1,n_chemins+1):							# pour les indices 1 à "chemin" 
					if col != 1 and line == k+1:						# on évite la première colonne et on limite au chemin en question
						chemins[k-1].append(float(a[k]))				# on ajoute dans la ligne[indice k-1]
				
	for i, chemin in enumerate(chemins):								# transformer les valeurs en positions d'ordonnées
		for j,val in enumerate(chemin):
			chemins[i][j] = str(y_abc - ratio * val)

	
	################# ICI ON COMMENCE LA DEFINITION DU SVG #####################
	svg = '<svg width="'+str(x2)+'px" height="'+str(y2)+'px" xml:lang="fr" '
	svg += 'xmlns="http://www.w3.org/2000/svg" '
	svg += 'xmlns:xlink="http://www.w3.org/1999/xlink">'
	svg += '<title>Kinetic</title>'

	# Cadre exterieur (en fonction de la définition de l'écran, avec un max et min)
	svg += '<rect x="'+str(x1)+'" y="'+str(y1)+'" width="'+str(x2)+'" height="'+str(y2)+'" fill="white" />'
	# liseré et son texte
	svg += '<path d="M '+str(x_mid-len(texte[0][0])*6)+','+lis[1]+' L '+lis[0]+','+lis[1]+' L '+lis[0]+','+lis[3]+' L '+lis[2]+','+lis[3]+' L '+lis[2]+','+lis[1]+' L '+str(x_mid+len(texte[0][0])*6)+','+lis[1]+'" style="fill:none; stroke:grey;"/>'
	#svg += '<text id="lisere" x="'+str(x_mid)+'" y="'+lis[1]+'" dominant-baseline="middle" text-anchor="middle">' + texte[0][0] + '</text>'
	svg += '<text id="lisere" x="'+str(x_mid)+'" y="'+str(y1+15)+'" text-anchor="middle">' + texte[0][0] + '</text>'
	# ligne des abcisses
	svg += '<line x1="'+abc[0]+'" y1="'+abc[1]+'" x2="'+abc[2]+'" y2="'+abc[3]+'" stroke="grey"/>'
	# ligne de base des ordonnées
	svg += '<line x1="'+ords[0]+'" y1="'+ords[1]+'" x2="'+ords[2]+'" y2="'+ords[3]+'" stroke="grey"/>'
	svg += '<text x="'+str(x_ord-10) + '" y="'+str(y_abc) + '" style="text-anchor:end;dominant-baseline:middle">0 %</text>'
	# lignes intermédiaires des ordonnées
	y_ech = y_abc
	for a in range(10,101,10):
		y_ech -= grad 
		svg += '<line x1="'+abc[0]+ '" y1="'+str(y_ech) + '" x2="' +abc[2]+ '" y2="'+str(y_ech) + '" stroke="#E8E8E8"/>'
		svg += '<text x="'+str(x_ord-10) + '" y="'+str(y_ech) + '" style="text-anchor:end; dominant-baseline:middle;">'+ str(a) +' %</text>'
	# Position des abcisses
	for i, a in enumerate(pos_abc):
		svg += '<line x1="'+str(a) + '" y1="'+ords[1]+'" x2="'+str(a) + '" y2="'+ ords[3] + '" style=" stroke:#D9D9D9"/>'
		# Le texte des abscisses
		y_text = str(y_abc + 16)		# position verticale du texte
		svg += '<text x="'+str(a+4)+'" y="'+y_text+'"  style="text-anchor:end" transform="rotate(-45,'+str(a)+','+y_text+')">'+x_text[i]+'</text>'
	# les positions des chemins
	for i, chemin in enumerate(chemins):								# Pour chaque chemin
		svg += '<path id="'+nom_path[i]+'" onclick="enforce_path(evt); return false" d="M '
		for j,val in enumerate(chemin):									# pour chaque position
			if j != 0:
				svg += ' L '
			svg += str(pos_abc[j])+','+val + ' '
		svg += '" stroke="'+color[i]+'" fill="none" stroke-width="4" stroke-dasharray="'+dash[i]+'" cursor="pointer" >'
		#svg += '<set attributeName="stroke-width" to="4" />'
		svg += '</path>'
	
	################# ICI ON TERMINE LA DEFINITION DU SVG #####################
	svg += '</svg>'									# la fin du fichier SVG
	return svg										# il ne reste plus qu'à retourner le fichier

def cartouche(texte):
	"""
	Le cartouche pour les graphiques
	Il est séparé, car un seul cartouche pour plusieurs graphique
	"""
	#print(texte)
	nb_chemins = 0										# nombre de chemins
	mark = ""											# le marqueur (chemin 1, grisé pâle)
	hrm = ""											# High Risk Mutation (les autres chemins, ex : TP53-CCF)
	xy = (0,0,300,160)									# rectangle exterieur
	lis = (xy[0]+10, xy[1]+10, xy[2]-20, xy[3]-20)	 	# points du liseré
	width = xy[2] - xy[0]								# largeur du graphique
	height = xy[3] - xy[1]								# hauteur du graphique
	texte = texte.split("\n")							# découper le texte en lignes
	for i,line in enumerate(texte):
		# Analyser la première ligne uniquement
		if i == 0:
			line = line.split(";")
			mark = line[1].split(")")[0]+")"			# marqueur (chemin 1, grisé pâle) (ex: del(5q))
			hrm = line[2].split(" ")[0]+"-CCF"			# high risk (les autres chemins) (ex: TP53-CCF)
			for field in line:							# nombre de chemins
				if "-CCF" in field:
					nb_chemins += 1				
	#print(nb_chemins, " - " , mark, " - ", hrm) 
	x_texte = xy[0] + 20								# début du texte
	x_dash = max(len(mark), len(hrm)) * 15 				# début des tirets
	xe_dash = xy[2]-50									# fin des tirets
	y_mark = xy[3] - ( 2 * height / 3 ) - 5				# ordonnée pour le marqueur mark
	y_hrm = xy[3] - ( height / 3 )	- 20				# ordonnée pour le texte du hrm
	ec_hrm = ( xy[3] - y_hrm ) / 3						# écart entre les traits d'hrm
	
	
	################# ICI ON COMMENCE LA DEFINITION DU CARTOUCHE #####################
	svg = '<svg width="'+str(width)+'px" height="'+str(height)+'px" xml:lang="fr" '
	svg += 'xmlns="http://www.w3.org/2000/svg" '
	svg += 'xmlns:xlink="http://www.w3.org/1999/xlink">'
	svg += '<title>Kinetic</title>'
	# Cadre exterieur (en fonction de la définition de l'écran, avec un max et min)
	svg += '<rect x="'+str(xy[0])+'" y="'+str(xy[1])+'" width="'+str(xy[2])+'" height="'+str(xy[3])+'" fill="white" />'
	# Liseré
	svg += '<rect x="'+str(lis[0])+'" y="'+str(lis[1])+'" width="'+str(lis[2])+'" height="'+str(lis[3])+'" fill="transparent" stroke="grey" />'
	# texte du marqueur	mark
	svg += '<text x="'+str(x_texte) + '" y="'+str(y_mark) + '" >'+ mark +'</text>'
	# texte du hrm (High Risk Mutation)
	svg += '<text x="'+str(x_texte) + '" y="'+str(y_hrm) + '" >'+ hrm +'</text>'
	# trait du marqueur mark
	svg += '<line x1="'+str(x_dash)+'" y1="'+str(y_mark-4)+'" x2="'+str(xe_dash)+'" y2="'+str(y_mark-4)+'"'
	svg += ' stroke="'+color[0]+'" stroke-width="3" stroke-dasharray="'+dash[0]+'" />'
	# traits des hrm
	y = y_hrm -5
	for a in range(1, nb_chemins+1):
		svg += '<line x1="'+str(x_dash)+'" y1="'+str(y)+'" x2="'+str(xe_dash)+'" y2="'+str(y)+'"'
		svg += ' stroke="'+color[a]+'" stroke-width="3" stroke-dasharray="'+dash[a]+'" />'
		y += ec_hrm

	################# ICI ON TERMINE LA DEFINITION DU CARTOUCHE #####################
	svg += '</svg>'									# la fin du fichier SVG
	return svg

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
	sous forme de graphique d'évolution clonale.
</p>
<p>
	Un fichier d'exemple est téléchargeable : <a href="/static/sample-kinetic.csv" download="sample-kinetic.csv" id="upload_file" >sample-kinetic.csv</a>
</p>
<br />
""")

common.formulaire("kinetic.py")

if os.environ['REQUEST_METHOD'] == 'POST':			# si la méthode est 'POST'
	fileitem = form['fichier_csv']
	# définit le nom du fichier sans son extension	
	fichier = fileitem.filename
	for i,a in enumerate(fichier):
		if a == ".": ind = i
	fichier = fichier[:ind]
	# définit le nom et emplacement du graphique png
	png_path = "../graphics/" + fichier + ".png"
	png_file = fichier + ".png"
	# définit le nom et emplacement du cartouche
	cart_path = "../graphics/cartouche.png"
	cart_file = "cartouche.png"
	
	# définit le nom et emplacement du graphique svg
	#svg_path = "../graphics/" + fichier + ".svg"
	#svg_file = fichier + ".svg"	
	print("<h4>{}</h4>".format(fileitem.filename))	# on affiche le nom du fichier

	btexte = fileitem.file.read()					# on passe dans la variable texte la partie texte
	texte = common.file_format(btexte)				# mettre le fichier en unicode(il est au format byte)
	if file_check_ok(texte):						# Si le controle du format de fichier est OK
		cart_svg = cartouche(texte)					# crée le  cartouche
		texte = common.parse_kinetic(texte)			# on analyse le fichier
		svg = calcule_svg1(texte)					# on crée le fichier svg1
		print(svg)									# AFFICHER LE SVG
		common.build_png_file(svg, png_path)		# créer un fichier PNG
		common.upload_png(png_path, png_file)		# créer le lien de téléchargement de ce PNG
		print(cart_svg)								# on affiche le cartouche
		common.build_png_file(cart_svg, cart_path)	# créer un fichier PNG
		common.upload_png(cart_path, cart_file)		# créer le lien de téléchargement de ce PNG
		#debug(texte)								# pour debugguer

		
print("""
</article>
</section>
<!--#include virtual="/footer.html" -->
""")
