# Exercices — SQLModel

Six exercices classés du **plus simple au plus difficile**. Chaque exercice a son dossier, avec le fichier à compléter (`exerciceN.py`), les tests (`test_exerciceN.py`) et la correction (`correction_exerciceN.py`). Le but : trouver la réponse seul·e.

## Fichiers

| Dossier / fichier | À quoi il sert |
|---|---|
| `enonces.md` | Ce document — les énoncés |
| `exercice_1_tagread/` | Exercice 1 |
| `exercice_2_3_category/` | Exercices 2 et 3 (ils modifient la même classe `Category`) |
| `exercice_4_product/` | Exercice 4 |
| `exercice_5_book/` | Exercice 5 |
| `exercice_6_author_novel/` | Exercice 6 |
| `../cours/01_presentation_sqlmodel.html` | La présentation du cours (à ouvrir dans un navigateur) |
| `../cours/02_cours_complet_sqlmodel.html` | Le cours complet et détaillé |

## Installation (une seule fois)

Il faut **Python 3.10 ou plus**, puis :

```bash
pip install sqlmodel pytest
```

## Méthode de travail

1. Ouvrez le dossier de l'exercice, par exemple `exercice_1_tagread/exercice1.py`, et écrivez votre code sous le `TODO`.
2. Lancez uniquement le test de cet exercice (depuis la racine du dépôt) :
   ```bash
   pytest exercices/exercice_1_tagread -v
   ```
3. **Lisez le message d'erreur.** Il dit précisément ce qui manque ou ce qui est faux : c'est fait pour que vous puissiez corriger seul·e.
4. Si vous êtes bloqué·e après plusieurs essais, dépliez l'**indice**. En dernier recours, ouvrez `correction_exerciceN.py`.
5. Quand l'exercice est vert, passez au suivant. À la fin, `pytest exercices -v` doit tout afficher en vert.

---

## Niveau 1 — Découverte

### Exercice 1 ★☆☆☆☆ — Un schéma pur, sans table

Créez une classe `TagRead` qui sert uniquement à valider/sérialiser des données API (comme un `BaseModel` Pydantic classique) — **pas** une table en base. Elle doit avoir un seul champ : `name: str`.

<details>
<summary>💡 Indice</summary>

Une classe qui n'est *pas* une table n'a pas l'argument `table=True`. Relisez la diapositive sur le rôle de `table=True`.
</details>

---

### Exercice 2 ★★☆☆☆ — Votre première vraie table

Créez une classe `Category` qui **est** une table en base, avec :
- `id` : entier optionnel, clé primaire, `None` par défaut (générée par la base)
- `name: str`

<details>
<summary>💡 Indice</summary>

Regardez comment `Hero` était défini dans la présentation : l'argument de classe qui crée la table, et `Field(...)` pour la clé primaire.
</details>

---

## Niveau 2 — Manipulation

### Exercice 3 ★★★☆☆ — Un champ optionnel avec valeur par défaut

Modifiez `Category` pour ajouter un champ `description`, de type texte, **optionnel**, qui vaut `None` si rien n'est fourni.

<details>
<summary>💡 Indice</summary>

Un champ optionnel typé s'écrit avec `| None` et une valeur par défaut. Pas besoin de `Field()` ici.
</details>

---

### Exercice 4 ★★★☆☆ — Refactoring, et un piège à connaître

Voici l'ancienne version, dupliquée entre SQLAlchemy et Pydantic :

```python
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class ProductCreate(BaseModel):
    name: str
```

Créez `Product` (la vraie table, avec `id`, `name`, `price: float`) **et** `ProductCreate` (un schéma d'entrée, sans table, avec `name` et `price`). Sur `ProductCreate` uniquement, `price` doit être **strictement positif**.

Essayez d'abord d'instancier `Product(name="x", price=-10)` puis `ProductCreate(name="x", price=-10)`. Comparez les résultats : c'est le piège de cet exercice.

<details>
<summary>💡 Indice</summary>

Cherchez un paramètre de `Field()` qui veut dire « greater than ». Et demandez-vous pourquoi la validation ne se comporte pas pareil sur une classe avec table et sur une classe sans table.
</details>

---

## Niveau 3 — Maîtrise

### Exercice 5 ★★★★☆ — Hiérarchie complète

En suivant le motif `HeroBase / Hero / HeroCreate / HeroPublic` de la présentation, construisez la hiérarchie pour une entité `Book` :

- `BookBase` : champs communs `title: str` et `author: str`
- `Book` : la vraie table — ajoute `id` (clé primaire) et `isbn: str`
- `BookCreate` : schéma d'entrée API (mêmes champs que `BookBase`, plus `isbn`)
- `BookPublic` : schéma de sortie API (mêmes champs que `BookBase`, plus `id`)

<details>
<summary>💡 Indice</summary>

Quatre classes, une seule avec `table=True`. Les trois autres héritent de `BookBase` sans réécrire `title` ni `author`.
</details>

---

### Exercice 6 ★★★★★ — Une vraie relation entre deux tables

Créez deux tables **liées** : `Author` (`id`, `name`) et `Novel` (`id`, `title`, et une référence vers son auteur). Un auteur peut avoir plusieurs romans. Vous devez pouvoir écrire :

```python
auteur = Author(name="Isaac Asimov")
roman = Novel(title="Fondation", author=auteur)
```

… et retrouver `roman.author.name == "Isaac Asimov"` après un aller-retour dans une vraie base SQLite en mémoire (le test le vérifie).

<details>
<summary>💡 Indice</summary>

Il vous faut deux choses sur `Novel` : une **clé étrangère** (cherchez le paramètre `foreign_key` de `Field`, la table d'un auteur s'appelle par défaut `author`) et une **relation ORM** (cherchez `Relationship` et son paramètre `back_populates`). Pensez à la déclarer aussi côté `Author`, dans l'autre sens.
</details>

---

*Basé sur le document de recherche « SQLModel — L'unification de Pydantic et SQLAlchemy ».*
