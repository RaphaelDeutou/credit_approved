# ============================================================
# main.py — API FastAPI
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import DossierCredit, ReponsePrediction
from model import predire
import uvicorn

# ---- Initialisation ----
app = FastAPI(
    title       = "API Analyse de Crédit",
    description = "Modèle ML de scoring crédit — particuliers et entreprises",
    version     = "1.0.0"
)

# ---- CORS (pour appels depuis un frontend) ----
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ---- Routes ----

@app.get("/")
def accueil():
    return {
        "message" : "✅ API Analyse de Crédit opérationnelle",
        "version" : "1.0.0",
        "endpoints": {
            "prediction" : "/predict",
            "sante"      : "/health",
            "docs"       : "/docs"
        }
    }

@app.get("/health")
def sante():
    return {"statut": "ok", "modele": "chargé"}


@app.post("/predict", response_model=ReponsePrediction)
def predire_credit(dossier: DossierCredit):
    """
    Analyse un dossier de crédit et retourne une décision.

    - **decision** : ACCORD ou REFUS
    - **probabilite_accord** : probabilité entre 0 et 1
    - **niveau_risque** : Faible / Modéré / Élevé / Très élevé
    - **message** : explication de la décision
    """
    try:
        resultat = predire(dossier.model_dump())
        return resultat
    except Exception as e:
        raise HTTPException(status_code=500,
                           detail=f"Erreur de prédiction : {str(e)}")


@app.post("/predict/batch")
def predire_batch(dossiers: list[DossierCredit]):
    """Analyse plusieurs dossiers en une seule requête"""
    try:
        resultats = [predire(d.model_dump()) for d in dossiers]
        return {
            "nombre_dossiers": len(resultats),
            "resultats"      : resultats,
            "resume"         : {
                "accords": sum(1 for r in resultats if r["decision"] == "ACCORD"),
                "refus"  : sum(1 for r in resultats if r["decision"] == "REFUS")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500,
                           detail=f"Erreur batch : {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
