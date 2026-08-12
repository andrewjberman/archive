#!/usr/bin/env python3
"""Kimi SVP CALL #1 v2 -- FRICTION axis WITH the null-gated documentation context (the wiring).
Extends the established call-1 canonical form (same envelope, same battery) with a
VERTICAL DOCUMENTATION CONTEXT block sourced from the v2 semantic scan artifact (BM25 axis,
family-wise null-gated admits, plane-labeled). Per-use egress: the standing Andrew-direct
spec-work authorization (continued this session: "get back to the Semantic Scan and Vertical
work for the Kimi pipeline"). Estate-structural payload only.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

import boto3

from kimi_call1_friction import BATTERY, build_friction_prompt  # the established canonical form

KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
KIMI_MODEL = "kimi-k3"
KIMI_SECRET_ID = "astn/kimi/api-key"
BUDGET = 16000
TIMEOUT = 300

WS = r"C:\Users\AndrewBerman\Desktop\ajb_workspace"
SCAN = os.path.join(WS, "org/tier1_exec/4.0.0_SA_CRO/deliverables/C3II_SEMANTIC_SCAN_V2_OUTPUT_20260811.json")
PLANE_CAPS = {"docs": 5, "projects": 3, "logs": 3}


def build_doc_context(vertical_key: str) -> dict:
    scan = json.load(open(SCAN, encoding="utf-8"))
    e = scan["verticals"][vertical_key]
    admitted = e["admitted"]["bm25"]
    picked, counts = [], {}
    for d in admitted:
        pl = d["plane"]
        if counts.get(pl, 0) < PLANE_CAPS[pl]:
            picked.append(d)
            counts[pl] = counts.get(pl, 0) + 1
        if all(counts.get(p, 0) >= c for p, c in PLANE_CAPS.items()):
            break
    return {
        "scan_vertical": vertical_key,
        "alias_note": "battery vertical 'mdpf' maps to scan vertical 'model-portfolios' (Andrew merged mdpf into model-portfolios 2026-08-07; resolver drift declared)",
        "retrieval": "BM25, family-wise null-gated (alpha=0.05 expected false admits over 5865 docs); semantic axis retired at gate severity (measured; positive-controlled)",
        "admitted_total": len(admitted),
        "docs": [{"path": d["path"], "plane": d["plane"], "bm25": d["score"]} for d in picked],
    }


def extend_prompt(base_prompt: str, ctx: dict) -> str:
    block = (
        "\n=== VERTICAL DOCUMENTATION CONTEXT (semantically retrieved, null-gated; %d docs admitted total, top shown per plane) ===\n"
        "%s\n"
        "  * LAW: these documents tell you WHAT this vertical IS (identity, purpose, architecture).\n"
        "    They are NOT friction evidence. Your friction characterization cites F-figures ONLY.\n"
        "  * In your output, list under \"doc_context_used\" the paths (from the list above ONLY) that\n"
        "    actually informed your reading of the vertical's identity. An empty list is legal.\n"
        % (ctx["admitted_total"], json.dumps(ctx["docs"], indent=None))
    )
    schema_tail = ' "confidence_reason": "e.g. 2 of 4 axes measured; direction unwired"}'
    assert schema_tail in base_prompt, "schema anchor line not found in base prompt"
    out = base_prompt.replace(
        schema_tail,
        ' "confidence_reason": "e.g. 2 of 4 axes measured; direction unwired",\n'
        ' "doc_context_used": ["<path from the context block above>", ...]}')
    anchor = "=== YOUR JOB ==="
    out = out.replace(anchor, block + "\n" + anchor)
    # assert on the SCHEMA REGION, not the whole prompt -- the law bullet also names the field, and
    # a whole-prompt substring check passes on that confirming limb (measured: fire #1 shipped a
    # schema without the field while the assert read green off the prose mention).
    schema_region = out[out.find("Return ONLY JSON"):]
    assert '"doc_context_used"' in schema_region, "doc_context_used missing from the SCHEMA block"
    return out


def main() -> None:
    ctx = build_doc_context("model-portfolios")
    prompt = extend_prompt(build_friction_prompt(BATTERY), ctx)
    assert '"doc_context_used"' in prompt, "output-schema extension failed to land in prompt"
    print("=" * 78)
    print("WIRED PROMPT (call #1 v2, friction + doc context) -- %d chars" % len(prompt))
    print("doc context block: %d paths (%s)" % (len(ctx["docs"]),
          ", ".join(sorted({d["plane"] for d in ctx["docs"]}))))
    for d in ctx["docs"]:
        print("   [%s] %.1f  %s" % (d["plane"], d["bm25"], d["path"]))
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
    print("USAGE  prompt=%s completion=%s reasoning=%s content=%s total=%s"
          % (u.get("prompt_tokens"), comp, reas,
             (comp - reas) if isinstance(comp, int) and isinstance(reas, int) else "?", u.get("total_tokens")))
    print("=" * 78)
    print(ch["message"].get("content") or "<EMPTY>")


if __name__ == "__main__":
    main()
