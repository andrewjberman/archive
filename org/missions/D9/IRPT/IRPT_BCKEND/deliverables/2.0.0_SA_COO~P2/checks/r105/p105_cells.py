"""IRPT_BCKEND round 105 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one apply order:
  IB105-1  IB-pr-404  land IB-pr-402's three NARROW per-firm holdings bundles (FWD-14 publish gate) on 0.7.0_AE_CloudOps~IB2, under the
                      COO half @a9d5043ef9 and the CTO half; packet blob 4f134ade55

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB105-1-AC1  each firm's key reads (head-object, now) ETag == the built md5 and members-sha256 == the packet's; after-reads A: ledger
               CLOSED stating pin and the three built sha256, rolled_back false. Base: FAIL (ETag == live).
  IB105-1-AC2  A.replay_on_uploaded: per firm real_<firm>_live_vs_built identical and fx_<firm>_worse_restored expected-diff, run on the
               uploaded bytes before the first fire. Base: FAIL (no A).
  IB105-1-AC3  A.first_fire: per firm outcome PUBLISHED or REFUSED, with the output line and (REFUSED) the refusal record's refused_at;
               fire_after_landing true. Base: FAIL (no A).
"""
import json
import subprocess
import sys
from pathlib import Path

A = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IB105-1_narrow_bundles_after_reads.json"
BUILT = {
    "49financial": ("3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901", "01387cef54b9e15e10023f05029e357d",
                    "f3247ea2964f9daae8d8439431cbbfae99108d39c50774b234821462c1d5d036"),
    "inflection": ("7036a650703a04b18bcf251717c1310fc5553c817eb9d7ce34ec34ed678c9718", "5daec38f0fbd604c65a770ce08029c67",
                   "0b1a3bf7077865054a330ba9360521425f6299bb1bb970766023d2011d70a093"),
    "cottonwood": ("3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901", "01387cef54b9e15e10023f05029e357d",
                   "f3247ea2964f9daae8d8439431cbbfae99108d39c50774b234821462c1d5d036"),
}


def head(root, firm):
    key = "irpt/%s/code/gold/investor-reporting-holdings.tar.gz" % firm
    p = subprocess.run(["bash", str(root / ".tools" / "aws"), "s3api", "head-object", "--bucket", "opal-data-" + firm, "--key", key,
                        "--output", "json"], capture_output=True, timeout=120)
    if p.returncode != 0:
        return {}
    return json.loads(p.stdout.decode("utf-8", "replace") or "{}")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB105"))
        sys.exit(1)

    def load():
        f = root / A
        if not f.is_file():
            fail("no %s" % A)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB105-1-AC1":
        for firm, (sha, md5, msha) in BUILT.items():
            h = head(root, firm)
            if h.get("ETag", "").strip('"') != md5 or (h.get("Metadata") or {}).get("members-sha256") != msha:
                fail("%s ETag %r metadata %r" % (firm, h.get("ETag"), h.get("Metadata")))
        led = load().get("ledger") or {}
        shas = set(led.get("sha256") or [])
        if led.get("state") != "CLOSED" or not str(led.get("pin", "")).startswith("6f7ca4840e") or shas != {v[0] for v in BUILT.values()}:
            fail("ledger %r" % led)
        if load().get("rolled_back") is not False:
            fail("rolled_back %r" % load().get("rolled_back"))
        print("OK: 3 keys serve the built bytes; ledger CLOSED")
    elif cid == "IB105-1-AC2":
        arms = {x.get("name"): x.get("verdict") for x in load().get("replay_on_uploaded") or []}
        for firm in BUILT:
            if arms.get("real_%s_live_vs_built" % firm) != "identical" or arms.get("fx_%s_worse_restored" % firm) != "expected-diff":
                fail("%s arms %r / %r" % (firm, arms.get("real_%s_live_vs_built" % firm), arms.get("fx_%s_worse_restored" % firm)))
        print("OK: replay on the uploaded bytes holds at 3 firms")
    elif cid == "IB105-1-AC3":
        ff = load().get("first_fire") or {}
        for firm in BUILT:
            r = ff.get(firm) or {}
            if r.get("outcome") not in ("PUBLISHED", "REFUSED") or not r.get("output_line") or r.get("fire_after_landing") is not True:
                fail("%s first fire %r" % (firm, r))
            if r["outcome"] == "REFUSED" and not r.get("refused_at"):
                fail("%s REFUSED without a refusal record" % firm)
        print("OK: first fire read at 3 firms: %s" % ", ".join("%s=%s" % (f, ff[f]["outcome"]) for f in BUILT))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
