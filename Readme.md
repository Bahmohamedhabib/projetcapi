# Planning Poker Application

## Description

Cette application de **Planning Poker** permet à une équipe de joueurs d'estimer la complexité ou l'effort nécessaire pour réaliser différentes fonctionnalités d'un projet. Les règles du Planning Poker sont respectées, et plusieurs modes de vote sont proposés. L'application est conviviale, visuelle et peut être utilisée localement sur votre machine.

---

## Fonctionnalités

- Gestion du backlog : chargement et sauvegarde des fonctionnalités à estimer (fichiers JSON).
- Modes de vote disponibles :
  - **Unanimité stricte** : tous les joueurs doivent voter la même estimation.
  - **Moyenne** : la moyenne des votes est utilisée.
  - **Médiane** : la médiane des votes est utilisée.
  - **Majorité absolue** : l'estimation la plus fréquente est retenue.
- Chronomètre : chaque joueur dispose d'une minute pour voter.
- Sauvegarde des résultats dans un fichier JSON (`resultats.json`).
- Bouton "Afficher les résultats" après la fin des votes pour visualiser les estimations.
- Interface utilisateur intuitive avec des cartes graphiques pour le vote.

---

## Pré-requis

Avant de commencer, assurez-vous d'avoir les éléments suivants :

- **Python** 3.8 ou une version ultérieure.
- Les bibliothèques Python suivantes installées :
  - `tkinter` (inclus par défaut avec Python).
  - `Pillow` (pour gérer les images SVG/PNG).
  - `cairosvg` (pour convertir les fichiers SVG en PNG).

---

## Installation

1. **Cloner le dépôt Git :**

   ```bash
   git clone https://github.com/Bahmohamedhabib/projetcapi

Installer les dépendances Python :

Exécutez la commande suivante pour installer les bibliothèques requises :

pip install pillow cairosvg
   



## Utilisation
Lancer l'application :

Exécutez la commande suivante depuis le terminal pour lancer l'application :


python app.py
Configurer le nombre de joueurs :

Cliquez sur "Configurer le nombre de joueurs".
Entrez le nombre de joueurs (minimum 2).
Entrer les noms des joueurs :

Une fenêtre apparaîtra pour entrer les noms des joueurs.
Choisir le mode de vote :

Sélectionnez l'un des modes disponibles dans le menu principal :
Strict (Unanimity)
Moyenne (Average)
Médiane (Median)
Majorité absolue (Absolute Majority)
Effectuer les votes :

Chaque joueur choisit une carte pour chaque fonctionnalité.
Un chronomètre de 1 minute s'affiche pour chaque joueur.
Afficher les résultats :

Une fois tous les votes terminés, cliquez sur "Afficher les Résultats" pour visualiser les estimations.
Organisation du Projet
Voici la structure des fichiers du projet :



planning-poker/
├── app.py                 # Point d'entrée principal pour lancer l'application
├── ui.py                  # Gestion de l'interface utilisateur
├── utils.py               # Fonctions utilitaires pour charger/sauvegarder les données et images
├── game_logic.py          # Logique pour calculer les résultats des votes
├── data/
│   └── backlog.json       # Backlog initial des fonctionnalités
├── svg_cards/             # Cartes SVG pour le Planning Poker
├── output_images/         # Cartes converties en PNG pour l'interface
└── README.md              # Documentation du projet
## Résultats
Les résultats des votes sont sauvegardés automatiquement dans un fichier JSON appelé resultats.json.
Les résultats peuvent être visualisés directement depuis l'interface utilisateur en cliquant sur "Afficher les Résultats".
Règles du Planning Poker
Le Planning Poker est une méthode d'estimation agile basée sur le consensus. Chaque joueur vote pour une estimation à l'aide de cartes numérotées. Les cartes suivantes sont disponibles :

0, 1, 2, 3, 5, 8, 13, 20, 40, 100, ? (indécis), Café (pause).
Les règles de validation des votes dépendent du mode choisi :

Unanimité stricte : Tous les joueurs doivent voter la même estimation.
Moyenne : La moyenne des votes est utilisée comme estimation.
Médiane : La médiane des votes est utilisée comme estimation.
Majorité absolue : L'estimation la plus fréquente est retenue.



## Intégration Continue, Tests Unitaires et Documentation

### Intégration Continue

- Une intégration continue est configurée via **GitHub Actions** pour exécuter des tests unitaires à chaque push ou pull request.
- Vous pouvez consulter le fichier de configuration dans `.github/workflows/ci.yml`.

### Tests Unitaires

- Les tests unitaires se trouvent dans le dossier `tests/`.
- Ils vérifient la logique du calcul des résultats pour différents modes de vote.
 
