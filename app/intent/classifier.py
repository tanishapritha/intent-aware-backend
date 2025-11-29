from transformers import pipeline
from app.config import settings
from app.utils.logger import logger

class IntentClassifier:
    def __init__(self):
        logger.info(f"Loading intent classification model: {settings.INTENT_MODEL_NAME}...")
        try:
            self.classifier = pipeline("zero-shot-classification", model=settings.INTENT_MODEL_NAME)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.classifier = None

    def predict_intent(self, text: str, candidate_labels: list) -> dict:
        if not self.classifier:
            logger.warning("Classifier not initialized. Returning default intent.")
            return {"labels": [candidate_labels[0]], "scores": [1.0]}
        
        try:
            result = self.classifier(text, candidate_labels)
            # result is like: {'sequence': '...', 'labels': ['pricing', 'technical'], 'scores': [0.9, 0.1]}
            return result
        except Exception as e:
            logger.error(f"Error predicting intent: {e}")
            return {"labels": [candidate_labels[0]], "scores": [0.0]}

# Global instance
intent_classifier = IntentClassifier()
