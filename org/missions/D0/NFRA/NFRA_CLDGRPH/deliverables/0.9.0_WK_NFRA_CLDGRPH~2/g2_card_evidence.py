#!/usr/bin/env python3
"""g2_card_evidence -- re-ground the three archive-read instances FROM THE RECORD.

NFRA_CLDGRPH.TO-CG-G-3 / CG-s-34, criterion G3-AC1. Slot 0.9.0_WK_NFRA_CLDGRPH~2.

WHY THIS SCRIPT EXISTS RATHER THAN A PARAGRAPH: the task-order face already states the three
instances in prose. A card built on that prose is a card about a summary. So this script reads
NOTHING from the face -- it opens exactly three record objects:

  1. the surprise channel, PARSED (every fenced json block, summed) -- the row itself;
  2. the git object database -- the commit that INTRODUCED each row, the row's bytes AT that
     commit, and the commit that INTRODUCED each fix (located by a code token with `git log -S`,
     `--full-history`, never a path-simplified log);
  3. the producer source and the round-6 analysis AT THIS WORKTREE'S HEAD -- the corroborating
     carrier for each visible-making number, which is a DIFFERENT object from the row that
     first reported it.

CUT DISCIPLINE (spine v3.8): every number below prints its instrument's COVERAGE, its harness's
GRAIN, and the ENVIRONMENT the compared value came from. The re-grounding environment is this
worktree's local git object DB and working tree ONLY -- no network, no AWS call, no ECS run, no
S3 read (the round-7 egress hold). The BASELINE values (1770, 955, 137, the served stamp) came
from CLOUD runs -- an ECS derive task and a CodeBuild artifact -- recorded by the rows at the
time; this script does not re-run them and does not claim to.

Usage: python g2_card_evidence.py        (no arguments; exit 0 always -- the verdict is the text)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
CHANNEL = ROOT / "org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md"
ANALYSIS = ROOT / "org/missions/D0/NFRA/NFRA_CLDGRPH/ledger/ROUND_ANALYSIS.round6.md"
PRODUCER = ROOT / "infra/aws/globgrph/derive_stitch.py"
CHANNEL_REL = "org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md"
PRODUCER_REL = "infra/aws/globgrph/derive_stitch.py"

# The three instances, keyed by CARRIER. `fix_token` is a code identifier whose INTRODUCTION into
# the producer is the fix; `numbers` are (label, regex) pairs read out of the ROW'S OWN TEXT.
INSTANCES = [
    {
        "carrier": "NODES",
        "row_id": "NFRA_CLDGRPH-W2-S61",
        "fix_token": "_retype_prior_cycle",
        "numbers": [("retyped_prior_cycle", r"retyped=(\d+)"),
                    ("carried_stitch_nodes", r"([\d,]+) nodes with source='portal-stitch'")],
        "corroborator": "PRODUCER_SOURCE",
        "corroborate_on": "_retype_prior_cycle",
    },
    {
        "carrier": "PROPS",
        "row_id": "NFRA_CLDGRPH-W2-S69",
        "fix_token": "RETIRED_STITCH_PROPS",
        "numbers": [("served_stamp_after_the_image_act", r"STITCH_V1_STAMPED_SERVED=(\d+)"),
                    ("fold_writer_output", r"stamped=(\d+)")],
        "corroborator": "PRODUCER_SOURCE",
        "corroborate_on": "RETIRED_STITCH_PROPS",
    },
    {
        "carrier": "EDGES",
        "row_id": "NFRA_CLDGRPH-W2-S71",
        "fix_token": "stored_in_prior_cycle_dropped",
        "numbers": [("stored_in_emitted_prior_cycle", r"STORED_IN emitted (\d+)"),
                    ("keys_answering_from_their_own_props", r"= (\d+) of 191")],
        "corroborator": "ROUND6_ANALYSIS",
        "corroborate_on": "955 emitted -> 137",
    },
]


def git(*args: str) -> str:
    out = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if out.returncode != 0:
        return "GIT-ERROR rc=%d %s" % (out.returncode, out.stderr.strip()[:200])
    return out.stdout


def parse_rows(text: str):
    """Every row in every fenced json block. The denominator instrument, never a loose id grep."""
    blocks = re.findall(r"```json\s*(.*?)```", text, re.S)
    rows, unparsed = [], 0
    for b in blocks:
        try:
            d = json.loads(b)
        except Exception:
            unparsed += 1
            continue
        rows.extend(d if isinstance(d, list) else [d])
    return rows, len(blocks), unparsed


def introducing_commit(token: str, path_rel: str) -> tuple:
    """The FIRST commit that added `token` to `path_rel`, over the full (unsimplified) history."""
    out = git("log", "--full-history", "--reverse", "-S", token, "--format=%h|%cI|%s", "--", path_rel)
    if out.startswith("GIT-ERROR") or not out.strip():
        return ("NONE", "NONE", out.strip()[:120])
    first = out.strip().split("\n")[0]
    h, iso, subj = first.split("|", 2)
    return (h, iso, subj)


def row_at_commit(commit: str, row_id: str):
    blob = git("show", "%s:%s" % (commit, CHANNEL_REL))
    if blob.startswith("GIT-ERROR"):
        return None, 0, blob[:120]
    rows, nblocks, _ = parse_rows(blob)
    for r in rows:
        if isinstance(r, dict) and r.get("id") == row_id:
            return r, len(rows), ""
    return None, len(rows), "row absent at that commit"


def main() -> int:
    head = git("rev-parse", "--short=10", "HEAD").strip()
    text = CHANNEL.read_text(encoding="utf-8")
    rows_head, blocks_head, unparsed = parse_rows(text)
    by_id_head = {r["id"]: r for r in rows_head if isinstance(r, dict) and "id" in r}
    producer_src = PRODUCER.read_text(encoding="utf-8")
    analysis_src = ANALYSIS.read_text(encoding="utf-8")

    print("G2 CARD EVIDENCE -- the three archive-read instances, re-grounded FROM THE RECORD")
    print("  ENVIRONMENT: worktree %s, HEAD %s, local git object DB; no network, no AWS, no run."
          % (ROOT, head))
    print("  INSTRUMENT COVERAGE (channel): every fenced json block of %s, PARSED and summed."
          % CHANNEL_REL)
    print("  DENOMINATOR (channel at HEAD): %d row(s) in %d fenced block(s), %d unparsed. GRAIN: "
          "one row object per surprise, counted by object, never by an id grep (the header line "
          "itself matches an id grep)." % (len(rows_head), blocks_head, unparsed))
    print("  INSTRUMENT COVERAGE (provenance): git log --full-history -S<token> over ONE path; "
          "GRAIN: one commit, the FIRST that added the token. A path-simplified log is refused "
          "here -- it can omit the very commit that introduced the change.")
    print("  BASELINE ENVIRONMENT, stated because it is NOT this one: every visible-making number "
          "below was produced by a CLOUD run (an ECS globgrph-derive-runner task, or a CodeBuild "
          "stitch-produce artifact) or by a served-projection read, at the time the row was "
          "filed. This script re-reads the RECORD of those runs; it does not re-run them.")
    print("")

    results = []
    for inst in INSTANCES:
        rid = inst["row_id"]
        carrier = inst["carrier"]
        print("=" * 96)
        print("CARRIER %s -- row %s" % (carrier, rid))
        checks = {}

        # 1 -- the row, at the commit that introduced it
        rh, iso, subj = introducing_commit('"id": "%s"' % rid, CHANNEL_REL)
        checks["row_commit_found"] = rh != "NONE"
        row_c, ncommit, err = row_at_commit(rh, rid) if rh != "NONE" else (None, 0, "no commit")
        checks["row_read_at_its_commit"] = row_c is not None
        print("  ROW AT ITS COMMIT: %s @%s (%s)" % (rid, rh, iso))
        print("    commit subject: %s" % subj[:140])
        print("    channel denominator AT that commit: %d row(s); at HEAD: %d row(s) -- the row is "
              "read from the vintage that minted it, not only from today's file."
              % (ncommit, len(rows_head)))
        if row_c is None:
            print("    ERROR: %s" % err)
        else:
            print("    surfaced_by=%s surfaced_at=%s class=%s hazard_standing=%s disarm_owner=%s"
                  % (row_c.get("surfaced_by"), row_c.get("surfaced_at"), row_c.get("class"),
                     row_c.get("hazard_standing"), row_c.get("disarm_owner")))
            print("    grounding.status=%s evidence_items=%d"
                  % (row_c.get("grounding", {}).get("status"),
                     len(row_c.get("grounding", {}).get("evidence", []))))

        # 2 -- the row is UNEDITED between its commit and HEAD (append-only, verified not assumed)
        row_h = by_id_head.get(rid)
        checks["row_unedited_since"] = bool(row_c and row_h and json.dumps(row_c, sort_keys=True)
                                            == json.dumps(row_h, sort_keys=True))
        print("  APPEND-ONLY CONTROL: row bytes at its commit == row bytes at HEAD -> %s"
              % checks["row_unedited_since"])

        # 3 -- the FIX, located by the code token it introduced
        fh, fiso, fsubj = introducing_commit(inst["fix_token"], PRODUCER_REL)
        checks["fix_commit_found"] = fh != "NONE"
        print("  FIX LOCATED BY TOKEN %r in %s: @%s (%s)" % (inst["fix_token"], PRODUCER_REL, fh, fiso))
        print("    commit subject: %s" % fsubj[:200])
        checks["fix_token_live_at_head"] = inst["fix_token"] in producer_src
        print("    token still present at HEAD: %s (a fix located in history and absent today "
              "would be a REVERT, and this control is what tells them apart)"
              % checks["fix_token_live_at_head"])

        # 4 -- the number that made it visible, taken from the ROW'S OWN TEXT
        blob = json.dumps(row_c, ensure_ascii=True) if row_c else ""
        found = {}
        for label, pat in inst["numbers"]:
            m = re.search(pat, blob)
            found[label] = m.group(1) if m else "NOT-FOUND"
        checks["numbers_from_row"] = all(v != "NOT-FOUND" for v in found.values())
        for label, val in found.items():
            print("  VISIBLE-MAKING NUMBER (from the row's own text, not from the order's prose): "
                  "%s=%s" % (label, val))

        # 5 -- corroboration on a DIFFERENT object than the row
        if inst["corroborator"] == "PRODUCER_SOURCE":
            ok = inst["corroborate_on"] in producer_src
            where = "%s @%s" % (PRODUCER_REL, head)
        else:
            ok = inst["corroborate_on"] in analysis_src
            where = "org/missions/D0/NFRA/NFRA_CLDGRPH/ledger/ROUND_ANALYSIS.round6.md @%s" % head
        checks["corroborated_on_a_second_object"] = ok
        print("  SECOND CARRIER (not the row): %r present in %s -> %s"
              % (inst["corroborate_on"], where, ok))

        ok_all = all(checks.values())
        results.append((carrier, rid, ok_all, checks))
        print("  CHECKS: %s" % json.dumps(checks))
        print("  CARRIER %s REGROUNDED: %s (%d of %d checks)"
              % (carrier, ok_all, sum(1 for v in checks.values() if v), len(checks)))

    # ---- the edges instance carries the round's lesson as a PAIR of numbers; print it explicitly
    print("=" * 96)
    m955 = re.search(r"STORED_IN emitted (\d+)", json.dumps(by_id_head.get("NFRA_CLDGRPH-W2-S71", {})))
    m137 = re.search(r"955 emitted -> (\d+)", analysis_src)
    print("THE SHRINK, from two independent objects: prior-cycle emission %s (row W2-S71's own "
          "re-derivation on its cycle-3 artifact) -> next emission %s (ROUND_ANALYSIS.round6.md "
          "s.2, the CVO-graded table). GRAIN: STORED_IN edges in one artifact. COVERAGE: the "
          "whole STORED_IN population of that artifact, denominator 191 firm-relative keys."
          % (m955.group(1) if m955 else "NOT-FOUND", m137.group(1) if m137 else "NOT-FOUND"))

    n_ok = sum(1 for _, _, ok, _ in results if ok)
    print("")
    print("SUMMARY")
    print("INSTANCES_REGROUNDED=%d of %d" % (n_ok, len(INSTANCES)))
    for carrier, rid, ok, _ in results:
        print("%s=%s regrounded=%s" % (carrier, rid, ok))
    print("EVIDENCE_FROM_RECORD=%s" % ("true" if n_ok == len(INSTANCES) else "false"))
    print("EVIDENCE_SOURCES=3 of 3 (the parsed channel at each row's own commit; the git object "
          "DB via --full-history -S; the producer source and the round-6 analysis at HEAD). "
          "THE TASK-ORDER FACE IS NOT READ BY THIS SCRIPT -- no path under task-orders/ is opened.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
