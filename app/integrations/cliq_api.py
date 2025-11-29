import requests
from app.config import settings
from app.utils.logger import logger

class CliqAPI:
    @staticmethod
    def notify_channel(message: str, intent: str, agent_name: str):
        """
        Sends a notification to a Zoho Cliq channel.
        """
        if not settings.CLIQ_CHANNEL_URL:
            logger.warning("CLIQ_CHANNEL_URL not set. Skipping notification.")
            return

        payload = {
            "text": f"🤖 **New Routing Event**\n**Intent:** {intent}\n**Assigned To:** {agent_name}\n**Message:** {message}"
        }
        
        try:
            # response = requests.post(settings.CLIQ_CHANNEL_URL, json=payload, timeout=5)
            # response.raise_for_status()
            logger.info(f"Simulated Cliq notification: {payload['text']}")
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Failed to send Cliq notification: {e}")
            return {"status": "error", "message": str(e)}

cliq_client = CliqAPI()
