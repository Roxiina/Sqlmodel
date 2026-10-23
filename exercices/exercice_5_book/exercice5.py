"""Exercice 5 — à compléter.

Écrivez votre code sous chaque TODO, puis lancez :
    pytest exercices/exercice_5_book -v

Bloqué·e ? La correction est dans correction_exercice5.py
"""

from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# TODO — Exercice 5 (★★★★☆) — Hiérarchie complète
#
# Créez BookBase (title: str, author: str), Book (vraie table, ajoute
# id et isbn: str), BookCreate (BookBase + isbn), BookPublic (BookBase + id).
# ---------------------------------------------------------------------------
