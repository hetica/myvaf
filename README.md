
####Travaux pratiques dans le cadre du cours Systèmes et réseaux

**Pour tester** : 

* télécharger un des fichiers **sample*.txt** dans le répertoire [other](https://github.com/hetica/myvaf/tree/master/other)
* puis aller sur : <http://jebimoh.fr>


# MyVAF (Variant Allele Frequency)

## Description
L'objectif est de fournir aux biologistes moléculaire un graphique du nombre des variants obtenus pour un échantillon.
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

* Les fichiers **sample*.txt** sont des fichiers d'exemple à télécharger pour test
* Le fichier **jebimoh.conf** contient la configuration d'Apache2


## Prérequis pour le serveur

* python3 avec les modules : 
	* cgi
	* cgitb
	* cairosvg

