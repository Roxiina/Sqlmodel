# SQLModel : exercices

Six exercices sur [SQLModel](https://sqlmodel.tiangolo.com/), la bibliothèque qui réunit **Pydantic** (validation des données) et **SQLAlchemy** (base de données) dans une seule classe Python.

Les six exercices sont résolus et les **29 tests passent**.

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `exercices_sqlmodel_start.py` | Les réponses aux 6 exercices, commentées |
| `test_exercices_sqlmodel.py` | Les tests pytest qui vérifient les réponses |
| `exercices_sqlmodel_eleve.md` | Les énoncés des exercices |
| `sqlmodel_cours_debutant.html` | Le cours pour débutants (à ouvrir dans un navigateur) |
| `sqlmodel_presentation.html` | La présentation interactive avec QCM et exercices |
| `sqlmodel_exercices.zip` | L'archive d'origine des exercices |
| `main.py` | Exemple complet : une table `Hero` dans une base SQLite |

## Installation

Il faut Python 3.10 ou plus récent.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

## Lancer les tests

```bash
pytest test_exercices_sqlmodel.py -v              # tous les exercices
pytest test_exercices_sqlmodel.py -k exercice3 -v # un seul exercice
```

## Lancer l'exemple

```bash
python main.py
```

Le script crée `database.db`, ajoute trois héros puis les affiche.

## Les exercices

| # | Niveau | Sujet | Notion clé |
|---|---|---|---|
| 1 | ★☆☆☆☆ | `TagRead` | Une classe **sans** `table=True` est un simple schéma de validation |
| 2 | ★★☆☆☆ | `Category` | `table=True` et une clé primaire avec `Field(default=None, primary_key=True)` |
| 3 | ★★★☆☆ | `Category.description` | Un champ optionnel : `str \| None = None` |
| 4 | ★★★☆☆ | `Product` / `ProductCreate` | La contrainte `Field(gt=0)` et le piège de la validation |
| 5 | ★★★★☆ | `BookBase` / `Book` / `BookCreate` / `BookPublic` | L'héritage : un modèle par usage |
| 6 | ★★★★★ | `Author` / `Novel` | `foreign_key`, `Relationship` et `back_populates` |

## À retenir

**`table=True` change la nature de la classe.** Sans cet argument, la classe sert seulement à valider des données, comme un modèle Pydantic. Avec, elle devient une vraie table en base.

**Le piège de la validation.** Une classe `table=True` n'est pas validée quand on crée l'objet :

```python
Product(name="x", price=-10)        # aucune erreur
ProductCreate(name="x", price=-10)  # ValidationError
```

Les contraintes comme `gt=0` se placent donc sur le schéma d'entrée (`ProductCreate`), qui valide les données avant qu'on construise l'objet de table.

**L'héritage évite d'écrire les champs deux fois.**

```
BookBase (title, author)
├── Book         + id, isbn   → table
├── BookCreate   + isbn       → ce que l'API reçoit
└── BookPublic   + id         → ce que l'API renvoie
```

**Une relation entre deux tables a besoin de deux éléments :**
- la **clé étrangère** `author_id = Field(foreign_key="author.id")`, qui est la vraie colonne en base ;
- la **relation** `Relationship(back_populates=...)`, déclarée des deux côtés, qui permet d'écrire `roman.author.name` en Python.

## Sources

### Supports du cours (dans ce dépôt)

- `sqlmodel_cours_debutant.html` : le cours pour débutants (bases de données, classes, `table=True`, héritage, relations)
- `sqlmodel_presentation.html` : les diapositives, les exemples `Hero` / `Author` / `Novel` et l'explication du piège de la validation
- `exercices_sqlmodel_eleve.md` : les énoncés et les indices
- `test_exercices_sqlmodel.py` : les tests, qui précisent le comportement attendu de chaque classe

### Sources utilisées pour la présentation

- [SQLModel Official Documentation](https://sqlmodel.tiangolo.com/)
- [FastAPI : SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [SQLModel and Pydantic Integration Guide (Moltres Docs)](https://moltres.readthedocs.io/en/stable/guides/sqlmodel-integration.html)
- *Is SQLModel better than using SQLAlchemy and Pydantic?* (Python in Plain English)
- *SQL DDL to SQLModel Converter* (Safe Web Utils)
- *What is table=True inside a subclass of SQLModel?* (Stack Overflow)

### Documentation SQLModel

- [Page d'accueil de la documentation](https://sqlmodel.tiangolo.com/)
- [Créer une table avec `table=True`](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/) (exercices 2 et 3)
- [Pourquoi `id` vaut `None` avant l'enregistrement](https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/) (exercice 2)
- [Plusieurs modèles avec l'héritage : Base / Create / Public](https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/) (exercices 4 et 5)
- [Créer des tables liées par une clé étrangère](https://sqlmodel.tiangolo.com/tutorial/connect/create-connected-tables/) (exercice 6)
- [Définir les attributs `Relationship`](https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/define-relationships-attributes/) (exercice 6)
- [Le rôle de `back_populates`](https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/back-populates/) (exercice 6)
- [Code source de SQLModel sur GitHub](https://github.com/fastapi/sqlmodel)
- [Issue #52 : « SQLModel doesn't raise ValidationError »](https://github.com/fastapi/sqlmodel/issues/52), une discussion sur le piège de la validation avec `table=True` (exercice 4)

### Bibliothèques sous-jacentes

- [Pydantic : `Field` et ses contraintes (`gt`, `ge`, `lt`…)](https://docs.pydantic.dev/latest/concepts/fields/) (exercice 4)
- [SQLAlchemy : les relations entre tables](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html) (exercice 6)
- [FastAPI : utiliser une base de données SQL avec SQLModel](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [pytest : lancer les tests et filtrer avec `-k`](https://docs.pytest.org/en/stable/how-to/usage.html)
