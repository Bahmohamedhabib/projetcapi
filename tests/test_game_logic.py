import pytest
from game_logic import calculate_results

def test_calculate_results_unanimity():
    votes = {"Player1": "5", "Player2": "5", "Player3": "5"}
    result = calculate_results(votes, "Strict (Unanimity)")
    assert result == 5

def test_calculate_results_average():
    votes = {"Player1": "3", "Player2": "5", "Player3": "8"}
    result = calculate_results(votes, "Moyenne (Average)")
    assert result == 5

def test_calculate_results_median():
    votes = {"Player1": "1", "Player2": "3", "Player3": "8"}
    result = calculate_results(votes, "Médiane (Median)")
    assert result == 3

def test_calculate_results_majority():
    votes = {"Player1": "5", "Player2": "5", "Player3": "8"}
    result = calculate_results(votes, "Majorité Absolue (Absolute Majority)")
    assert result == "5"
