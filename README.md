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
| *sentences_n_punctuation_segmentation.py* |   Segmentation of a paragraph in EDU tabular using punctuation   |
| *sentences_n_link_words_segmentation.py* | Segmentation of a paragraph in EDU tabular using link words |
| *sentences_n_punctuation_n_lwords_seg.py* | Segmentation of a paragraph in EDU tabular using punctuation and link words |

<!---
http://python.physique.free.fr/aide/Partie1.html 
--->