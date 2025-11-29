# Intent-Aware Routing Engine

This is a production-ready FastAPI backend for an AI-powered routing engine that integrates with Zoho SalesIQ and Zoho Cliq.

## Architecture

- **Framework**: FastAPI
- **Intent Classification**: Zero-shot BART (`facebook/bart-large-mnli`)
- **Routing Logic**: Weighted score based on Skill (70%) and Language (30%)
- **Integrations**: Zoho SalesIQ (Assignment), Zoho Cliq (Notification)

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory with the following variables:
    ```env
    SALESIQ_AUTH_TOKEN=your_salesiq_token
    CLIQ_WEBHOOK_TOKEN=your_cliq_token
    CLIQ_CHANNEL_URL=your_cliq_webhook_url
    CRM_API_KEY=your_crm_key
    ```

3.  **Run the Server**:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

## API Endpoints

### `POST /webhook`

Receives a webhook from SalesIQ.

**Payload:**
```json
{
    "visitor_id": "string",
    "message": "string",
    "language": "string"
}
```

**Response:**
```json
{
    "status": "ok",
    "assigned_to": "Agent Name",
    "intent": "predicted_intent"
}
```

## Testing

You can test the webhook using `curl` or Postman with the `test_webhook.json` payload.

```bash
curl -X POST "http://localhost:8000/webhook" \
     -H "Content-Type: application/json" \
     -d @test_webhook.json
```
