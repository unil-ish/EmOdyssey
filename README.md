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
