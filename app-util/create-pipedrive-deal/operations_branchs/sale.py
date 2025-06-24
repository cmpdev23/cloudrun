from utils.format_phone_number import format_phone_number
from pipedrives_operations.search_person_by_phone import search_person_by_phone
from pipedrives_operations.create_person import create_person
from pipedrives_operations.get_deals_for_person_id import get_deals_for_person_id
from pipedrives_operations.update_deals_stage_rdv import update_deal_stage
from pipedrives_operations.add_note_to_deal import add_note_to_deals
from pipedrives_operations.create_deal import create_deal
from flask import jsonify


def sale_branchs(data):
    try:
        
        phone = data.get('phone')
        if not phone:
            return jsonify({'error': 'Numéro de téléphone requis'}), 400

        phone_number = format_phone_number(phone)

        if not phone_number:
            return jsonify({'error': 'Numéro de téléphone invalide'}), 400

        person_id = search_person_by_phone(phone_number)

        if person_id:
            print(f"✅ Contact trouvé - Person ID: {person_id}")
            deal_ids = get_deals_for_person_id(person_id)

            if deal_ids:
                print(f"📋 Deals trouvés: {deal_ids}")
                update_result = update_deal_stage(deal_ids, stage_id=3)
                add_note_to_deals(deal_ids, data)
                if update_result['success']:
                    deal_id = update_result['first_deal_id']
                    pipedrive_url = f"https://comparermaprime.pipedrive.com/deal/{deal_id}"
                    return jsonify({'url': pipedrive_url}), 200
                else:
                    return jsonify({'error': 'Échec de la mise à jour des deals'}), 500
            else:
                print("❌ Aucun deal trouvé pour ce contact")
                new_deal_ids = create_deal(person_id, data)
                if new_deal_ids:
                    update_result = update_deal_stage(new_deal_ids, stage_id=3)
                    add_note_to_deals(new_deal_ids, data)
                    deal_id = update_result['first_deal_id']
                    pipedrive_url = f"https://comparermaprime.pipedrive.com/deal/{deal_id}"
                    return jsonify({'url': pipedrive_url}), 200
                else:
                    return jsonify({'error': 'Échec de la création du deal'}), 500
        else:
            print("❌ Contact non trouvé, création d'une nouvelle personne")
            new_person_id = create_person(data)
            if new_person_id:
                print(f"✅ Nouvelle personne créée - Person ID: {new_person_id}")
                new_deal_ids = create_deal(new_person_id, data)
                if new_deal_ids:
                    update_result = update_deal_stage(new_deal_ids, stage_id=3)
                    add_note_to_deals(new_deal_ids, data)
                    deal_id = update_result['first_deal_id']
                    pipedrive_url = f"https://comparermaprime.pipedrive.com/deal/{deal_id}"
                    return jsonify({'url': pipedrive_url}), 200
                else:
                    return jsonify({'error': 'Échec de la création du deal'}), 500
            else:
                return jsonify({'error': 'Échec de la création de la personne'}), 500
            
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return jsonify({'error': f'Erreur interne: {str(e)}'}), 500
        
