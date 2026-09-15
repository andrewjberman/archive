#!/usr/bin/env python
"""
Append this worker's TO-B3-1 surprise rows to the project channel, TEXTUALLY.

The array is NOT re-serialized: existing rows are append-only and must not be touched, so this inserts the new
row text before the array's closing bracket and adds the one comma the previous row now needs. It refuses if an
id is already present, if the array does not parse before the edit, or if it does not parse after it.
"""
import json
import os
import re
import sys

CHANNEL = ("org/missions/D4/POSN/POSN_AGGFIX/surprise-channel/investigations/INVESTIGATION_v1.md")
ROOT = "C:/tmp/wk-aggfix-1-3"
SCRIPT = "org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~2/c1_live_tier_arms.mjs"
TO = "org/missions/D4/POSN/POSN_AGGFIX/task-orders/POSN_AGGFIX.TO-B3-1.five-model-views-and-the-aggregate-on-live-bytes.md"
VINTAGE = "0e395c7c9b"

ROWS = [
    {
        "id": "POSN_AGGFIX-Z-W3-S5",
        "project": "POSN_AGGFIX",
        "fabric": "site-z",
        "surfaced_by": "0.9.0_WK_POSN_AGGFIX~3",
        "surfaced_at": "2026-09-15T22:58:00Z",
        "one_line": (
            "B3-AC4 names four readings on ONE invocation, and the script it names produces three: "
            "c1_live_tier_arms.mjs --phase post requests the control URL as all four classes and prints status, "
            "length, sha256 and the first 120 bytes, but no limb parses the control body for "
            "current_holdings.AGG, so 'that body carries no current_holdings.AGG' is absent from its output at "
            "any vintage. The other three readings ARE in the output (24 of 24 rows MATCH)."
        ),
        "class": "OBSERVATION",
        "hazard_standing": "INERT",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                TO + " @" + VINTAGE + " B3-AC4 <expect>: '... all four classes on "
                "/api/general/positioning/positioning_data.json return 200 and that body carries no "
                "current_holdings.AGG.'",
                SCRIPT + " @" + VINTAGE + " :202-205 -- the control loop is "
                "`for (const cls of CLASS_ORDER) { const r = await get(CONTROL_URL, tokens[cls]); "
                "row(n++, cls, CONTROL_URL, r, \"200\", r.status === 200) }`: the predicate is the status alone "
                "and the row prints status, len, sha256 and first120 only.",
                SCRIPT + " @" + VINTAGE + " :212 -- the only current_holdings.AGG test in the file, "
                "`/\"current_holdings\"\\s*:\\s*\\{\\s*\"AGG\"/`, is computed as `looksAgg` inside the "
                "AMENDMENT_URLS loop (:209-215) for the advisor and client classes, and is never applied to "
                "CONTROL_URL.",
                "B3-AC4 run 2026-09-15T22:57:39Z, the invocation TO-C1-1's instance names, verbatim: rows 11-14 "
                "read `opal|dev|advisor|client /api/general/positioning/positioning_data.json 200 len=67273 "
                "sha256=86314ec65f3877e6 first120=\"{\\\"generated_at\\\":\\\"2026-09-15T22:12:22Z\\\","
                "\\\"data_as_of\\\":\\\"2026-09-14\\\",\\\"note\\\":\\\"Optimized positioning data with "
                "benchmarks and \" [expect 200]` -- the printed prefix ends inside `note`, before "
                "current_holdings.",
                "Same run, the three readings that ARE produced: rows 3 and 5 (opal, dev on "
                "/api/general/positioning/opal_aggregate.json) 200 len=14410 first120="
                "\"{\\\"status\\\":\\\"OK\\\",...\"; rows 7-10 (advisor, client on both aggregate URLs) 401 with "
                "the gate's message; rows 11-14 200. TABLE ROWS 24; MATCH 24 of 24.",
            ],
        },
        "disposition": "UNDER_INVESTIGATION",
        "spec_asserts": (
            "TO-B3-1 B3-AC4: `timeout 900 node <LIVE_TIER_ARMS_FROM_C1> --phase post` produces, among its named "
            "results, that all four classes on /api/general/positioning/positioning_data.json return 200 AND "
            "that that body carries no current_holdings.AGG."
        ),
        "world_is": (
            "The named script tests and prints the status for those four requests and nothing about the body's "
            "keys; its one AGG-shaped predicate is scoped to the AMENDMENT_URLS rows. The reading exists nowhere "
            "in the output, so the criterion cannot be met by output on the invocation it names. The criterion "
            "is recorded REFUSED with its measurement rather than satisfied by a second read of the served body: "
            "the order's refusal clause forbids satisfying a criterion by another route, and the script is "
            "TO-C1-1's deliverable, outside this order's <paths> grant, so it cannot be extended either."
        ),
        "notes": (
            "Form only. NOT measured here: whether the served control body in fact carries current_holdings.AGG. "
            "B3-AC1 measured the OBJECT at the new VersionId (dFjRdciig4Y.4DBiK_F0eyHtn1.YBCOC) and read "
            "current_holdings UST ST INT LT ULT with no AGG, and rows 11-14 carry generated_at 2026-09-15T22:12:22Z "
            "at len 67273 where the 21:08Z run of the same script read 80704 at generated_at 2026-09-15T11:06:19Z; "
            "those are two different reads on two planes, not the criterion's reading."
        ),
    },
    {
        "id": "POSN_AGGFIX-Z-W3-S6",
        "project": "POSN_AGGFIX",
        "fabric": "site-z",
        "surfaced_by": "0.9.0_WK_POSN_AGGFIX~3",
        "surfaced_at": "2026-09-15T22:58:30Z",
        "one_line": (
            "c1_live_tier_arms.mjs --phase post resolves its C1-AC17 baseline to <the RUNNING worktree>/"
            ".scratch/c1_families_before.json, so the invocation exits 1 for every worker except the one that "
            "captured it: in this worktree all 24 printed rows MATCH and the process still returns rc=1 because "
            "the families file is absent. The process exit is not a usable verdict for that invocation outside "
            "0.9.0_WK_POSN_AGGFIX~2's worktree."
        ),
        "class": "OBSERVATION",
        "hazard_standing": "INERT",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                SCRIPT + " @" + VINTAGE + " :25 `const ROOT = spawnSync(\"git\", [\"rev-parse\", "
                "\"--show-toplevel\"], { cwd: HERE ... })` -- HERE is the script's own directory, so ROOT is the "
                "worktree the script is RUN from, not the one that wrote the baseline; :26 `const FAMILIES_FILE = "
                "path.join(ROOT, \".scratch\", \"c1_families_before.json\")`.",
                SCRIPT + " @" + VINTAGE + " :216-218 -- `if (!existsSync(FAMILIES_FILE)) { console.log(... ABSENT "
                "-- C1-AC17 was not captured); failures += 1 }`, and :232 `process.exit(failures === 0 ? 0 : 1)`.",
                "B3-AC4 run 2026-09-15T22:57:39Z from /c/tmp/wk-aggfix-1-3: 'FAMILIES: "
                "C:\\tmp\\wk-aggfix-1-3\\.scratch\\c1_families_before.json ABSENT -- C1-AC17 was not captured' "
                "followed by 'TABLE ROWS 24; MATCH 24 of 24', rc=1.",
                "Device read 2026-09-15T22:5xZ: the baseline exists only in the capturing worker's worktree -- "
                "/c/tmp/wk-aggfix-1-2/.scratch/c1_families_before.json, 1965 bytes, mtime 2026-09-15 16:41 -- and "
                "is absent at /c/tmp/wk-aggfix-1-3/.scratch/. Both paths are device paths outside the repo, so "
                "the file is in no commit and travels with no drain.",
            ],
        },
        "disposition": "UNDER_INVESTIGATION",
        "spec_asserts": (
            "TO-B3-1 B3-AC4: run the script TO-C1-1's instance names for C1-AC13 with --phase post and read its "
            "output; the criterion names the aggregate rows, the 401 rows and the control rows, and names no "
            "families rows."
        ),
        "world_is": (
            "The script's families limb reads a scratch file scoped to the running worktree, so from this "
            "worker's worktree that limb cannot run and contributes +1 to `failures`, making rc=1 while every "
            "row the criterion names MATCHes. The rows the criterion does name are unaffected; only the exit "
            "code is. Nothing was copied between worktrees to change this: the file is another worker's "
            "measurement and moving it would change what the run compares."
        ),
        "notes": (
            "Form only. NOT measured: whether TO-C1-1's own C1-AC13 run exited 0 in "
            "0.9.0_WK_POSN_AGGFIX~2's worktree, nor whether the three behaviour families have moved since that "
            "capture -- this order does not read them."
        ),
    },
]


