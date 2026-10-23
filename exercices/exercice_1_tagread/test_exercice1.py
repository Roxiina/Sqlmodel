"""Tests de l'exercice 1.

    pytest exercices/exercice_1_tagread -v
"""

import pytest
from sqlmodel import SQLModel
import solution_exercice1 as ex


def get_fields(model):
    """Compatible pydantic v1 (SQLModel ancien) et v2 (SQLModel récent)."""
    if hasattr(model, "model_fields"):
        return model.model_fields
    return model.__fields__


def is_table(model) -> bool:
    return getattr(model, "__table__", None) is not None


# ---------------------------------------------------------------------------
# Exercice 1 — TagRead (schéma pur)
# ---------------------------------------------------------------------------

def test_exercice1_tagread_existe():
    assert hasattr(ex, "TagRead"), "La classe TagRead est introuvable. L'avez-vous écrite ?"


def test_exercice1_tagread_pas_une_table():
    assert not is_table(ex.TagRead), (
        "TagRead ne doit PAS être une table : retirez table=True s'il est présent."
    )


def test_exercice1_tagread_a_le_champ_name():
    fields = get_fields(ex.TagRead)
    assert "name" in fields, "Le champ 'name' est manquant sur TagRead."


def test_exercice1_tagread_instanciation():
    t = ex.TagRead(name="python")
    assert t.name == "python"
