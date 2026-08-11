#!/usr/bin/env python3
"""Kimi SVP CALL #2 v2 -- STATE axis WITH the null-gated documentation context (the wiring).
Same context block as call-1 v2, with the STATE-layer law added: docs give IDENTITY context;
a doc's own lifecycle language is NEVER evidence of a shift (docs age; the ratified value and
the friction figures are the live inputs). Per-use egress: standing Andrew-direct authorization
(this session's continuation). Estate-structural payload only.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

import boto3

from kimi_call1_friction_v2 import build_doc_context
from kimi_call2_state import build_state_prompt

KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
KIMI_MODEL = "kimi-k3"
KIMI_SECRET_ID = "astn/kimi/api-key"
BUDGET = 16000
TIMEOUT = 300


def extend_state_prompt(base_prompt: str, ctx: dict) -> str:
    block = (
        "\n=== VERTICAL DOCUMENTATION CONTEXT (semantically retrieved, null-gated; %d docs admitted total, top shown per plane) ===\n"
        "%s\n"
        "  * LAW: these documents tell you WHAT this vertical IS (identity, purpose, architecture) --\n"
        "    directly relevant to a lifecycle read. BUT a document's own lifecycle language (a revamp\n"
        "    plan, a deprecation note, an old status line) is NEVER evidence of a shift: documents age;\n"
        "    the ratified value and the friction figures are the only live inputs. Your shift assessment\n"
        "    cites FRICTION figures.\n"
        "  * In your output, list under \"doc_context_used\" the paths (from the list above ONLY) that\n"
        "    actually informed your reading of the vertical's identity. An empty list is legal.\n"
        % (ctx["admitted_total"], json.dumps(ctx["docs"], indent=None))
    )
    schema_tail = ' "sovereignty": "PROPOSAL -- Andrew ratifies, CVO lands"}'
    assert schema_tail in base_prompt, "schema anchor line not found in base state prompt"
    out = base_prompt.replace(
        schema_tail,
        ' "sovereignty": "PROPOSAL -- Andrew ratifies, CVO lands",\n'
        ' "doc_context_used": ["<path from the context block above>", ...]}')
    anchor = "=== YOUR JOB ==="
    out = out.replace(anchor, block + "\n" + anchor)
    schema_region = out[out.find("Return ONLY JSON"):]
    assert '"doc_context_used"' in schema_region, "doc_context_used missing from the SCHEMA block"
    return out


def main() -> None:
    ctx = build_doc_context("model-portfolios")
    prompt = extend_state_prompt(build_state_prompt(), ctx)
    print("=" * 78)
    print("WIRED PROMPT (call #2 v2, state + doc context) -- %d chars, %d context paths"
          % (len(prompt), len(ctx["docs"])))
    print("=" * 78)
    key = boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(
        SecretId=KIMI_SECRET_ID)["SecretString"].strip()
    payload = json.dumps({"model": KIMI_MODEL, "temperature": 1, "max_tokens": BUDGET,
                          "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    print("LIVE CALL -> %s  model=%s  max_tokens=%d  timeout=%ds" % (KIMI_URL, KIMI_MODEL, BUDGET, TIMEOUT))
    t0 = time.monotonic()
    try:
        req = urllib.request.Request(KIMI_URL, data=payload,
                                     headers={"Authorization": "Bearer %s" % key,
                                              "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print("HTTP_%s: %s" % (e.code, e.read().decode("utf-8", "replace")[:600]))
        return
    except Exception as e:  # noqa: BLE001
        print("ERROR %.1fs: %s" % (time.monotonic() - t0, str(e)[:300]))
        return
    elapsed = round(time.monotonic() - t0, 1)
    ch = body["choices"][0]
    u = body.get("usage", {}) or {}
    det = u.get("completion_tokens_details", {}) or {}
    comp, reas = u.get("completion_tokens"), det.get("reasoning_tokens")
    print("\n" + "=" * 78)
    print("RESPONSE  elapsed=%ss  finish=%s" % (elapsed, ch.get("finish_reason")))
    print("USAGE  prompt=%s completion=%s reasoning=%s content=%s"
          % (u.get("prompt_tokens"), comp, reas,
             (comp - reas) if isinstance(comp, int) and isinstance(reas, int) else "?"))
    print("=" * 78)
    print(ch["message"].get("content") or "<EMPTY>")


if __name__ == "__main__":
    main()
