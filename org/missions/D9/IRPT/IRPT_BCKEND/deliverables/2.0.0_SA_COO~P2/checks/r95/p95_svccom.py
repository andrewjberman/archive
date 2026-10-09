"""IRPT_BCKEND round 95 cell IB-pr-386 (CTO ruling msg 2340 on ~P msg 2337 / ~T2 msg 2333) -- ArtifactRepository.get() admits ONE named
subject, svc-commentary: read-only, family REQUEST_COMPOSITION only, retention check kept, tenant taken from the READY item IRPT emitted;
never ALL, never another family, no direct S3 or DynamoDB read.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB95-3-AC1  in reports/tests, `-k svc_commentary` passes (>= 5): own-tenant REQUEST_COMPOSITION read admitted; another tenant
              refused; another family refused; put() refused (read-only); any other service subject refused as today.
              Base: FAIL (no such tests).
  IB95-3-AC2  the whole reports/tests suite passes. Base: PASS; must stay so with the change.
  IB95-3-AC3  the surface file S names the ONE callable surface the commentary Lambda uses (kind: route|lambda; name built by
              lib/opal_naming.py), its request shape (tenant, request_ref) and response shape (composition document + sha256, no
              owner), and the caller's exact IAM (no dynamodb:GetItem, kms:Decrypt or s3:GetObjectVersion). Base: FAIL (no file).
"""
import re
import subprocess
import sys
from pathlib import Path

REPORTS = "infra/aws/lambda/investor-reporting/reports"
S = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~197/IB95-3_svc_commentary_surface.json"
FORBIDDEN = ("dynamodb:GetItem", "kms:Decrypt", "s3:GetObjectVersion", "s3:GetObject")


def pytest(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd),
                       capture_output=True, timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    last = [ln for ln in out.splitlines() if ln.strip()]
    return p.returncode, (last[-1] if last else "")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB95-3"))
        sys.exit(1)

    if cid == "IB95-3-AC1":
        rc, last = pytest(root / REPORTS, "tests", "-k", "svc_commentary")
        m = re.search(r"\b(\d+) passed", last)
        if rc != 0 or not m or int(m.group(1)) < 5:
            fail("-k svc_commentary rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB95-3-AC2":
        rc, last = pytest(root / REPORTS, "tests")
        if rc != 0:
            fail("reports suite rc %d: %s" % (rc, last))
        print("OK: reports suite %s" % last)
    elif cid == "IB95-3-AC3":
        import json
        f = root / S
        if not f.is_file():
            fail("no %s" % S)
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("kind") not in ("route", "lambda") or not str(d.get("name", "")).strip():
            fail("surface kind/name %r" % {k: d.get(k) for k in ("kind", "name")})
        req, resp = d.get("request") or {}, d.get("response") or {}
        if not {"tenant", "request_ref"} <= set(req) or "owner" in json.dumps(resp) or "sha256" not in json.dumps(resp):
            fail("request %r / response %r" % (sorted(req), sorted(resp)))
        iam = json.dumps(d.get("caller_iam") or [])
        if not d.get("caller_iam") or any(a in iam for a in FORBIDDEN):
            fail("caller_iam %s" % iam)
        print("OK: surface %s %s; caller IAM %s" % (d["kind"], d["name"], iam))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
