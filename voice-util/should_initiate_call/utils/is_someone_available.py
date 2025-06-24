import os
import requests
from dotenv import load_dotenv
load_dotenv()

DEFAULT_API_URL = os.getenv("AVAILABILITY_API_URL")

def is_someone_available(api_key: str, api_url: str = DEFAULT_API_URL) -> bool:
    """
    Vérifie si un agent est disponible via l’API.
    Lève une exception en cas de mauvaise configuration ou erreur de requête.
    """
    if not api_key:
        raise ValueError("Clé API manquante pour l'appel distant.")

    if not api_url:
        raise ValueError("AVAILABILITY_API_URL non définie.")

    try:
        response = requests.get(api_url, headers={"X-API-KEY": api_key}, timeout=5)
        response.raise_for_status()
        data = response.json()
        available = data.get("available", False)
        return available

    except requests.exceptions.Timeout:
        raise RuntimeError("⏱ Timeout lors de l’appel à l’API de disponibilité.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur de requête : {e}")