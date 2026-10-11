"""IRPT_BCKEND round 114 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one apply order:
  IB114-1  IB-pr-413  land IB-pr-410's 49F-only narrow holdings bundle (e56 + IB-pr-403 with ticker) on 0.7.0_AE_CloudOps~IB2, under the
                      COO half @ec2d6b6f68, the CTO half @56bc28957c and dell1 ~M1's half; packet blob 92994b0980

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB114-1-AC1  the 49financial key reads (head-object, now) ETag == 8b482c8d... and members-sha256 == 73f33c3c... (IB-pr-417); after-reads A: ledger
               CLOSED with pin 4b008d15 and the built sha256, rolled_back false. Base: FAIL (ETag == 404's bytes).
  IB114-1-AC2  A.replay_on_uploaded: fwd14_gate_unchanged and smartx_class_parity identical. Base: FAIL (no A).
  IB114-1-AC3  A.first_fire: outcome PUBLISHED or REFUSED with output_line, fire_after_landing true, wall_time_s and prior_wall_time_s
               both numbers. Base: FAIL (no A).
"""
import json
import subprocess
import sys
from pathlib import Path

A = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IB114-1_49f_bundle_after_reads.json"
# TO-IB-pr-413 AMENDMENTS 3-5: re-pointed to IB-pr-417 (IB-pr-410's 47be54d6 bundle is NOT applied; row D2-S64)
SHA = "fe4000cbd31aaee971793854ad6cf26bc7b2d9a37a484e953896a09084f02f2e"
MD5 = "8b482c8db26c2e913aeee72023bacc7e"
MSHA = "73f33c3c59b77528c6eaaa56799e9c55f570a7adac23a0c6bcd12e66fe343a81"


def head(root):
    p = subprocess.run(["bash", str(root / ".tools" / "aws"), "s3api", "head-object", "--bucket", "opal-data-49financial", "--key",
                        "irpt/49financial/code/gold/investor-reporting-holdings.tar.gz", "--output", "json"], capture_output=True,
                       timeout=120)
    return json.loads(p.stdout.decode("utf-8", "replace") or "{}") if p.returncode == 0 else {}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB114"))
        sys.exit(1)

    def load():
        f = root / A
        if not f.is_file():
            fail("no %s" % A)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB114-1-AC1":
        h = head(root)
        if h.get("ETag", "").strip('"') != MD5 or (h.get("Metadata") or {}).get("members-sha256") != MSHA:
            fail("ETag %r metadata %r" % (h.get("ETag"), h.get("Metadata")))
        a = load()
        led = a.get("ledger") or {}
        if led.get("state") != "CLOSED" or not str(led.get("pin", "")).startswith("4b008d15") or led.get("sha256") != SHA:
            fail("ledger %r" % led)
        if a.get("rolled_back") is not False:
            fail("rolled_back %r" % a.get("rolled_back"))
        print("OK: 49F key serves the built bytes; ledger CLOSED")
    elif cid == "IB114-1-AC2":
        arms = {x.get("name"): x.get("verdict") for x in load().get("replay_on_uploaded") or []}
        for name in ("fwd14_gate_unchanged", "smartx_class_parity"):
            if arms.get(name) != "identical":
                fail("%s reads %r" % (name, arms.get(name)))
        print("OK: replay on the uploaded bytes holds")
    elif cid == "IB114-1-AC3":
        ff = load().get("first_fire") or {}
        if ff.get("outcome") not in ("PUBLISHED", "REFUSED") or not ff.get("output_line") or ff.get("fire_after_landing") is not True:
            fail("first fire %r" % ff)
        if not all(isinstance(ff.get(k), (int, float)) for k in ("wall_time_s", "prior_wall_time_s")):
            fail("wall times %r / %r" % (ff.get("wall_time_s"), ff.get("prior_wall_time_s")))
        print("OK: first fire %s; wall %ss vs prior %ss" % (ff["outcome"], ff["wall_time_s"], ff["prior_wall_time_s"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
