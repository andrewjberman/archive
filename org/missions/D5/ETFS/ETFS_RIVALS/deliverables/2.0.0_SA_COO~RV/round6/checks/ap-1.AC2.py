"""RIV-ap-1 AC2: the Lambda's AI client is SDK-free, using `requests`, which the layer already carries (build ladder rung 5).
`ai_client.RestClient(api_key).chat(messages, model)` (new module `rivalfunds/ai_client.py`) POSTs to https://api.openai.com/v1/chat/completions with
`Authorization: Bearer <key>`, the model, the messages, `response_format` {"type": "json_object"} and temperature 0.2, and
returns choices[0].message.content. `ai_client.default_client()`, with the gate and the secret name set, returns a RestClient
built from the secret's `api_key`, read at call time from Secrets Manager.
Offline: `requests.post` and `boto3.client` are stubbed."""
import json
import os
import pathlib
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    import requests

    from rivalfunds import ai_client as ai

    sent = {}

    class Resp:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": '{"text": "ok"}'}}]}

    def fake_post(url, headers=None, json=None, timeout=None, **k):  # noqa: A002 -- requests' own keyword
        sent.update(url=url, headers=headers or {}, body=json or {}, timeout=timeout)
        return Resp()

    requests.post = fake_post
    out = ai.RestClient("k-123").chat([{"role": "user", "content": "x"}], "gpt-5.4")
    print("sent:", sent.get("url"), {k: sent.get("body", {}).get(k) for k in ("model", "response_format", "temperature")})
    v.check(out == '{"text": "ok"}' and sent.get("url") == "https://api.openai.com/v1/chat/completions"
            and sent["headers"].get("Authorization") == "Bearer k-123" and sent["body"].get("model") == "gpt-5.4"
            and sent["body"].get("response_format") == {"type": "json_object"} and sent["body"].get("temperature") == 0.2,
            "RestClient.chat posts the documented request and returns the message content")

    fake_boto3 = types.ModuleType("boto3")
    asked = []

    class SM:
        def get_secret_value(self, SecretId):  # noqa: N803 -- boto3's own keyword
            asked.append(SecretId)
            return {"SecretString": json.dumps({"api_key": "k-from-secret"})}

    fake_boto3.client = lambda svc, **k: SM()
    sys.modules["boto3"] = fake_boto3
    os.environ["RIVALFUNDS_AI_ENABLE"] = "1"
    os.environ["RIVALFUNDS_OPENAI_SECRET"] = "fixture/openai"
    cl = ai.default_client()
    print("default_client:", type(cl).__name__, "| secret asked:", asked)
    v.check(isinstance(cl, ai.RestClient) and asked == ["fixture/openai"],
            "default_client builds a RestClient from the named secret, read at call time")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
