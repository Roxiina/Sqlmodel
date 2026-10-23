"""Exercice 6 — solution.

Tester : pytest exercices/exercice_6_author_novel -v
"""

from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# Exercice 6 (★★★★★) — Relation entre deux tables
#
# Créez Author (id, name, novels: liste de Novel) et Novel (id, title,
# author_id en clé étrangère vers author.id, author: relation vers Author).
# ---------------------------------------------------------------------------

class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    # "Novel" entre guillemets : la classe n'est pas encore définie ici.
    novels: list["Novel"] = Relationship(back_populates="author")


class Novel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    # Clé étrangère : la colonne en base qui pointe vers author.id.
    author_id: int | None = Field(default=None, foreign_key="author.id")
    # Relation ORM : l'objet Author côté Python, synchronisé avec Author.novels.
    author: Author | None = Relationship(back_populates="novels")
