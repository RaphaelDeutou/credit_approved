from __future__ import annotations

import os
import sys
from pathlib import Path

import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from credit_api.model import predire


class PredictionServiceError(Exception):
    """Raised when prediction cannot be completed."""


def _api_url() -> str:
    return os.getenv("CREDIT_API_URL", "").rstrip("/")


def backend_label() -> str:
    return "API distante" if _api_url() else "modele local"


def predict_one(dossier: dict) -> dict:
    api_url = _api_url()
    if api_url:
        try:
            response = requests.post(f"{api_url}/predict", json=dossier, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise PredictionServiceError(f"Echec de l'appel API: {exc}") from exc

    try:
        return predire(dossier)
    except Exception as exc:
        raise PredictionServiceError(f"Echec de la prediction locale: {exc}") from exc


def predict_batch(dossiers: list[dict]) -> list[dict]:
    return [predict_one(dossier) for dossier in dossiers]
