#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

"""
Liens :
	http://webpython.codepoint.net/cgi_file_upload
	//// la réponse faites est très intérressante (WSGIScriptAlias)
	http://stackoverflow.com/questions/882430/how-to-hide-cgi-bin-py-etc-from-my-urls
"""

import os, sys
import cgi
import cgitb; cgitb.enable() 								# Affiche les erreurs dans le browser
import cairosvg												# pour générer un graphique au format png
import common

form = cgi.FieldStorage()

def file_format(texte):										# mettre en unicode
	try:
		t = texte.decode("utf-8")
	except:
		t = texte.decode("ISO-8859-1")
	return t

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
	################# ICI DEFINIT LES POINTS DU SVG #####################
	# les abcisses
	abc1 = 100 ; abc2 = 560									# longueur utile de la barre des abcisses
	abc_t = abc2 - abc1										# longueur utile pour les abcisses
	eb = (abc2-abc1) / len(texte) 							# espace entre chaque barre (1/2 espace au début et à la fin)
	# les ordonnées
	ord1 = 330 ; ord2 = 60									# ord1 : base ; ord2 : hauteur max
	ord_t = ord1 - ord2										# longueur utile pour les ordonnées
	# plus_grand : plus grande valeur de variant
	plus_grand = max([ int(v) for w,x,y,z,v in texte])		# plus_grande valeur trouvée (pour le calcul des traits d'ordonnées)
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
	
	################# ICI ON COMMENCE LA DEFINITION DU SVG #####################
	svg = '<?xml version="1.0" encoding="utf-8"?> '
	svg += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" '
	svg += '"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"> '
	svg += '<svg width="620px" height="420px" xml:lang="fr" '
	svg += 'xmlns="http://www.w3.org/2000/svg" '
	svg += 'xmlns:xlink="http://www.w3.org/1999/xlink">'
	svg += '<title>My VAF</title>'
	
	
	# Cadre exterieur (en fonction de la définition de l'écran, avec un max et min)
	svg += '<rect x="0" y="0" width="620" height="420" fill="white"/>'
	# Position du liseré exterieur 
	svg += '<path d="M 150,10 L 10,10 L 10,410 L 610,410 L 610,10 L 250,10" style="fill:none; stroke:grey;"/>'
	# texte du liseré
	svg += '<text id="lisere1" x="160" y="15">' + fichier + '</text>'
	# ligne des abcisses
	svg += '<line x1="' + str(abc1-5) +'" y1="330" x2="' + str(abc2+5) + '" y2="330" stroke="grey"/>'
	# ligne de base des ordonnées
	svg += '<line x1="'+str(abc1)+'" y1="'+ str(ord1+5)+'" x2="'+str(abc1)+'" y2="'+str(ord2-5)+'" stroke="grey"/>'
	svg += '<text x="'+str(abc1-10) + '" y="'+str(ord1+5) + '" style="text-anchor:end;">0 %</text>'
	# lignes intermédiaires des ordonnées
	Y = ord1
	for a in val_ord:
		Y -= ea
		svg += '<line x1="'+str(abc1-5) + '" y1="'+str(Y) + '" x2="' + str(abc2+5) + '" y2="'+str(Y) + '" stroke="#B3B3B3"/>'
		svg += '<text x="'+str(abc1-10) + '" y="'+str(Y+5) + '" style="text-anchor:end; baseline-shift:5;">'+ str(a) +' %</text>'
	# Position des barres
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
		svg += '<ellipse cx="'+str(X+23)+'" cy="'+str(Y2-15)+'" rx="'+str(len(a[3])*8)+'" ry="14" style="fill:white; stroke-width:1; stroke:transparent"/>'
		#svg += '<set attributeName="fill" to="white" begin="2" />'
		#svg += '<set attributeName="stroke" to="grey" begin="2" /></ellipse>'
		svg += '<text x="'+str(X+23) + '" y="' + str(Y2-15) + '" style="text-anchor:middle; fill:grey; dominant-baseline:middle">' + a[3]
		svg += '</text>'
		#svg += '<set attributeName="fill" to="grey" begin="2" /></text>'

	################# ICI ON TERMINE LA DEFINITION DU SVG #####################
	svg += '</svg>'									# la fin du fichier SVG
	return svg										# il ne reste plus qu'à retourner le fichier

