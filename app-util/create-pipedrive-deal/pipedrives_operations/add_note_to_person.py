import requests
from utils.config import api_token

def add_note_to_person(person_id, data):
    url = f"https://api.pipedrive.com/v1/notes"
    params = {"api_token": api_token}

    # 🧱 Construction de la note HTML
    html_note = f"""
    <h4>Demande de services</h4>
    <ul>
        <li><strong>Nom :</strong> {data.get("name")}</li>
        <li><strong>Type de demande :</strong> {data.get("follow_up_type")}</li>
        <li><strong>Téléphone :</strong> {data.get("phone")}</li>
        <li><strong>Détails :</strong> {data.get("additional_details", "")}</li>
    </ul>
    """

    payload = {
        "content": html_note,
        "person_id": person_id
    }

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        print(f"📝 Note HTML ajoutée à la personne {person_id}")
    except requests.RequestException as e:
        print(f"❌ Erreur lors de l'ajout de la note à la personne {person_id} : {e}")
