"""Difference control for p250_cells.py: builds a temp root (the real signed documents, a git object store borrowed from the real repo, a synthetic record), runs the three
positives, then each negative against the one arm it must break. Usage: python control250.py <real_repo_root>; last line "CONTROL250 OK" or "CONTROL250 FAIL: ...".
"""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~S2/checks/r250/p250_cells.py"
D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
A3 = D + "2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_3_GETOBJECT_ONLY_SHA256_REFUSAL_COO_HALF.md"
CTO = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_CTO_HALF.md"
REC = D + "0.7.0_AE_CloudOps~IB2/IB250-1_bundle_record.json"
TARGET = "infra/aws/lambda/investor-reporting/export/retained_export.py"
BUILD = "1dab1295ef"


def git(*a, cwd=REAL):
    return subprocess.run(["git", *a], cwd=str(cwd), capture_output=True, text=True, timeout=60)


head = git("rev-parse", "HEAD").stdout.strip()
build = git("rev-parse", BUILD).stdout.strip()
blob = git("rev-parse", "%s:%s" % (build, TARGET)).stdout.strip()
base = {
    "gates": {"addendum_3_blob": "87a46d9cf370c293dae46a413cba213db721b5ef", "all_halves_signed": True,
              "ledger_616": {"l1_to_l6_closed": True, "l7_open_by_design": True},
              "one_change_at_a_time": True, "open_deploys_worktrees_read": 3,
              "before": {"export_function_sha256": "5bIgn/MLNgtNtDnRpmE3OejAMw2IpoJBmzzRfHvFLXI="}},
    "build": {"commit": build, "retained_export_blob": blob, "built_sha256": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=", "import_smoke_rc": 0},
    "apply": {"plan": {"add": 0, "change": 1, "destroy": 0, "resources": ["aws_lambda_function.export_render"]},
              "after_sha256": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=", "replan_changes": 0, "env_vars_before": 14, "env_vars_after": 14,
              "switch_changes": 0, "stamp_file": "function-map", "read_stamp_sha256": "z634S2QsrfCpY4c3cD2UGwicdmLDo6/Rmng8SrEskCQ="},
    "counters": {"rollback_performed": False, "console_edits": 0, "invokes": 0, "iam_changes": 0},
}


def run(root, cid):
    p = subprocess.run([sys.executable, "-I", str(CHECK), str(root), cid], capture_output=True, text=True, timeout=110)
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT"


def mk(rec, a3_text=None):
    root = Path(tempfile.mkdtemp(prefix="c250_"))
    subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
    (root / ".git/objects/info").mkdir(parents=True, exist_ok=True)
    (root / ".git/objects/info/alternates").write_bytes((str(REAL / ".git/objects").replace("\\", "/") + "\n").encode("ascii"))
    git("update-ref", "HEAD", head, cwd=root)
    for rel in (A3, CTO):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        data = (REAL / rel).read_bytes()
        if rel == A3 and a3_text is not None:
            data = a3_text
        (root / rel).write_bytes(data)
    if rec is not None:
        (root / REC).parent.mkdir(parents=True, exist_ok=True)
        (root / REC).write_text(json.dumps(rec), encoding="utf-8")
    return root


def mut(path, value):
    r = copy.deepcopy(base)
    cur = r
    for k in path[:-1]:
        cur = cur[k]
    cur[path[-1]] = value
    return r


bad = []
root = mk(base)
for cid in ("IB250-1-AC1", "IB250-1-AC2", "IB250-1-AC3"):
    got = run(root, cid)
    if got != cid + " PASS":
        bad.append("positive %s: %s" % (cid, got))
negs = [
    ("AC1", ["gates", "addendum_3_blob"], "0" * 40),
    ("AC1", ["gates", "all_halves_signed"], False),
    ("AC1", ["gates", "ledger_616"], {"l1_to_l6_closed": True, "l7_open_by_design": False}),
    ("AC1", ["gates", "open_deploys_worktrees_read"], 0),
    ("AC1", ["gates", "before"], {"export_function_sha256": "5/9LZBbTEWOfrnNZufc6Mqz5pbDxTxYAxpWcZVURGs4="}),
    ("AC2", ["build", "commit"], "0" * 40),
    ("AC2", ["build", "retained_export_blob"], "1" * 40),
    ("AC2", ["build", "import_smoke_rc"], 1),
    ("AC3", ["apply", "plan"], {"add": 0, "change": 1, "destroy": 1, "resources": ["x"]}),
    ("AC3", ["apply", "after_sha256"], "5bIgn/MLNgtNtDnRpmE3OejAMw2IpoJBmzzRfHvFLXI="),
    ("AC3", ["apply", "replan_changes"], 1),
    ("AC3", ["apply", "env_vars_after"], 15),
    ("AC3", ["apply", "read_stamp_sha256"], "WjnDxvu2biEPXcwuF8oXJWRUqFaeUY550xnRxa2daa0="),
    ("AC3", ["apply", "stamp_file"], "lambda-source-map"),
    ("AC3", ["counters", "iam_changes"], 1),
    ("AC3", ["counters", "rollback_performed"], True),
]
for arm, path, value in negs:
    cid = "IB250-1-" + arm
    got = run(mk(mut(path, value)), cid)
    if not got.startswith(cid + " FAIL"):
        bad.append("negative %s %s: %s" % (cid, "/".join(path), got))
if not run(mk(None), "IB250-1-AC1").startswith("IB250-1-AC1 FAIL"):
    bad.append("negative no-record AC1 did not fail")
if not run(mk(base, a3_text=b"changed"), "IB250-1-AC1").startswith("IB250-1-AC1 FAIL"):
    bad.append("negative changed ADDENDUM 3 bytes did not fail AC1")
print("CONTROL250 FAIL: " + "; ".join(bad) if bad else "CONTROL250 OK (3 positives, %d negatives, the no-record and changed-bytes cases)" % len(negs))
sys.exit(1 if bad else 0)
