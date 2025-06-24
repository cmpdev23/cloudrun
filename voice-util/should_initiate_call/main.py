import os
import logging
from flask import Flask, request, jsonify, abort, make_response
from utils.office_hours import is_office_hour
from utils.is_someone_available import is_someone_available
from utils.is_auto_call_enabled import is_auto_call_enabled
from dotenv import load_dotenv

# 📌 Chargement des variables d'environnement
load_dotenv()

# 📘 Configuration du logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 🧱 Initialisation de l'app Flask
app = Flask(__name__)
request_key = os.getenv("REQUEST_KEY")

# 🔐 Vérification du token avant chaque requête
@app.before_request
def verify_api_key():
    if request.headers.get("X-API-KEY") != request_key:
        logger.warning("Tentative d'accès sans clé valide")
        abort(403)

# 🔍 Route principale : détermine si un appel peut être lancé
@app.route("/", methods=["GET"])
def should_initiate_call():
    try: 
        if not is_office_hour():
            logger.info("⛔ En dehors des heures.")
            return make_response(jsonify({"allowed": False, "reason": "out_of_hours"}), 200)

        if not is_auto_call_enabled():
            logger.info("⛔ Appels automatiques désactivés.")
            return make_response(jsonify({"allowed": False, "reason": "auto_call_disabled"}), 200)

        if not is_someone_available(request_key):
            logger.info("⛔ Personne n’est dispo.")
            return make_response(jsonify({"allowed": False, "reason": "no_available_agent"}), 200)

    except Exception as e:
        logger.exception("[should_initiate_call] ❌ Erreur serveur:")
        return make_response(jsonify({
            "allowed": False,
            "error": str(e)
        }), 500)

    logger.info("✅ Appel autorisé.")
    return make_response(jsonify({"allowed": True}), 200)

# 🔁 Lancement local
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
