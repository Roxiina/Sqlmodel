"""Exercices 2 et 3 — correction.

À ne regarder qu'en cas de blocage !
Tester la correction : CORRECTION=1 pytest exercices/exercice_2_3_category -v
"""

from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# Exercice 2 (★★☆☆☆) — Votre première vraie table
#
# Créez Category, une VRAIE table : id (clé primaire, optionnelle),
# name: str.
# ---------------------------------------------------------------------------

# table=True : la classe devient une vraie table "category" en base.
# id vaut None tant que l'objet n'est pas enregistré ; la base le génère.
class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None  # Exercice 3 : optionnel, None par défaut


# ---------------------------------------------------------------------------
# Exercice 3 (★★★☆☆) — Champ optionnel avec valeur par défaut
#
# Modifiez Category ci-dessus pour ajouter description: str | None = None.
# (Ne créez pas une deuxième classe Category : modifiez celle de l'exercice 2.)
# ---------------------------------------------------------------------------

# Fait directement dans Category ci-dessus (champ description).
