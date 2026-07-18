# ============================================================
# model.py - Chargement et préparation du modèle
# ============================================================

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

VARS_NUMERIQUES = [
    "duree_mois",
    "montant_credit",
    "taux_versement",
    "residence_depuis",
    "age",
    "nb_credits",
    "nb_personnes_charge",
]

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

SEUIL_MONTANT_ELEVE = 3969
SEUIL_DUREE_LONGUE = 20
SEUIL_OPTIMAL = 0.25

modele: Any = None
scaler: Any = None
MODEL_LOAD_ERROR: str | None = None


def _charger_modele() -> None:
    global modele, scaler, MODEL_LOAD_ERROR
    if modele is not None or scaler is not None:
        return

    try:
        modele = joblib.load(BASE_DIR / "meilleur_modele_credit.pkl")
        scaler = joblib.load(BASE_DIR / "scaler_credit.pkl")
        MODEL_LOAD_ERROR = None
    except Exception as exc:  # pragma: no cover - protection contre un modèle indisponible
        modele = None
        scaler = None
        MODEL_LOAD_ERROR = str(exc)


_charger_modele()


def model_status_label() -> str:
    if modele is not None and scaler is not None:
        return "modèle prêt"
    return "fallback heuristique"


def _score_heuristique(dossier: dict) -> float:
    score = 0.50

    if dossier.get("age", 0) >= 35:
        score += 0.05
    if dossier.get("age", 0) <= 24:
        score -= 0.10

    if dossier.get("montant_credit", 0) <= 5000:
        score += 0.05
    if dossier.get("montant_credit", 0) >= 12000:
        score -= 0.10

    if dossier.get("duree_mois", 0) <= 24:
        score += 0.05
    if dossier.get("duree_mois", 0) >= 48:
        score -= 0.08

    if dossier.get("taux_versement", 0) <= 2:
        score += 0.05
    if dossier.get("taux_versement", 0) >= 3:
        score -= 0.07

    if dossier.get("nb_credits", 0) <= 1:
        score += 0.04
    if dossier.get("nb_credits", 0) >= 3:
        score -= 0.06

    if dossier.get("nb_personnes_charge", 0) <= 1:
        score += 0.03

    if dossier.get("residence_depuis", 0) >= 3:
        score += 0.04

    if dossier.get("statut_compte") in {"A12", "A13", "A14"}:
        score += 0.05
    if dossier.get("historique_credit") in {"A30", "A31", "A32"}:
        score += 0.05
    if dossier.get("epargne") in {"A63", "A64"}:
        score += 0.04
    if dossier.get("emploi_depuis") in {"A74", "A75"}:
        score += 0.03
    if dossier.get("statut_sexe") in {"A92", "A95"}:
        score += 0.02
    if dossier.get("propriete") in {"A121", "A122"}:
        score += 0.03

    return float(max(0.02, min(0.98, score)))


def _niveau_risque(proba: float) -> str:
    if proba >= 0.75:
        return "Faible"
    if proba >= 0.50:
        return "Modéré"
    if proba >= 0.30:
        return "Élevé"
    return "Très élevé"


def preparer_donnees(dossier: dict) -> pd.DataFrame:
    """Transforme les données brutes en features compatibles avec le modèle."""
    df = pd.DataFrame([dossier])

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

    if scaler is not None:
        df[VARS_NUMERIQUES] = scaler.transform(df[VARS_NUMERIQUES])
    else:
        df[VARS_NUMERIQUES] = df[VARS_NUMERIQUES].astype(float)

    if modele is not None:
        features_modele = getattr(modele, "feature_names_in_", df.columns)
        return df.reindex(columns=features_modele, fill_value=0)
    return df


def predire(dossier: dict) -> dict:
    """Effectue la prédiction et retourne une décision métier interprétable."""
    if modele is None:
        proba = _score_heuristique(dossier)
        decision = "ACCORD" if proba >= SEUIL_OPTIMAL else "REFUS"
        return {
            "decision": decision,
            "probabilite_accord": round(proba, 4),
            "niveau_risque": _niveau_risque(proba),
            "message": "Prédiction par heuristique de secours - le modèle principal n'est pas disponible.",
        }

    X = preparer_donnees(dossier)
    proba = float(modele.predict_proba(X)[0][1])
    decision = "ACCORD" if proba >= SEUIL_OPTIMAL else "REFUS"

    return {
        "decision": decision,
        "probabilite_accord": round(proba, 4),
        "niveau_risque": _niveau_risque(proba),
        "message": (
            "Crédit accordé - profil favorable."
            if decision == "ACCORD"
            else "Crédit refusé - risque trop élevé."
        ),
    }
