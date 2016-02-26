Roadmap
======
intégration de spot thema 2015
------
----------
Système en pre-releases / releases calqué sur la publication de projets informatiques.

> *En italique ce qui reste à faire.*

Synthèse
------
|version|jalons|calendrier prévisoionnel|
|:---|:---|---:|
|0.1 alpha|sources|fait|
|0.5 alpha|merge|16/02/2016|
|*0.9 beta*|*final*|*15/03/2016*|
|*1.0 spot thema*|*release initiale*|*15/04/2016*|
|*1.1 spot thema*|*release consolidée*|*15/07/2016*|

pre-releases
------
> **Note**
> pour valider chaque étape, tous les items doivent être achevés. Ca ne veut pas dire qu'on ne peut pas commencer des items de l'étape suivante.

###0.1 alpha : sources

 - les sources sont rassemblées
	 - millésimes
	 - territoires
 - *les concepts sont définis:*
	 - *modèle de données (bases millésime / base overlay)*
	 - *référentiel communal*
	 - *spécification des classes d'occupation du sol (dents creuses ?)*
 - la topologie des sources est évaluée
	 - définition des règles
	 - évaluation
 - *les données alphanumériques sont évaluées*
	 - *qualité de l'interprétation*
	 - *adéquation aux spécifications (UMET...)*

 > **Produit**
 > jeu de fichiers, rapports, rétroplanning indicatif.
 > A ce stade, pas de modification des données sources.

###0.5 alpha : merge
 - les territoires sont assemblés par année
 - l'overlay est effectué (4 millésimes + référentiel communal)
 - la topologie est corrigée après opération d'overlay

 > **Produit**
 > une classe d’entités par années ( avec depcom), une classe d’entités overlay

###0.9 beta : final
- *les données alphas sont corrigées*
- *le modèle de données est appliqué (dents creuses)*
- *un process de test/debug est adopté par les 3 agences*
- les outils de production existants sont adaptés:
	- dossier spot (cartes et stats standard)
	- script mezcal pour production en série
 
 > **Produit**
 > une base avec ses outils, prête pour la prod
 > un process de test/debug prêt à démarrer

Releases
---
###1.0 spot thema (durée de vie : 3 - 6 mois)
- la base est testée et stabilisée en interne (équipes SIG)
- les docs explicatifs (pédago pour CE) sont formalisés
- la base est publiée prête à l'usage (dossiers spot standard mis à dispo des CE, appli web ?...)
- un système de remontées de bug est en place

###1.1 spot thema (durée de vie: 4 ans ?) 
- les bugs sont corrigés
- la base est consolidée
