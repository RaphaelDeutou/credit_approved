# ============================================================
# pages/3_dashboard.py — Dashboard statistiques
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("Dashboard — Statistiques Globales")

# Simulation de données (remplacer par vos vraies données)
np.random.seed(42)
n = 500

df_dash = pd.DataFrame({
    "decision"           : np.random.choice(["ACCORD", "REFUS"], n, p=[0.7, 0.3]),
    "probabilite_accord" : np.random.beta(5, 2, n),
    "age"                : np.random.randint(18, 75, n),
    "montant_credit"     : np.random.randint(500, 15000, n),
    "duree_mois"         : np.random.choice([6,12,18,24,36,48,60], n),
    "niveau_risque"      : np.random.choice(
        ["Faible","Modéré","Élevé","Très élevé"], n, p=[0.4,0.3,0.2,0.1])
})

# ---- KPIs ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total dossiers",   n)
col2.metric("Taux d'accord",    f"{(df_dash['decision']=='ACCORD').mean()*100:.1f}%")
col3.metric("Score moyen",      f"{df_dash['probabilite_accord'].mean()*100:.1f}%")
col4.metric("Risque faible",    f"{(df_dash['niveau_risque']=='Faible').mean()*100:.1f}%")

st.markdown("---")

# ---- Graphiques ----
col_g1, col_g2 = st.columns(2)

with col_g1:
    fig1 = px.pie(
        df_dash, names="decision",
        color="decision",
        color_discrete_map={"ACCORD": "#2ecc71", "REFUS": "#e74c3c"},
        title="Répartition Accord / Refus"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    fig2 = px.histogram(
        df_dash, x="probabilite_accord",
        color="decision",
        color_discrete_map={"ACCORD": "#2ecc71", "REFUS": "#e74c3c"},
        nbins=30,
        title="Distribution des scores de crédit"
    )
    st.plotly_chart(fig2, use_container_width=True)

col_g3, col_g4 = st.columns(2)

with col_g3:
    fig3 = px.box(
        df_dash, x="decision", y="montant_credit",
        color="decision",
        color_discrete_map={"ACCORD": "#2ecc71", "REFUS": "#e74c3c"},
        title="Montant du crédit par décision"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_g4:
    fig4 = px.bar(
        df_dash.groupby("niveau_risque").size().reset_index(name="count"),
        x="niveau_risque", y="count",
        color="niveau_risque",
        color_discrete_map={
            "Faible"    : "#2ecc71",
            "Modéré"    : "#f39c12",
            "Élevé"     : "#e67e22",
            "Très élevé": "#e74c3c"
        },
        title="Répartition par niveau de risque"
    )
    st.plotly_chart(fig4, use_container_width=True)
