# ============================================================
# pages/1_analyse.py - Analyse d'un dossier individuel
# ============================================================

from pathlib import Path
import sys

import plotly.graph_objects as go
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from credit_app.prediction_service import PredictionServiceError, backend_label, predict_one

st.set_page_config(page_title="Analyse Individuelle", page_icon="📋", layout="wide")

st.title("Analyse d'un Dossier de Credit")
st.caption(f"Source de prediction active : {backend_label()}")
st.markdown("Remplissez le formulaire ci-dessous pour obtenir une decision.")
st.markdown("---")


with st.form("formulaire_credit"):
    st.subheader("Informations personnelles")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        statut_sexe = st.selectbox(
            "Statut personnel",
            {
                "A91": "Homme divorce",
                "A92": "Femme divorcee/mariee",
                "A93": "Homme celibataire",
                "A94": "Homme marie",
                "A95": "Femme celibataire",
            }.keys(),
            format_func=lambda x: {
                "A91": "Homme divorce",
                "A92": "Femme divorcee/mariee",
                "A93": "Homme celibataire",
                "A94": "Homme marie",
                "A95": "Femme celibataire",
            }[x],
        )

    with col2:
        emploi = st.selectbox(
            "Type d'emploi",
            {
                "A171": "Sans emploi",
                "A172": "Employe non qualifie",
                "A173": "Employe qualifie",
                "A174": "Cadre / Dirigeant",
            }.keys(),
            format_func=lambda x: {
                "A171": "Sans emploi",
                "A172": "Employe non qualifie",
                "A173": "Employe qualifie",
                "A174": "Cadre / Dirigeant",
            }[x],
        )

        emploi_depuis = st.selectbox(
            "Emploi actuel depuis",
            {
                "A71": "Sans emploi",
                "A72": "Moins d'1 an",
                "A73": "1 a 4 ans",
                "A74": "4 a 7 ans",
                "A75": "Plus de 7 ans",
            }.keys(),
            format_func=lambda x: {
                "A71": "Sans emploi",
                "A72": "Moins d'1 an",
                "A73": "1 a 4 ans",
                "A74": "4 a 7 ans",
                "A75": "Plus de 7 ans",
            }[x],
        )

    with col3:
        nb_personnes_charge = st.number_input("Personnes a charge", min_value=1, max_value=2, value=1)
        telephone = st.selectbox(
            "Telephone enregistre",
            {"A191": "Non", "A192": "Oui"}.keys(),
            format_func=lambda x: {"A191": "Non", "A192": "Oui"}[x],
        )
        travailleur_etranger = st.selectbox(
            "Travailleur etranger",
            {"A201": "Oui", "A202": "Non"}.keys(),
            format_func=lambda x: {"A201": "Oui", "A202": "Non"}[x],
        )

    st.markdown("---")
    st.subheader("Informations financieres")
    col4, col5, col6 = st.columns(3)

    with col4:
        montant_credit = st.number_input("Montant du credit (EUR)", min_value=250, max_value=20000, value=5000)
        duree_mois = st.slider("Duree (mois)", min_value=6, max_value=72, value=24, step=6)

    with col5:
        statut_compte = st.selectbox(
            "Statut compte cheque",
            {
                "A11": "Solde negatif",
                "A12": "0 a 200 DM",
                "A13": "Plus de 200 DM",
                "A14": "Pas de compte",
            }.keys(),
            format_func=lambda x: {
                "A11": "Solde negatif",
                "A12": "0 a 200 DM",
                "A13": "Plus de 200 DM",
                "A14": "Pas de compte",
            }[x],
        )

        epargne = st.selectbox(
            "Epargne",
            {
                "A61": "Moins de 100 DM",
                "A62": "100 a 500 DM",
                "A63": "500 a 1000 DM",
                "A64": "Plus de 1000 DM",
                "A65": "Inconnu / Pas d'epargne",
            }.keys(),
            format_func=lambda x: {
                "A61": "Moins de 100 DM",
                "A62": "100 a 500 DM",
                "A63": "500 a 1000 DM",
                "A64": "Plus de 1000 DM",
                "A65": "Inconnu / Pas d'epargne",
            }[x],
        )

    with col6:
        taux_versement = st.slider("Taux de versement (% revenu)", min_value=1, max_value=4, value=2)
        nb_credits = st.number_input("Nombre de credits existants", min_value=1, max_value=4, value=1)

    st.markdown("---")
    st.subheader("Informations complementaires")
    col7, col8, col9 = st.columns(3)

    with col7:
        objet_credit = st.selectbox(
            "Objet du credit",
            {
                "A40": "Voiture neuve",
                "A41": "Voiture d'occasion",
                "A42": "Mobilier",
                "A43": "Electromenager / Hi-Fi",
                "A44": "Informatique",
                "A45": "Autres appareils",
                "A46": "Reparations",
                "A48": "Formation",
                "A49": "Vacances",
                "A410": "Autre",
            }.keys(),
            format_func=lambda x: {
                "A40": "Voiture neuve",
                "A41": "Voiture d'occasion",
                "A42": "Mobilier",
                "A43": "Electromenager / Hi-Fi",
                "A44": "Informatique",
                "A45": "Autres appareils",
                "A46": "Reparations",
                "A48": "Formation",
                "A49": "Vacances",
                "A410": "Autre",
            }[x],
        )

        historique_credit = st.selectbox(
            "Historique de credit",
            {
                "A30": "Aucun credit / tous rembourses",
                "A31": "Tous rembourses ici",
                "A32": "Credits existants rembourses",
                "A33": "Retards passes",
                "A34": "Compte critique",
            }.keys(),
            format_func=lambda x: {
                "A30": "Aucun credit / tous rembourses",
                "A31": "Tous rembourses ici",
                "A32": "Credits existants rembourses",
                "A33": "Retards passes",
                "A34": "Compte critique",
            }[x],
        )

    with col8:
        propriete = st.selectbox(
            "Propriete",
            {
                "A121": "Immobilier",
                "A122": "Epargne / Assurance vie",
                "A123": "Voiture",
                "A124": "Inconnu / Aucune",
            }.keys(),
            format_func=lambda x: {
                "A121": "Immobilier",
                "A122": "Epargne / Assurance vie",
                "A123": "Voiture",
                "A124": "Inconnu / Aucune",
            }[x],
        )

        logement = st.selectbox(
            "Logement",
            {"A151": "Gratuit", "A152": "Proprietaire", "A153": "Locataire"}.keys(),
            format_func=lambda x: {"A151": "Gratuit", "A152": "Proprietaire", "A153": "Locataire"}[x],
        )

    with col9:
        autres_debiteurs = st.selectbox(
            "Autres debiteurs / garants",
            {"A101": "Aucun", "A102": "Co-debiteur", "A103": "Garant"}.keys(),
            format_func=lambda x: {"A101": "Aucun", "A102": "Co-debiteur", "A103": "Garant"}[x],
        )

        autres_credits = st.selectbox(
            "Autres credits en cours",
            {"A141": "Banque", "A142": "Magasins", "A143": "Aucun"}.keys(),
            format_func=lambda x: {"A141": "Banque", "A142": "Magasins", "A143": "Aucun"}[x],
        )

        residence_depuis = st.slider("Residence actuelle depuis (annees)", min_value=1, max_value=4, value=3)

    st.markdown("---")
    soumettre = st.form_submit_button("Analyser le dossier", use_container_width=True)


