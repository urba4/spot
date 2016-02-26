Validation spot thema 2016
=
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
###règles générales

- exlusivement des polygones non nuls
- tolérance à 0.001 m
- projection Lambert93 (epsg:2154)
- ni lacune ni superposition: valable pour toutes les classes
- les limites extérieures de la couverture sont communales (bdtopo 2016)

###règles particulières aux millésimes
la taille minimale de l'objet est définie par l'UMET spécifiée dans les dernières spécification de niveau 3 publiées par Spot 
