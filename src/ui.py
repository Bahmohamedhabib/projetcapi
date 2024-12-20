import tkinter as tk
from tkinter import messagebox
from utils import load_backlog, save_backlog, load_card_images
from game_logic import calculate_results
import time
import json

backlog = []
votes = {}
current_feature = 0
timer_running = False
num_players = 0
player_names = []
current_player_index = 0  # Indice du joueur en cours


def ask_num_players(root, rule_var):
    def set_num_players():
        global num_players
        try:
            players = int(entry_players.get())
            if players < 2:
                raise ValueError("Le nombre de joueurs doit être au moins 2.")
            num_players = players
            messagebox.showinfo("Confirmation", f"Nombre de joueurs défini : {num_players}")
            popup.destroy()
            ask_player_names(root, rule_var)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide de joueurs (minimum 2).")

    popup = tk.Toplevel()
    popup.title("Nombre de joueurs")
    tk.Label(popup, text="Entrez le nombre de joueurs :").pack(pady=10)
    entry_players = tk.Entry(popup, width=10)
    entry_players.pack(pady=5)
    tk.Button(popup, text="Confirmer", command=set_num_players).pack(pady=10)


def ask_player_names(root, rule_var):
    global num_players, player_names
    player_names = []

    def set_player_names():
        for i in range(num_players):
            name = entries[i].get()
            if not name.strip():
                messagebox.showerror("Erreur", f"Le nom du joueur {i + 1} ne peut pas être vide.")
                return
            player_names.append(name)
        messagebox.showinfo("Confirmation", "Tous les noms des joueurs ont été enregistrés.")
        popup.destroy()
        start_game(root, rule_var)

    popup = tk.Toplevel()
    popup.title("Noms des joueurs")
    tk.Label(popup, text="Entrez les noms des joueurs :").pack(pady=10)

    entries = []
    for i in range(num_players):
        frame = tk.Frame(popup)
        frame.pack(pady=5)
        tk.Label(frame, text=f"Joueur {i + 1} :").pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=20)
        entry.pack(side=tk.LEFT)
        entries.append(entry)

    tk.Button(popup, text="Confirmer", command=set_player_names).pack(pady=10)


def display_feature(root, rule_var):
    """
    Affiche la fonctionnalité actuelle pour le vote.
    """
    global current_feature, votes, timer_running, current_player_index

    feature = backlog[current_feature]
    votes.clear()
    current_player_index = 0

    feature_frame = tk.Frame(root)
    feature_frame.pack(pady=20)
    tk.Label(feature_frame, text=f"Fonctionnalité {feature['feature_id']}: {feature['description']}",
             font=("Arial", 14)).pack()

    initiate_player_vote(root, rule_var, feature_frame)


def initiate_player_vote(root, rule_var, feature_frame):
    """
    Lance le vote pour un joueur spécifique avec un chronomètre visible.
    """
    global current_player_index, num_players

    if current_player_index >= num_players:
        validate_feature_vote(root, rule_var, feature_frame)
        return

    player = player_names[current_player_index]
    tk.Label(feature_frame, text=f"Tour de {player}", font=("Arial", 12)).pack(pady=5)

    # Chronomètre visuel
    timer_label = tk.Label(feature_frame, text="Temps restant : 60 secondes", font=("Arial", 14), fg="red")
    timer_label.pack(pady=5)

    card_images = load_card_images()
    player_frame = tk.Frame(feature_frame)
    player_frame.pack(pady=10)

    for value, image in card_images.items():
        tk.Button(
            player_frame,
            image=image,
            command=lambda v=value: cast_vote(v, player, root, rule_var, feature_frame)
        ).pack(side=tk.LEFT, padx=5)

    start_timer(60, player, timer_label, root, rule_var, feature_frame)


def cast_vote(vote, player, root, rule_var, feature_frame):
    """
    Enregistre le vote d'un joueur. Si tous les joueurs ont voté, tente de valider le consensus.
    """
    global votes, current_player_index

    if player in votes:
        messagebox.showwarning("Attention", f"{player} a déjà voté.")
        return

    votes[player] = vote
    messagebox.showinfo("Vote enregistré", f"{player} a voté {vote}.")
    current_player_index += 1
    initiate_player_vote(root, rule_var, feature_frame)


