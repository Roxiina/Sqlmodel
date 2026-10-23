"""Tests de l'exercice 4.

    pytest exercices/exercice_4_product -v

Pour tester la correction à la place de votre fichier :
    CORRECTION=1 pytest exercices/exercice_4_product -v
"""

import importlib
import os

import pytest
from sqlmodel import SQLModel

ex = importlib.import_module(
    "correction_exercice4" if os.environ.get("CORRECTION") else "exercice4"
)


def get_fields(model):
    """Compatible pydantic v1 (SQLModel ancien) et v2 (SQLModel récent)."""
    if hasattr(model, "model_fields"):
        return model.model_fields
    return model.__fields__


def is_table(model) -> bool:
    return getattr(model, "__table__", None) is not None


# ---------------------------------------------------------------------------
# Exercice 4 — Product (refactoring + contrainte de validation)
# ---------------------------------------------------------------------------

def test_exercice4_product_existe():
    assert hasattr(ex, "Product"), "La classe Product est introuvable."


def test_exercice4_product_est_une_table():
    assert is_table(ex.Product), "Product doit être déclarée avec table=True."


def test_exercice4_product_a_les_bons_champs():
    fields = get_fields(ex.Product)
    for champ in ("id", "name", "price"):
        assert champ in fields, f"Le champ '{champ}' est manquant sur Product."


def test_exercice4_product_instanciation_valide():
    p = ex.Product(name="Clavier mécanique", price=49.90)
    assert p.name == "Clavier mécanique"
    assert p.price == 49.90


def test_exercice4_productcreate_existe():
    assert hasattr(ex, "ProductCreate"), "La classe ProductCreate est introuvable."


def test_exercice4_productcreate_pas_une_table():
    assert not is_table(ex.ProductCreate), (
        "ProductCreate ne doit PAS être une table (pas de table=True)."
    )


def test_exercice4_productcreate_instanciation_valide():
    pc = ex.ProductCreate(name="Clavier mécanique", price=49.90)
    assert pc.price == 49.90


def test_exercice4_productcreate_prix_negatif_refuse():
    with pytest.raises(Exception):
        ex.ProductCreate(name="Clavier cassé", price=-10)
    # Si ce test échoue : le champ price de ProductCreate n'a pas Field(gt=0).
