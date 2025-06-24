from flask import Flask, request, jsonify
from flask_cors import CORS
from operations_branchs.sale import sale_branchs
from operations_branchs.service import service_branche
import os
from dotenv import load_dotenv



app = Flask(__name__)
CORS(app)
load_dotenv()

@app.route('/deal-processing', methods=['POST', 'OPTIONS'])
def deal_processing():
    # Gestion des requêtes OPTIONS pour CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    try:
        data = request.get_json()
        print(f"🔗 Données reçues: {data}")

        if not data:
            return jsonify({'error': 'Aucune donnée fournie'}), 400

        deal_type = data.get('deal_type', '').strip().lower()

        if deal_type == 'vente':
            return sale_branchs(data)
        elif deal_type == 'suivi':
            return service_branche(data)
        else:
            return jsonify({'error': f"Type de transaction inconnu: '{deal_type}'"}), 400

    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return jsonify({'error': f'Erreur interne: {str(e)}'}), 500


if __name__ == '__main__':
    # Utiliser le port fourni par Cloud Run ou 8080 par défaut
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)