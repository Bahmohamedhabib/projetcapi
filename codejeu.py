import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from unittest.mock import MagicMock
from PIL import Image, ImageTk
import cairosvg
import json
import time
from threading import Thread

# Désactiver Tkinter dans un environnement sans affichage graphique
if not os.environ.get("DISPLAY") and os.name != "nt":  # Si pas de $DISPLAY (Linux/Unix)
    print("Mode test détecté : désactivation de Tkinter.")
    tk.Tk = MagicMock()
    messagebox.showinfo = MagicMock()
    simpledialog.askstring = MagicMock()

# Global variables for game state
backlog = []
votes = {}
results = []
current_feature = 0
card_images = {}

# Load and convert SVG files to Tkinter-compatible images
def load_card_images():
    global card_images
    card_files = {
        "0": "cartes_0.svg",
        "1": "cartes_1.svg",
        "2": "cartes_2.svg",
        "3": "cartes_3.svg",
        "5": "cartes_5.svg",
        "8": "cartes_8.svg",
        "13": "cartes_13.svg",
        "20": "cartes_20.svg",
        "40": "cartes_40.svg",
        "100": "cartes_100.svg",
        "?": "cartes_interro.svg",
        "cafe": "cartes_cafe.svg"
    }

    output_dir = "output_images"
    os.makedirs(output_dir, exist_ok=True)

    for key, file in card_files.items():
        try:
            output_path = os.path.join(output_dir, f"{key}.png")
            cairosvg.svg2png(url=file, write_to=output_path)
            image = Image.open(output_path).resize((100, 150))
            card_images[key] = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Function to calculate results based on the chosen rule
def calculate_results(votes, rule):
    """
    Calculate results based on the voting rule.
    """
    feature_votes = list(votes.values())

    if rule == "Strict (Unanimity)":
        if len(set(feature_votes)) == 1:  # Tous les votes doivent être identiques
            return int(feature_votes[0])  # Retourne le vote unique
        return None  # Indique qu'un nouveau vote est nécessaire

    elif rule == "Moyenne (Average)":
        avg = sum(map(int, feature_votes)) / len(feature_votes)
        return round(avg)  # Retourne la moyenne arrondie

    elif rule == "Médiane (Median)":
        sorted_votes = sorted(map(int, feature_votes))
        mid = len(sorted_votes) // 2
        return sorted_votes[mid] if len(sorted_votes) % 2 != 0 else \
            (sorted_votes[mid - 1] + sorted_votes[mid]) // 2  # Médiane arrondie

    elif rule == "Majorité Absolue (Absolute Majority)":
        mode_vote = max(set(feature_votes), key=feature_votes.count)  # Vote le plus fréquent
        return mode_vote

    return None  # Si la règle n'est pas reconnue, retourne None

# Main application window
if __name__ == "__main__":  # Ne s'exécute que si on lance le script directement
    root = tk.Tk()
    root.title("CAPI")
    root.geometry("800x600")

    # Load card images
    load_card_images()

    # Setup screen
    tk.Label(root, text="Projet Capi", font=("Arial", 16)).pack(pady=10)

    frame_players = tk.Frame(root)
    frame_players.pack(pady=5)
    tk.Label(frame_players, text="Nombre de joueurs:").pack(side=tk.LEFT)
    entry_players = tk.Entry(frame_players, width=10)
    entry_players.pack(side=tk.LEFT)

    rule_var = tk.StringVar()
    tk.Label(root, text="Voting Rule:").pack(pady=5)
    rules = ["Strict (Unanimity)", "Moyenne (Average)", "Médiane (Median)", "Majorité Absolue (Absolute Majority)"]
    for rule in rules:
        tk.Radiobutton(root, text=rule, variable=rule_var, value=rule).pack(anchor=tk.W)

    tk.Button(root, text="Start Game", command=lambda: print("Game started")).pack(pady=20)

    root.mainloop()
