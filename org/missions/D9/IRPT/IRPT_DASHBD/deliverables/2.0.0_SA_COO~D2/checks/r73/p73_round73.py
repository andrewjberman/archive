"""IRPT_DASHBD round 73 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 5496 (its half on R45 REFRESH 4, answer to question 5).

Cell: DB-b-139 the 24-key thresholds file inside the function's code package is replaced by a file of the five values and their claims,
after a kit run on that file: the kit run, and the packet for the swap as its own later release. No apply.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB73-1-AC1  ~112/THRESHOLDS_FILE_SWAP.json: file {path, pin, sha256, top_level_keys (list)} where `git show <pin>:<path>` hashes to
              sha256 and the file's top-level keys are exactly the five values plus threshold_claims; kit {ran (bool), tables,
              tables_equal_to_refresh4 (int), reason}: ran false carries a reason; claims_served (five entries); packet {path,
              sha256} whose file hashes to it; s3_writes == 0; no string holds a run of 8 or more digits (members named *sha256
              excepted).
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

FIVE = ["tolerance", "large_flow_share", "plausibility_band_low", "plausibility_band_high", "comparability_max_excluded_weight"]
RUN = re.compile(r"\d{8,}")
SHA = re.compile(r"^[0-9a-f]{64}$")


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB73"))
        sys.exit(1)

    if cid != "DB73-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~112/THRESHOLDS_FILE_SWAP.json"
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    f = r.get("file") or {}
    path, pin, sha = str(f.get("path") or ""), str(f.get("pin") or ""), str(f.get("sha256") or "")
    if not path or not pin or not SHA.match(sha):
        fail("file lacks path, pin or sha256")
    out = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (pin, path)], capture_output=True)
    if out.returncode != 0 or hashlib.sha256(out.stdout).hexdigest() != sha:
        fail("%s at %s is missing or does not hash to the record's sha256" % (path, pin))
    keys = sorted(json.loads(out.stdout.decode("utf-8")))
    if keys != sorted(FIVE + ["threshold_claims"]) or sorted(f.get("top_level_keys") or []) != keys:
        fail("the file's top-level keys are %r" % keys)
    kit = r.get("kit") or {}
    if not isinstance(kit.get("ran"), bool):
        fail("kit.ran is not a bool")
    if kit["ran"]:
        if not isinstance(kit.get("tables"), int) or not isinstance(kit.get("tables_equal_to_refresh4"), int):
            fail("a kit that ran states tables and tables_equal_to_refresh4")
    elif not str(kit.get("reason") or "").strip():
        fail("a kit that did not run gives its reason")
    cs = r.get("claims_served") or {}
    if sorted(cs) != sorted(FIVE):
        fail("claims_served keys %r" % sorted(cs))
    pk = r.get("packet") or {}
    pp = root / str(pk.get("path") or "")
    if not pp.is_file() or hashlib.sha256(pp.read_bytes()).hexdigest() != pk.get("sha256"):
        fail("the packet is missing or its sha256 is not the record's")
    if r.get("s3_writes") != 0:
        fail("s3_writes %r" % r.get("s3_writes"))
    hits = long_digit_runs(r)
    if hits:
        fail("the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: the file at its pin holds six keys; kit ran=%s (%s of %s tables equal to REFRESH 4's run); packet bound by hash"
          % (kit["ran"], kit.get("tables_equal_to_refresh4"), kit.get("tables")))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
