
####Travaux pratiques dans le cadre du cours Système.

**Pour tester** : 

* Se rendre sur : <http://jebimoh.fr>

* télécharger le fichier d'exemple fourni en lien (sample.txt)

# Jebimoh 

#### Myvaf (Variant Allele Frequency)

Fournit un graphique du pourcentage de variants obtenus pour un échantillon.
Le fichier doit être formaté de la manière suivante :

	Gene	Variant_sur_Génome_g.	Variant_sur_CDS_c.	Variant_sur_protéine_p_c.	VAF_%
	
**Nota** : le séparateur de champs est une tabulation (et une seule).

#### Kinetic

Cinetique de l'évolution clonale pour un ou plusieurs patients
Le fichier doit être formaté de la manière suivante :

	UPN-23;del(5q) %;TP53 p.R282W VAF %;R282W-CCF;TP53 p.R248Q VAF %;R248Q-CCF;TP53 p.R273C VAF %;R273C-CCF

- Un champs d'entête contenant le motif "-CCF" correspond à un patient

- Une ligne correspond à une date

**Nota** : le séparateur de champs est le ";" (point virgule).

### Les objectifs

* Utiliser python (ok)

* Utiliser CGI (ok)

* Créer un formulaire (ok)

* Créer un élément graphique SVG (ok)

* Utiliser Javascript (ok)

En supléments aux fichier du site, il y a le répertoire **other** :

* Les fichiers **sample*.txt** sont d'autre fichiers d'exemple à télécharger pour tester

* Le fichier **jebimoh.conf** contient la configuration d'Apache2


### Prérequis pour le serveur

* python3 avec les modules : 
	* cgi
	* cgitb					(pour le debugage)
	* python3-markdown (pour lire les fichiers markdown)
	* python3-cairosvg (pour transformer des SVG en PNG)

