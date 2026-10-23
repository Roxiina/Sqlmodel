"""Exercice 4 — correction.

À ne regarder qu'en cas de blocage !
Tester la correction : CORRECTION=1 pytest exercices/exercice_4_product -v
"""

from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# Exercice 4 (★★★☆☆) — Refactoring
#
# Créez Product, une vraie table : id (clé primaire, optionnelle),
# name: str, price: float strictement positif (price > 0).
# ---------------------------------------------------------------------------

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float


# Le piège : une classe table=True n'est PAS validée à la création,
# donc Product(price=-10) passe. La contrainte gt=0 va sur le schéma d'entrée.
class ProductCreate(SQLModel):
    name: str
    price: float = Field(gt=0)
