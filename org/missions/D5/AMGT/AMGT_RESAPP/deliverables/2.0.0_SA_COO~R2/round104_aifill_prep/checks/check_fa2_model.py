"""check_fa2_model.py -- acceptance arms for AMGT-fa-2 (the model seam and the served-inputs reader).

  PYTHONPATH=<repo root> python check_fa2_model.py
Offline: no network, no AWS. Imports lib.research.aifill.model and lib.research.aifill.inputs.
"""
from __future__ import annotations

import io
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402


def main():
    from lib.research.aifill import inputs, model

    arms = L.Arms("FA-2")
    fixture = L.web_response()
    response = fixture["response"]

    def parsed():
        r = model.parse_response(response)
        urls = [c["url"] for c in r.citations]
        return ("Christophe Fouquet" in r.text and len(set(urls)) >= 3 and len(urls) == len(set(urls)) and all(u.startswith("http") for u in urls)
                and all(set(c) >= {"url", "title", "cited_text"} for c in r.citations)), (len(r.citations), r.text[:60])
    arms.run("parse_response: text and de-duplicated cited urls", parsed)

    def parsed_counts():
        r = model.parse_response(response)
        return len(r.searches) == 2 and all(isinstance(q, str) and q for q in r.searches) and r.web_search_requests == 2 \
            and r.input_tokens > 0 and r.output_tokens > 0 and r.stop_reason == "end_turn" and isinstance(r.model, str), (r.searches, r.web_search_requests)
    arms.run("parse_response: searches, usage, stop reason, model", parsed_counts)

    def request_shape():
        seen = []

        def transport(body):
            seen.append(body)
            return response
        r = model.call_model("PROMPT", web_search_max_uses=2, transport=transport)
        body = seen[0]
        return body["model"] == model.MODEL and body["max_tokens"] == 1500 and body["messages"] == [{"role": "user", "content": "PROMPT"}] \
            and body["tools"] == [{"type": "web_search_20250305", "name": "web_search", "max_uses": 2}] and "system" not in body \
            and "Christophe Fouquet" in r.text
    arms.run("call_model request body with web search", request_shape)

    def request_no_tools():
        seen = []
        model.call_model("P", system="SYS", max_tokens=800, transport=lambda body: (seen.append(body), response)[1])
        body = seen[0]
        return "tools" not in body and body["system"] == "SYS" and body["max_tokens"] == 800
    arms.run("call_model without web search sends no tools, passes system", request_no_tools)

    def model_const():
        return model.MODEL == "claude-opus-5"
    arms.run("MODEL is the existing filings model", model_const)

    errors = [
        ("transport raises OSError", lambda: model.call_model("P", transport=lambda b: (_ for _ in ()).throw(OSError("down")))),
        ("api error body", lambda: model.call_model("P", transport=lambda b: {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}})),
        ("no content list", lambda: model.call_model("P", transport=lambda b: {"stop_reason": "end_turn"})),
        ("truncated answer (max_tokens)", lambda: model.call_model("P", transport=lambda b: dict(response, stop_reason="max_tokens"))),
        ("empty text", lambda: model.call_model("P", transport=lambda b: {"content": [], "stop_reason": "end_turn", "usage": {}})),
    ]
    for label, fn in errors:
        arms.raises("ModelError: " + label, "ModelError", fn)

    def error_message():
        try:
            model.call_model("P", transport=lambda b: {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}})
        except Exception as err:  # noqa: BLE001
            return "busy" in str(err) or "overloaded" in str(err), str(err)
        return False
    arms.run("ModelError carries the API's own message", error_message)

    def no_key_no_network():
        saved = os.environ.pop("ANTHROPIC_API_KEY", None)
        real = urllib.request.urlopen

        def forbidden(*a, **k):
            raise AssertionError("network used with no key")
        urllib.request.urlopen = forbidden
        try:
            try:
                model.call_model("P")
            except Exception as err:  # noqa: BLE001
                return type(err).__name__ == "ModelError" and "ANTHROPIC_API_KEY" in str(err), str(err)[:80]
            return False, "no error"
        finally:
            urllib.request.urlopen = real
            if saved is not None:
                os.environ["ANTHROPIC_API_KEY"] = saved
    arms.run("no key -> ModelError naming ANTHROPIC_API_KEY, before any request", no_key_no_network)

    def default_transport_headers():
        saved = os.environ.get("ANTHROPIC_API_KEY")
        os.environ["ANTHROPIC_API_KEY"] = "test-key-not-real"
        real = urllib.request.urlopen
        seen = {}

        class Resp(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        def fake(req, timeout=None):
            seen["url"] = req.full_url
            seen["headers"] = {k.lower(): v for k, v in req.header_items()}
            seen["body"] = json.loads(req.data.decode("utf-8"))
            seen["timeout"] = timeout
            return Resp(json.dumps(response).encode("utf-8"))
        urllib.request.urlopen = fake
        try:
            r = model.call_model("P", web_search_max_uses=1, timeout=33)
        finally:
            urllib.request.urlopen = real
            if saved is None:
                os.environ.pop("ANTHROPIC_API_KEY", None)
            else:
                os.environ["ANTHROPIC_API_KEY"] = saved
        h = seen.get("headers", {})
        return seen.get("url") == "https://api.anthropic.com/v1/messages" and h.get("x-api-key") == "test-key-not-real" \
            and h.get("anthropic-version") == "2023-06-01" and h.get("content-type") == "application/json" \
            and seen.get("timeout") == 33 and seen["body"]["tools"][0]["max_uses"] == 1 and "Christophe Fouquet" in r.text, seen.get("url")
    arms.run("default transport: url, headers, timeout (urlopen faked)", default_transport_headers)

    def never_logs_key():
        src = open(model.__file__, "r", encoding="utf-8").read()
        return "print(" not in src or "x-api-key" not in src.split("print(")[1][:200], "ok"
    arms.run("the key is never printed", never_logs_key)

    class FakeLambda:
        def __init__(self, bodies):
            self.bodies = bodies
            self.events = []

        def invoke(self, FunctionName, Payload):
            event = json.loads(Payload.decode("utf-8") if isinstance(Payload, bytes) else Payload)
            self.events.append((FunctionName, event))
            route = event["rawPath"].rsplit("/", 1)[1]
            spec = self.bodies[route]
            if isinstance(spec, Exception):
                raise spec
            status, body = spec
            payload = json.dumps({"statusCode": status, "body": json.dumps(body)}).encode("utf-8")
            return {"Payload": io.BytesIO(payload)}

    def served_ok():
        lam = FakeLambda({"overlay": (200, {"name": "A"}), "thesis": (200, {"management": {}})})
        out = inputs.served_inputs("ASML_NA_Equity", lam=lam)
        names = [e[0] for e in lam.events]
        paths = [e[1]["rawPath"] for e in lam.events]
        ev = lam.events[0][1]
        return out == {"overlay": {"name": "A"}, "thesis": {"management": {}}, "errors": {}} and set(names) == {"opal-amgt-scoped-api"} \
            and sorted(paths) == ["/api/scoped/amgt/security/ASML_NA_Equity/overlay", "/api/scoped/amgt/security/ASML_NA_Equity/thesis"] \
            and ev["requestContext"]["http"]["method"] == "GET" and ev["headers"]["x-firm-id"] == "opal", paths
    arms.run("served_inputs: two GET invokes, both bodies returned", served_ok)

    def served_failures():
        lam = FakeLambda({"overlay": (500, {"message": "x"}), "thesis": RuntimeError("lambda down")})
        out = inputs.served_inputs("K", lam=lam)
        return out["overlay"] is None and out["thesis"] is None and "500" in out["errors"]["overlay"] and "RuntimeError" in out["errors"]["thesis"], out["errors"]
    arms.run("served_inputs: a 500 or a raise is an error entry, body None", served_failures)

    def served_one_failure():
        lam = FakeLambda({"overlay": (200, {"name": "A"}), "thesis": (404, {})})
        out = inputs.served_inputs("K", lam=lam)
        return out["overlay"] == {"name": "A"} and out["thesis"] is None and list(out["errors"]) == ["thesis"]
    arms.run("served_inputs: one route failing leaves the other served", served_one_failure)

    def no_sdk():
        return "anthropic" not in sys.modules, "anthropic imported"
    arms.run("the anthropic SDK was never imported (0.45 cannot parse server-tool blocks)", no_sdk)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
