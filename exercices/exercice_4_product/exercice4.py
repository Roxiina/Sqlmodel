"""Exercice 4 — à compléter.

Écrivez votre code sous chaque TODO, puis lancez :
    pytest exercices/exercice_4_product -v

Bloqué·e ? La correction est dans correction_exercice4.py
"""

from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# TODO — Exercice 4 (★★★☆☆) — Refactoring
#
# Créez Product, une vraie table : id (clé primaire, optionnelle),
# name: str, price: float strictement positif (price > 0).
# ---------------------------------------------------------------------------
