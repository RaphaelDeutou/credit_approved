# ============================================================
# app.py — Page d'accueil
# ============================================================

import streamlit as st

st.set_page_config(
    page_title = "Analyse de Crédit",
    page_icon  = "🏦",
    layout     = "wide"
)

# ---- CSS personnalisé ----
st.markdown("""
    <style>
        .titre-principal {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            padding: 1rem 0;
        }
        .carte {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            border-left: 5px solid #3498db;
            margin: 1rem 0;
        }
        .accord {
            background-color: #d5f5e3;
            border-left: 5px solid #2ecc71;
            border-radius: 10px;
            padding: 1rem;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
        }
        .refus {
            background-color: #fadbd8;
            border-left: 5px solid #e74c3c;
            border-radius: 10px;
            padding: 1rem;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Contenu ----
st.markdown('<div class="titre-principal">🏦 Système d\'Analyse de Crédit</div>',
            unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="carte">
        <h3>📋 Analyse Individuelle</h3>
        <p>Analysez un dossier de crédit client en temps réel.
        Obtenez une décision immédiate avec explication détaillée.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #4d4e50;" class="carte">
        <h3 >📂 Analyse en Masse</h3>
        <p>Importez un fichier CSV pour analyser
        plusieurs dossiers simultanément et exportez les résultats.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color: #4d4e50;" class="carte">
        <h3>📊 Dashboard</h3>
        <p>Visualisez les statistiques globales,
        les tendances et les performances du modèle.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("👈 Utilisez le menu latéral pour naviguer entre les pages.")