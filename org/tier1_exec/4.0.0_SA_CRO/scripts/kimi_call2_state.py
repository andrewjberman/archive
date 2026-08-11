#!/usr/bin/env python3
"""Kimi SVP CALL #2 -- STATE axis (R2). Chains from call #1's friction output.
STATE = does the vertical's ratified lifecycle_value appear to be SHIFTING? Kimi PROPOSES; Andrew
ratifies; CVO lands (the sovereignty triangle, design s.8.1). Per-use egress authorized (spec work).
"""
from __future__ import annotations
import json
import time
import urllib.error
import urllib.request
import boto3

KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
KIMI_MODEL = "kimi-k3"
KIMI_SECRET_ID = "astn/kimi/api-key"
STATE_BUDGET = 16000
STATE_TIMEOUT = 300

# ---- INPUT: call #1's friction output (the CONSOLIDATING result, verbatim) + the ratified baseline ----
FRICTION = {
    "vertical": "mdpf", "friction_character": "CONSOLIDATING", "direction": "DIVERGING",
    "summary": ("F2's consolidation subsignal: work consolidated onto the live gold path (hot 0.90-0.998 "
                "across 6 windows) while the one-off backfill cooled to 0.554; commit-volume 5.0x newer-vs-"
                "older = accelerating. F1: mdpf's changed files belong to only 2 of 14 C3.i structures "
                "(own refinery + shared serving spine) -- contained, not spreading. F4: concentrated single-"
                "owner (DS 88.8%), low cross-type contention, consistent with consolidation, not abandonment."),
    "cites": ["F2", "F1", "F4"],
    "blind_spots": ["F3: operator-input capture (B6) unbuilt -- operator intent UNMEASURED, not calm"],
    "confidence": "HIGH",
    "confidence_reason": "3 of 4 axes measured (F1,F2,F4) converge on consolidation; F3 dark",
}
CURRENT_LIFECYCLE = "PERMANENT"   # mdpf, Andrew-ratified 2026-08-06 (Phase-0 sitting, 17 of 28)
LIFECYCLE_ENUM = "PERMANENT | TRANSIENT | EVENT_CREATED | DORMANT | LEGACY | RETIRED | UNDECLARED"


def build_state_prompt() -> str:
    return (
        "You are proposing a LIFECYCLE assessment for ONE semantic vertical of a cloud data estate,\n"
        "from its friction characterization. This is the STATE layer: does the vertical's lifecycle_value\n"
        "appear to be SHIFTING from its current ratified value?\n"
        "YOU PROPOSE. YOU DO NOT ASSERT. lifecycle_class is producer-asserted by ratified law; Andrew\n"
        "ratifies your proposal, CVO lands it. You may never declare a value as fact.\n"
        "VERTICAL: mdpf\n\n"
        "=== CURRENT RATIFIED LIFECYCLE VALUE (the baseline you assess a shift FROM) ===\n"
        "mdpf = %s  (Andrew-ratified 2026-08-06)\n"
        "enum: %s\n\n"
        "=== THE FRICTION CHARACTERIZATION (from the friction axis -- deterministic instruments translated) ===\n"
        "%s\n\n"
        "=== HOW TO READ THIS -- the distinction the whole layer turns on ===\n"
        "  * Friction is CHANGE DYNAMICS. Lifecycle is WHAT THE VERTICAL IS. They are NOT the same axis.\n"
        "  * A PERMANENT vertical under active development -- heating, consolidating onto its OWN live\n"
        "    path -- is HEALTHY PERMANENCE, NOT a lifecycle shift. Busy does not mean transitioning.\n"
        "  * A real shift needs friction pointing AWAY from the current value: e.g. a LEGACY vertical whose\n"
        "    work is consolidating onto a REPLACEMENT route (LEGACY->RETIRED), or one going quiet (->DORMANT).\n"
        "  * THE DANGEROUS DIRECTION (rule-bank law): proposing decline (DORMANT/LEGACY/RETIRED) on a\n"
        "    healthy, active system -- reporting a live thing as dead. Do NOT shift a PERMANENT vertical\n"
        "    toward decline because it is busy. Under-calling a real shift is recoverable; a false decline\n"
        "    proposes deleting a live system.\n"
        "  * NO-SHIFT is a valid, common, and often correct verdict. State it with its denominator (which\n"
        "    axes measured), never leave it silent. An UNMEASURED axis (F3) caps your confidence; name it.\n"
        "  * Cite the friction figure(s) each part of your assessment rests on.\n\n"
        "=== YOUR JOB ===\n"
        "Propose whether mdpf's lifecycle_value is shifting from %s.\n"
        "Return ONLY JSON:\n"
        '{"vertical": "mdpf",\n'
        ' "current": "%s",\n'
        ' "proposed": "<enum value -- MAY equal current; equal is the common case>",\n'
        ' "shift": "NONE | IN-PROGRESS | PROPOSED",\n'
        ' "summary": "2-4 plain sentences, each citing the friction figure it rests on",\n'
        ' "cites": ["friction.character", "friction.F1", ...],\n'
        ' "confidence": "HIGH|MEDIUM|LOW",\n'
        ' "confidence_reason": "which axes measured; what is dark",\n'
        ' "sovereignty": "PROPOSAL -- Andrew ratifies, CVO lands"}\n\n'
        "ASCII only. No em-dashes, no smart quotes."
        % (CURRENT_LIFECYCLE, LIFECYCLE_ENUM, json.dumps(FRICTION, indent=1),
           CURRENT_LIFECYCLE, CURRENT_LIFECYCLE)
    )


def main() -> None:
    prompt = build_state_prompt()
    print("=" * 78)
    print("CANONICAL PROMPT (call #2 STATE) -- %d chars" % len(prompt))
    print("=" * 78)
    print(prompt)
    print("=" * 78)
    key = boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(
        SecretId=KIMI_SECRET_ID)["SecretString"].strip()
    payload = json.dumps({"model": KIMI_MODEL, "temperature": 1, "max_tokens": STATE_BUDGET,
                          "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    print("LIVE CALL -> %s  model=%s  max_tokens=%d" % (KIMI_URL, KIMI_MODEL, STATE_BUDGET))
    t0 = time.monotonic()
    try:
        req = urllib.request.Request(KIMI_URL, data=payload,
                                     headers={"Authorization": "Bearer %s" % key,
                                              "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=STATE_TIMEOUT) as resp:
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
