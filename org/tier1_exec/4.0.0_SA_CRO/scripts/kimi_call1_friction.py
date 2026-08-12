#!/usr/bin/env python3
"""Kimi SVP CALL #1 -- FRICTION axis. Canonical-form spec + LIVE exercise.
Mirrors estate_report_runner.call_kimi_sub (single user msg, temp=1, JSON out, Bearer/SecretsMgr).
Per-use egress authorized by Andrew-direct 2026-08-11 (spec work). Estate-structural payload only.
"""
from __future__ import annotations
import json
import time
import urllib.request
import urllib.error
import boto3

KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
KIMI_MODEL = "kimi-k3"
KIMI_SECRET_ID = "astn/kimi/api-key"
FRICTION_BUDGET = 16000     # small task != small budget (kimi-k3 meters reasoning+content one budget)
FRICTION_TIMEOUT = 300      # a MEASUREMENT window, not a derived answer

# ---- CANONICAL INPUT CONTRACT: the F1-F4 friction battery for ONE vertical ----
# F2 + F4 measured REAL this session; F1 + F3 declared UNMEASURED (true build state).
BATTERY = {
    "window": "trailing 14 days (2026-07-28 .. 2026-08-11)",
    "vertical": "mdpf",
    "changed_in_window_note": "mdpf gold tree is actively changing (see F2 hottest)",
    "friction": {
        "F1_blast_overlap": {
            "status": "MEASURED",
            "axis_content": "STRUCTURAL MEMBERSHIP breadth -- how many of the 14 C3.i structures this vertical's OWN in-window changed files BELONG to. NOT blast/reachability (CVO steer: blast would count structures a change only PROPAGATES to, inflating the number).",
            "instrument": "family-membership join: mdpf in-window changed files -> chain.family (dual key family->C3.i) -> C3.i structure",
            "source": "family membership, graph-derived (resolver family key now; re-homes to comp-kuzu / B-9 mechanical half on landing -- same relation, live derivation, zero semantic change)",
            "structures_touched": 2,
            "of": 14,
            "which": [
                {"structure": "sys-cot-mdpf-assets", "kind": "FIRM-MEDALLION", "in_window_changed_files": 40,
                 "note": "mdpf's own data refinery (family cot-and-mdpf)"},
                {"structure": "sys-partner-serving-platform", "kind": "SERVING-PLATFORM, SHARED (spans 6 verticals)", "in_window_changed_files": 30,
                 "note": "the shared partner-serving spine -- mdpf's serving side (mdpf-manifest lambda, gold-calendar layer, publisher)"},
            ],
            "boundary_declaration": "F1 = |distinct C3.i structures whose MEMBERSHIP includes an in-window mdpf changed file| of 14. MEMBERSHIP, not reachability. 2 of 14 = structurally CONTAINED to mdpf's own 2 structures, spanning the data->serving seam; one of the two (serving-platform) is SHARED across 6 verticals. failure_direction: none on the count. Cross-vertical IMPACT is a separate reachability question, deliberately excluded.",
        },
        "F2_heat_trajectory": {
            "status": "MEASURED",
            "instrument": "comp-heat freshness (snapshot, scores-only) + comp-heat compare (6 x 7d window series)",
            "snapshot": {"mean_score": 0.497, "half_life_days": 30, "paths_scanned": 57},
            "hottest": [
                {"path": "data/mdpf/scripts/gold/build_portal_gold_accrual.py", "score": 0.998, "age_days": 0.08},
                {"path": "data/mdpf/scripts/gold/build_mdpf_spine.py", "score": 0.993, "age_days": 0.32},
            ],
            "trajectory_series_newest_first": [
                {"w7d": 0, "heat": 0.998, "commits": 22}, {"w7d": 1, "heat": 0.997, "commits": 21},
                {"w7d": 2, "heat": 0.921, "commits": 43}, {"w7d": 3, "heat": 0.991, "commits": 10},
                {"w7d": 4, "heat": 0.904, "commits": 4}, {"w7d": 5, "heat": 0.900, "commits": 3},
            ],
            "trajectory_ratios_newer_half_vs_older_half": {
                "commit_volume": 5.0, "heat": 1.04,
                "rule": "comp-heat compare's own rule: <0.8x=CONVERGING, >1.25x=DIVERGING, else PARALLEL"},
            "consolidation_subsignal": "the vertical's active(gold) path stays hot (0.90-0.998 across all 6 windows) while its one-off(backfill) path cooled to 0.554 with ~0 commits in mid-windows, then only sporadic recent touches -- work has consolidated onto the live gold path (NOT the vertical cooling)",
            "trajectory_direction": "DERIVE-FROM-SERIES",
            "boundary_declaration": "trajectory = the vertical's OWN active-tree heat+commit series over 6x7d windows (comp-heat compare; SCORES + COMMIT-COUNTS, bands excluded); NOT a cross-vertical comparison. The newer/older RATIOS are deterministic; the DIRECTION LABEL is left to you to translate from the series. failure_direction: none on the series itself.",
        },
        "F3_operator_signal": {
            "status": "UNMEASURED",
            "value": None,
            "boundary_declaration": "the operator-input capture uploader (B6) is UNBUILT (design s.9.1); zero in-window operator utterances captured for this vertical. failure_direction: silent-toward-reading-calm (absence of captured input is not absence of operator attention).",
        },
        "F4_co_movement": {
            "status": "MEASURED",
            "grain": "PER-VERTICAL, file-scoped to mdpf (who moves this vertical's files)",
            "instrument": "comp-cochange file data/mdpf --since '42 days ago'",
            "files_scanned": 38,
            "file_touches": 170,
            "agent_type_attribution": {"DS": 151, "AE": 12, "SA": 5, "AB": 2},
            "ds_share_pct": 88.8,
            "ownership": "CONCENTRATED single-owner (DS 88.8%)",
            "cross_type_seams": [
                {"file": "mdpf_aggregate_aua.py", "types": {"AE": 5, "DS": 4}},
                {"file": "build_aggregate_aua_timeseries.py", "types": {"SA": 1, "DS": 1}},
                {"file": "build_legacy_compat_emit.py", "types": {"DS": 1, "AE": 1}},
            ],
            "boundary_declaration": "agent-type attribution PER mdpf file (who commits mdpf's own files) -- NOW mdpf-scoped, replacing the estate-wide matrix. A per-vertical concentration/coupling signal, NOT cross-artifact blast (that is F1). failure_direction: none -- a concentrated single-owner read is a real low-cross-type-contention signal, not an absence of coupling; do NOT read 88.8% one-owner as abandonment (F2 shows the vertical is hot).",
        },
    },
}


