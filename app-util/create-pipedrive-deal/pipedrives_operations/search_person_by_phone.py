import requests
from utils.config import base_url, api_token

def search_person_by_phone(phone_number):
    url = f"{base_url}/persons/search"
    params = {
        'term': phone_number,
        'fields': 'phone',
        'api_token': api_token
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lève une exception si status != 200
        
        data = response.json()
        
        # Vérifie si la recherche a réussi et s'il y a des résultats
        if data.get('success') and data.get('data', {}).get('items'):
            # Retourne l'ID du premier résultat trouvé
            return data['data']['items'][0]['item']['id']
        else:
            return False
            
    except requests.exceptions.RequestException:
        # En cas d'erreur de requête (réseau, HTTP, etc.)
        return False
    except (KeyError, IndexError, ValueError):
        # En cas d'erreur dans la structure des données JSON
        return False