def build_png_file(svg, png):
	"""
	Crée un fichier png pour le téléchargement
	"""	
	#png = cairosvg.svg2png(bytestring = svg)
	cairosvg.svg2png(bytestring=bytes(svg,'UTF-8'), write_to = png)

def upload_png(png):
	"""
	Affiche le lien de téléchargement du fichier png
	"""
	# print("<p>"+png_file+"</p>")
	print('<br /><a href="' + png + '" download="' + png_file + '" id="upload_file" >Télécharger le graphique<a>' )


def build_svg_file(svgContent, svgFile):
	"""
	Crée un fichier svg pour le téléchargement
	"""
	with open(svgFile, 'w') as f:
		f.write(svg)

def upload_svg(svg):
	"""
	Affiche le lien de téléchargement du fichier svg
	"""
	# print("<p>"+png_file+"</p>")
	print('<br /><a href="' + svg + '" download="' + svg_file + '" id="upload_file" >Télécharger le graphique<a>' )


def debug(texte):
	"""
	Pour le debug
	"""
	print('<br/><h3>--- DEBUG ---</h3>')
	# print(texte)										# Afficher la liste 'texte'
	for i,line in enumerate(texte):						# afficher les éléments des éléments de 'texte'
		for j,field in enumerate(line):
			print("ligne {} - champs {} : {}<br/>".format(i, j, field))


def affiche_env():
	"""
	Affiche les variables renvoyées par Apache
	"""
	print("<br/><h3>--- VARIABLES D'ENVIRONNEMENT ---</h3>")
	for a,b in os.environ.items():
		print("{} -> {}<br/>".format(a,b))

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
<h1>MyVAF</h1>
<p>
	Affiche un graphique de la fréquence des allèles variants pour un échantilon.<br/>
	Un fichier d'exemple est téléchargeable : <a href="/static/sample-myvaf.txt" download="sample-myvaf.txt" id="upload_file" >sample-myvaf.txt</a>
</p>
<br />
""")

common.formulaire("index.py")

#formulaire()

if os.environ['REQUEST_METHOD'] == 'POST':		# si la méthode est 'POST'
		
	fileitem = form['fichier_csv']

	# définit le nom du fichier sans son extension	
	fichier = fileitem.filename
	for i,a in enumerate(fichier):
		if a == ".": ind = i
	fichier = fichier[:ind]
	# définit le nom et emplacement du graphique png
	png_path = "../graphics/" + fichier + ".png"
	png_file = fichier + ".png"
	# définit le nom et emplacement du graphique svg
	svg_path = "../graphics/" + fichier + ".svg"
	svg_file = fichier + ".svg"	
	print("<h4>{}</h4>".format(fileitem.filename))	# on affiche le nom du fichier
		
	texte = fileitem.file.read()				# on passe dans la variable texte la partie texte
	texte = file_format(texte)					# mettre le fichier en unicode
	if file_check_ok(texte):					# Si le controle du format de fichier est OK
		texte = common.parse_myvaf(texte)		# on analyse on fichier
		svg = calcule_svg1(texte)				# on crée le fichier svg1
		print(svg)								# AFFICHER LE SVG
		common.build_png_file(svg, png_path)	# créer un fichier PNG (pas au point)
		common.upload_png(png_path, png_file)	# créer le lien de téléchargement de ce PNG
		#build_svg_file(svg, svg_path)			# créer un fichier SVG
		#upload_svg(svg_path)					# créer le lien de téléchargement de ce SVG
		#debug(texte)							# pour debugguer
		#affiche_env()							# affiche les variables d'environnement renvoyées par Apache
		
	
print("""
</article>
</section>
<!--#include virtual="/footer.html" -->
""")
