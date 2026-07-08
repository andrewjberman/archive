#!/usr/bin/env python3
"""NFRA_PROMOTE recognizer-materializer -- the loop-close ACCEPTANCE path (COO GO 2026-07-08).

The acceptance run's 2 promote-eligible candidates (coupling_ratio >= 0.15: silent-display-fork +
firm-conditional-display) materialize AS RECOGNIZERS via a git-versioned MANIFEST registration -- the
PROPOSE/manifest version of ~D's arch-ratified GOV-B design (4d0886493). Per CTO condition d, a recognizer
registration (NOT a new Entity primitive / node_type) does NOT trip the governed algebra/taxonomy gate.

Grounded on ~D's GOV-B refinements (CTO-ratified):
  R2 -- template+params ONLY (pure-lexical, fidelity-checkable by construction); NO code-gen (that is a
        category change needing its own arch-gate). A manifest entry is a template + params, not code.
  R3 -- the git-versioned manifest is a NAMED CRITICAL SURFACE: materialize() writes ONLY under the
        ratifier's commission_id (ratify-gated); a write is a commit that runs comp-surface-check.
  R1 -- vintage honesty: the entry carries promoted_at; a promoted recognizer is 'live as-of <marker>'.
  R4 -- every materialize/demote emits a MATERIALIZED/DEMOTED CSE (PROMOTE/MATERIALIZER ProducerKind).

REVERSIBLE (invariant #4): demote() removes the entry (exact inverse) + emits a DEMOTED CSE. ZERO
auto-mutation (invariant #3): materialize() is GATED on a ratifier commission_id -- without CTO's explicit
ratify verdict, it REFUSES (propose-only). The manifest write is the governed application.

Usage:
  python NFRA_PROMOTE_recognizer_materializer.py                         # PROPOSE: the 2 manifest entries CTO ratifies
  python NFRA_PROMOTE_recognizer_materializer.py --self-test            # register(gated)+demote round-trip + refusal
  python NFRA_PROMOTE_recognizer_materializer.py --materialize <cid> --commission <CTO-commission-id>   # post-ratify register
  python NFRA_PROMOTE_recognizer_materializer.py --demote <cid> --commission <id>                       # reversibility exercise (CVO)

Author: 0.4.0_DS_ClientPlatform~B. NFRA_PROMOTE acceptance (recognizer-materializer, GOV-B PROPOSE version).
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)

import NFRA_PROMOTE_P1_promotion_engine as P1  # noqa: E402

MANIFEST = os.path.join(_HERE, "promote_recognizer_manifest.json")   # the git-versioned critical surface (R3)
MEASURE_ARTIFACT = os.path.join(_HERE, "fedobs_frontend_coevolution.json")
CSE_TRAIL = os.path.join(_HERE, "promote_materializer_cse.jsonl")     # R4/AC5: durable MATERIALIZED/DEMOTED CSE trail


def _emit_cse(cse: dict) -> None:
    """R4/AC5: every materialize/demote emits a DURABLE CSE (append to the inspectable trail). Emitted at
    the point of the manifest write so ANY caller (CLI or programmatic) produces the audit record -- a
    critical-surface mutation with no durable CSE was the CVO-caught gap (2026-07-08)."""
    with open(CSE_TRAIL, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(cse) + "\n")


def _measures() -> dict:
    with open(MEASURE_ARTIFACT, encoding="utf-8") as fh:
        return {m["candidate_id"]: m for m in json.load(fh).get("measures", [])}


def acceptance_set() -> list:
    """The candidates the PROMOTE-P1 gate advanced to PROPOSED (coupling_ratio >= floor) -- the promote-eligible."""
    recs = P1.load_candidates()
    for r in recs:
        P1.advance(r)   # gate on the real joined measures -> PROPOSED for the tight-coupled
    return [r for r in recs if r.state == "PROPOSED"]


def _template_params(rec) -> dict:
    """Template + params (R2 -- NOT generated code): the recognizer is a pure-lexical, fidelity-checkable
    detector template parameterized by the motif's idiom. The template IS the D1-D7 detector query shape."""
    is_system = rec.candidate_id.startswith("system:")
    idiom = rec.candidate_id.split(":", 1)[1]
    return {"template": "c3-system-recognizer" if is_system else "c2-motif-recognizer",
            "params": {"idiom": idiom, "detector": "TSGRAPH D1-D7 query shape (pure-lexical, fidelity-checkable)"},
            "code_gen": False}   # R2: template+params only, no generated code


