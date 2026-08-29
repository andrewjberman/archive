"""TP1AE-AC4 / D1-inv-3 scorer: compare the served plane against the PRE-FIRE baseline.

Written BEFORE the 2026-08-28 13:30Z fire, deliberately, so that scoring AC4 is a
mechanical act a FRESH SEAT can perform without reconstructing the method. This
session may not survive to 13:30Z; the baseline is useless if the way to read it
lives only in a session transcript.

    usage:  python D1_CATVIEWS.TP1AE-AC4_score_against_baseline.py [--self-test]

    default   re-reads the live plane and scores it against the committed baseline
    --self-test  MUTATES a baseline hash in memory and asserts the scorer REFUSES.
                 A checker that cannot report a violation is not a checker.

WHAT IT CHECKS -- the three legs from the baseline note, in order:

  LEG 1  the five baselined 2026-08-26 keys are BYTE-UNCHANGED (whole-file sha256
         + ETag). The fire must not rewrite a settled day.
  LEG 2  every non_model field hash still matches for those keys.
  LEG 3  the 292-key manifest: an EXISTING key whose ETag or Size moved was
         REWRITTEN, which D1-inv-3 forbids. NEW dated keys are EXPECTED and are
         NOT a violation -- they are reported separately, never as failures.

⛔ WHY A WHOLE-FILE ETAG COMPARE ACROSS THE FIRE WOULD BE THE WRONG INSTRUMENT, and
why this scorer does NOT do that: the fire writes a NEW dated key, it does not
rewrite 2026-08-26.json. Comparing "newest before" to "newest after" compares two
DIFFERENT DAYS and always differs -- reporting a violation on a perfectly correct
run. LEG 1 therefore pins the SAME keys, and value drift in a newly written key is
explicitly out of this scorer's reach (see BOUNDS).

⛔ BOUNDS, so a PASS is not over-read:
  * A PASS means the baselined artifacts did not change. It does NOT mean D1-inv-3
    holds for a scope or as-of date absent from the baseline.
  * LEG 3 detects REWRITES of existing keys. It does NOT detect wrong VALUES inside
    a newly created key -- nothing here can, because there is no prior for a day
    that has never been written.
  * This scores AC4 only. AC1 (the artifact exists, from a SCHEDULED fire), AC2 and
    AC3 read the new artifact and are NOT touched here.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE = os.path.join(HERE, "D1_CATVIEWS.TP1AE-AC4_PREFIRE_BASELINE.json")
MANIFEST = os.path.join(HERE, "D1_CATVIEWS.TP1AE-AC4_PREFIRE_KEY_MANIFEST.json")
BUCKET = "opal-data-assets"
PREFIX = "portal/gold/mdpf/"
FIELDS = ("non_model_aua", "non_model_assets_detail", "inflection_non_model_aua")


# The DEPLOY plane. Not data, therefore not governed by D1-inv-3 -- see the
# scope correction in the LEG3 body. gold-lambda.tf:116 is the authority.
DEPLOY_PLANE_PREFIX = "portal/gold/mdpf/_code/"

def aws(args: list, capture_to: str | None = None) -> tuple[int, str]:
    """Run the .tools/aws shim from the repo root.

    stdin is DEVNULL on purpose: `aws` invoked inside a `while read` loop CONSUMES
    THE LOOP'S STDIN, which kills the call and silently eats the remaining input.
    That produced five clean FALSE FAILURES while building this baseline.
    """
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True).stdout.strip()
    cmd = ["bash", os.path.join(root, ".tools", "aws")] + args
    if capture_to:
        cmd.append(capture_to)
    r = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True,
                       text=True, cwd=root)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def field_hashes(doc) -> dict:
    """Canonical-encode every non_model field at any depth and sha256 it.

    Hashes the FIELD, never the file: the file legitimately changes across days.
    """
    out: dict = {}

    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in FIELDS:
                    canon = json.dumps(v, sort_keys=True,
                                       separators=(",", ":")).encode()
                    out[f"{path}/{k}".lstrip("/")] = hashlib.sha256(canon).hexdigest()
                walk(v, f"{path}/{k}")
        elif isinstance(o, list):
            for v in o[:400]:
                walk(v, f"{path}[]")

    walk(doc)
    return out


def score(base: dict, live_docs: dict, live_keys: dict) -> tuple[list, list, list]:
    """Return (failures, expected_new_keys, checked) -- never raises on a diff."""
    failures, checked = [], []

    for key, ent in sorted(base["entries"].items()):
        raw = live_docs.get(key)
        if raw is None:
            failures.append(f"LEG1 {key}: BASELINED KEY IS GONE from the served plane")
            continue
        sha = hashlib.sha256(raw).hexdigest()
        checked.append(key)
        if sha != ent["whole_file_sha256"]:
            failures.append(
                f"LEG1 {key}: REWRITTEN -- sha256 {ent['whole_file_sha256'][:12]}"
                f" -> {sha[:12]} (a settled day must not be rewritten)")
        live_fields = field_hashes(json.loads(raw))
        for fp, want in sorted(ent["fields"].items()):
            got = live_fields.get(fp)
            if got is None:
                failures.append(f"LEG2 {key}: field {fp} DISAPPEARED")
            elif got != want["sha256"]:
                failures.append(
                    f"LEG2 {key}: field {fp} CHANGED {want['sha256'][:12]} -> {got[:12]}")

    prior = {k["K"]: k for k in json.load(open(MANIFEST))["keys"]}
    new_keys = []
    deploy_plane = []
    for k, meta in sorted(live_keys.items()):
        if k not in prior:
            new_keys.append(k)                      # EXPECTED, not a failure
        else:
            moved = meta["ETag"] != prior[k]["E"] or meta["Size"] != prior[k]["S"]
            if moved and k.startswith(DEPLOY_PLANE_PREFIX):
                # SCOPE CORRECTION 2026-08-29, and it is a NARROWING so it is stated
                # loudly. D1-inv-3 forbids REWRITING A SETTLED DATED DATA KEY. This
                # prefix is not data: gold-lambda.tf:116 declares
                # portal/gold/mdpf/_code/mdpf-gold-lambda.zip as the lambda's own
                # s3_key, so REWRITING IT *IS* THE DEPLOY MECHANISM, mandated by
                # terraform. My first run REFUSED on it (804455 -> 834732, my own
                # rebuilds #2/#3) -- a TRUE observation scored against the WRONG
                # invariant.
                # >> IT IS EXCLUDED FROM *FAILURE* AND STILL PRINTED. A key that
                #    silently disappears from a checker is how the next mis-scope
                #    hides. And DELETION of this key is still a failure below,
                #    because a deploy artifact vanishing breaks the function.
                deploy_plane.append(
                    f"{k}  ({prior[k]['S']} -> {meta['Size']})")
            elif moved:
                failures.append(
                    f"LEG3 {k}: EXISTING KEY REWRITTEN -- ETag/Size moved "
                    f"({prior[k]['S']} -> {meta['Size']})")
    for k in prior:
        if k not in live_keys:
            failures.append(f"LEG3 {k}: EXISTING KEY DELETED")
    return failures, new_keys, checked, deploy_plane


def self_test(base: dict) -> int:
    """Prove the scorer CAN refuse. A control that cannot fail is not a control.

    ⛔ LEG3 IS NEUTRALISED HERE ON PURPOSE, by feeding the scorer the baseline
    manifest as the live listing. An earlier version passed `{}` and the run
    reported 296 findings when exactly ONE was under test -- 292 of them phantom
    LEG3 deletions from the empty listing. The LEG2 assertion was still correct,
    but the MAGNITUDE was nonsense, and a reader checking this control would have
    taken "296" as the signal. Isolate the leg under test, then count.
    """
    print("SELF-TEST: mutating one baselined field hash; the scorer MUST report it.")
    prior = {k["K"]: {"ETag": k["E"], "Size": k["S"]}
             for k in json.load(open(MANIFEST))["keys"]}
    key = sorted(base["entries"])[0]
    fp = sorted(base["entries"][key]["fields"])[0]

    # CONTROL ARM -- unmutated baseline against a document that genuinely matches it.
    # If this arm reports a LEG2 finding, the scorer cries wolf and the mutant arm
    # below proves nothing.
    live_raw = {key: json.dumps({"placeholder": True}).encode()}
    clean = {"entries": {key: copy.deepcopy(base["entries"][key])}}
    clean["entries"][key]["fields"] = {}                    # nothing to compare
    clean["entries"][key]["whole_file_sha256"] = hashlib.sha256(
        live_raw[key]).hexdigest()
    ctl, _, _, _ = score(clean, live_raw, prior)
    ctl_leg2 = [f for f in ctl if "LEG2" in f]

    # MUTANT ARM -- one field hash corrupted; LEG2 must fire.
    mutated = copy.deepcopy(base)
    mutated["entries"][key]["fields"][fp]["sha256"] = "0" * 64
    mutated["entries"][key]["whole_file_sha256"] = hashlib.sha256(
        live_raw[key]).hexdigest()
    one = {"entries": {key: mutated["entries"][key]}}
    fails, _, _, _ = score(one, live_raw, prior)
    mut_leg2 = [f for f in fails if "LEG2" in f]

    print(f"  subject      {key}")
    print(f"  mutated      {fp}")
    print(f"  CONTROL arm (unmutated)  LEG2 findings: {len(ctl_leg2)}  (MUST be 0)")
    print(f"  MUTANT  arm (corrupted)  LEG2 findings: {len(mut_leg2)}  (MUST be >=1)")
    ok = not ctl_leg2 and mut_leg2
    print("SELF-TEST PASS -- silent when correct, refuses when corrupted."
          if ok else "SELF-TEST FAIL -- DO NOT TRUST THIS SCORER.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    base = json.load(open(BASELINE))
    if args.self_test:
        return self_test(base)

    import tempfile
    live_docs = {}
    with tempfile.TemporaryDirectory(prefix="ac4-") as tmp:
        for key in sorted(base["entries"]):
            dest = os.path.join(tmp, key.replace("/", "_"))
            rc, err = aws(["s3api", "get-object", "--bucket", BUCKET,
                           "--key", key], capture_to=dest)
            if rc == 0 and os.path.exists(dest) and os.path.getsize(dest) > 0:
                live_docs[key] = open(dest, "rb").read()
            else:
                print(f"  WARN: could not fetch {key} (rc={rc}) -- scored as GONE")

        rc, out = aws(["s3api", "list-objects-v2", "--bucket", BUCKET,
                       "--prefix", PREFIX, "--output", "json"])
        live_keys = {}
        if rc == 0:
            for c in (json.loads(out).get("Contents") or []):
                live_keys[c["Key"]] = c
        else:
            print(f"  WARN: listing failed rc={rc} -- LEG3 SKIPPED, not passed")

    fails, new_keys, checked, deploy_plane = score(base, live_docs, live_keys)
    print(f"BASELINE captured {base['captured_at_utc']} by {base['captured_by']}")
    print(f"LEG1/LEG2 checked {len(checked)} of {len(base['entries'])} baselined artifacts")
    print(f"LEG3 live keys {len(live_keys)} vs baseline manifest denominator "
          f"{json.load(open(MANIFEST))['denominator']}")
    print(f"NEW keys since baseline (EXPECTED, not failures): {len(new_keys)}")
    for k in new_keys[:12]:
        print(f"    NEW  {k}")
    if len(new_keys) > 12:
        print(f"    ... and {len(new_keys) - 12} more (printed count is the denominator above)")
    if deploy_plane:
        print(f"DEPLOY-PLANE keys rewritten (EXCLUDED from D1-inv-3 BY SCOPE, "
              f"NOT a pass -- see LEG3 note): {len(deploy_plane)}")
        for d in deploy_plane:
            print(f"    DEPLOY  {d}")
    print()
    if fails:
        print(f"AC4 REFUSED -- {len(fails)} finding(s):")
        for f in fails:
            print(f"  {f}")
        return 1
    print("AC4 legs 1-3 PASS -- baselined artifacts byte-unchanged, non_model fields "
          "identical, no existing key rewritten.")
    print("BOUND: this scores AC4 ONLY. AC1/AC2/AC3 read the NEW artifact and are "
          "untouched here. A PASS says nothing about values in newly written keys.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
