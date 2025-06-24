import requests

API_URL = "https://twilio-dashboard-apr.pages.dev/auto-call-status"

def is_auto_call_enabled() -> bool:
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        # status peut être 1 ou 0
        return data.get("status") == 1

    except requests.exceptions.Timeout:
        print("[is_auto_call_enabled] ⚠️ Timeout lors de la requête")
    except requests.exceptions.RequestException as e:
        print(f"[is_auto_call_enabled] ❌ Erreur de requête : {e}")
    except Exception as e:
        print(f"[is_auto_call_enabled] ❌ Erreur inattendue : {e}")

    return False
