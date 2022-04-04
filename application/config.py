from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


AppName = "PicoQuant Plateforme de visualisation de données des fichiers pt3"
AppVersion = "1.0.0a\n\n"
AppDev = ("Réalisé par:\n"
          "BADANIN Roman\n"
          "<rom.badanin@gmail.com>\n\n"
          "LALANNE Loic\n"
          "<loic.lalanne@etud.univ-pau.fr>\n\n"
          "Université de Pau et Pays de l'Adour - IPREM\n"
          "Dans le cadre d'un projet tutoré 2022.\n\n")
AppGit = "https://git.univ-pau.fr/rbadanin/visualisation_des_donnee_picoquant"


SelectedFile = ""
