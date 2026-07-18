import unittest
from unittest.mock import patch

from credit_api import model as model_module


class PredictionFallbackTests(unittest.TestCase):
    def test_predire_uses_fallback_when_model_components_unavailable(self):
        dossier = {
            "duree_mois": 24,
            "montant_credit": 5000,
            "taux_versement": 2,
            "age": 35,
            "nb_credits": 1,
            "nb_personnes_charge": 1,
            "residence_depuis": 3,
            "statut_compte": "A12",
            "historique_credit": "A32",
            "objet_credit": "A43",
            "epargne": "A61",
            "emploi_depuis": "A73",
            "statut_sexe": "A93",
            "autres_debiteurs": "A101",
            "propriete": "A121",
            "autres_credits": "A143",
            "logement": "A152",
            "emploi": "A173",
            "telephone": "A192",
            "travailleur_etranger": "A201",
        }

        with patch.object(model_module, "modele", None), patch.object(model_module, "scaler", None):
            result = model_module.predire(dossier)

        self.assertIn(result["decision"], {"ACCORD", "REFUS"})
        self.assertIsInstance(result["probabilite_accord"], float)
        self.assertIn(result["niveau_risque"], {"Faible", "Modéré", "Élevé", "Très élevé"})
        self.assertIn("message", result)


if __name__ == "__main__":
    unittest.main()
