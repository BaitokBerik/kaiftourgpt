import gpt_module


def test_ask_gpt_inserts_system_prompt(monkeypatch):
    captured = {}

    def fake_create(model, messages):
        captured['messages'] = messages
        return {"choices": [{"message": {"content": "mocked content"}}]}

    monkeypatch.setattr(gpt_module.openai.ChatCompletion, 'create', fake_create)
    messages = []
    result = gpt_module.ask_gpt(messages)

    assert result == "mocked content"
    assert messages[0] == gpt_module.SYSTEM_PROMPT
    assert captured['messages'][0] == gpt_module.SYSTEM_PROMPT