def main():
    path = os.path.join(ROOT, CHANNEL)
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8")

    start = text.index("```json")
    body_start = text.index("[", start)
    end = text.rindex("]")
    before = json.loads(text[body_start:end + 1])
    have = {r.get("id") for r in before}
    print("CHANNEL %s: rows before %d; last id %s" % (CHANNEL, len(before), before[-1].get("id")))

    new = [r for r in ROWS if r["id"] not in have]
    if len(new) != len(ROWS):
        print("ERROR: already present: %s" % sorted({r["id"] for r in ROWS} & have))
        return 1
    for r in new:
        print("  appending %s (%s / %s)" % (r["id"], r["class"], r["hazard_standing"]))

    block = ",\n".join("\n".join("  " + ln for ln in json.dumps(r, indent=2).splitlines()) for r in new)
    tail = text[:end]
    m = re.search(r"\n(\s*)\}\s*\n\s*$", tail)
    if not m:
        print("ERROR: the array's last row does not end where expected")
        return 1
    out = tail.rstrip() + ",\n" + block + "\n" + text[end:]

    after = json.loads(out[body_start:out.rindex("]") + 1])
    print("PARSED AFTER THE EDIT: rows %d (was %d, appended %d)" % (len(after), len(before), len(new)))
    if len(after) != len(before) + len(new):
        print("ERROR: row count did not move by exactly the appended rows")
        return 1
    if json.dumps(after[:len(before)], sort_keys=True) != json.dumps(before, sort_keys=True):
        print("ERROR: an existing row changed -- refusing")
        return 1
    print("EXISTING ROWS UNCHANGED: %d of %d compare equal" % (len(before), len(before)))

    with open(path, "wb") as fh:   # binary: a text-mode write CRLF-ifies repo files on this device
        fh.write(out.encode("utf-8"))
    back = open(path, "rb").read().decode("utf-8")
    print("WROTE %s bytes=%d (read-back equal: %s)" % (CHANNEL, len(back.encode("utf-8")), back == out))
    nonascii = len(back.encode("utf-8")) - len(back)
    print("NON-ASCII in the channel after the edit: %d (this worker's rows are pure ASCII: %s)"
          % (nonascii, all(len(json.dumps(r).encode("utf-8")) == len(json.dumps(r)) for r in new)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
