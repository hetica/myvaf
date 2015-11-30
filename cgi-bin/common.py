


def formulaire(cgi_fic):
	print('<form id="upload_form" enctype="multipart/form-data" method="post" action="/cgi-bin/' + cgi_fic + '">')
	print("""
		<label for="image_file">Sélectionner un fichier</label><br />
		<input type="file" name="fichier_csv" id="fichier_csv" onchange="fileSelected();"/>
		<p>
			<input type="submit" name="Submit" value="Télécharger" />
		</p>
	</form>
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
	for i,champs in enumerate(texte[0]):					# déterminer les champs utiles
		if "-CCF" in champs or i == 0:
			items.append(i)
	
	tab_text = []											# tab_text = texte avec les champs utiles
	for i, ligne in enumerate(texte):
		l = []
		for j, champs in enumerate(ligne):
			 if j in items:
				 l.append(champs)
		tab_text.append(l)

	return tab_text
