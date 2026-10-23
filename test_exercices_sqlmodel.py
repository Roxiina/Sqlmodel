"""
Tests automatiques pour exercices_sqlmodel_start.py

Tout lancer :
    pytest test_exercices_sqlmodel.py -v

Un seul exercice (remplacez le numéro) :
    pytest test_exercices_sqlmodel.py -k exercice3 -v
"""

import pytest
from sqlmodel import SQLModel
import exercices_sqlmodel_start as ex


def get_fields(model):
    """Compatible pydantic v1 (SQLModel ancien) et v2 (SQLModel récent)."""
    if hasattr(model, "model_fields"):
        return model.model_fields
    return model.__fields__


def is_table(model) -> bool:
    return getattr(model, "__table__", None) is not None


# ---------------------------------------------------------------------------
# Exercice 1 — TagRead (schéma pur)
# ---------------------------------------------------------------------------

def test_exercice1_tagread_existe():
    assert hasattr(ex, "TagRead"), "La classe TagRead est introuvable. L'avez-vous écrite ?"


def test_exercice1_tagread_pas_une_table():
    assert not is_table(ex.TagRead), (
        "TagRead ne doit PAS être une table : retirez table=True s'il est présent."
    )


def test_exercice1_tagread_a_le_champ_name():
    fields = get_fields(ex.TagRead)
    assert "name" in fields, "Le champ 'name' est manquant sur TagRead."


def test_exercice1_tagread_instanciation():
    t = ex.TagRead(name="python")
    assert t.name == "python"


# ---------------------------------------------------------------------------
# Exercice 2 — Category (première table)
# ---------------------------------------------------------------------------

def test_exercice2_category_existe():
    assert hasattr(ex, "Category"), "La classe Category est introuvable."


def test_exercice2_category_est_une_table():
    assert is_table(ex.Category), "Category doit être déclarée avec table=True."


def test_exercice2_category_a_les_bons_champs():
    fields = get_fields(ex.Category)
    for champ in ("id", "name"):
        assert champ in fields, f"Le champ '{champ}' est manquant sur Category."


def test_exercice2_category_instanciation():
    c = ex.Category(name="Romans")
    assert c.name == "Romans"
    assert c.id is None  # pas encore enregistrée en base


# ---------------------------------------------------------------------------
# Exercice 3 — Category.description (champ optionnel)
# ---------------------------------------------------------------------------

def test_exercice3_category_a_description():
    fields = get_fields(ex.Category)
    assert "description" in fields, (
        "Le champ 'description' est manquant sur Category (exercice 3)."
    )


def test_exercice3_description_est_optionnelle():
    c = ex.Category(name="Romans")  # sans description
    assert c.description is None, (
        "description doit valoir None par défaut si elle n'est pas fournie."
    )


def test_exercice3_description_peut_etre_fournie():
    c = ex.Category(name="Romans", description="Fiction narrative")
    assert c.description == "Fiction narrative"


# ---------------------------------------------------------------------------
# Exercice 4 — Product (refactoring + contrainte de validation)
# ---------------------------------------------------------------------------

def test_exercice4_product_existe():
    assert hasattr(ex, "Product"), "La classe Product est introuvable."


def test_exercice4_product_est_une_table():
    assert is_table(ex.Product), "Product doit être déclarée avec table=True."


def test_exercice4_product_a_les_bons_champs():
    fields = get_fields(ex.Product)
    for champ in ("id", "name", "price"):
        assert champ in fields, f"Le champ '{champ}' est manquant sur Product."


def test_exercice4_product_instanciation_valide():
    p = ex.Product(name="Clavier mécanique", price=49.90)
    assert p.name == "Clavier mécanique"
    assert p.price == 49.90


def test_exercice4_productcreate_existe():
    assert hasattr(ex, "ProductCreate"), "La classe ProductCreate est introuvable."


def test_exercice4_productcreate_pas_une_table():
    assert not is_table(ex.ProductCreate), (
        "ProductCreate ne doit PAS être une table (pas de table=True)."
    )


def test_exercice4_productcreate_instanciation_valide():
    pc = ex.ProductCreate(name="Clavier mécanique", price=49.90)
    assert pc.price == 49.90


def test_exercice4_productcreate_prix_negatif_refuse():
    with pytest.raises(Exception):
        ex.ProductCreate(name="Clavier cassé", price=-10)
    # Si ce test échoue : le champ price de ProductCreate n'a pas Field(gt=0).


# ---------------------------------------------------------------------------
# Exercice 5 — hiérarchie Book
# ---------------------------------------------------------------------------

def test_exercice5_classes_existent():
    for nom in ("BookBase", "Book", "BookCreate", "BookPublic"):
        assert hasattr(ex, nom), f"La classe {nom} est introuvable."


def test_exercice5_bookbase_pas_une_table():
    assert not is_table(ex.BookBase), "BookBase ne doit PAS être une table."


def test_exercice5_bookbase_champs_communs():
    fields = get_fields(ex.BookBase)
    for champ in ("title", "author"):
        assert champ in fields, f"Le champ '{champ}' est manquant sur BookBase."


def test_exercice5_book_est_une_table():
    assert is_table(ex.Book), "Book doit être déclarée avec table=True."


def test_exercice5_book_a_tous_les_champs():
    fields = get_fields(ex.Book)
    for champ in ("title", "author", "id", "isbn"):
        assert champ in fields, f"Le champ '{champ}' est manquant sur Book."


def test_exercice5_bookcreate_bookpublic():
    fields_create = get_fields(ex.BookCreate)
    for champ in ("title", "author", "isbn"):
        assert champ in fields_create, f"Le champ '{champ}' est manquant sur BookCreate."
    fields_public = get_fields(ex.BookPublic)
    for champ in ("title", "author", "id"):
        assert champ in fields_public, f"Le champ '{champ}' est manquant sur BookPublic."


def test_exercice5_book_instanciation():
    b = ex.Book(title="Fondation", author="Isaac Asimov", isbn="978-2070368228")
    assert b.title == "Fondation"
    assert b.isbn == "978-2070368228"


# ---------------------------------------------------------------------------
# Exercice 6 — relation Author <-> Novel, testée avec une vraie base SQLite
# ---------------------------------------------------------------------------

def test_exercice6_classes_existent():
    assert hasattr(ex, "Author"), "La classe Author est introuvable."
    assert hasattr(ex, "Novel"), "La classe Novel est introuvable."


def test_exercice6_novel_a_la_cle_etrangere():
    fields = get_fields(ex.Novel)
    assert "author_id" in fields, (
        "Le champ 'author_id' est manquant sur Novel (clé étrangère vers author.id)."
    )


def test_exercice6_relation_fonctionne_reellement():
    """Crée une vraie base SQLite en mémoire, insère un auteur et un roman,
    puis vérifie que la relation ORM les relie correctement."""
    from sqlmodel import create_engine, Session

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        auteur = ex.Author(name="Isaac Asimov")
        roman = ex.Novel(title="Fondation", author=auteur)
        session.add(auteur)
        session.add(roman)
        session.commit()
        session.refresh(roman)

        assert roman.author is not None, (
            "roman.author est vide : vérifiez le Relationship() sur Novel."
        )
        assert roman.author.name == "Isaac Asimov", (
            "La relation ne pointe pas vers le bon auteur."
        )
        assert roman in auteur.novels, (
            "auteur.novels ne contient pas le roman : vérifiez back_populates des deux côtés."
        )
