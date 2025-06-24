import requests
import json
from utils.config import api_token
from utils.format_phone_number import format_phone_number

base_url = "https://api.pipedrive.com/v1"

def create_person(data):

    name = data.get("name")
    raw_phone = data.get("phone")

    phone = format_phone_number(raw_phone)
    
    url = f"{base_url}/persons?api_token={api_token}"
    headers = {'Content-Type': 'application/json'}

    payload = {
        "name": name,
        "owner_id": 13009293,  
        "phone": phone,
        "visible_to": 7,  

    }

    try:
        response = requests.post(url, headers=headers, json=payload )
        response.raise_for_status()
        
        data_response = response.json()
        
        # Vérifie si la création a réussi
        if data_response.get('success') and data_response.get('data', {}).get('id'):
            person_id = data_response['data']['id']
            print(f"✅ Personne créée avec succès - ID: {person_id}")
            return person_id
        else:
            print("❌ Erreur: Réponse inattendue de l'API")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la création de la personne: {e}")
        return False
    except (KeyError, ValueError) as e:
        print(f"❌ Erreur dans le parsing de la réponse: {e}")
        return False