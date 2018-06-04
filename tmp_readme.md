``debates`` - A TAL project, conceived to predict a winner of a presidential debates.
===================================

Global Informations
-------------------------------

- **Name of project** : debates
- **Author** : Sablayrolles Louis (louis.sablayrolles@gmail.com)
- **Directeur de Stage** : Asher Nicholas
- **Equipe** : MELODI (Méthodes et ingénierie des Langues, des Ontologies et du Discours)
- **Laboratoire** : IRIT (Institut de Recherche en Informatique de Toulouse)

Description
------------------

- le dossier **step_1** contient le travail effectué pour la définition des types d'EDU et des relations possibles entre elles
- le dossier **step2_M1** contient le travail effectué pour la segmentation automatique des EDU

Installation
------------------

``
$ pip install -r ./step2_M1/requirements.txt
``

Documentation
------------------------

[Documentation link](https://github.com/Sablayrolles/debates/wiki)

Examples
---------------

Some of examples files in examples/ can help you to use this project

| **Files**   |      **Description**      |
|----------|-------------|
| *sentences_segmentation.py* | Segmentation of a paragraph in sentences tabular |
| *sentences\_n\_punctuation_segmentation.py* |   Segmentation of a paragraph in EDU tabular using punctuation   |
| *sentences\_n\_punctuation\_n\_linkwords_segmentation.py* | Segmentation of a paragraph in EDU tabular using punctuation and linkwords |

Results
-----------

Precision and recall for splitters

| **Size paragraph**  | **Sentences splitter**   |      **Sentences and punctuation splitter**      |      **Sentences, punctuation and linkword splitter**      |
|----------|----------|-------------|
| *<u>small</u>* | *p* = 1.0, *r* = 0.74 | *p* = 0.94, *r* = 0.83 | *p* = 0.89, *r* = 1.0|
| *<u>medium</u>* | *p* = 0.97, *r* = 0.74 | *p* = 0.92, *r* = 0.80 | *p* = 0.89, *r* = 0.81|
| *<u>long</u>* | *p* = 1.0, *r* = 0.64 | *p* = 1.0, *r* = 0.72| *p* = 0.92, *r* = 0.88 |
| **<u>Corpus</u>** | ***p* = 0.99, *r* = 0.73**  | ***p* = 0.91, *r* = 0.75** | ***p* = 0.89, *r* = 0.95** |
<!---
http://python.physique.free.fr/aide/Partie1.html 

Markdown fichier export restructured text

--->