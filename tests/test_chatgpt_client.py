from pathlib import Path
from unittest.mock import patch

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from chatgpt_client import ChatGPTClient


def test_chatgpt_client_call():
    with patch("chatgpt_client.openai") as mock_openai:
        mock_openai.ChatCompletion.create.return_value = type(
            "Resp", (), {"choices": [type("Choice", (), {"message": {"content": "result"}})()]}
        )()
        client = ChatGPTClient(api_key="key")
        result = client.complete("hello")
        assert result == "result"
        mock_openai.ChatCompletion.create.assert_called_once()