def propose_entry(rec, m: dict) -> dict:
    """The manifest entry CTO ratifies (the typed advisory commission's materialization target)."""
    return {
        "recognizer_id": "recognizer:" + rec.candidate_id.split(":", 1)[1],
        "from_candidate": rec.candidate_id,
        "promotion_class": rec.promotion_class,
        "kind": _template_params(rec),
        "warrant": {   # invariant #5 -- evidence + measured-effect + decompression, all git-real
            "coupling_ratio": m.get("coupling_ratio"),
            "co_sessions": m.get("co_sessions"),
            "co_session_shas": [s["run_id"] for s in m.get("sessions", [])[:8]],   # CVO git-verifies these
            "decompression_c0_facts": rec.decompression_chain.get("n_c0_facts"),
        },
        "vintage": {"promoted_at": None, "live_as_of": "<load-marker at materialize>"},   # R1 -- filled at materialize
        "commission_id": None,   # R3 -- filled with the CTO ratifier's commission at materialize (ratify-gated)
        # DISCOVERABILITY (CTO ruling 2026-07-08): route an inspector from the entry to its durable event log.
        "trail_ref": os.path.basename(CSE_TRAIL) + " (append-only MATERIALIZED/DEMOTED CSE event log; grep verb+subject_ref)",
        "state": "PROPOSED",
    }


_EVENT_TRAIL_DESC = (os.path.basename(CSE_TRAIL) + " (durable append-only MATERIALIZED/DEMOTED CSE events -- R4/AC5; "
                     "the manifest is the STATE snapshot, this trail is the EVENT log -- event-log-vs-state-snapshot separation)")


def _load_manifest() -> dict:
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as fh:
            man = json.load(fh)
        man.setdefault("event_trail", _EVENT_TRAIL_DESC)   # backfill the discoverability pointer on load (CTO ruling)
        return man
    return {"surface": "promote_recognizer_manifest (NAMED CRITICAL SURFACE -- comp-surface-check on write)",
            "event_trail": _EVENT_TRAIL_DESC, "recognizers": {}}


def _cse(verb, rid, commission, extra=""):
    return {"cse_kind": "promotion_materialize", "verb": verb, "subject_ref": rid,
            "producer_kind": "PROMOTE/MATERIALIZER", "commission_id": commission, "detail": extra}


def materialize(cid: str, commission_id: str | None) -> tuple:
    """REGISTER a ratified recognizer in the manifest (R3 -- ratify-gated: REFUSES without a commission_id).
    Returns (entry, cse, reason). ZERO auto-mutation without CTO's explicit ratify (the commission)."""
    if not commission_id:
        return None, None, ("REFUSED -- no ratifier commission_id. materialize() is ratify-gated (invariant #3, "
                            "R3): the manifest (a critical surface) is written ONLY under CTO's promotion-ratify.")
    eligible = {r.candidate_id: r for r in acceptance_set()}
    rec = eligible.get(cid)
    if rec is None:
        return None, None, "REFUSED -- %s is not promote-eligible (not in the PROPOSED set / anti-Goodhart-dropped)" % cid
    m = _measures().get(cid, {})
    entry = propose_entry(rec, m)
    entry["commission_id"] = commission_id
    entry["vintage"]["promoted_at"] = "<stamp at commit>"   # Date.* unavailable here; stamp at the safe-commit
    entry["state"] = "MATERIALIZED"
    man = _load_manifest()
    man["recognizers"][entry["recognizer_id"]] = entry
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=2)
    cse = _cse("materialize", entry["recognizer_id"], commission_id, "recognizer registered in manifest")
    _emit_cse(cse)   # R4/AC5: durable MATERIALIZED CSE
    return entry, cse, "MATERIALIZED -> manifest (reversible; write is a comp-surface-check'd commit)"


def demote(cid: str, commission_id: str | None) -> tuple:
    """REVERSIBILITY (invariant #4 / CVO's exercised bar): deregister the recognizer (exact inverse of
    materialize) + emit a DEMOTED CSE. The manifest returns to its pre-materialize state exactly."""
    rid = "recognizer:" + cid.split(":", 1)[1]
    man = _load_manifest()
    if rid not in man["recognizers"]:
        return None, None, "not registered (%s) -- nothing to demote" % rid
    removed = man["recognizers"].pop(rid)
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=2)
    cse = _cse("demote", rid, commission_id, "recognizer deregistered from manifest (exact inverse)")
    _emit_cse(cse)   # R4/AC5: durable DEMOTED CSE
    return removed, cse, "DEMOTED -> deregistered (the exact inverse of materialize; manifest restored)"


def run_propose() -> int:
    print("=" * 80)
    print("NFRA_PROMOTE recognizer-materializer -- PROPOSE (the entries CTO ratifies; nothing written)")
    print("=" * 80)
    ms = _measures()
    eligible = acceptance_set()
    print("\nPromote-eligible (coupling_ratio >= %.2f, gate-passed -> PROPOSED): %d\n" % (P1.FEDOBS_RATIO_FLOOR, len(eligible)))
    for rec in eligible:
        e = propose_entry(rec, ms.get(rec.candidate_id, {}))
        print("  %s  <- %s" % (e["recognizer_id"], e["from_candidate"]))
        print("     kind: %s (template+params, NO code-gen -- R2)" % e["kind"]["template"])
        print("     warrant: coupling_ratio=%s, co_sessions=%s, decompression=%s C0 facts"
              % (e["warrant"]["coupling_ratio"], e["warrant"]["co_sessions"], e["warrant"]["decompression_c0_facts"]))
        print("     co_session shas (CVO git-verifies): %s" % ", ".join(s[:10] for s in e["warrant"]["co_session_shas"][:4]))
        print("     RATIFY-GATED: materializes ONLY under CTO's commission_id (R3); reversible (demote=deregister).")
    print("\nNEXT: re-route these to CTO for the promotion-ratify (warrant cited); on CTO's per-candidate")
    print("  commission -> materialize (manifest-register) -> MATERIALIZED CSE -> CVO reversibility exercise.")
    return 0


