"""Exercice 5 — correction.

À ne regarder qu'en cas de blocage !
Tester la correction : CORRECTION=1 pytest exercices/exercice_5_book -v
"""

from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# Exercice 5 (★★★★☆) — Hiérarchie complète
#
# Créez BookBase (title: str, author: str), Book (vraie table, ajoute
# id et isbn: str), BookCreate (BookBase + isbn), BookPublic (BookBase + id).
# ---------------------------------------------------------------------------

# Champs communs écrits une seule fois.
class BookBase(SQLModel):
    title: str
    author: str


# La seule vraie table.
class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    isbn: str


# Ce que l'API reçoit : pas d'id, la base le génère.
class BookCreate(BookBase):
    isbn: str


# Ce que l'API renvoie : l'id est forcément connu.
class BookPublic(BookBase):
    id: int
