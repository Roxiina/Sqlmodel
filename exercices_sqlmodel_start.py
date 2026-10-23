"""
Exercices SQLModel — fichier à compléter.

Remplacez chaque zone marquée "TODO" par votre code, puis lancez :
    pytest test_exercices_sqlmodel.py -v

Pour ne lancer qu'un seul exercice :
    pytest test_exercices_sqlmodel.py -k exercice1 -v

Installation requise (une seule fois) :
    pip install sqlmodel pytest
"""

from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# TODO — Exercice 1 (★☆☆☆☆) — Un schéma pur, sans table
#
# Créez TagRead : un seul champ name: str. Ce n'est PAS une table.
# ---------------------------------------------------------------------------

# Pas de table=True : TagRead est un simple schéma Pydantic (validation API).
class TagRead(SQLModel):
    name: str


# ---------------------------------------------------------------------------
# TODO — Exercice 2 (★★☆☆☆) — Votre première vraie table
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
# TODO — Exercice 3 (★★★☆☆) — Champ optionnel avec valeur par défaut
#
# Modifiez Category ci-dessus pour ajouter description: str | None = None.
# (Ne créez pas une deuxième classe Category : modifiez celle de l'exercice 2.)
# ---------------------------------------------------------------------------

# Fait directement dans Category ci-dessus (champ description).


# ---------------------------------------------------------------------------
# TODO — Exercice 4 (★★★☆☆) — Refactoring
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


# ---------------------------------------------------------------------------
# TODO — Exercice 5 (★★★★☆) — Hiérarchie complète
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


# ---------------------------------------------------------------------------
# TODO — Exercice 6 (★★★★★) — Relation entre deux tables
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
