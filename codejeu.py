import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from unittest.mock import MagicMock
from PIL import Image, ImageTk
import cairosvg
import json
import time
from threading import Thread

# Disable Tkinter if running in a test environment
if os.environ.get("TEST_ENVIRONMENT"):
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

# Function to start the game
def start_game():
    global backlog, votes, current_feature

    try:
        num_players = int(entry_players.get())
        if num_players < 1:
            raise ValueError("Number of players must be at least 1.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
        return

    players = [simpledialog.askstring("Player Name", f"Enter name for Player {i + 1}") for i in range(num_players)]

    rules = rule_var.get()
    if not rules:
        messagebox.showerror("Invalid Input", "Please select a voting rule.")
        return

    # Load backlog
    try:
        with open("backlog.json", "r") as file:
            backlog = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "backlog.json not found. Please add a backlog.")
        return

    votes = {player: None for player in players}
    current_feature = 0

    start_voting(players, rules)

# Function to start voting on a feature
def start_voting(players, rule):
    global current_feature

    if current_feature >= len(backlog):
        save_results()
        messagebox.showinfo("Game Over", "All features have been validated!")
        return

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Feature: {backlog[current_feature]['description']}", font=("Arial", 16)).pack(pady=10)

    def select_vote(player, card):
        votes[player] = card
        messagebox.showinfo("Vote Selected", f"{player} selected: {card}")

    for player in players:
        tk.Label(root, text=f"{player}, select your card:").pack(pady=5)
        card_frame = tk.Frame(root)
        card_frame.pack(pady=5)

        for key, image in card_images.items():
            button = tk.Button(card_frame, image=image, command=lambda p=player, c=key: select_vote(p, c))
            button.pack(side=tk.LEFT, padx=5)

    def submit_votes():
        if None in votes.values():
            messagebox.showerror("Incomplete Votes", "All players must select a card before proceeding.")
            return

        calculate_results(rule, players)

    tk.Button(root, text="Submit Votes", command=submit_votes).pack(pady=20)

# Function to calculate results based on the chosen rule
def calculate_results(rule, players):
    global current_feature

    feature_votes = list(votes.values())

    if rule == "Strict (Unanimity)":
        if len(set(feature_votes)) == 1:
            finalize_feature(max(feature_votes))
        else:
            messagebox.showinfo("Re-vote Required", "Votes are not unanimous. Please vote again.")
            start_voting(players, rule)

    elif rule == "Moyenne (Average)":
        avg = sum(map(int, feature_votes)) / len(feature_votes)
        finalize_feature(round(avg))

    elif rule == "Médiane (Median)":
        sorted_votes = sorted(map(int, feature_votes))
        median = sorted_votes[len(sorted_votes) // 2]
        finalize_feature(median)

    elif rule == "Majorité Absolue (Absolute Majority)":
        mode_vote = max(set(feature_votes), key=feature_votes.count)
        finalize_feature(mode_vote)

# Function to finalize a feature
def finalize_feature(difficulty):
    global current_feature

    backlog[current_feature]["difficulty"] = difficulty
    backlog[current_feature]["status"] = "validated"
    results.append(backlog[current_feature])
    current_feature += 1
    start_voting(list(votes.keys()), rule_var.get())

# Save results to JSON
def save_results():
    with open("results.json", "w") as file:
        json.dump(results, file, indent=4)
    messagebox.showinfo("Results Saved", "The results have been saved to results.json.")

# Timer Functionality
def start_timer():
    timer_label = tk.Label(root, text="Time Remaining: 60", font=("Arial", 12))
    timer_label.pack()

    def countdown():
        time_left = 60
        while time_left > 0:
            time.sleep(1)
            time_left -= 1
            timer_label.config(text=f"Time Remaining: {time_left}")

    Thread(target=countdown, daemon=True).start()

# Main application window
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

tk.Button(root, text="Start Game", command=start_game).pack(pady=20)

root.mainloop()
