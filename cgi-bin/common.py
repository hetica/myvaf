#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import cairosvg


def formulaire(cgi_fic):
	print('<form enctype="multipart/form-data" onsubmit="test()" method="post" action="/cgi-bin/' + cgi_fic + '">')
	print("""
		<div id="upload-file-container">
			Télécharger
			<!--<input type="file" onChange="this.form.submit()" name="fichier_csv" />-->
			<input type="file" onChange="checkFile(this.form, this.form.fichier_csv.value)" name="fichier_csv" />
		</div>
		</form>
		<br/>
	""")

def file_format(texte):
	# MET EN UNICODE
	try:
		t = texte.decode("utf-8")							# Pour téléchargement depuis Linux
	except:
		t = texte.decode("ISO-8859-1")						# Pour téléchargement depuis Windows
	# REMPLACE LES VIRGULES PAR DES POINTS
	t = t.replace(",", ".")									# remplace les virgules par des points  (float)
	return t

def parse_myvaf(texte):
	"""
	découpe le fichier en autant de lignes / champs
	input : le fichier
	output : liste [ [champs1, champs2], [champs1, champs2], etc. ]
	"""
	
	texte = texte.split("\n")								# Sépare la chaine en liste de lignes

	if "Gene" or "gene" in texte[0]:						# supprime la ligne d'entete si nécessaire
		del texte[0]
	for i,line in enumerate(texte):							# supprime les lignes non conformes
		if not "\t" in line:
			del texte[i]
		try:
			if line == '': del texte[i]
		except:
			pass
	for i,line in enumerate(texte):							# sépare les lignes en champs 
		texte[i] = line.split("\t")
		
	return texte

def parse_kinetic(texte):
	"""
	découper le fichier en autant de lignes / champs
	input : le fichier
	output : liste [ [ligne1, champs1], [ligne2, champs2], etc. ]
	"""
	
	texte = texte.split("\n")								# Sépare la chaine en liste de lignes

	for i,line in enumerate(texte):							# supprime les lignes non conformes
		if not ";" in line:
			del texte[i]

	for i,line in enumerate(texte):							# sépare les lignes en champs 
		texte[i] = line.split(";")
	
	items = []
	for i,champs in enumerate(texte[0]):					# détermine les champs utiles
		if i == 1:
			items.append(i)
		if "-CCF" in champs or i == 0:						# Les champs utiles doivent contenir "-CCF"
			items.append(i)
	
	tab_text = []											# tab_text = tous les champs utiles sont récupérés
	for i, ligne in enumerate(texte):
		l = []
		for j, champs in enumerate(ligne):
			 if j in items:
				 l.append(champs)
		tab_text.append(l)
	
	return tab_text


def build_png_file(svg, png):
	"""
	Crée un fichier png pour le téléchargement
	"""	
	#png = cairosvg.svg2png(bytestring = svg)
	cairosvg.svg2png(bytestring=bytes(svg,'UTF-8'), write_to = png)

def upload_png(png_path, png_file):
	"""
	Affiche le lien de téléchargement du fichier png
	"""
	if png_file == "cartouche.png":
		name = "cartouche"
	else:
		name = "graphique"
		
	print('<p><a href="' + png_path + '" download="' + png_file + '" id="upload_file" >Télécharger le '+name+'</a></p>' )
