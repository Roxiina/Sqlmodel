"""Exercice 6 — à compléter.

Écrivez votre code sous chaque TODO, puis lancez :
    pytest exercices/exercice_6_author_novel -v

Bloqué·e ? La correction est dans correction_exercice6.py
"""

from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# TODO — Exercice 6 (★★★★★) — Relation entre deux tables
#
# Créez Author (id, name, novels: liste de Novel) et Novel (id, title,
# author_id en clé étrangère vers author.id, author: relation vers Author).
# ---------------------------------------------------------------------------
