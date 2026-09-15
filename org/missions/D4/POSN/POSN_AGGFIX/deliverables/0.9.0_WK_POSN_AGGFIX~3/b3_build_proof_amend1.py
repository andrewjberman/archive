#!/usr/bin/env python
"""
Re-record POSN_AGGFIX.TO-B3-1's proof instance at AMENDMENT 1.

TOUCHES EXACTLY TWO ACCEPTANCE ROWS and nothing else in that array: it REPLACES the B3-AC4 row (which
was FAIL against the pre-amendment wording) and APPENDS a B3-AC6 row. B3-AC1, B3-AC2, B3-AC3 and
B3-AC5 stand exactly as recorded -- the script compares them byte-for-byte before and after and
REFUSES if any of them moved.

It also: pins the four artifacts this amendment produced at the commit that carries them (read from
git at run time, never typed); removes the ONE declared exclusion AMENDMENT 1 superseded (the served
control body's AGG reading is no longer excluded -- B3-AC6 measures it); adds the positive control to
the controls block; and updates compiler_tools.

Run AFTER the artifacts are committed and BEFORE the instance is committed.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      cwd=os.path.dirname(os.path.abspath(__file__)),
                      capture_output=True, text=True).stdout.strip()
DELIV = "org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~3/"
INSTANCE = DELIV + "POSN_AGGFIX.TO-B3-1.five-model-views-and-the-aggregate-on-live-bytes.proof_of_spec.json"
AC4_EVIDENCE = DELIV + "b3_ac4_live_tier_arms_post_rerun.txt"
AC6_EVIDENCE = DELIV + "b3_ac6_served_tier_bodies.txt"
UNTOUCHED = ["B3-AC1", "B3-AC2", "B3-AC3", "B3-AC5"]

AC4_VERBATIM = (
    "(AMENDMENT 1) graded on the PRINTED ROWS, never on the exit code (row W3-S6: that script resolves "
    "its C1-AC17 baseline to the running worktree, so its rc is a false negative outside slot ~2's): "
    "the script is the one TO-C1-1's instance names for C1-AC13 (its path printed first); on the live "
    "distribution after TO-A3-1, Opal-staff and Dev tokens on "
    "/api/general/positioning/opal_aggregate.json return 200 with a body whose status is OK; "
    "advisor-class and client-class tokens on both aggregate URLs return 401; all four classes on "
    "/api/general/positioning/positioning_data.json return 200; the table's MATCH count equals its row "
    "count."
)
AC6_VERBATIM = (
    "(AMENDMENT 1) one table, one row per (class, URL), tokens minted per this order's secrets rule and "
    "redacted: for the advisor class and the client class, "
    "/api/general/positioning/positioning_data.json returns 200 and its PARSED body carries no "
    "current_holdings.AGG (its current_holdings key set printed per row), while both aggregate URL "
    "forms return 401; for Opal staff and Dev, /api/general/positioning/opal_aggregate.json returns 200 "
    "with a body whose status is OK; and the POSITIVE CONTROL: the same parsed check run against "
    "TO-A3-1's PRIOR shared-file version, fetched by VersionId, reports AGG PRESENT, so the check can "
    "fail."
)
AC4_DENOM = (
    "table rows MATCH 24 of 24 (the criterion's bar: the MATCH count equals the row count). Of the "
    "readings it names: the aggregate-200 rows 2 of 2 (opal row 3, dev row 5, both on "
    "/api/general/positioning/opal_aggregate.json, each first120 carrying \"status\":\"OK\"); the 401 "
    "rows 4 of 4 (advisor and client x both aggregate URLs, rows 7-10); the control-URL 200 rows 4 of 4 "
    "(all four classes, rows 11-14). Process rc=1 AS OBSERVED, from the families limb alone, which this "
    "criterion does not name and AMENDMENT 1 excludes from the grade (row POSN_AGGFIX-Z-W3-S6)."
)
AC6_DENOM = (
    "table rows MATCH 8 of 8, rc=0. Outside Opal on the control URL 2 of 2 (advisor, client: 200 and "
    "current_holdings [UST ST INT LT ULT], AGG ABSENT, the key set printed on each row); the same two "
    "classes on both aggregate URL forms 4 of 4 at 401; admitted classes on the aggregate 2 of 2 (opal, "
    "dev: 200 with body status OK). POSITIVE CONTROL 1 of 1: the same aggReading() on TO-A3-1's PRIOR "
    "version (VersionId aJ7nhwRKko3H_AMRzsNvvwkf1NiO9aou, stored 8657 bytes gzip, decompressed 80704, "
    "sha256 806bfe06c991e6b0) reports current_holdings [UST ST INT LT ULT AGG] -- AGG PRESENT."
)
AC4_REASON = (
    "PASS on the criterion AS AMENDED. AMENDMENT 1 grades this criterion on the printed rows and their "
    "MATCH count, never on the exit code, and the re-run at 2026-09-15T23:28:14Z prints TABLE ROWS 24; "
    "MATCH 24 of 24 with every named reading present. The process still exits 1 in this worktree, and "
    "that rc is recorded beside the rows rather than hidden: the script resolves its C1-AC17 families "
    "baseline to the RUNNING worktree (row POSN_AGGFIX-Z-W3-S6), where this worker has no capture, so "
    "the families limb adds 1 to `failures` while no row the criterion names is affected. The reading "
    "the pre-amendment wording named and this script never produced (row POSN_AGGFIX-Z-W3-S5) is now "
    "B3-AC6, measured by this worker's own script; no file of TO-C1-1's was edited."
)
ARTIFACTS = [
    (DELIV + "b3_served_tier_bodies.mjs", "test",
     "B3-AC6's invocation, in THIS worker's deliverables because no worker edits another's file. It "
     "IMPORTS the four viewer classes and the URL forms from TO-C1-1's c1_classes.mjs (read, never "
     "edited; its sha256 is printed at run time) so these rows and C1's live rows are driven by ONE "
     "definition, and it applies this order's secrets rule exactly as c1_live_tier_arms.mjs does: "
     "`comp-secrets get opal/auth/jwt-private-key --reveal` inside the signing process, no key or token "
     "printed, written, placed in argv or committed, RS256, exp = iat + 300.",
     ["B3-AC6"]),
    (DELIV + "b3_ac6_prior_fetch.py", "script",
     "The positive control's bytes only: it reads the PRIOR VersionId from TWO loci of TO-A3-1's proof "
     "instance and requires them to agree, fetches that version by VersionId (read-only head_object + "
     "get_object), decompresses and writes to .scratch. The parsing and the verdict stay in the caller, "
     "so the served body and the prior version go through the SAME check.",
     ["B3-AC6"]),
    (DELIV + "b3_ac6_served_tier_bodies.txt", "doc",
     "The full B3-AC6 run: the eight (class, URL) rows with each parsed current_holdings key set, and "
     "the positive control's fetch provenance and verdict.",
     ["B3-AC6"]),
    (DELIV + "b3_ac4_live_tier_arms_post_rerun.txt", "doc",
     "The full B3-AC4 re-run at AMENDMENT 1: the named script's path read from TO-C1-1's instance, the "
     "24 printed rows, the observed rc, and the families line that produces it.",
     ["B3-AC4"]),
]


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def main():
    pin = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                         text=True).stdout.strip()
    print("ARTIFACT PIN (git rev-parse HEAD, read not typed): %s" % pin)
    for rel, _kind, _ev, _cov in ARTIFACTS:
        rc = subprocess.run(["git", "cat-file", "-e", "%s:%s" % (pin, rel)], cwd=ROOT,
                            capture_output=True).returncode
        print("  %s carries %s: %s" % (pin[:10], rel.split("/")[-1], "YES" if rc == 0 else "NO"))
        if rc != 0:
            print("ERROR: the pin does not carry that artifact -- commit the artifacts first")
            return 1

    path = os.path.join(ROOT, INSTANCE)
    with open(path, "rb") as fh:
        inst = json.loads(fh.read().decode("utf-8"))
    before = {r["criterion_id"]: json.dumps(r, sort_keys=True) for r in inst["acceptance"]}
    print("ACCEPTANCE ROWS BEFORE: %d (%s)" % (len(inst["acceptance"]), ", ".join(before)))

    ac4 = {
        "criterion_id": "B3-AC4",
        "criterion_verbatim": AC4_VERBATIM,
        "method": "live_read",
        "invocation": ("timeout 900 node org/missions/D4/POSN/POSN_AGGFIX/deliverables/"
                       "0.9.0_WK_POSN_AGGFIX~2/c1_live_tier_arms.mjs --phase post"),
        "output_evidence": read(AC4_EVIDENCE),
        "denominator": AC4_DENOM,
        "status": "PASS",
        "status_reason": AC4_REASON,
    }
    ac6 = {
        "criterion_id": "B3-AC6",
        "criterion_verbatim": AC6_VERBATIM,
        "method": "live_read",
        "invocation": ("timeout 900 node org/missions/D4/POSN/POSN_AGGFIX/deliverables/"
                       "0.9.0_WK_POSN_AGGFIX~3/b3_served_tier_bodies.mjs"),
        "output_evidence": read(AC6_EVIDENCE),
        "denominator": AC6_DENOM,
        "status": "PASS",
    }

    rows, replaced = [], 0
    for r in inst["acceptance"]:
        if r["criterion_id"] == "B3-AC4":
            rows.append(ac4)
            replaced += 1
        else:
            rows.append(r)
    if replaced != 1:
        print("ERROR: expected exactly one B3-AC4 row, found %d" % replaced)
        return 1
    if any(r["criterion_id"] == "B3-AC6" for r in rows):
        print("ERROR: a B3-AC6 row is already present -- refusing to double-add")
        return 1
    rows.append(ac6)
    inst["acceptance"] = rows

    after = {r["criterion_id"]: json.dumps(r, sort_keys=True) for r in inst["acceptance"]}
    moved = [cid for cid in UNTOUCHED if before.get(cid) != after.get(cid)]
    print("ROWS LEFT EXACTLY AS RECORDED: %d of %d compare byte-equal (%s)"
          % (len(UNTOUCHED) - len(moved), len(UNTOUCHED), ", ".join(UNTOUCHED)))
    if moved:
        print("ERROR: these rows moved and must not have: %s" % moved)
        return 1
    print("B3-AC4: FAIL -> PASS (re-recorded at AMENDMENT 1); B3-AC6: ADDED as PASS")

    have = {a["path_or_key"] for a in inst["artifacts_produced"]}
    added = 0
    for rel, kind, ev, cov in ARTIFACTS:
        if rel in have:
            continue
        inst["artifacts_produced"].append({
            "path_or_key": rel,
            "kind": kind,
            "commit_or_etag": pin,
            "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": "LOCAL commit %s on wk-posn_aggfix-1-3. %s Nothing in TO-B3-1 deploys, "
                               "serves, promotes or pushes." % (pin, ev),
            "artifact_covered_by": cov,
        })
        added += 1
    print("ARTIFACT ROWS: %d added, %d total" % (added, len(inst["artifacts_produced"])))

    superseded = "reading the SERVED control body for current_holdings.AGG by any route other than the script B3-AC4 names"
    kept = [e for e in inst["declared_exclusions"] if e["item"] != superseded]
    print("DECLARED EXCLUSIONS: %d -> %d (the one AMENDMENT 1 superseded is removed: B3-AC6 now MEASURES "
          "that reading, so declaring it excluded would be false)" % (len(inst["declared_exclusions"]), len(kept)))
    if len(kept) != len(inst["declared_exclusions"]) - 1:
        print("ERROR: expected to remove exactly one exclusion")
        return 1
    inst["declared_exclusions"] = kept

    inst["controls"]["mutant"]["description"] += (
        " (4) B3-AC6 (AMENDMENT 1): the AGG-absence check the criterion runs on the SERVED control body "
        "is ALSO run, by the same aggReading() function, against TO-A3-1's PRIOR shared-file version "
        "fetched by VersionId -- without it a check that can only ever report ABSENT is "
        "indistinguishable from one that works."
    )
    inst["controls"]["mutant"]["observed"] += (
        " (4) 'PARSED by the SAME aggReading(): current_holdings=[UST ST INT LT ULT AGG] AGG=PRESENT' on "
        "VersionId aJ7nhwRKko3H_AMRzsNvvwkf1NiO9aou, against 'current_holdings=[UST ST INT LT ULT] "
        "AGG=ABSENT' on what the advisor and client classes actually receive at the same minute -- the "
        "same function, two inputs, two answers."
    )

    for t in inst["compiler_tools"]:
        if "c1_live_tier_arms.mjs" in t.get("invocation", ""):
            t["result"] = (
                "RE-RUN at AMENDMENT 1 (2026-09-15T23:28:14Z): rc=1 with TABLE ROWS 24; MATCH 24 of 24. "
                "AMENDMENT 1 grades the criterion on the printed rows, never on rc; the rc is the "
                "families limb alone (row POSN_AGGFIX-Z-W3-S6). The path was read from TO-C1-1's "
                "instance and printed first. The script was NOT edited: it lies outside this order's "
                "<paths> grant. Its key read is `comp-secrets get opal/auth/jwt-private-key --reveal` "
                "inside the signing process; no key or token is printed, written, placed in argv or "
                "committed, and the tokens carry exp = iat + 300."
            )
        if t.get("tool", "").startswith("proof-of-spec-check"):
            t["invocation"] = ("python .tools/proof-of-spec-check.py " + INSTANCE
                               + " B3-AC1,B3-AC2,B3-AC3,B3-AC4,B3-AC5,B3-AC6")
    inst["compiler_tools"].append({
        "tool": "node 26.8.2 + comp-secrets (b3_served_tier_bodies.mjs, b3_ac6_prior_fetch.py)",
        "invocation": ("timeout 900 node org/missions/D4/POSN/POSN_AGGFIX/deliverables/"
                       "0.9.0_WK_POSN_AGGFIX~3/b3_served_tier_bodies.mjs"),
        "result": ("rc=0, TABLE ROWS 8; MATCH 8 of 8, POSITIVE CONTROL AGG PRESENT ON THE PRIOR "
                   "VERSION: TRUE. Live HTTPS GETs against https://opalinvest.dev and one read-only S3 "
                   "get_object by VersionId; no write to any bucket. The class definitions are IMPORTED "
                   "from TO-C1-1's c1_classes.mjs (read, never edited, sha256 8b952e3f890cd3fd)."),
    })

    blob = (json.dumps(inst, indent=1, ensure_ascii=True) + "\n").encode("utf-8")
    with open(path, "wb") as fh:   # binary: a text-mode write CRLF-ifies repo files on this device
        fh.write(blob)
    back = open(path, "rb").read()
    print("WROTE %s bytes=%d (read-back equal: %s)" % (INSTANCE, len(blob), back == blob))
    reparsed = json.loads(back.decode("utf-8"))
    print("REPARSED: acceptance rows %d (%s)"
          % (len(reparsed["acceptance"]), ", ".join(r["criterion_id"] for r in reparsed["acceptance"])))
    print("NON-ASCII in the instance: %d" % (len(back) - len(back.decode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
