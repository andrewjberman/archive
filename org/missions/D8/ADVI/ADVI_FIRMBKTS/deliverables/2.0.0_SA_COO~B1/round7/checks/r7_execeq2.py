"""ADVI_FIRMBKTS round 7 (FB-j-6, step 3 as amended): the exec-summary generator's READ helpers read the same data in the PRIOR
deployed code and in the NEW built code, both in `canonical` mode, at the same instant. Issuer 2.0.0_SA_COO~B1.

Why this and not round 4's legacy-versus-canonical equality: since the cutover the producers write only the canonical home and the
legacy home is frozen (act 2), so `legacy` and `canonical` DIFFER by design. What this deploy must show is that the new code's reads
are unchanged: the new artifact differs from the deployed one only by the dry-run branch.

  python r7_execeq2.py --zip-prior <deployed artifact.zip> --zip-new <built artifact.zip> [--firm 49financial] [--data-bucket opal-data-bd]
Prints COUNTS and SHA-256 digests only (never an advisor id or a body). Last line:
  EXEC READS: prior and new canonical <EQUAL|DIFFER>: advisors <n>/<n>, leaderboards <k>/<k>, artifacts <m>/<m>.
Exit 0 only when EQUAL and n >= 1. A DIFFER is re-read once (a chain may write between the two reads); a second DIFFER stands.
READ-ONLY (s3 list/get through the seam). Plain ASCII. Never edit this file.
"""
import argparse
import importlib.util
import os
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
R4 = os.path.join(HERE, "..", "..", "round4", "checks", "r4_execeq.py")


def _r4():
    spec = importlib.util.spec_from_file_location("r4_execeq", os.path.normpath(R4))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _pair(r4, td_a, td_b, firm, bucket):
    a, ea = r4.run("canonical", td_a, firm, bucket)
    b, eb = r4.run("canonical", td_b, firm, bucket)
    return a, b, ea, eb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip-prior", required=True)
    ap.add_argument("--zip-new", required=True)
    ap.add_argument("--firm", default="49financial")
    ap.add_argument("--data-bucket", default="opal-data-bd")
    a = ap.parse_args()
    r4 = _r4()
    with tempfile.TemporaryDirectory() as ta, tempfile.TemporaryDirectory() as tb:
        with zipfile.ZipFile(a.zip_prior) as z:
            z.extractall(ta)
        with zipfile.ZipFile(a.zip_new) as z:
            z.extractall(tb)
        p, n, e1, e2 = _pair(r4, ta, tb, a.firm, a.data_bucket)
        if p is not None and n is not None and not all(p[k] == n[k] for k in p):
            p, n, e1, e2 = _pair(r4, ta, tb, a.firm, a.data_bucket)  # a chain may have written between the reads
    if p is None or n is None:
        print("ERROR: prior=%s new=%s" % (e1 or "ok", e2 or "ok"))
        print("EXEC READS: prior and new canonical DIFFER: advisors 0/0, leaderboards 0/0, artifacts 0/0")
        return 1
    same = all(p[k] == n[k] for k in p)
    print("prior : advisors %s ids %s | leaderboards %s %s | artifacts %s %s" % (
        p["n"], p["ids"][:12], p["lb_keys"], p["lb"][:12], p["art_keys"], p["art"][:12]))
    print("new   : advisors %s ids %s | leaderboards %s %s | artifacts %s %s" % (
        n["n"], n["ids"][:12], n["lb_keys"], n["lb"][:12], n["art_keys"], n["art"][:12]))
    print("EXEC READS: prior and new canonical %s: advisors %s/%s, leaderboards %s/%s, artifacts %s/%s" % (
        "EQUAL" if same else "DIFFER", p["n"], n["n"], p["lb_keys"], n["lb_keys"], p["art_keys"], n["art_keys"]))
    return 0 if (same and p["n"] >= 1) else 1


if __name__ == "__main__":
    sys.exit(main())
