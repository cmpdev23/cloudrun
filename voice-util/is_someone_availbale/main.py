import os
from flask import Flask, request, jsonify, abort
from twilio_operations.client import TwilioClient

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")
AVAILABLE_SID = "WA7dcc5e18ef0ea61a2b2a5c548155d4e8"

@app.before_request
def verify_api_key():
    if request.headers.get("X-API-KEY") != API_KEY:
        abort(403)

@app.route("/", methods=["GET"])
def check_availability():
    try:
        client = TwilioClient()
        workspace = client.client.taskrouter.workspaces(client.workspace_sid)
        workers = workspace.workers.list()

        available = any(w.activity_sid == AVAILABLE_SID for w in workers)

        raw_data = [
            {
                "friendly_name": w.friendly_name,
                "sid": w.sid,
                "activity_sid": w.activity_sid,
                "activity_name": w.activity_name
            } for w in workers
        ]

        return jsonify({
            "available": available,
            "twilio_raw": raw_data
        })

    except Exception as e:
        return jsonify({
            "available": False,
            "error": str(e)
        }), 500



if __name__ == '__main__':
    # Utiliser le port fourni par Cloud Run ou 8080 par défaut
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)