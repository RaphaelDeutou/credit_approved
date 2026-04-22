# ============================================================
# schemas.py — Définition des données d'entrée/sortie
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional

class DossierCredit(BaseModel):
    # Variables numériques
    duree_mois          : int   = Field(..., ge=1,  le=72,   description="Durée du crédit en mois")
    montant_credit      : float = Field(..., ge=250, le=20000, description="Montant du crédit")
    taux_versement      : int   = Field(..., ge=1,  le=4,    description="Taux de versement (1-4)")
    age                 : int   = Field(..., ge=18, le=100,  description="Âge du demandeur")
    nb_credits          : int   = Field(..., ge=1,  le=4,    description="Nombre de crédits existants")
    nb_personnes_charge : int   = Field(..., ge=1,  le=2,    description="Personnes à charge")
    residence_depuis    : int   = Field(..., ge=1,  le=4,    description="Résidence actuelle depuis")

    # Variables catégorielles
    statut_compte       : str = Field(..., description="Statut du compte chèque (A11/A12/A13/A14)")
    historique_credit   : str = Field(..., description="Historique crédit (A30/A31/A32/A33/A34)")
    objet_credit        : str = Field(..., description="Objet du crédit (A40 à A410)")
    epargne             : str = Field(..., description="Épargne (A61/A62/A63/A64/A65)")
    emploi_depuis       : str = Field(..., description="Emploi depuis (A71/A72/A73/A74/A75)")
    statut_sexe         : str = Field(..., description="Statut personnel (A91/A92/A93/A94/A95)")
    autres_debiteurs    : str = Field(..., description="Autres débiteurs (A101/A102/A103)")
    propriete           : str = Field(..., description="Propriété (A121/A122/A123/A124)")
    autres_credits      : str = Field(..., description="Autres crédits (A141/A142/A143)")
    logement            : str = Field(..., description="Logement (A151/A152/A153)")
    emploi              : str = Field(..., description="Emploi (A171/A172/A173/A174)")
    telephone           : str = Field(..., description="Téléphone (A191/A192)")
    travailleur_etranger: str = Field(..., description="Travailleur étranger (A201/A202)")

    class Config:
        json_schema_extra = {
            "example": {
                "duree_mois"          : 24,
                "montant_credit"      : 5000,
                "taux_versement"      : 2,
                "age"                 : 35,
                "nb_credits"          : 1,
                "nb_personnes_charge" : 1,
                "residence_depuis"    : 3,
                "statut_compte"       : "A11",
                "historique_credit"   : "A32",
                "objet_credit"        : "A43",
                "epargne"             : "A61",
                "emploi_depuis"       : "A73",
                "statut_sexe"         : "A93",
                "autres_debiteurs"    : "A101",
                "propriete"           : "A121",
                "autres_credits"      : "A143",
                "logement"            : "A152",
                "emploi"              : "A173",
                "telephone"           : "A192",
                "travailleur_etranger": "A201"
            }
        }

class ReponsePrediction(BaseModel):
    decision          : str
    probabilite_accord: float
    niveau_risque     : str
    message           : str