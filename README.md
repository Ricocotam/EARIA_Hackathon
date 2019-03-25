# Installation
Executer `pip install -r requirements.txt`pour installer tout les packages utiles
Ou `pip3 install -r requirements.txt`

# Architecture des fichiers
- Dans `data` toute les données (peut être uploadées, peut être pas)
- Dans `logs` Tout les logs dont on a besoin pour analyser les modèles
- Dans `model_saves` une sauvegarde des modèles appris pour pouvoir reproduire les résultats
- Dans `config` les fichiers de config des modèles
- Dans `src` tout le code

## Architectur du dossier src
- `__main__.py` entrée du programme, cf exemple pour ajouter des modèles
- `api.py` tout les appelles à l'api pour les requêtes et les calculs de score
- `data.py` tout le traitement des données

## Architecture du dossier src/models
Dans chaque fichier :

- Une fonction start qui lance le modèles en utilisant le(s) fichier de configuration dans `config/*`

# Pour lancer le programme
`python3 -m src *nom du modèle*`

## List des modèles
TBD