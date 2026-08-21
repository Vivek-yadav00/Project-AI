import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
@patch("app.core.tts.text_to_speech", new_callable=AsyncMock)
def test_process_tts(mock_tts, client):
    mock_tts.return_value = b"fake audio data"
    
    response = client.post(
        "/api/v1/voice/tts",
        json={"text": "Namaste", "language": "hi"}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert response.content == b"fake audio data"
