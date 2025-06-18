import requests
import json
from utils.config import base_url, api_token

def update_deal_stage(deal_ids, stage_id=3):

    
    if not deal_ids:
        return {'success': False, 'first_deal_id': None}
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    params = {
        'api_token': api_token
    }
    
    # Récupère le premier deal_id
    first_deal_id = deal_ids[0]
    all_success = True
    
    # Boucle sur chaque deal_id
    for index, deal_id in enumerate(deal_ids):
        try:
            url = f"{base_url}/deals/{deal_id}"
            
            # Payload de base : changer le stage pour tous
            payload_data = {"stage_id": stage_id}
            
            # Si ce n'est pas le premier deal, ajouter le label 167
            if index > 0:  # Tous sauf le premier (index 0)
                payload_data["label_ids"] = [167]
            
            payload = json.dumps(payload_data)
            
            response = requests.patch(url, headers=headers, data=payload, params=params)
            response.raise_for_status()
            
            if index == 0:
                print(f"✅ Deal {deal_id} (PRINCIPAL) mis à jour avec succès")
            else:
                print(f"✅ Deal {deal_id} (DOUBLON) mis à jour avec succès + label 167")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de la mise à jour du deal {deal_id}: {e}")
            all_success = False
    
    return {
        'success': all_success,
        'first_deal_id': first_deal_id
    }