# Scripts pour Spongo

## Annotations
* Ifremer_v1 : Fichier original du HDD
* Ifremer_v1_sorted : Fichier original trié, avec les classes renommées et certains morphotypes supprimés
* Ifremer_v2 : Fichier d'annotation corrigé par l'Ifremer donné après la réunion
* Ifremer_v2_sorted : Fichier corrigé les classes renommées et certains morphotypes supprimés
* Ifremer_v3 : Basé sur Ifremer_v2_sorted avec les annotations complétées par nous

Les annotations ajoutées enter la v2_sorted et la v3 sont résumées dans ce tableau :
| Fichier           | Ball   | Vase   | Red   | Corona | Crown | Grey_white | Total annotations | Total images |
|-------------------|--------|--------|-------|--------|-------|------------|-------------------|--------------|
| Ifremer_v2_sorted | 243    | 338    | 217   | 226    | 220   | 163        | 1407              | 277          |
| Ifremer_v3        | 378    | 390    | 202   | 236    | 218   | 159        | 1583              | 247          |
| Augmentation      | +55,6% | +15,4% | -6,9% | +4,4%  | -0,9% | -2,5%      | +12,5%            | -10,8%       |

<br><br>

## Scripts
Attention : Tous les scripts doivent être exécutés depuis le dossier parent (càd le dossier contenant ce README).

* summarize_annotations : Liste les morphotypes trouvés dans le fichier csv d'annotations avec le nombre d'éponge par morphotypes.

* extract_morphotypes : Génère une image par morphotype trouvé dans le fichier d'annotation, avec 16 miniatures des éponges de ce morphotype.

* check_overlaps : Liste toutes les photos prisent à moins de 4 secondes d'interval (basé sur le nom de l'image), et qui pourrait causer un chevauchement des annotations.

* generate_yolo_annotations : Récupère les images du HDD et créer le fichier .txt d'annotation yolo associé à chaque image.

* generate_sets : Génère les fichiers train.txt et test.txt contenant les chemins des images pour l'apprentissage de yolo

* highlight_sponges : Utilise les images listées dans test.txt en encadrant les éponges annotées. Ces images sont sauvegardées dans le dossier data/highlighted.