from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


AppName = "PicoPeek"
AppVersion = "1.1.0a\n\n"
AppDev = ("Réalisé par:\n"
          "BADANIN Roman\n"
          "<rom.badanin@gmail.com>\n\n"
          "LALANNE Loic\n"
          "<loic.lalanne@etud.univ-pau.fr>\n\n"
          "Université de Pau et Pays de l'Adour - IPREM\n"
          "Dans le cadre d'un projet tutoré 2021-2022.\n\n")
AppGit = "https://git.univ-pau.fr/rbadanin/visualisation_des_donnee_picoquant"


SelectedFile = ""
SaveFile = ""
image_cree = False
couronne_cree = False

config_rayon_1 = 0
config_rayon_2 = 0
config_center_x = 0
config_center_y = 0
