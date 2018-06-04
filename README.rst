``debates`` - A TAL project, conceived to predict a winner of a presidential debates.
=====================================================================================

Global Informations
-------------------

-  **Name of project** : debates

-  **Author** : Sablayrolles Louis (louis.sablayrolles@gmail.com)

-  **Directeur de Stage** : Asher Nicholas

-  **Equipe** : MELODI (Méthodes et ingénierie des Langues, des
   Ontologies et du Discours)

-  **Laboratoire** : IRIT (Institut de Recherche en Informatique de
   Toulouse)

Description
-----------

-  le dossier **step\_1** contient le travail effectué pour la
   définition des types d'EDU et des relations possibles entre elles

-  le dossier **step2\_M1** contient le travail effectué pour la
   segmentation automatique des EDU

Installation
------------

::

	$ git clone git@github.com:Sablayrolles/debates.git
	$ pip install -r ./step2\_M1/requirements.txt

Documentation
-------------

`Documentation link <https://github.com/Sablayrolles/debates/wiki>`__

Examples
--------

Some of examples files in examples/ can help you to use this project

+--------------------------------------------------------------+------------------------------------------------------------------------------+
| **Files**                                                    | **Description**                                                              |
+==============================================================+==============================================================================+
| *sentences\_segmentation.py*                                 | Segmentation of a paragraph in sentences tabular                             |
+--------------------------------------------------------------+------------------------------------------------------------------------------+
| *sentences\_n\_punctuation\_segmentation.py*                 | Segmentation of a paragraph in EDU tabular using punctuation                 |
+--------------------------------------------------------------+------------------------------------------------------------------------------+
| *sentences\_n\_punctuation\_n\_linkwords\_segmentation.py*   | Segmentation of a paragraph in EDU tabular using punctuation and linkwords   |
+--------------------------------------------------------------+------------------------------------------------------------------------------+