def validate_feature_vote(root, rule_var, feature_frame):
    """
    Valide les votes pour la fonctionnalité actuelle. Si le consensus n'est pas atteint,
    recommence les votes pour la même fonctionnalité.
    """
    global votes, current_feature, backlog

    feature = backlog[current_feature]
    rule = rule_var.get()
    result = calculate_results(votes, rule)

    if result is not None:
        feature["status"] = "validated"
        feature["votes"] = votes
        messagebox.showinfo("Résultat", f"Fonctionnalité validée avec une estimation de {result}.")
        current_feature += 1
        feature_frame.destroy()
        if current_feature < len(backlog):
            display_feature(root, rule_var)
        else:
            generate_results_file()
            messagebox.showinfo("Fin", "Toutes les fonctionnalités ont été votées.")
            tk.Button(
                root,
                text="Afficher les Résultats",
                command=show_results
            ).pack(pady=20)
    else:
        messagebox.showwarning("Vote insuffisant", "Le consensus n'a pas été atteint. Recommencez le vote.")
        current_player_index = 0
        votes.clear()
        feature_frame.destroy()
        display_feature(root, rule_var)


def start_timer(seconds, player, timer_label, root, rule_var, feature_frame):
    """
    Démarre un chronomètre pour limiter la durée du vote d'un joueur.
    """
    if seconds > 0:
        timer_label.config(text=f"Temps restant : {seconds} secondes")
        feature_frame.after(1000, start_timer, seconds - 1, player, timer_label, root, rule_var, feature_frame)
    else:
        timer_label.config(text="Temps écoulé !")
        messagebox.showwarning("Temps écoulé", f"{player} n'a pas voté à temps.")
        global current_player_index
        current_player_index += 1
        initiate_player_vote(root, rule_var, feature_frame)


def generate_results_file():
    """
    Générer un fichier JSON avec les résultats des votes.
    """
    with open("resultats.json", "w") as f:
        json.dump(backlog, f, indent=4)
    messagebox.showinfo("Résultats enregistrés", "Les résultats ont été enregistrés dans resultats.json.")


def show_results():
    """
    Afficher les résultats des votes pour toutes les fonctionnalités.
    """
    results_window = tk.Toplevel()
    results_window.title("Résultats des votes")
    tk.Label(results_window, text="Résultats des fonctionnalités", font=("Arial", 16)).pack(pady=10)

    for feature in backlog:
        result_text = f"Fonctionnalité {feature['feature_id']}: {feature['description']}\n"
        result_text += f"Statut : {feature['status']}\n"
        result_text += f"Votes : {feature['votes']}\n" if feature["votes"] else "Votes : Aucun vote enregistré.\n"
        tk.Label(results_window, text=result_text, font=("Arial", 12), justify="left").pack(pady=5)


def start_game(root, rule_var):
    global backlog, current_feature
    backlog = load_backlog("data/backlog.json")
    current_feature = 0

    if not backlog:
        messagebox.showerror("Erreur", "Le backlog est vide ou introuvable.")
        return

    display_feature(root, rule_var)


def start_app():
    root = tk.Tk()
    root.title("Planning Poker")
    tk.Label(root, text="Planning Poker", font=("Arial", 18)).pack(pady=10)

    rule_var = tk.StringVar(value="Strict (Unanimity)")
    tk.Label(root, text="Mode de vote:").pack(pady=5)
    rules = ["Strict (Unanimity)", "Moyenne (Average)", "Médiane (Median)", "Majorité Absolue (Absolute Majority)"]
    for rule in rules:
        tk.Radiobutton(root, text=rule, variable=rule_var, value=rule).pack(anchor=tk.W)

    tk.Button(
        root,
        text="Configurer le nombre de joueurs",
        command=lambda: ask_num_players(root, rule_var)
    ).pack(pady=20)

    root.mainloop()
