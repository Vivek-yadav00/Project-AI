import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
@patch("app.services.ai_pipeline.process_sms", new_callable=AsyncMock)
def test_incoming_sms(mock_process_sms, client):
    mock_process_sms.return_value = "Hello, this is DadaAI!"
    
    response = client.post(
        "/api/v1/sms/incoming",
        json={"from_number": "+1234567890", "body": "Namaste"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["to"] == "+1234567890"
    assert data["body"] == "Hello, this is DadaAI!"

def test_get_sms_history_not_found(client):
    response = client.get("/api/v1/sms/history/+9999999999")
    assert response.status_code == 404
