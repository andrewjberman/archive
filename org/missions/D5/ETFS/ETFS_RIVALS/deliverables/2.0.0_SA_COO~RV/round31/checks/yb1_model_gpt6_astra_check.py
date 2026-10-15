"""RIV-yb-1 checks (round 31): the rivalfunds AI writer runs on `gpt-6-astra`, and the request it sends is one that model accepts.
Authority: Andrew at the 2.0.0_SA_COO~RV terminal, 2026-10-15 ~16:5x ET: "the openai model being used for that analysis should be
updated from 5.4 to 6 because it needs to be smarter and not make mistakes on figure representations" ("gpt 6 astra").

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: `requests.post` and the `openai` SDK are replaced by recorders; no network, no Secrets Manager. MEASURED by the issuer
2026-10-15 against the live API with the project key: `gpt-6-astra` is listed; a chat completion with `response_format` json_object
and NO `temperature` returns 200; the same request with `temperature: 0.2` returns HTTP 400 "'temperature' does not support 0.2 with
this model. Only the default (1) value is supported". `gpt-5.4` accepts both. The rule this file pins:
  * `ai_accounts.DEFAULT_MODEL` is "gpt-6-astra" when RIVALFUNDS_AI_MODEL is unset, and the env var still overrides it;
  * `ai_client.RestClient.chat` (the Lambda's path) sends a `temperature` key ONLY for a model whose name starts with "gpt-5"
    (value 0.2, as today); for "gpt-6-astra" and any other model the key is absent;
  * `ai_accounts.OpenAIClient.chat` (the seat's SDK path) follows the same rule: `temperature=0.2` only for a "gpt-5" model;
  * everything else in the request (model, messages, response_format json_object) is unchanged for both models.
"""
import importlib
import sys
import types

from rivalfunds import ai_accounts, ai_client


class _Resp:
    def __init__(self):
        self.status_code = 200

    def raise_for_status(self):
        return None

    def json(self):
        return {"choices": [{"message": {"content": "{}"}}]}


def _rest_body(monkeypatch, model):
    seen = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        seen["json"] = json
        return _Resp()

    import requests

    monkeypatch.setattr(requests, "post", fake_post)
    ai_client.RestClient("k").chat([{"role": "user", "content": "x"}], model)
    return seen["json"]


def test_ac1_the_default_model_is_gpt_6_astra_and_the_env_var_still_overrides(monkeypatch):
    monkeypatch.delenv("RIVALFUNDS_AI_MODEL", raising=False)
    assert importlib.reload(ai_accounts).DEFAULT_MODEL == "gpt-6-astra"
    monkeypatch.setenv("RIVALFUNDS_AI_MODEL", "gpt-5.4")
    assert importlib.reload(ai_accounts).DEFAULT_MODEL == "gpt-5.4"
    monkeypatch.delenv("RIVALFUNDS_AI_MODEL", raising=False)
    importlib.reload(ai_accounts)


def test_ac2_the_lambda_client_sends_no_temperature_to_gpt_6_astra_and_keeps_it_for_gpt_5(monkeypatch):
    b6 = _rest_body(monkeypatch, "gpt-6-astra")
    assert "temperature" not in b6 and b6["model"] == "gpt-6-astra" and b6["response_format"] == {"type": "json_object"}
    assert b6["messages"] == [{"role": "user", "content": "x"}]
    b5 = _rest_body(monkeypatch, "gpt-5.4")      # the difference control: the old model still gets the old request
    assert b5["temperature"] == 0.2 and b5["model"] == "gpt-5.4" and b5["response_format"] == {"type": "json_object"}


def test_ac2_the_seat_sdk_client_follows_the_same_rule(monkeypatch):
    calls = []

    class _Comp:
        def create(self, **kw):
            calls.append(kw)
            return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="{}"))])

    class _OpenAI:
        def __init__(self, api_key=None):
            self.chat = types.SimpleNamespace(completions=_Comp())

    monkeypatch.setitem(sys.modules, "openai", types.SimpleNamespace(OpenAI=_OpenAI))
    c = ai_accounts.OpenAIClient("k")
    c.chat([{"role": "user", "content": "x"}], "gpt-6-astra")
    c.chat([{"role": "user", "content": "x"}], "gpt-5.4")
    assert "temperature" not in calls[0] and calls[0]["model"] == "gpt-6-astra" and calls[0]["response_format"] == {"type": "json_object"}
    assert calls[1]["temperature"] == 0.2 and calls[1]["model"] == "gpt-5.4"
