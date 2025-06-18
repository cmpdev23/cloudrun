import requests
from utils.config import base_url, api_token

def get_deals_for_person_id(person_id):
    url = f"{base_url}/deals"
    params = {
        'person_id': person_id,
        'api_token': api_token,
        'status': "open"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lève une exception si status != 200
        
        data = response.json()
        
        # Vérifie si la requête a réussi et s'il y a des données
        if data.get('success') and data.get('data'):
            # Extrait tous les IDs des deals et les retourne dans une liste
            deal_ids = [deal['id'] for deal in data['data']]
            return deal_ids
        else:
            return []  # Retourne une liste vide si aucun deal trouvé
            
    except requests.exceptions.RequestException:
        # En cas d'erreur de requête (réseau, HTTP, etc.)
        return []
    except (KeyError, ValueError):
        # En cas d'erreur dans la structure des données JSON
        return []