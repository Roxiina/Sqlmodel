"""Tests de l'exercice 5.

    pytest exercices/exercice_5_book -v
"""

import pytest
from sqlmodel import SQLModel
import solution_exercice5 as ex


def get_fields(model):
    """Compatible pydantic v1 (SQLModel ancien) et v2 (SQLModel récent)."""
    if hasattr(model, "model_fields"):
        return model.model_fields
    return model.__fields__


def is_table(model) -> bool:
    return getattr(model, "__table__", None) is not None


# ---------------------------------------------------------------------------
# Exercice 5 — hiérarchie Book
# ---------------------------------------------------------------------------

def test_exercice5_classes_existent():
    for nom in ("BookBase", "Book", "BookCreate", "BookPublic"):
        assert hasattr(ex, nom), f"La classe {nom} est introuvable."


def test_exercice5_bookbase_pas_une_table():
    assert not is_table(ex.BookBase), "BookBase ne doit PAS être une table."


def test_exercice5_bookbase_champs_communs():
    fields = get_fields(ex.BookBase)
    for champ in ("title", "author"):
        assert champ in fields, f"Le champ '{champ}' est manquant sur BookBase."


def test_exercice5_book_est_une_table():
    assert is_table(ex.Book), "Book doit être déclarée avec table=True."


def test_exercice5_book_a_tous_les_champs():
    fields = get_fields(ex.Book)
    for champ in ("title", "author", "id", "isbn"):
        assert champ in fields, f"Le champ '{champ}' est manquant sur Book."


def test_exercice5_bookcreate_bookpublic():
    fields_create = get_fields(ex.BookCreate)
    for champ in ("title", "author", "isbn"):
        assert champ in fields_create, f"Le champ '{champ}' est manquant sur BookCreate."
    fields_public = get_fields(ex.BookPublic)
    for champ in ("title", "author", "id"):
        assert champ in fields_public, f"Le champ '{champ}' est manquant sur BookPublic."


def test_exercice5_book_instanciation():
    b = ex.Book(title="Fondation", author="Isaac Asimov", isbn="978-2070368228")
    assert b.title == "Fondation"
    assert b.isbn == "978-2070368228"
