"""IRPT_DASHBD round 138, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the 49 Financial function-map file carries the RE-STAGED state (cell DB-f-2601).

  Why: the retirement of lambda-source-map.json (NFRA_CTLPLN round 30) ported the entry `irpt-49f-reporting-gold-lambda` into
  infra/aws/lambda/ci/function-map/irpt-49f-reporting-gold-lambda.json from a base taken BEFORE the re-stage (IB2, 3ff444434e): the drained file holds the FIRST-stage
  artifact_sha256 (SCt7IgN3..) and the older pins of lib/trading_calendar.py and infra/logic/registry/systems.json. The deployed code is JgSV12Tz...

  DBF138-1-AC1  the file's bytes equal the pinned corrected bytes (sha256 below): against the drained base exactly three fields differ (artifact_sha256 and the two staged_from pins)
  DBF138-1-AC2  BUILD_ONLY through the function-map path prints the base64 sha256 JgSV12TzBm0nHmWKKvtk35PWQvFePk3NHQzGWeACYes= (the deployed bundle)
  DBF138-1-AC3  the applier's record FM49F_PORT_RECORD.json: one commit that touched exactly that one file, and `terraform plan -detailed-exitcode` of the reporting-gold root read exit 0 / No changes

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

CHECKS = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r138/"
FILE_REL = "infra/aws/lambda/ci/function-map/irpt-49f-reporting-gold-lambda.json"
CORRECTED_SHA256 = "51193ac1b91d8b327ae24502eb51db8a80ff50c31a5f23c860b618fc51eb1691"
BASE_SHA256 = "fa6a4d9ec4419bc51bcb9aa9d2522e2ae9e212f84b1933e2e8d7429c50141d58"
BUILD_B64 = "JgSV12TzBm0nHmWKKvtk35PWQvFePk3NHQzGWeACYes="
RECORD_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.7.0_AE_CloudOps~IB2/FM49F_PORT_RECORD.json"
THREE_FIELDS = {"artifact_sha256", "staged_from"}
PIN_PATHS = {"lib/trading_calendar.py", "infra/logic/registry/systems.json"}


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(root, *args):
    return subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, timeout=120)


def differing_fields(base, new):
    """(top-level keys that differ, repo_paths of the staged_from items that differ)."""
    keys = {k for k in set(base) | set(new) if base.get(k) != new.get(k)}
    bs = {x["repo_path"]: x for x in base.get("staged_from", [])}
    ns = {x["repo_path"]: x for x in new.get("staged_from", [])}
    paths = {p for p in set(bs) | set(ns) if bs.get(p) != ns.get(p)}
    return keys, paths


def parse_build_line(text):
    """The base64 sha256 on the `BUILD_ONLY: <zip> sha256=<b64> key=<key>` line, or None."""
    m = re.search(r"^BUILD_ONLY: \S+ sha256=(\S+) key=", text, re.M)
    return m.group(1) if m else None


def record_problems(rec, commit_paths):
    """Problems with the applier's record; commit_paths is the list of paths the recorded commit touched."""
    out = []
    if rec.get("claim") != "measured":
        out.append("claim is not measured")
    if rec.get("plan_exit_code") != 0:
        out.append("plan_exit_code is not 0 (got %r)" % (rec.get("plan_exit_code"),))
    if rec.get("plan_no_changes") is not True:
        out.append("plan_no_changes is not true")
    if commit_paths != [FILE_REL]:
        out.append("the commit touched %r, not exactly [%s]" % (commit_paths, FILE_REL))
    return out


def ac1(root):
    p = Path(root, FILE_REL)
    need(p.is_file(), "missing " + FILE_REL)
    b = p.read_bytes()
    need(sha(b) == CORRECTED_SHA256, "file sha256 %s is not the corrected bytes %s" % (sha(b)[:12], CORRECTED_SHA256[:12]))
    base = json.loads(Path(root, CHECKS, "fm49f_drained_base.json").read_text(encoding="utf-8"))
    keys, paths = differing_fields(base, json.loads(b.decode("utf-8")))
    need(keys == THREE_FIELDS and paths == PIN_PATHS, "differences against the drained base: keys %s, pins %s" % (sorted(keys), sorted(paths)))


