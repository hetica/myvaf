
####Travaux pratiques dans le cadre du cours Système.

**Pour tester** : 

* Se rendre sur : <http://jebimoh.fr>
* télécharger le fichier d'exemple fourni en lien (sample.txt)

# MyVAF (Variant Allele Frequency)

## Description
L'objectif est de fournir aux biologistes moléculaires un graphique du pourcentage de variants obtenus pour un échantillon.
Le biologiste utilise un fichier formaté ainsi :

	Gene	Variant_sur_Génome_g.	Variant_sur_CDS_c.	Variant_sur_protéine_p_c.	VAF_%
	
**Nota** : le séparateur de champs est une tabulation (et une seule).

## Objectifs
* Utiliser python
* Utiliser CGI
* Créer un formulaire
* Créer un élément graphique SVG
* Utiliser Javascript

En supléments aux fichier du site, il y a le répertoire **other** :

* Les fichiers **sample*.txt** sont d'autre fichiers d'exemple à télécharger pour tester
* Le fichier **jebimoh.conf** contient la configuration d'Apache2


## Prérequis pour le serveur

* python3 avec les modules : 
	* cgi
	* cgitb
	* cairosvg

