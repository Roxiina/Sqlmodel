"""Exercice 1 — correction.

À ne regarder qu'en cas de blocage !
Tester la correction : CORRECTION=1 pytest exercices/exercice_1_tagread -v
"""

from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# Exercice 1 (★☆☆☆☆) — Un schéma pur, sans table
#
# Créez TagRead : un seul champ name: str. Ce n'est PAS une table.
# ---------------------------------------------------------------------------

# Pas de table=True : TagRead est un simple schéma Pydantic (validation API).
class TagRead(SQLModel):
    name: str
