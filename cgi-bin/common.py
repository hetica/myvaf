#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import cairosvg

def formulaire(cgi_fic):
	print('<form enctype="multipart/form-data" method="post" action="/cgi-bin/' + cgi_fic + '">')
	print("""
		<!--<label for="image_file">Sélectionner un fichier :</label><br />-->
		<div id="upload-file-container">
			Télécharger
			<input type="file" onChange="this.form.submit()" name="fichier_csv" />
		</div>
		</form>
		<br/>
	""")




def parse_myvaf(texte):
	"""
	découper le fichier en autant de lignes / champs
	input : le fichier
	output : liste [ [ligne1, champs1], [ligne2, champs2], etc. ]
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
	
	tab_text = []											# tab_text = texte avec les champs utiles
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
	# print("<p>"+png_file+"</p>")
	print('<br /><a href="' + png_path + '" download="' + png_file + '" id="upload_file" >Télécharger le graphique<a>' )
