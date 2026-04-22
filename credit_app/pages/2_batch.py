# ============================================================
# pages/2_batch.py - Analyse en masse via CSV
# ============================================================

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from credit_app.prediction_service import PredictionServiceError, backend_label, predict_one

st.set_page_config(page_title="Analyse en Masse", page_icon="📂", layout="wide")
st.title("Analyse en Masse")
st.caption(f"Source de prediction active : {backend_label()}")
st.markdown("Importez un fichier CSV pour analyser plusieurs dossiers.")

uploaded = st.file_uploader("Importer un fichier CSV", type=["csv"])

if uploaded:
    df_batch = pd.read_csv(uploaded)
    st.success(f"{len(df_batch)} dossiers importes")
    st.dataframe(df_batch.head(), use_container_width=True)

    if st.button("Lancer l'analyse", use_container_width=True):
        dossiers = df_batch.to_dict(orient="records")
        resultats = []
        progress = st.progress(0)

        for index, dossier in enumerate(dossiers):
            try:
                resultats.append(predict_one(dossier))
            except PredictionServiceError as exc:
                resultats.append(
                    {
                        "decision": "ERREUR",
                        "probabilite_accord": 0,
                        "niveau_risque": "Inconnu",
                        "message": str(exc),
                    }
                )
            progress.progress((index + 1) / len(dossiers))

        df_res = df_batch.copy()
        df_res["decision"] = [r["decision"] for r in resultats]
        df_res["probabilite_accord"] = [r["probabilite_accord"] for r in resultats]
        df_res["niveau_risque"] = [r["niveau_risque"] for r in resultats]
        df_res["message"] = [r["message"] for r in resultats]

        st.markdown("---")
        st.subheader("Resultats")

        col1, col2, col3 = st.columns(3)
        accords = (df_res["decision"] == "ACCORD").sum()
        refus = (df_res["decision"] == "REFUS").sum()

        col1.metric("Total dossiers", len(df_res))
        col2.metric("Accords", accords)
        col3.metric("Refus", refus)

        st.dataframe(
            df_res[["decision", "probabilite_accord", "niveau_risque", "message"]],
            use_container_width=True,
        )

        csv = df_res.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Telecharger les resultats",
            data=csv,
            file_name="resultats_credit.csv",
            mime="text/csv",
            use_container_width=True,
        )