def self_test() -> int:
    print("=== NFRA_PROMOTE recognizer-materializer self-test ===")
    # isolate the writes to a temp dir so the self-test never mutates the REAL manifest / CSE trail (audit-clean)
    global MANIFEST, CSE_TRAIL
    _real = (MANIFEST, CSE_TRAIL)
    _td = tempfile.mkdtemp(prefix="promote_selftest_")
    MANIFEST = os.path.join(_td, "manifest.json")
    CSE_TRAIL = os.path.join(_td, "cse.jsonl")
    try:
        return _self_test_body()
    finally:
        MANIFEST, CSE_TRAIL = _real
        shutil.rmtree(_td, ignore_errors=True)


def _self_test_body() -> int:
    ok = []

    def chk(name, cond):
        ok.append(cond)
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    eligible = acceptance_set()
    # exactly 1 promote-eligible on the honest measure: silent-display-fork (independent motif warrant).
    # firm-conditional-display (the system) is HELD -- file-subsumed by silent-display-fork, no independent
    # co-evolution warrant (the CVO-smell / COO disposition: measure the system independently, don't inherit).
    chk("1  exactly 1 promote-eligible: silent-display-fork (system HELD -- file-subsumed, not independent)",
        len(eligible) == 1 and eligible[0].candidate_id == "motif:silent-display-fork")
    cid = eligible[0].candidate_id if eligible else "motif:silent-display-fork"

    # RATIFY-GATE: materialize REFUSES without a commission_id (zero auto-mutation, R3)
    e, _, reason = materialize(cid, None)
    chk("2  ratify-gate: materialize REFUSES without a ratifier commission_id (zero auto-mutation)",
        e is None and "REFUSED" in reason)

    def _trail_lines():
        if not os.path.exists(CSE_TRAIL):
            return 0
        with open(CSE_TRAIL, encoding="utf-8") as fh:
            return sum(1 for ln in fh if ln.strip())

    # WITH a commission -> registers; carries the git-real warrant (shas) + template+params (no code-gen)
    t0 = _trail_lines()
    e, cse, _ = materialize(cid, "CTO-commission-TEST")
    reg_ok = e is not None and e["kind"]["code_gen"] is False and len(e["warrant"]["co_session_shas"]) >= 1 \
        and cse["verb"] == "materialize"
    chk("3  with commission -> registered: template+params (no code-gen), git-real shas, MATERIALIZED CSE", reg_ok)
    # R4/AC5 (CVO-caught gap fix): the MATERIALIZED CSE is DURABLY EMITTED to the trail, not just returned.
    chk("3b R4/AC5: materialize EMITS a durable MATERIALIZED CSE to the trail (not just returns it)", _trail_lines() == t0 + 1)

    # REVERSIBILITY: demote deregisters (exact inverse) + DEMOTED CSE; manifest restored
    man_after_reg = _load_manifest()["recognizers"]
    t1 = _trail_lines()
    d, dcse, _ = demote(cid, "CTO-commission-TEST")
    man_after_demote = _load_manifest()["recognizers"]
    chk("4  reversible: demote deregisters (exact inverse); manifest restored",
        d is not None and dcse["verb"] == "demote" and ("recognizer:" + cid.split(":", 1)[1]) not in man_after_demote
        and ("recognizer:" + cid.split(":", 1)[1]) in man_after_reg)
    # R4/AC5: the DEMOTED CSE is DURABLY EMITTED (this is exactly the demote-CSE that was 0-before-0-after)
    chk("4b R4/AC5: demote EMITS a durable DEMOTED CSE to the trail (the CVO-caught gap, fixed)", _trail_lines() == t1 + 1)

    # the manifest is left clean (round-trip)
    chk("5  round-trip clean: manifest has no test recognizer after demote", len(man_after_demote) == 0)

    n = sum(1 for x in ok if x)
    print("--- self-test: %d/%d passed ---" % (n, len(ok)))
    return 0 if n == len(ok) else 1


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()
    if "--materialize" in args:
        cid = args[args.index("--materialize") + 1]
        comm = args[args.index("--commission") + 1] if "--commission" in args else None
        e, cse, reason = materialize(cid, comm)
        print(reason)
        if e:
            print(json.dumps({"entry": e, "cse": cse}, indent=2))
        return 0 if e else 1
    if "--demote" in args:
        cid = args[args.index("--demote") + 1]
        comm = args[args.index("--commission") + 1] if "--commission" in args else None
        d, cse, reason = demote(cid, comm)
        print(reason)
        return 0 if d else 1
    return run_propose()


if __name__ == "__main__":
    sys.exit(main())
