# Visualisation_Des_Donnée_PicoQuant

## Lancement du programme

```sh
python3 main.py -i data/pt3/SRV_2.pt3 -o ./data/json/SRV_2.json
python3 img.py -i data/pt3/SRV_2.pt3 -a [[10,15],[100,105]]
```

## Arguments de commande main.py

| Options | Options Long | Significtion | Obligatoire |exemples(argument)|
| ------ | ------ |------ | ------ | ------ |
| -h | --help | Affiche de l'aide | Non ||
| -i | --ifile | Fichier de lecture .pt3 | Oui | ./data/pt3/SRV_2.pt3|
| -o | --ofile | Fichier json qui sera crée | Non | ./data/pt3/SRV_2.json|
| -I | --indent | Facilite la lecture pour humain mais prend 2 fois plus de place| Non ||


## Arguments de commande img.py

| Options | Options Long | Significtion | Obligatoire | exemples(argument)|
| ------ | ------ |------ | ------ |------ |
| -h | --help | Affiche de l'aide | Non ||
| -i | --ifile | Fichier de lecture .pt3 | Oui(json ou pt3 au moins un) | ./data/pt3/SRV_2.pt3 |
| -j | --json | Fichier de lecture .json | Oui(json ou pt3 au moins un) | ./data/pt3/SRV_2.json |
| -a | --affichage | tableau contant les immages à afficher | Oui | [[numero debut immage1 , numero fin immage1],[numero debut immage2 , numero fin immage2]]|
| -o | --ofile | Fichier json qui sera crée(sauf lecture depuis .json) | Non | ./data/pt3/SRV_2.json |
| -I | --indent | Facilite la lecture pour humain mais prend 2 fois plus de place| Non ||

## Significations des abréviations dans le fichier .json

| Abréviation | Signification |
| ------ | ------ |
| px | pixel |
| pt | photon |
| lg | ligne |
| nlg | numéro de ligne |
| img | image |
| nimg | numéro de l'image |
| file | fichier |
