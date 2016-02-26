Validation spot thema 2016
=
> **Remarque :** les concepts techniques utilisés dans cette note proviennent des outils esri. Cela se justifie par le fait que c'est l'outil qui est utilisé pour effectuer la réception et la mise en oeuvre de la base. Néanmoins ils sont suffisamment génériques pour trouver leur correspondance dans n'importe quel environnement SIG.

Structuration
-
###classes millésime

Chaque classe millésime contient les champs suivants:

> **Note :** YY pour millésime sur deux chiffres. Ex: 05

- ST_YY: indice de classe niveau 2
  - entier court
  - pas de valeur nulle possible
  
- ST5_YY: indice de classe niveau 3
  - entier court
  - valeur nulle possible (<Null>: non-zero) hors couverture niveau 3
  
- depcom_16: code communal
  - texte 5 caractères
  - pas de valeur nulle possible

###classe overlay

Il n'y a qu'une classe overlay qui contient toutes les années. Elle contient les champs suivants

- ST_YY par millésime (ST00, ST05, ST10, ST15): indices de classe niveau 2
  - entier court
  - valeur nulle possible si la zome n'est pas couverte par le millésime
  
- ST5_YY par millésime (ST5_00, ST5_05, ST5_10, ST5_15): indices de classe niveau 3
  - entier court 
  - valeur nulle possible si la zone n'est pas couverte au niveau 3 par le millésime
  
- depcom_16:
  - texte 5 caractères
  - pas de valeur nulle possible

Topologie
-
###méthode de vérification

La topologie sera vérifiée grâce à l'outil topologie d'arcgis. Elle sera validée lorsqu'aucune erreur ne sera constatée dans chaune des règles énoncées ci-dessous en dehors des exception légitimes.

###règles générales

- exlusivement des polygones non nuls
- pas de polygones multiples
- pas d'auto-intersection
- tolérance à 0.001 m
- projection Lambert93 (epsg:2154)
- ni lacune ni superposition: valable pour toutes les classes
- les limites extérieures de la couverture sont communales (bdtopo 2016)

###règles particulières aux millésimes

la taille minimale de l'objet est définie par l'UMET spécifiée dans les dernières spécification de niveau 3 publiées par Spot en 2005 (https://github.com/urba4/spot/blob/master/doc/Spec_ThemaST5_V1-3.pdf).

Qualité alphanumérique
-
> **Note :** le contrôle de la qualité alphanumérique restera forcément partiel et ne pourra s'améliorer qu'avec le temps et l'usage de la donnée qui permettra d'identifier progressivement les erreurs les plus gênantes. Cependant l'expérience ainsi que certains croisement doivent permettre de cibler certains problèmes potentiels bien connus.

###méthode de vérification

####Identification des évolutions aberrantes

En l'absence de nouvelles spécifications, nous nous réfèrerons aux dernières publiées par spot (https://github.com/urba4/spot/blob/master/doc/Spec_ThemaST5_V1-3.pdf).
La consommation d'espaces naturels et agricoles est un processus généralement irréversible. Des retours en arrières sont possibles mais tout phénomène massif doit attirer l'attention.

