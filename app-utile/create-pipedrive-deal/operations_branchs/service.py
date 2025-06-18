from utils.format_phone_number import format_phone_number
from pipedrives_operations.search_person_by_phone import search_person_by_phone
from pipedrives_operations.create_person import create_person
from pipedrives_operations.add_note_to_person import add_note_to_person
from flask import jsonify


def service_branche(data):
    phone = data.get('phone')
    if not phone:
        return jsonify({'error': 'Numéro de téléphone requis'}), 400

    try:
        # Formatage du numéro de téléphone
        phone_number = format_phone_number(phone)
    except Exception as e:
        print(f"❌ Erreur de formatage du numéro: {e}")
        return jsonify({'error': 'Numéro de téléphone invalide'}), 400

    try:
        # Recherche de la personne dans Pipedrive
        person_id = search_person_by_phone(phone_number)
    except Exception as e:
        print(f"❌ Erreur lors de la recherche de contact: {e}")
        return jsonify({'error': 'Erreur interne lors de la recherche de contact'}), 500

    if person_id:
        print(f"✅ Contact trouvé - Person ID: {person_id}")
        # Ajout de la note à la personne
        add_note_to_person(person_id, data)
        pipedrive_url = f"https://comparermaprime.pipedrive.com/person/{person_id}"
        return jsonify({'url': pipedrive_url}), 200

    try:
        # Création de la personne si non trouvée
        new_person_id = create_person(data)
    except Exception as e:
        print(f"❌ Erreur lors de la création de la personne: {e}")
        return jsonify({'error': 'Erreur interne lors de la création de la personne'}), 500

    if new_person_id:
        print(f"✅ Nouvelle personne créée - Person ID: {new_person_id}")
        # Ajout de la note à la nouvelle personne
        add_note_to_person(new_person_id, data)
        pipedrive_url = f"https://comparermaprime.pipedrive.com/person/{new_person_id}"
        return jsonify({'url': pipedrive_url}), 200
    else:
        print("❌ Échec de la création de la personne")
        return jsonify({'error': 'Échec de la création de la personne'}), 500
