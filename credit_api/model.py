# ============================================================
# model.py - Chargement et preparation du modele
# ============================================================

from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

# Chargement du modele et du scaler
modele = joblib.load(BASE_DIR / "meilleur_modele_credit.pkl")
scaler = joblib.load(BASE_DIR / "scaler_credit.pkl")

# Variables numeriques utilisees pour le scaler pendant l'entrainement
VARS_NUMERIQUES = [
    "duree_mois",
    "montant_credit",
    "taux_versement",
    "residence_depuis",
    "age",
    "nb_credits",
    "nb_personnes_charge",
]

# Variables categorielles encodees en one-hot dans le notebook
VARS_CATEGORIELLES = [
    "statut_compte",
    "historique_credit",
    "objet_credit",
    "epargne",
    "emploi_depuis",
    "statut_sexe",
    "autres_debiteurs",
    "propriete",
    "autres_credits",
    "logement",
    "emploi",
    "telephone",
    "travailleur_etranger",
    "tranche_age",
]

# Seuils derives des moyennes du jeu d'entrainement
SEUIL_MONTANT_ELEVE = 3969
SEUIL_DUREE_LONGUE = 20

# Seuil optimal retenu dans le notebook final
SEUIL_OPTIMAL = 0.25


def preparer_donnees(dossier: dict) -> pd.DataFrame:
    """Transforme les donnees brutes en features compatibles avec le modele."""
    df = pd.DataFrame([dossier])

    # Feature engineering reproduit depuis le notebook d'entrainement.
    df["mensualite_estimee"] = df["montant_credit"] / df["duree_mois"]
    df["ratio_montant_age"] = df["montant_credit"] / df["age"]
    df["tranche_age"] = pd.cut(
        df["age"],
        bins=[0, 25, 35, 50, 100],
        labels=["Jeune", "Adulte", "Senior", "Retraite"],
    )
    df["credit_eleve"] = (df["montant_credit"] > SEUIL_MONTANT_ELEVE).astype(int)
    df["duree_longue"] = (df["duree_mois"] > SEUIL_DUREE_LONGUE).astype(int)
    df["score_risque"] = (
        df["taux_versement"] * 0.4
        + df["nb_credits"] * 0.3
        + df["nb_personnes_charge"] * 0.3
    )

    df = pd.get_dummies(df, columns=VARS_CATEGORIELLES, drop_first=True)

    # Le scaler a ete entraine uniquement sur les variables numeriques d'origine.
    df[VARS_NUMERIQUES] = scaler.transform(df[VARS_NUMERIQUES])

    # Alignement strict avec les colonnes attendues par le modele sauvegarde.
    features_modele = getattr(modele, "feature_names_in_", df.columns)
    return df.reindex(columns=features_modele, fill_value=0)


def predire(dossier: dict) -> dict:
    """Effectue la prediction et retourne une decision metier interpretable."""
    X = preparer_donnees(dossier)

    proba = float(modele.predict_proba(X)[0][1])
    decision = "ACCORD" if proba >= SEUIL_OPTIMAL else "REFUS"

    if proba >= 0.75:
        niveau_risque = "Faible"
    elif proba >= 0.50:
        niveau_risque = "Mod\u00e9r\u00e9"
    elif proba >= 0.30:
        niveau_risque = "\u00c9lev\u00e9"
    else:
        niveau_risque = "Tr\u00e8s \u00e9lev\u00e9"

    return {
        "decision": decision,
        "probabilite_accord": round(proba, 4),
        "niveau_risque": niveau_risque,
        "message": (
            "Cr\u00e9dit accord\u00e9 - profil favorable."
            if decision == "ACCORD"
            else "Cr\u00e9dit refus\u00e9 - risque trop \u00e9lev\u00e9."
        ),
    }
