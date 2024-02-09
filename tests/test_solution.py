from Final.solution import solution
from Final.contraintes import var_personnel_final, contr_final

import pytest

Liste = [
    ("Janvier", 3),
    ("Fevrier", 0),
    ("Mars", 4),
    ("Avril", 6),
    ("Mai", 7),
    ("Juin", 4),
    ("Juillet", 6),
    ("Aout", 2),
    ("Septembre", 3),
]

Liste_1 = [
    ("Janvier", 3),
    ("Fevrier", 0),
    ("Mars", 4),
    ("Avril", -6),
    ("Mai", 7),
    ("Juin", 4),
    ("Juillet", 6),
    ("Aout", 2),
    ("Septembre", 3),
]


Liste_5 = [("Janvier", 3), ("Fevrier", 2), ("Mars", 10)]


def test_solution():
    solution(Liste)


def test_solution_val_error_liste():
    with pytest.raises(ValueError):
        solution(Liste_1)


def test_solition_no_sol():
    with pytest.raises(ValueError):
        solution(Liste_5)
