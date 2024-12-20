def calculate_results(votes, rule):
    """
    Calcule les résultats en fonction des votes et de la règle sélectionnée.

    Args:
        votes (dict): Les votes des joueurs sous la forme {"Player1": "5", "Player2": "8"}.
        rule (str): La règle de vote choisie. Peut être l'une des suivantes :
            - "Strict (Unanimity)" : Tous les votes doivent être identiques.
            - "Moyenne (Average)" : La moyenne des votes est utilisée.
            - "Médiane (Median)" : La médiane des votes est utilisée.
            - "Majorité Absolue (Absolute Majority)" : Le vote le plus fréquent est retenu.

    Returns:
        int | None: Le résultat de l'estimation. Retourne `None` si le consensus
        n'est pas atteint (pour "Strict (Unanimity)" seulement).
    """
    feature_votes = list(votes.values())

    if rule == "Strict (Unanimity)":
        # Vérifie si tous les votes sont identiques
        if len(set(feature_votes)) == 1:
            return int(feature_votes[0])
        return None

    elif rule == "Moyenne (Average)":
        # Calcule la moyenne des votes
        avg = sum(map(int, feature_votes)) / len(feature_votes)
        return round(avg)

    elif rule == "Médiane (Median)":
        # Calcule la médiane des votes
        sorted_votes = sorted(map(int, feature_votes))
        mid = len(sorted_votes) // 2
        if len(sorted_votes) % 2 == 0:
            # Si pair, moyenne des deux valeurs centrales
            return (sorted_votes[mid - 1] + sorted_votes[mid]) // 2
        return sorted_votes[mid]

    elif rule == "Majorité Absolue (Absolute Majority)":
        # Trouve le vote le plus fréquent
        return max(set(feature_votes), key=feature_votes.count)

    return None  # Si la règle est invalide


def validate_votes(votes, rule):
    """
    Vérifie si les votes respectent les règles choisies.

    Args:
        votes (dict): Les votes des joueurs sous la forme {"Player1": "5", "Player2": "8"}.
        rule (str): La règle de vote choisie.

    Returns:
        bool: `True` si les votes respectent les règles, `False` sinon.
    """
    result = calculate_results(votes, rule)
    return result is not None


def get_vote_summary(votes):
    """
    Génère un résumé des votes pour une fonctionnalité.

    Args:
        votes (dict): Les votes des joueurs sous la forme {"Player1": "5", "Player2": "8"}.

    Returns:
        dict: Un résumé des votes comprenant le nombre total de votes
        et une répartition des votes par valeur.
    """
    summary = {
        "total_votes": len(votes),
        "vote_distribution": {}
    }
    for vote in votes.values():
        if vote not in summary["vote_distribution"]:
            summary["vote_distribution"][vote] = 0
        summary["vote_distribution"][vote] += 1
    return summary
