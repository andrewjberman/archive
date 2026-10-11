"""IRPT_DASHBD round 71 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 5375 on DB-b-131's read, two cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB71-1-AC1  ~109/MANIFEST_COUNT_AND_READERS.json: prefixes [{role, listed (bool), manifests (int), first_date, last_date}] (a prefix
              not listed carries a `reason`); total_manifests == the sum over listed prefixes; bodies_read == 0; s3_writes == 0;
              readers holds exactly the ten readers of ~94's census (same file and line), each {passes_onward (bool), to_what};
              any_passes_onward equals the OR of the ten; no string holds a run of 8 or more digits.
  DB71-2-AC1  ~110/R45_REFRESH4.json and the packet beside it: packet.sha256 is the packet file's sha256; members (4 or more) are
              each {file, pin, sha256} and `git show <pin>:<file>` hashes to that sha256; the producer member at its pin defines
              served_thresholds and no longer copies the whole thresholds object; manifest_thresholds_keys is exactly the five
              values plus threshold_claims; kit.ran is a bool (false carries a reason); s3_writes == 0.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
ARD = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
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
        print("%s FAIL" % (cid or "DB71"))
        sys.exit(1)

    def record(rel):
        p = root / (M + rel)
        if not p.is_file():
            fail("no record %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB71-1-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~109/MANIFEST_COUNT_AND_READERS.json")
        px = r.get("prefixes")
        if not isinstance(px, list) or not px:
            fail("no prefixes")
        total = 0
        for p in px:
            if not str(p.get("role") or "").strip() or not isinstance(p.get("listed"), bool):
                fail("a prefix lacks role or listed")
            if p["listed"]:
                if not isinstance(p.get("manifests"), int) or (p["manifests"] and not (p.get("first_date") and p.get("last_date"))):
                    fail("prefix %r lacks its count or its first and last dates" % p["role"])
                total += p["manifests"]
            elif not str(p.get("reason") or "").strip():
                fail("prefix %r was not listed and gives no reason" % p["role"])
        if r.get("total_manifests") != total:
            fail("total_manifests %r, the listed prefixes sum to %d" % (r.get("total_manifests"), total))
        if r.get("bodies_read") != 0 or r.get("s3_writes") != 0:
            fail("bodies_read %r, s3_writes %r" % (r.get("bodies_read"), r.get("s3_writes")))
        census = record("0.9.0_WK_IRPT_DASHBD~94/RETURNS_MANIFEST_READERS.json")["readers"]
        want = sorted((str(x["file"]), str(x["line"])) for x in census)
        rd = r.get("readers") or []
        got = sorted((str(x.get("file")), str(x.get("line"))) for x in rd)
        if got != want:
            fail("readers are not the census's %d (file, line) pairs" % len(want))
        for x in rd:
            if not isinstance(x.get("passes_onward"), bool) or not str(x.get("to_what") or "").strip():
                fail("reader %s:%s lacks passes_onward or to_what" % (x.get("file"), x.get("line")))
        if r.get("any_passes_onward") is not any(x["passes_onward"] for x in rd):
            fail("any_passes_onward does not equal the OR of the readers")
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: %d manifest(s) over %d listed prefix(es); 0 bodies read; %d of %d readers pass the object onward"
              % (total, sum(1 for p in px if p["listed"]), sum(1 for x in rd if x["passes_onward"]), len(rd)))
    elif cid == "DB71-2-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~110/R45_REFRESH4.json")
        pk = r.get("packet") or {}
        pp = root / str(pk.get("path") or "")
        if not pp.is_file() or hashlib.sha256(pp.read_bytes()).hexdigest() != pk.get("sha256"):
            fail("the packet is missing or its sha256 is not the record's")
        mem = r.get("members") or []
        if len(mem) < 4:
            fail("%d member(s), want 4 or more" % len(mem))
        producer = None
        for m in mem:
            f, pin, sha = str(m.get("file") or ""), str(m.get("pin") or ""), str(m.get("sha256") or "")
            if not f or not pin or not SHA.match(sha):
                fail("a member lacks file, pin or sha256")
            out = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (pin, f)], capture_output=True)
            if out.returncode != 0:
                fail("git show %s:%s failed" % (pin, f))
            if hashlib.sha256(out.stdout).hexdigest() != sha:
                fail("%s at %s does not hash to the record's sha256" % (f, pin))
            if f == ARD:
                producer = out.stdout.decode("utf-8")
        if producer is None:
            fail("the producer is not a member")
        if "def served_thresholds(" not in producer or '"thresholds": thresholds' in producer:
            fail("the producer at its pin does not carry DB-b-132")
        if sorted(r.get("manifest_thresholds_keys") or []) != sorted(FIVE + ["threshold_claims"]):
            fail("manifest_thresholds_keys %r" % r.get("manifest_thresholds_keys"))
        kit = r.get("kit") or {}
        if not isinstance(kit.get("ran"), bool) or (kit["ran"] is False and not str(kit.get("reason") or "").strip()):
            fail("kit.ran is not a bool, or false with no reason")
        if r.get("s3_writes") != 0:
            fail("s3_writes %r" % r.get("s3_writes"))
        print("OK: packet bound by hash; %d member(s) hash at their pins; the producer carries DB-b-132; the manifest serves six keys; kit ran=%s"
              % (len(mem), kit["ran"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
