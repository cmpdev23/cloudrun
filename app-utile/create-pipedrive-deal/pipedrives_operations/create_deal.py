import requests
import json
from utils.config import api_token
from utils.format_insurance_amount import format_insurance_amount

base_url = "https://api.pipedrive.com/v1"

def create_deal(person_id, data):
    # Extraction des données
    title = data.get("name")
    insurance_type = data.get("insurance_type")
    gender = data.get("gender")
    birth_year = data.get("birth_year")

    raw_insurance_amount = data.get("insurance_amount")
    insurance_amount = format_insurance_amount(raw_insurance_amount)
    
    url = f"{base_url}/deals?api_token={api_token}"

    payload = {
        "title": title,
        "person_id": person_id,
        "user_id": 13009293,
        "pipeline_id": 1,
        "stage_id": 3,
        "visible_to": 7,
        "050ece283e6f7bb16fb4b13e211e01f6af527ef1": insurance_type,
        "4766eb24cb07f1f1912d63c4ea0ca65f6885139e": insurance_amount,
        "f186ef4f1a9e9dce35fb92e5ff166a099383d1b4": gender,
        "7e420a7f8c71554ad2a547d1364d5f665b40b1c8": birth_year
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data_response = response.json()



        if data_response.get('success') and data_response.get('data', {}).get('id'):
            deal_id = data_response['data']['id']
            return [deal_id]
        else:
            return []

    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            print(e.response.text)
        return []

    except (KeyError, ValueError) as e:
        print(f"❌ Erreur de parsing de la réponse : {e}")
        return []

    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return []
