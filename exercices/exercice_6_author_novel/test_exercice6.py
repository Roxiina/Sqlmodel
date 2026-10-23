"""Tests de l'exercice 6.

    pytest exercices/exercice_6_author_novel -v

Pour tester la correction à la place de votre fichier :
    CORRECTION=1 pytest exercices/exercice_6_author_novel -v
"""

import importlib
import os

import pytest
from sqlmodel import SQLModel

ex = importlib.import_module(
    "correction_exercice6" if os.environ.get("CORRECTION") else "exercice6"
)


def get_fields(model):
    """Compatible pydantic v1 (SQLModel ancien) et v2 (SQLModel récent)."""
    if hasattr(model, "model_fields"):
        return model.model_fields
    return model.__fields__


def is_table(model) -> bool:
    return getattr(model, "__table__", None) is not None


# ---------------------------------------------------------------------------
# Exercice 6 — relation Author <-> Novel, testée avec une vraie base SQLite
# ---------------------------------------------------------------------------

def test_exercice6_classes_existent():
    assert hasattr(ex, "Author"), "La classe Author est introuvable."
    assert hasattr(ex, "Novel"), "La classe Novel est introuvable."


def test_exercice6_novel_a_la_cle_etrangere():
    fields = get_fields(ex.Novel)
    assert "author_id" in fields, (
        "Le champ 'author_id' est manquant sur Novel (clé étrangère vers author.id)."
    )


def test_exercice6_relation_fonctionne_reellement():
    """Crée une vraie base SQLite en mémoire, insère un auteur et un roman,
    puis vérifie que la relation ORM les relie correctement."""
    from sqlmodel import create_engine, Session

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        auteur = ex.Author(name="Isaac Asimov")
        roman = ex.Novel(title="Fondation", author=auteur)
        session.add(auteur)
        session.add(roman)
        session.commit()
        session.refresh(roman)

        assert roman.author is not None, (
            "roman.author est vide : vérifiez le Relationship() sur Novel."
        )
        assert roman.author.name == "Isaac Asimov", (
            "La relation ne pointe pas vers le bon auteur."
        )
        assert roman in auteur.novels, (
            "auteur.novels ne contient pas le roman : vérifiez back_populates des deux côtés."
        )
