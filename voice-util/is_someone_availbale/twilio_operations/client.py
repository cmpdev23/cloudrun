# twilio_operations/client.py

import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


class TwilioClient:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.workspace_sid = os.getenv("TWILIO_WORKSPACE_SID")

        if not self.account_sid or not self.auth_token:
            raise Exception("⚠️ Credentials Twilio manquants.")

        self.client = Client(self.account_sid, self.auth_token)

    @property
    def auth(self):
        return (self.account_sid, self.auth_token)

    def update_worker_activity(self, worker_sid: str, activity_sid: str):
        try:
            worker = self.client.taskrouter.workspaces(self.workspace_sid).workers(worker_sid).update(
                activity_sid=activity_sid
            )
            return {
                "success": True,
                "worker_sid": worker.sid,
                "activity_sid": activity_sid
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
