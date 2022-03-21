# Visualisation_Des_Donnée_PicoQuant

## Lancement du programme

```sh
python3 main.py -i data/pt3/SRV_2.pt3 -o ./data/json/SRV_2.json
python3 img.py -i data/pt3/SRV_2.pt3 -a [[10,15],[100,105]]
```

## Arguments de commande

| Options | Options Long | Significtion | Obligatoire |
| ------ | ------ |------ | ------ |
| -h | --help | Affiche de l'aide | Non |
| -i | --ifile | Fichier de lecture .pt3 | Oui |
| -o | --ofile | Fichier json qui sera crée | Oui |
| -I | --indent | Facilite la lecture pour humain mais prend 2 fois plus de place| Non |
| -j | --json | Si on ne veux pas generer le fichier json | Non |

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
