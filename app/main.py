from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from app.config import settings
from app.utils.logger import logger
from app.utils.preprocess import clean_text
from app.intent.classifier import intent_classifier
from app.router.agent_router import agent_router
from app.integrations.salesiq_api import salesiq_client
from app.integrations.cliq_api import cliq_client
from app.integrations.crm_api import crm_client

app = FastAPI(title="Intent-Aware Routing Engine")

class WebhookPayload(BaseModel):
    visitor_id: str
    message: str
    language: str = "en"  # Default to English if not provided

@app.get("/")
def health_check():
    return {"status": "running", "service": "Intent-Aware Routing Engine"}

@app.post("/webhook")
async def handle_webhook(payload: WebhookPayload):
    try:
        logger.info(f"Received webhook for visitor: {payload.visitor_id}")
        
        # 1. Preprocess text
        cleaned_message = clean_text(payload.message)
        if not cleaned_message:
            logger.warning("Empty message received.")
            return {"status": "ignored", "reason": "empty_message"}

        # 2. Predict Intent
        # Candidate labels based on the prompt
        candidate_labels = ["pricing", "technical", "complaint", "demo", "refund", "billing"]
        prediction = intent_classifier.predict_intent(cleaned_message, candidate_labels)
        
        top_intent = prediction['labels'][0]
        confidence = prediction['scores'][0]
        logger.info(f"Predicted Intent: {top_intent} (Confidence: {confidence:.2f})")

        # 3. Route to Best Agent
        best_agent = agent_router.find_best_agent(top_intent, payload.language)
        
        if not best_agent:
            logger.warning("No suitable agent found.")
            # Fallback logic could go here
            return {"status": "ok", "message": "No agent available"}

        logger.info(f"Routing to agent: {best_agent['name']} ({best_agent['id']})")

        # 4. Assign Chat via SalesIQ
        salesiq_client.assign_agent(payload.visitor_id, best_agent['salesiq_id'])

        # 5. Notify via Cliq
        cliq_client.notify_channel(
            message=cleaned_message,
            intent=top_intent,
            agent_name=best_agent['name']
        )

        return {"status": "ok", "assigned_to": best_agent['name'], "intent": top_intent}

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
