import requests
from utils.config import api_token

def add_note_to_deals(deal_ids, data):
    title = data.get("name")
    insurance_type = data.get("insurance_type")
    insurance_amount = data.get("insurance_amount")
    gender = data.get("gender")
    birth_year = data.get("birth_year")
    details = data.get("additional_details", "")

    url = "https://api.pipedrive.com/v1/notes"
    params = {"api_token": api_token}

    # 🧱 Construction de la note HTML
    html_note = f"""
    <h4>Informations du lead</h4>
    <ul>
        <li><strong>Nom :</strong> {title}</li>
        <li><strong>Type d'assurance :</strong> {insurance_type}</li>
        <li><strong>Montant :</strong> {insurance_amount}</li>
        <li><strong>Sexe :</strong> {gender}</li>
        <li><strong>Année de naissance :</strong> {birth_year}</li>
        <li><strong>Détails :</strong> {details}</li>
    </ul>
    """

    for deal_id in deal_ids:
        payload = {
            "content": html_note,
            "deal_id": deal_id
        }

        try:
            response = requests.post(url, params=params, json=payload)
            response.raise_for_status()
            print(f"📝 Note HTML ajoutée au deal {deal_id}")
        except requests.RequestException as e:
            print(f"❌ Erreur lors de l'ajout de la note au deal {deal_id} : {e}")
