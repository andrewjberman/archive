"""YCD-x-6 checks. One argument: census | cases | regress. One RESULT line each.

census : a static census of every place the server records an acting principal (upload, analysis submit) and every field
         of the ACCEPTED analysis request the resident receives, with denominators. Read from source, no AWS, no run.
cases  : the four producer cases (tests/test_producer_actor.py). PASS only when all four PASS (an xfail is not a pass).
regress: the existing resident_worker and opal-thread tests.
"""
import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
PKG = ROOT / "infra/aws/lambda/investor-reporting"
GEN = PKG / "ycharts/generate"


def read(rel):
    return (PKG / rel).read_text(encoding="utf-8")


def dict_keys_assigned(path, target, in_function):
    """Keys of the dict literal assigned to `target` inside function `in_function` (ast, top-level keys, incl. nested name)."""
    tree = ast.parse((PKG / path).read_text(encoding="utf-8"))
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef) and fn.name == in_function:
            for node in ast.walk(fn):
                if (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == target for t in node.targets)
                        and isinstance(node.value, ast.Dict)):
                    return [k.value for k in node.value.keys if isinstance(k, ast.Constant)]
    return None


def census():
    sources = [p for p in PKG.rglob("*.py") if "tests" not in p.parts and "__pycache__" not in p.parts]
    writers, mentions = [], []
    for p in sources:
        text = p.read_text(encoding="utf-8", errors="replace")
        for n, line in enumerate(text.splitlines(), 1):
            if re.search(r"acting_principal", line):
                (writers if re.search(r"\[[\"']acting_principal\w*[\"']\]\s*=", line) else mentions).append(
                    "%s:%d" % (p.relative_to(PKG).as_posix(), n))
    print("CENSUS 1 (actor fields, non-test .py under investor-reporting): scanned %d files; 'acting_principal' lines: "
          "writers=%d %s ; other mentions=%d %s" % (len(sources), len(writers), writers, len(mentions), mentions))
    record = dict_keys_assigned("ycharts/generate/acceptance.py", "record", "accept")
    top = record or []
    acc_text = (GEN / "acceptance.py").read_text(encoding="utf-8")
    ident_keys = re.findall(r'"identity": \{(.*?)\},\s*\n\s*"owner"', acc_text, re.S)
    ident_fields = re.findall(r'"(\w+)":', ident_keys[0]) if ident_keys else []
    print("CENSUS 2 (ACCEPTED analysis request record, acceptance.py DynamoAcceptance.accept): top-level fields=%d %s ; "
          "identity fields=%d %s" % (len(top), top, len(ident_fields), ident_fields))
    queue = re.search(r'queue_message\("analysis_generate", \{(.*?)\}\)', acc_text, re.S)
    queue_fields = re.findall(r'"(\w+)":', queue.group(1)) if queue else []
    job = re.search(r"job_item = dict\(self\._job_key\(tenant, request_id\), (.*?)\)\n", acc_text, re.S)
    job_fields = ["tenant", "job"] + re.findall(r"(\w+)=_s\(", job.group(1)) if job else []
    print("CENSUS 3 (queue message / job row): queue message fields=%d %s ; job row fields=%d %s" % (
        len(queue_fields), queue_fields, len(job_fields), job_fields))
    svc = (GEN / "submission_service.py").read_text(encoding="utf-8")
    submitter = 'owner.get("principal_id") != principal.get("principal_id")' in svc and "ACTUAL_SUBMITTER_REQUIRED" in svc
    prosp = (GEN / "prospect_submission.py").read_text(encoding="utf-8")
    owner_from_viewer = "actor_owner = access.prospect_owner(input_owner[\"firm_id\"])" in prosp and "resolve_owner=lambda *_: (viewer, copy.deepcopy(request_owner))" in prosp
    print("CENSUS 4 (analysis SUBMIT): submission_service.submit refuses owner != submitter (ACTUAL_SUBMITTER_REQUIRED)=%s ; "
          "prospect_submission builds the request owner from the VIEWER and passes (viewer, request_owner)=%s ; "
          "neither writes an actor field onto the accepted record" % (submitter, owner_from_viewer))
    up = read("intake/uploads.py")
    upload_ok = 'original["acting_principal_id"] = principal["principal_id"]' in up and "if on_behalf:" in up
    print("CENSUS 5 (UPLOAD): intake/uploads.py create() writes original['acting_principal_id'] on an on-behalf upload only=%s ; "
          "the record is the UPLOAD# index row, not the accepted analysis record" % upload_ok)
    actor_in_accepted = any(re.search(r"actor|acting|principal", k) and k != "owner" for k in top + ident_fields + queue_fields + job_fields)
    verdict = bool(top and ident_fields and queue_fields and job_fields and len(writers) == 1 and submitter
                   and owner_from_viewer and upload_ok and not actor_in_accepted)
    print("CENSUS RESULT: server-recorded actor on UPLOAD=1 (uploads.py:267); on ANALYSIS SUBMIT/accepted record/queue message/"
          "job row=0 of %d fields (%d+%d+%d+%d); producer_for can read only record['owner']" % (
              len(top) + len(ident_fields) + len(queue_fields) + len(job_fields),
              len(top), len(ident_fields), len(queue_fields), len(job_fields)))
    print("RESULT: census %s" % ("PASS" if verdict else "FAIL"))
    return 0 if verdict else 1


def pytest(files):
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rxX"] + files,
                          cwd=str(GEN), capture_output=True, text=True, timeout=600)
    out = proc.stdout + proc.stderr
    print(out.strip().splitlines()[-1] if out.strip() else "(no pytest output)")
    for line in out.splitlines():
        if line.startswith(("XFAIL", "FAILED", "ERROR")):
            print(line)
    return proc.returncode, out


def cases():
    rc, out = pytest(["tests/test_producer_actor.py"])
    passed = re.search(r"(\d+) passed", out)
    ok = rc == 0 and passed and int(passed.group(1)) == 4 and "xfail" not in out.lower().split("passed")[-1]
    print("RESULT: cases %s (%s of 4 producer cases pass)" % ("PASS" if ok else "FAIL", passed.group(1) if passed else "0"))
    return 0 if ok else 1


def regress():
    rc, out = pytest(["tests/test_resident_worker.py", "tests/test_opal_thread_integration.py"])
    print("RESULT: regress %s (pytest rc=%d)" % ("PASS" if rc == 0 else "FAIL", rc))
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("census", "cases", "regress"):
        sys.exit("usage: x6_checks.py census|cases|regress")
    sys.exit({"census": census, "cases": cases, "regress": regress}[sys.argv[1]]())
