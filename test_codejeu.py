import pytest
from codejeu import calculate_results

def test_calculate_results_average():
    votes = {"Player1": "5", "Player2": "8", "Player3": "13"}
    rule = "Moyenne (Average)"
    result = calculate_results(votes, rule)
    assert result == 9  # La moyenne arrondie de 5, 8 et 13 est 9

def test_calculate_results_strict_unanimity():
    votes = {"Player1": "5", "Player2": "5", "Player3": "5"}
    rule = "Strict (Unanimity)"
    result = calculate_results(votes, rule)
    assert result == 5  # Tous les votes sont identiques

def test_calculate_results_median():
    votes = {"Player1": "3", "Player2": "5", "Player3": "8"}
    rule = "Médiane (Median)"
    result = calculate_results(votes, rule)
    assert result == 5  # La médiane de 3, 5, 8 est 5

def test_calculate_results_majority():
    votes = {"Player1": "8", "Player2": "8", "Player3": "5"}
    rule = "Majorité Absolue (Absolute Majority)"
    result = calculate_results(votes, rule)
    assert result == "8"  # Le vote majoritaire est "8"