def build_friction_prompt(b: dict) -> str:
    f = b["friction"]
    def blk(axis, title, body):
        return "%s %s\n  %s\n" % (axis, title, body)
    def render(a):
        return json.dumps(a, indent=None)
    return (
        "You are assessing the CHANGE DYNAMICS -- the FRICTION -- of ONE vertical in a cloud data estate.\n"
        "Only this vertical. Only its friction. You are NOT proposing any change or lifecycle value.\n"
        "WINDOW: %s\nVERTICAL: %s\n\n"
        "=== THE FRICTION BATTERY (deterministic instruments; every figure carries its denominator, vintage, and boundary_declaration) ===\n"
        "%s\n%s\n%s\n%s\n"
        "=== HOW TO READ THIS BATTERY ===\n"
        "  * Each axis is a DETERMINISTIC measurement, not your judgment. You TRANSLATE the numbers; you do not re-measure.\n"
        "  * An axis marked UNMEASURED is an ABSENCE OF MEASUREMENT, never a zero. It is a declared BLIND SPOT.\n"
        "    You must NAME it as a blind spot and must NOT read it as calm, stable, or quiet.\n"
        "  * Cite the specific F-figure(s) each part of your characterization rests on. A characterization that\n"
        "    cannot cite a figure is not permitted.\n\n"
        "=== YOUR JOB ===\n"
        "From ONLY the figures above, characterize this vertical's friction: is it HEATING / SPREADING /\n"
        "CONSOLIDATING / STABLE / BEING-ABANDONED / INDETERMINATE, and in what DIRECTION (diverging / converging /\n"
        "flat / undetermined)? Keep it to the evidence -- do NOT reason beyond the figures, do NOT propose a\n"
        "lifecycle value (that is the next call), do NOT invent an axis that was not measured.\n\n"
        "PRECEDENCE RULE (the enum permits ONE character, and a vertical can honestly be several at once --\n"
        "two fires on this identical battery returned HEATING and CONSOLIDATING, both defensible, so the\n"
        "convention is stated rather than left to chance):\n"
        "  * CHARACTER is carried by the CONSOLIDATION/SPREAD evidence -- where the work is going. If a\n"
        "    consolidation subsignal is present and holds (one path staying hot while a sibling cools),\n"
        "    the character is CONSOLIDATING even when heat is at ceiling.\n"
        "  * DIRECTION is carried by the RATIO bands (commit-volume and heat, newer vs older half) against\n"
        "    the instrument's own thresholds. A saturated heat ratio does not soften a diverging volume ratio.\n"
        "  * Use HEATING only when intensity is rising with NO consolidation/spread signal to place it.\n\n"
        "Return ONLY JSON -- the raw object, no code fences, no ```json wrapper, no prose around it:\n"
        '{"vertical": "%s",\n'
        ' "friction_character": "HEATING|SPREADING|CONSOLIDATING|STABLE|BEING-ABANDONED|INDETERMINATE",\n'
        ' "direction": "DIVERGING|CONVERGING|FLAT|UNDETERMINED",\n'
        ' "summary": "2-4 plain sentences, each citing the F-figure it rests on",\n'
        ' "cites": ["F2", "F4", ...],\n'
        ' "blind_spots": ["F1: <one line why it is blind>", "F3: <one line why it is blind>"],\n'
        ' "confidence": "HIGH|MEDIUM|LOW",\n'
        ' "confidence_reason": "e.g. 2 of 4 axes measured; direction unwired"}\n\n'
        "ASCII only. No em-dashes, no smart quotes."
        % (b["window"], b["vertical"],
           blk("F1 STRUCTURAL MEMBERSHIP -- how many of the 14 C3.i structural systems this vertical's OWN changed files BELONG to (membership breadth; NOT blast/reachability).", "", render(f["F1_blast_overlap"])),
           blk("F2 HEAT TRAJECTORY -- how active this vertical's own files are (recency scores; bands excluded).", "", render(f["F2_heat_trajectory"])),
           blk("F3 OPERATOR SIGNAL -- the character of the operator's in-window input about this vertical.", "", render(f["F3_operator_signal"])),
           blk("F4 CO-MOVEMENT     -- which agent types / artifacts move together with this vertical's files.", "", render(f["F4_co_movement"])),
           b["vertical"])
    )


def main() -> None:
    prompt = build_friction_prompt(BATTERY)
    print("=" * 78)
    print("CANONICAL PROMPT (call #1 FRICTION) -- %d chars" % len(prompt))
    print("=" * 78)
    print(prompt)
    print("=" * 78)
    key = boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(
        SecretId=KIMI_SECRET_ID)["SecretString"].strip()
    payload = json.dumps({"model": KIMI_MODEL, "temperature": 1, "max_tokens": FRICTION_BUDGET,
                          "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    print("LIVE CALL -> %s  model=%s  max_tokens=%d  timeout=%ds" % (KIMI_URL, KIMI_MODEL, FRICTION_BUDGET, FRICTION_TIMEOUT))
    t0 = time.monotonic()
    try:
        req = urllib.request.Request(KIMI_URL, data=payload,
                                     headers={"Authorization": "Bearer %s" % key,
                                              "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=FRICTION_TIMEOUT) as resp:
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
