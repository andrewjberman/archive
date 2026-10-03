"""Round 39 (IRPT_BCKEND ~P, rows W105-S1 and W105-S2) -- a render token can REACH the 49F reporting series route: the edge admits
the path, and the reporting-read function is wired to read the render grant.

Usage: python <this file> <repo_root> <criterion_id>
  IB39-1-AC1  infra/aws/lambda-edge/auth-validator-edge/render_auth.mjs: RENDER_API_PATH_PATTERNS still carries the three named
              patterns (performance, sections, narrative) and gains one whose regex matches
              /api/scoped/investor-reporting/reporting/acc_x/series and matches NEITHER .../reporting/acc_x/manifest NOR
              .../reporting/client/cli_x/summary (the series read only). Graded statically: each `re: /.../` literal is
              compiled as a Python regex (JS `\\/` read as `/`).
  IB39-1-AC2  the reporting-read function is wired for render grants:
              - infra/aws/terraform/investor-reporting/reporting-read/lambda.tf sets IRPT_EVIDENCE_BUCKET;
              - .../reporting-read/iam.tf grants s3:GetObject on a resource naming "generations/exr_" and "render_grant.json"
                (no "*" resource in that statement);
              - the irpt-reporting-read-lambda entry of infra/aws/lambda/ci/lambda-source-map.json stages grant.py and
                report_owner.py from infra/aws/lambda/investor-reporting/_render_identity/, each pin sound (sha256 matches);
              - the package materialized from the map imports `entry` with the repo off sys.path, and with
                IRPT_EVIDENCE_BUCKET set `served.render_ports_from_env()` returns a value (not None).
  IB39-1-AC3  regression: reporting/tests at least 21 passed and 0 failed; _authz/tests at least 207 passed with its only
              failures the 6 base census tests (row S15). Each suite bounded at 110 s.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

EDGE = "infra/aws/lambda-edge/auth-validator-edge/render_auth.mjs"
RR = "infra/aws/terraform/investor-reporting/reporting-read/"
MAP = "infra/aws/lambda/ci/lambda-source-map.json"
L = "infra/aws/lambda/investor-reporting/"
SERIES = "/api/scoped/investor-reporting/reporting/acc_x/series"
NOT = ("/api/scoped/investor-reporting/reporting/acc_x/manifest", "/api/scoped/investor-reporting/reporting/client/cli_x/summary")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB39"))
        sys.exit(1)

    def git_blob(ref, path):
        r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], cwd=str(root), capture_output=True)
        return r.stdout if r.returncode == 0 else None

    if cid == "IB39-1-AC1":
        src = (root / EDGE).read_text(encoding="utf-8")
        m = re.search(r"RENDER_API_PATH_PATTERNS\s*=\s*\[(.*?)\];", src, re.S)
        if not m:
            fail("no RENDER_API_PATH_PATTERNS array")
        entries = re.findall(r'name:\s*"([^"]+)"\s*,\s*re:\s*/(.+?)/[a-z]*\s*\}', m.group(1))
        names = {n for n, _ in entries}
        if not {"performance", "sections", "narrative"} <= names:
            fail("an existing pattern is gone: %s" % sorted(names))
        hits = [(n, r) for n, r in entries if re.search(r.replace("\\/", "/"), SERIES)]
        if not hits:
            fail("no pattern admits the reporting series path")
        for n, r in entries:
            for u in NOT:
                if re.search(r.replace("\\/", "/"), u):
                    fail("pattern %r admits %s (series only)" % (n, u))
        print("OK: %d patterns; %s admits the series read and nothing else on the reporting route"
              % (len(entries), [n for n, _ in hits]))
    elif cid == "IB39-1-AC2":
        lam = (root / (RR + "lambda.tf")).read_text(encoding="utf-8")
        if "IRPT_EVIDENCE_BUCKET" not in lam:
            fail("reporting-read lambda.tf sets no IRPT_EVIDENCE_BUCKET")
        iam = (root / (RR + "iam.tf")).read_text(encoding="utf-8")
        blocks = [b for b in re.split(r"\n\s*statement\s*\{", iam) if "render_grant.json" in b]
        if not blocks or not any("generations/exr_" in b and "s3:GetObject" in b for b in blocks):
            fail("no GetObject statement on generations/exr_*/render_grant.json")
        if any('"*"' in b for b in blocks):
            fail("the render-grant statement carries a wildcard resource")
        e = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"].get("irpt-reporting-read-lambda") or {}
        staged = {}
        for s in e.get("staged_from") or []:
            b = git_blob(s["pin"], s["repo_path"])
            if b is None or hashlib.sha256(b).hexdigest() != s.get("sha256"):
                fail("pin %s:%s unsound" % (s["pin"][:10], s["repo_path"]))
            staged[s["packaged_as"]] = (s["repo_path"], b)
        for need in ("grant.py", "report_owner.py"):
            hit = [k for k, (rp, _) in staged.items() if k.endswith(need) and "_render_identity/" in rp]
            if not hit:
                fail("the read entry does not stage _render_identity/%s" % need)
        tmp = Path(tempfile.mkdtemp(prefix="db39-"))
        for member in e.get("files") or []:
            data = staged[member][1] if member in staged else git_blob("HEAD", "%s/%s" % (e["source_dir"], member))
            if data is None:
                fail("member %s resolves to nothing" % member)
            out = tmp / member
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        env["IRPT_EVIDENCE_BUCKET"] = "probe-bucket"
        probe = "import entry\nimport served\np = served.render_ports_from_env()\nassert p is not None\nprint('PORTS_OK')"
        r = subprocess.run([sys.executable, "-c", probe], cwd=str(tmp), env=env, capture_output=True, text=True, timeout=110)
        if r.returncode != 0 or "PORTS_OK" not in r.stdout:
            fail("the materialized read package does not install render ports: %s" % (r.stderr or r.stdout).strip()[-300:])
        print("OK: IRPT_EVIDENCE_BUCKET set; the render-grant read is scoped; grant.py and report_owner.py staged; the package "
              "installs render ports")
    elif cid == "IB39-1-AC3":
        def run(target):
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rf", target],
                               cwd=str(root), capture_output=True, text=True, timeout=110)
            out = (r.stdout or "") + (r.stderr or "")
            p = re.search(r"(\d+) passed", out)
            return int(p.group(1)) if p else 0, re.findall(r"^(?:FAILED|ERROR) (\S+)", out, re.M)
        n, f = run(L + "reporting/tests")
        if f or n < 21:
            fail("reporting: %d passed, failures %s" % (n, f[:3]))
        n2, f2 = run(L + "_authz/tests")
        foreign = [x for x in f2 if "test_unguarded_census.py" not in x]
        if n2 < 207 or foreign or len(f2) > 6:
            fail("_authz: %d passed, foreign failures %s, total %d" % (n2, foreign[:3], len(f2)))
        print("OK: reporting %d passed; _authz %d passed with only the %d base census failures" % (n, n2, len(f2)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
