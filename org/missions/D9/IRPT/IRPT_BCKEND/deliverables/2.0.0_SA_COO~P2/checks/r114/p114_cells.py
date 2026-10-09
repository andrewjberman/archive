"""IRPT_BCKEND round 114 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one apply order:
  IB114-1  IB-pr-413  land IB-pr-410's 49F-only narrow holdings bundle (e56 + IB-pr-403 with ticker) on 0.7.0_AE_CloudOps~IB2, under the
                      COO half @ec2d6b6f68, the CTO half @56bc28957c and dell1 ~M1's half; packet blob 92994b0980

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB114-1-AC1  the 49financial key reads (head-object, now) ETag == 1e8ff309... and members-sha256 == 96925f38...; after-reads A: ledger
               CLOSED with pin 9b7256a99f and the built sha256, rolled_back false. Base: FAIL (ETag == 404's bytes).
  IB114-1-AC2  A.replay_on_uploaded: fwd14_gate_unchanged and smartx_class_parity identical. Base: FAIL (no A).
  IB114-1-AC3  A.first_fire: outcome PUBLISHED or REFUSED with output_line, fire_after_landing true, wall_time_s and prior_wall_time_s
               both numbers. Base: FAIL (no A).
"""
import json
import subprocess
import sys
from pathlib import Path

A = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IB114-1_49f_bundle_after_reads.json"
SHA = "47be54d6479fdb849477a41b7cffa089319f2f18d38069b3384393fec192dda5"
MD5 = "1e8ff3096af151f91b96c4e8a3712e4a"
MSHA = "96925f389381e64beeeb31ebf61eecdd5335fddf30cce0335300b455979bfd62"


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
        if led.get("state") != "CLOSED" or not str(led.get("pin", "")).startswith("9b7256a99f") or led.get("sha256") != SHA:
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
