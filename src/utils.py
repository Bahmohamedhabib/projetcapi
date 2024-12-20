import os
import json
from PIL import Image, ImageTk
import cairosvg

# Dictionnaire global pour stocker les images des cartes
card_images = {}


def load_backlog(filepath="data/backlog.json"):
    """
    Charge le backlog depuis un fichier JSON.

    Args:
        filepath (str): Chemin vers le fichier JSON contenant le backlog.

    Returns:
        list: Liste des éléments du backlog ou une liste vide en cas d'erreur.
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : le fichier {filepath} est introuvable.")
        return []
    except json.JSONDecodeError:
        print(f"Erreur : le fichier {filepath} contient des données JSON invalides.")
        return []


def save_backlog(filepath="data/backlog.json", data=None):
    """
    Sauvegarde le backlog dans un fichier JSON.

    Args:
        filepath (str): Chemin vers le fichier où sauvegarder les données.
        data (list): Données du backlog à sauvegarder.
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du backlog : {e}")


def load_card_images():
    """
    Charge les cartes SVG, les convertit en PNG, et les redimensionne pour
    l'interface graphique.

    Returns:
        dict: Dictionnaire associant les clés des cartes aux objets ImageTk.PhotoImage.
    """
    global card_images
    card_files = {
        "0": "svg_cards/cartes_0.svg",
        "1": "svg_cards/cartes_1.svg",
        "2": "svg_cards/cartes_2.svg",
        "3": "svg_cards/cartes_3.svg",
        "5": "svg_cards/cartes_5.svg",
        "8": "svg_cards/cartes_8.svg",
        "13": "svg_cards/cartes_13.svg",
        "20": "svg_cards/cartes_20.svg",
        "40": "svg_cards/cartes_40.svg",
        "100": "svg_cards/cartes_100.svg",
        "?": "svg_cards/cartes_interro.svg",
        "cafe": "svg_cards/cartes_cafe.svg"
    }

    output_dir = "output_images"
    os.makedirs(output_dir, exist_ok=True)

    for key, file in card_files.items():
        try:
            output_path = os.path.join(output_dir, f"{key}.png")
            # Convertir le fichier SVG en PNG
            cairosvg.svg2png(url=file, write_to=output_path)
            # Charger et redimensionner l'image
            image = Image.open(output_path).resize((100, 150))
            card_images[key] = ImageTk.PhotoImage(image)  # Stocker dans le dictionnaire
        except FileNotFoundError:
            print(f"Erreur : le fichier {file} est introuvable.")
        except Exception as e:
            print(f"Erreur lors de la conversion de {file} : {e}")

    return card_images
