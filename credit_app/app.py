# ============================================================
# app.py — Page d'accueil
# ============================================================

import streamlit as st

st.set_page_config(
    page_title="Analyse de Crédit",
    page_icon="🏦",
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --bg-card: rgba(255,255,255,0.92);
            --border-card: rgba(15, 76, 129, 0.18);
            --text-main: #102a43;
            --text-muted: #4b5563;
            --hero-start: #0f4c81;
            --hero-end: #1e88e5;
        }
<<<<<<< HEAD
        .carte {
            background-color: #4d4e50;
            border-radius: 10px;
            padding: 1.5rem;
            border-left: 5px solid #3498db;
            margin: 1rem 0;
=======

        .stApp {
            background: linear-gradient(180deg, rgba(248,251,255,0.85), rgba(240,246,255,0.95));
>>>>>>> e252f9b (Amelioration UI Streamlit et robustesse prediction)
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        .hero {
            background: linear-gradient(135deg, var(--hero-start) 0%, var(--hero-end) 100%);
            border-radius: 20px;
            padding: 1.7rem 1.8rem;
            color: white;
            margin-bottom: 1rem;
            box-shadow: 0 10px 25px rgba(15, 76, 129, 0.2);
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            box-shadow: 0 6px 18px rgba(15, 76, 129, 0.08);
            height: 100%;
            color: var(--text-main);
        }

        .card h3 {
            margin-top: 0;
            margin-bottom: 0.5rem;
            color: var(--text-main);
        }

        .card p {
            color: var(--text-muted);
            margin-bottom: 0;
            line-height: 1.45;
        }

        .stAlert {
            border-radius: 12px;
        }

        @media (prefers-color-scheme: dark) {
            .stApp {
                background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
            }

            .card {
                background: rgba(15, 23, 42, 0.92);
                border-color: rgba(148, 163, 184, 0.2);
                color: #f8fafc;
                box-shadow: 0 6px 18px rgba(2, 8, 23, 0.35);
            }

            .card h3, .card p {
                color: #f8fafc;
            }

            .card p {
                color: #cbd5e1;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

<<<<<<< HEAD
# ---- Contenu ----
st.markdown('<div class="titre-principal">Système d\'Analyse de Crédit</div>',
            unsafe_allow_html=True)

st.markdown("---")
=======
st.markdown(
    """
    <div class="hero">
        <h1 style="margin-bottom:0.35rem; font-size: 2rem;">Système d'analyse de crédit</h1>
        <p style="margin:0; font-size:1.04rem; line-height:1.5;">Une expérience plus claire et plus rapide pour évaluer un dossier, analyser plusieurs demandes et suivre les indicateurs clés.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
>>>>>>> e252f9b (Amelioration UI Streamlit et robustesse prediction)

col1, col2, col3 = st.columns(3)
with col1:
<<<<<<< HEAD
    st.markdown("""
    <div class="carte">
        <h3>Analyse Individuelle</h3>
        <p>Analysez un dossier de crédit client en temps réel.
        Obtenez une décision immédiate avec explication détaillée.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="carte">
        <h3 >Analyse en Masse</h3>
        <p>Importez un fichier CSV pour analyser
        plusieurs dossiers simultanément et exportez les résultats.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="carte">
        <h3>Dashboard</h3>
        <p>Visualisez les statistiques globales,
        les tendances et les performances du modèle.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("<<< Utilisez le menu latéral pour naviguer entre les pages.")
=======
    st.markdown(
        """
        <div class="card">
            <h3>📋 Analyse individuelle</h3>
            <p>Remplissez un formulaire simple pour obtenir une décision rapide, un score et un niveau de risque.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="card">
            <h3>📂 Analyse en masse</h3>
            <p>Importez un fichier CSV et obtenez un résultat structuré pour l’ensemble de vos dossiers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="card">
            <h3>📊 Dashboard</h3>
            <p>Consultez des indicateurs synthétiques et des graphiques pour suivre les tendances de votre pipeline.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.info("Utilisez le menu latéral pour naviguer entre les différentes vues et lancer une analyse en quelques clics.")
>>>>>>> e252f9b (Amelioration UI Streamlit et robustesse prediction)
