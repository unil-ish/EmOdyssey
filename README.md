# EmOdyssey - Emotion Odyssey

## Déscription

Bienvenue dans ce projet qui vous permettra d'explorer les capacités de traitement de texte 
de SenticNet et PYfeel, ainsi que d'apprendre à utiliser le RDF et l'A-Box RDF. 
Dans ce projet, vous travaillerez avec des fichiers JSON, qui sont couramment utilisés 
dans les applications Web. Vous apprendrez également à extraire des données à partir de ces fichiers 
et à les utiliser pour effectuer des comparaisons et des analyses de texte.

Ce projet est divisé en plusieurs étapes, où vous prendrez en entrée des fichiers JSON, 
que vous passerez à travers un parseur pour extraire le texte. 
Ensuite, vous utiliserez les outils [SenticNet](https://sentic.net/about/) et 
[PYfeel](https://github.com/AdilZouitine/pyFeel) pour tagger le texte 
en fonction de son contenu émotionnel, 
et vous comparerez ces tags avec ceux des annotateurs dans le JSON. 

Enfin, vous effectuerez des statistiques pour mesurer l'exactitude des outils SenticNet et PYfeel, 
et vous construirez un RDF et une A-Box RDF pour stocker et organiser les données.

Ce projet vous permettra de travailler avec des outils avancés de traitement de texte 
et de manipulation de données, et de développer des compétences en analyse de texte 
et en organisation de données sémantiques. 

De plus, ce projet pourra être utilisé comme base pour d'autres projets en création
de jeux vidéo et autres applications qui nécessitent une analyse émotionnelle du texte.

## Etapes
Le projet consiste en plusieurs étapes:

1. Vous devez prendre des fichiers JSON en entrée et les passer à travers [le parseur](https://github.com/dpicca/tagtog2df).
ATTENTION: le parseur est un outil externe, vous devez donc l'installer sur votre machine avant de pouvoir l'utiliser
Le parseur prendra les fichiers JSON en entrée et les convertira en fichiers DataFrame

2. Ensuite, vous devez prendre le texte extrait du JSON et
le passer à travers les outils de traitement de texte SenticNet (que vous pouvez retrouver [ici](senticnet.py))
3. et [PYfeel](https://github.com/AdilZouitine/pyFeel). Ces outils sont utilisés pour tagger le texte en fonction de son contenu émotionnel. 
Les tags permettront de décrire l'émotion que l'auteur du texte veut transmettre.

3. Après avoir taggé le texte, vous devez comparer les tags de SenticNet et PYfeel 
avec ceux des annotateurs que vous trouverez dans [les JSON](./data/input). 
Les annotateurs ont étiqueté le texte avec des informations sur l'émotion qu'il transmet.

4. Une fois les tags comparés, vous devez faire des statistiques pour voir combien 
de tags concordent entre les différentes méthodes d'étiquetage. 
Cela permettra de mesurer l'exactitude des outils SenticNet et PYfeel.

5. Enfin, vous devez construire un RDF (Resource Description Framework) pour les statistiques. 
Le RDF permettra de stocker et d'organiser les données de manière à ce qu'elles soient facilement accessibles et consultables.
6. Vous devez étudier l'ontologie [psy_model.owl](./ontologies/psy_model.owl) et la comprendre.
6. Vous devez également construire une A-Box RDF pour [psy_model.owl](./ontologies/psy_model.owl)
L'A-Box RDF est une extension du RDF qui permet de décrire les instances individuelles de concepts de l'ontologie. 
Cette étape est importante pour la création d'une base de données complète.

Ce projet vous permettra de travailler avec des outils de traitement de texte avancés, ainsi que d'apprendre à utiliser le RDF et l'A-Box RDF. Il vous permettra également de travailler avec des fichiers JSON, qui sont couramment utilisés dans les applications Web et mobiles.
# Contexte

Ce projet a été effectué en cadre du cours “Programmation pour le Web Sémantique”, donné par prof. Davide Picca à l’Université de Lausanne au semestre de printemps 2023. Le projet a été réalisé par trois étudiants de l’UNIL: Nicolas Bovet, Antonin Schnyder et Sofia Boteva. Le but du projet était de se familiariser avec les concepts principaux du Web Sémantique, apprendre d’utiliser le RDF et construire l’Abox RDF, tout en explorant les capacités et les limites de traitement de texte de SenticNet et PYfeel, comparés à l’analyse humaine.
# Structure
Ci-dessous est décrit la structure du projet en détaillant le contenu des dossiers et sous-dossiers  
## Dossier ```csv```
Dans ce dossier sont stockés les fichiers csv contenant chacun une dataframe généré par la classe EvalFeel.
 
 - ```all_df.csv``` contient la dataframe brute qui réunit tous les fichiers JSON
 - ```all_df_clean.csv``` contient la dataframe nettoyée avec seulement les extraits et les émotions TagTog associées
 -  ```emotions_df.csv``` contient la dataframe qui réunit la classification des émotions des trois méthodes (TagTog,Senticnet,PyFeel) et le texte correspondant
 - ```stats_emotions.csv``` contient le récapitulatif des statistiques faits sur les données avec une ligne par émotion et ses occurences avec chaque méthode et chaque intersection de méthode. 

## Dossier ```ontologies```
Ce dossier contient les ontologies utilisées et les ontologies exportées par le programme.

- ```psy_model.owl``` est l'ontologie de base, avant d'avoir été modifiée
- ```emotions_modif.rdf``` est l'ontologie de base (ci-dessus) modifiée selon les besoins. On y a ajouté les "datatype properties" ```hasCommonEmotion```, ```hasAllCommonEmotions``` et ```hasTotalEmotions``` ainsi que les "object properties" ```hasTagtogEmotion```, ```hasSenticnetEmotion``` et ```hasPyfeelEmotion```. On a aussi retravaillé l'ontologie de telle sorte à refléter la hiérarchie des émotions de SenticNet et faire le pont entre les différents systèmes d'émotions (TagTog, SenticNet et PyFeel).
- ```emotion_modif_filled.rdf``` est un exemple d'output (avec la A-Box créée) tel qu'il est possible de l'obtenir après avoir lancé et utilisé le programme.
## Dossier ```png```
Chaque fichier png représente des diagrammes de Venn illustrant le nombre de reconnaissances de chaque émotion par les trois programmes, ainsi que le nombre de reconnaissances communes par les différentes méthodes (en intersections). Le finchier “none” illustre le cas limite de fonctionnement de Senticnet, où aucune émotion n’a été reconnue pour les speechs.
## Dossier ```rapport```
Dans le dossier rapport se trouve le rapport qui décrit en détail notre processus lors de ce travail.
## Fichier  ```abox.py```
Dans le fichier ```abox.py```se trouve la classe ```abox``` qui a pour fonction de remplir une ontologie avec des extraits de textes, des émotions et des statistiques
## Fichier  ```evalfeel.py```
Dans le fichier ```evalfeel.py``` se trouve la classe ```evalfeel``` qui a pour fonction de créer une dataframe contenant extraits de textes et émotions correspondantes. Elle s'occupe également de calculer des statistiques de représentation à partir de cette dataframe.
# Fichier ```main.py```
Le fichier ```main.py``` peremt d'exécuter les fonctions des deux classes ```abox``` et ```evalfeel```.

# Classes utilisables 
## EvalFeel
EvalFeel est une classe qui permet de créer une dataframe à partir de fichiers JSON dans lesquels sont stockées des textes tagués avec une émotion par TagTog.

La méthode ```make_df_emotions()``` créer une dataframe stockée dans le fichier _emotions_df.csv_ qui contient tous les extraits avec les émotions évaluées par les différentes méthodes (TagTog, Senticnet, PyFeel).

La méthode ```make_diagram(emotion)``` crée un diagrame de Venn avec la comparaison de tags entre les trois métohdes pour une émotion donnée en paramètre

La méthode ```make_all_stats()``` évalue chaque émotion présentes dans le fichier _emotions_df.csv_ et crée un diagrame de Venn pour chaque émotion et stocke une dataframe regroupant toutes les statistiques de comparaison entre les méthodes dans le fichier _stats_emotions.csv_

Utilisation :

```
f = EvalFeel('jsons/members')
f.make_df_emotions()
f.make_diagram('joy')
f.make_all_stats()
```

## ABoxFiller
ABoxFiller est une classe qui permet de peupler l'ontologie (créer la A-Box) avec les données extraites par la classe EvalFeel, ci-dessus. Elle prend comme paramètre le nom du fichier ```csv``` contenant les données relatives aux extraits dont on souhaite peupler l'ontologie, un fichier ```csv``` contenant des statistiques selon les différents systèmes (Tagtog, Senticnet, PyFeel) et selon les émotions, ainsi que l'ontologie utilisée comme base.

La méthode ```fill()``` charge les différents ```csv``` et l'ontologie, puis peuple l'ontologie (création de la A-Box) avec les données des fichiers ```csv```. Une fois la A-Box créée, l'ontologie est automatiquement exportée dans le même dossier que l'ontologie de base, en rajoutant ```_filled``` à son nom d'origine.

Utilisation :
```
abf = ABoxFiller('path/to/emotions.csv', 'path/to/statistics.csv', 'path/to/ontology') # Création d'un nouvel objet en spécifiant les fichiers utilisés
abf.fill() # Création de la A-Box et exportation de la nouvelle ontologie
```