from dotenv import load_dotenv
import os

load_dotenv()

api_token = os.getenv("API_TOKEN")
if not api_token:
    raise ValueError("API_TOKEN is not set in the environment variables.")


base_url = "https://api.pipedrive.com/api/v2"