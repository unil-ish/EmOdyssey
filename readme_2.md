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