if soumettre:
    dossier = {
        "duree_mois": duree_mois,
        "montant_credit": montant_credit,
        "taux_versement": taux_versement,
        "age": age,
        "nb_credits": nb_credits,
        "nb_personnes_charge": nb_personnes_charge,
        "residence_depuis": residence_depuis,
        "statut_compte": statut_compte,
        "historique_credit": historique_credit,
        "objet_credit": objet_credit,
        "epargne": epargne,
        "emploi_depuis": emploi_depuis,
        "statut_sexe": statut_sexe,
        "autres_debiteurs": autres_debiteurs,
        "propriete": propriete,
        "autres_credits": autres_credits,
        "logement": logement,
        "emploi": emploi,
        "telephone": telephone,
        "travailleur_etranger": travailleur_etranger,
    }

    with st.spinner("Analyse en cours..."):
        try:
            resultat = predict_one(dossier)

            st.markdown("---")
            st.subheader("Resultat de l'analyse")

            col_res1, col_res2, col_res3 = st.columns(3)

            with col_res1:
                if resultat["decision"] == "ACCORD":
                    st.success(f"Accord : {resultat['decision']}")
                else:
                    st.error(f"Decision : {resultat['decision']}")

            with col_res2:
                st.metric("Probabilite d'accord", f"{resultat['probabilite_accord'] * 100:.1f}%")

            with col_res3:
                couleurs = {
                    "Faible": "🟢",
                    "Modéré": "🟡",
                    "Élevé": "🟠",
                    "Très élevé": "🔴",
                }
                emoji = couleurs.get(resultat["niveau_risque"], "⚪")
                st.metric("Niveau de risque", f"{emoji} {resultat['niveau_risque']}")

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=resultat["probabilite_accord"] * 100,
                    title={"text": "Score de credit (%)"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#2ecc71" if resultat["decision"] == "ACCORD" else "#e74c3c"},
                        "steps": [
                            {"range": [0, 30], "color": "#fadbd8"},
                            {"range": [30, 50], "color": "#fdebd0"},
                            {"range": [50, 75], "color": "#d5f5e3"},
                            {"range": [75, 100], "color": "#a9dfbf"},
                        ],
                        "threshold": {
                            "line": {"color": "black", "width": 4},
                            "thickness": 0.75,
                            "value": 25,
                        },
                    },
                )
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            st.info(resultat["message"])

        except PredictionServiceError as exc:
            st.error(str(exc))
