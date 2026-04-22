# Credit Approved

Application Streamlit d'analyse de dossiers de credit, avec prediction individuelle, analyse batch CSV et dashboard.

## Structure

- `credit_app/app.py` : point d'entree Streamlit
- `credit_app/pages/` : pages multipages
- `credit_api/` : API FastAPI et logique de prediction
- `meilleur_modele_credit.pkl` et `scaler_credit.pkl` : artefacts ML utilises par l'app

## Lancer en local

Depuis la racine du projet :

```bash
streamlit run credit_app/app.py
```

L'application Streamlit sait utiliser le modele localement. L'API FastAPI est donc optionnelle pour l'usage de l'interface.

Si vous voulez quand meme lancer l'API :

```bash
cd credit_api
uvicorn main:app --reload
```

## Deploy sur Streamlit Community Cloud

1. Poussez ce depot sur GitHub.
2. Ouvrez Streamlit Community Cloud.
3. Cliquez sur `Create app`.
4. Selectionnez le depot, la branche, puis le fichier d'entree :
   `credit_app/app.py`
5. Verifiez que la version Python est `3.12`.
6. Deployez.

L'app est preparee pour tourner sans backend separe sur Streamlit Cloud.

## Option API distante

Si vous voulez que Streamlit utilise une API distante au lieu du modele local, configurez une variable `CREDIT_API_URL`.

En local, vous pouvez la definir avant de lancer l'app. Sur Streamlit Community Cloud, vous pouvez l'ajouter dans les secrets si vous deployez aussi votre API ailleurs.

## Git

Commandes utiles :

```bash
git init
git add .
git commit -m "Prepare Streamlit deployment"
git branch -M main
git remote add origin <URL_DU_REPO_GITHUB>
git push -u origin main
```
