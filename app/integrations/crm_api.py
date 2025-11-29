from app.utils.logger import logger

class CRMAPI:
    @staticmethod
    def get_customer_tier(visitor_id: str) -> str:
        """
        Mock CRM lookup to get customer tier (e.g., premium, standard).
        """
        logger.info(f"Looking up CRM data for visitor {visitor_id}...")
        # Mock logic
        if visitor_id.endswith("9"):
            return "premium"
        return "standard"

crm_client = CRMAPI()
