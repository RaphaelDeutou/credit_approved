# ============================================================
# test_api.py — Tests de l'API
# ============================================================

import requests

BASE_URL = "http://localhost:8000"

# ---- Dossier test : bon profil ----
bon_profil = {
    "duree_mois"          : 12,
    "montant_credit"      : 2000,
    "taux_versement"      : 1,
    "age"                 : 40,
    "nb_credits"          : 1,
    "nb_personnes_charge" : 1,
    "residence_depuis"    : 4,
    "statut_compte"       : "A14",
    "historique_credit"   : "A34",
    "objet_credit"        : "A43",
    "epargne"             : "A65",
    "emploi_depuis"       : "A75",
    "statut_sexe"         : "A93",
    "autres_debiteurs"    : "A101",
    "propriete"           : "A121",
    "autres_credits"      : "A143",
    "logement"            : "A152",
    "emploi"              : "A173",
    "telephone"           : "A192",
    "travailleur_etranger": "A201"
}

# ---- Dossier test : profil risqué ----
mauvais_profil = {**bon_profil,
    "duree_mois"    : 60,
    "montant_credit": 15000,
    "taux_versement": 4,
    "age"           : 22,
    "statut_compte" : "A11",
    "epargne"       : "A61"
}

# ---- Tests ----
print("🔍 TEST 1 — Bon profil")
r1 = requests.post(f"{BASE_URL}/predict", json=bon_profil)
print(r1.json())

print("\n🔍 TEST 2 — Profil risqué")
r2 = requests.post(f"{BASE_URL}/predict", json=mauvais_profil)
print(r2.json())

print("\n🔍 TEST 3 — Batch (2 dossiers)")
r3 = requests.post(f"{BASE_URL}/predict/batch",
                   json=[bon_profil, mauvais_profil])
print(r3.json())