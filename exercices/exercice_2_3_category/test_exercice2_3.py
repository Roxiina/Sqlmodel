"""Tests des exercices 2 et 3.

    pytest exercices/exercice_2_3_category -v

Pour tester la correction à la place de votre fichier :
    CORRECTION=1 pytest exercices/exercice_2_3_category -v
"""

import importlib
import os

import pytest
from sqlmodel import SQLModel

ex = importlib.import_module(
    "correction_exercice2_3" if os.environ.get("CORRECTION") else "exercice2_3"
)


def get_fields(model):
    """Compatible pydantic v1 (SQLModel ancien) et v2 (SQLModel récent)."""
    if hasattr(model, "model_fields"):
        return model.model_fields
    return model.__fields__


def is_table(model) -> bool:
    return getattr(model, "__table__", None) is not None


# ---------------------------------------------------------------------------
# Exercice 2 — Category (première table)
# ---------------------------------------------------------------------------

def test_exercice2_category_existe():
    assert hasattr(ex, "Category"), "La classe Category est introuvable."


def test_exercice2_category_est_une_table():
    assert is_table(ex.Category), "Category doit être déclarée avec table=True."


def test_exercice2_category_a_les_bons_champs():
    fields = get_fields(ex.Category)
    for champ in ("id", "name"):
        assert champ in fields, f"Le champ '{champ}' est manquant sur Category."


def test_exercice2_category_instanciation():
    c = ex.Category(name="Romans")
    assert c.name == "Romans"
    assert c.id is None  # pas encore enregistrée en base


# ---------------------------------------------------------------------------
# Exercice 3 — Category.description (champ optionnel)
# ---------------------------------------------------------------------------

def test_exercice3_category_a_description():
    fields = get_fields(ex.Category)
    assert "description" in fields, (
        "Le champ 'description' est manquant sur Category (exercice 3)."
    )


def test_exercice3_description_est_optionnelle():
    c = ex.Category(name="Romans")  # sans description
    assert c.description is None, (
        "description doit valoir None par défaut si elle n'est pas fournie."
    )


def test_exercice3_description_peut_etre_fournie():
    c = ex.Category(name="Romans", description="Fiction narrative")
    assert c.description == "Fiction narrative"