def ac2(root):
    r = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", "irpt-49f-reporting-gold-lambda"],
                       cwd=str(root), capture_output=True, text=True, timeout=600, env=dict(__import__("os").environ, BUILD_ONLY="1"))
    got = parse_build_line(r.stdout)
    need(got is not None, "no BUILD_ONLY line (rc %s): %s" % (r.returncode, (r.stderr or r.stdout)[-300:]))
    need(got == BUILD_B64, "BUILD_ONLY sha256 %s is not %s" % (got, BUILD_B64))


def ac3(root):
    rp = Path(root, RECORD_REL)
    need(rp.is_file(), "missing " + RECORD_REL)
    rec = json.loads(rp.read_text(encoding="utf-8"))
    c = rec.get("commit")
    need(isinstance(c, str) and re.fullmatch(r"[0-9a-f]{7,40}", c), "record has no commit")
    r = git(root, "show", "--name-only", "--format=", c)
    need(r.returncode == 0, "cannot read commit " + c)
    paths = [x for x in r.stdout.decode("utf-8").splitlines() if x.strip()]
    probs = record_problems(rec, paths)
    need(not probs, "; ".join(probs))


def selftest():
    arms = []
    base = {"a": 1, "artifact_sha256": "x", "staged_from": [{"repo_path": "lib/trading_calendar.py", "pin": "1"}, {"repo_path": "q", "pin": "2"}]}
    new = {"a": 1, "artifact_sha256": "y", "staged_from": [{"repo_path": "lib/trading_calendar.py", "pin": "9"}, {"repo_path": "q", "pin": "2"}]}
    arms.append(("diff finds artifact_sha256, staged_from and the one pin", differing_fields(base, new) == ({"artifact_sha256", "staged_from"}, {"lib/trading_calendar.py"})))
    arms.append(("an unchanged file differs nowhere", differing_fields(base, base) == (set(), set())))
    arms.append(("an extra top-level key is seen", "zz" in differing_fields(base, dict(new, zz=1))[0]))
    arms.append(("build line parsed", parse_build_line("x\nBUILD_ONLY: /tmp/a.zip sha256=AbC+/= key=k/z.zip\n") == "AbC+/="))
    arms.append(("no build line -> None", parse_build_line("Complete\n") is None))
    good = {"claim": "measured", "plan_exit_code": 0, "plan_no_changes": True}
    arms.append(("a good record passes", record_problems(good, [FILE_REL]) == []))
    arms.append(("plan exit 2 refused", any("plan_exit_code" in p for p in record_problems(dict(good, plan_exit_code=2), [FILE_REL]))))
    arms.append(("a second file in the commit refused", any("touched" in p for p in record_problems(good, [FILE_REL, "x.txt"]))))
    arms.append(("an unmeasured claim refused", any("claim" in p for p in record_problems(dict(good, claim="inferred"), [FILE_REL]))))
    ok = True
    for name, res in arms:
        print(("  ok   " if res else "  FAIL ") + name)
        ok = ok and res
    print("selftest %s (%d arms)" % ("PASS" if ok else "FAIL", len(arms)))
    return 0 if ok else 1


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3 or argv[2] not in ("DBF138-1-AC1", "DBF138-1-AC2", "DBF138-1-AC3"):
        print("usage: p138_port.py <repo_root> DBF138-1-AC1|AC2|AC3 | --selftest")
        return 2
    fn = {"DBF138-1-AC1": ac1, "DBF138-1-AC2": ac2, "DBF138-1-AC3": ac3}[argv[2]]
    try:
        fn(argv[1])
    except Fail as e:
        print("reason: " + str(e))
        print(argv[2] + " FAIL")
        return 1
    except Exception as e:  # an unreadable input is a FAIL with its cause, never a PASS
        print("reason: %s: %s" % (type(e).__name__, e))
        print(argv[2] + " FAIL")
        return 1
    print(argv[2] + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
