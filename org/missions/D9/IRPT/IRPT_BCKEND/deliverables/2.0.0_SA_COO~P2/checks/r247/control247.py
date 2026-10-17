"""Positive control and negatives for p247_cells.py (run by the issuer at the cut). Usage: python control247.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r247/p247_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p247_cells as P  # noqa: E402

EV = "src/example.py:3"


def q(**kw):
    d = {"answer": "text", "evidence": [EV]}
    d.update(kw)
    return d


GOOD = {
    "q1": q(),
    "q2": q(id_kind="account", field_names=["accounts"]),
    "q3": q(hook_token_regex="[0-9]{8,10}", upper_equal=True),
    "q4": q(registry_rows_to_add=["secret_row", "product_row"]),
    "q5": q(existing_sids=["ReadFirmDirectoryPrefixOnly"], statements_to_add=["secretsmanager:GetSecretValue", "s3:PutObject"], env_file="lambda.tf", new_env_var=True),
    "q6": q(flagged=False),
    "q7": q(test_files=["tests/test_refresh.py"], model_test="test_x"),
    "notes": "n",
}


def mut(path, value):
    def f(r):
        r = copy.deepcopy(r)
        cur = r
        for k in path[:-1]:
            cur = cur[k]
        cur[path[-1]] = value
        return r
    return f


def drop(key):
    def f(r):
        r = copy.deepcopy(r)
        r.pop(key)
        return r
    return f


NEGS = [
    ("q3_missing", "AC1", drop("q3")),
    ("q7_missing", "AC1", drop("q7")),
    ("empty_answer", "AC1", mut(["q1", "answer"], " ")),
    ("no_evidence", "AC1", mut(["q2", "evidence"], [])),
    ("evidence_not_path_line", "AC1", mut(["q4", "evidence"], ["src/example.py"])),
    ("evidence_missing_file", "AC1", mut(["q5", "evidence"], ["src/nope.py:1"])),
    ("evidence_line_past_end", "AC1", mut(["q6", "evidence"], ["src/example.py:99"])),
    ("long_digit_run", "AC2", mut(["notes"], "id 12345678901")),
    ("acc_token", "AC2", mut(["notes"], "acc_62bce3163422")),
    ("no_id_kind", "AC2", mut(["q2", "id_kind"], "")),
    ("no_field_names", "AC2", mut(["q2", "field_names"], [])),
    ("empty_registry_rows", "AC3", mut(["q4", "registry_rows_to_add"], [])),
    ("wrong_iam_statements", "AC3", mut(["q5", "statements_to_add"], ["s3:PutObject", "s3:GetObject"])),
    ("no_env_file", "AC3", mut(["q5", "env_file"], "")),
    ("no_hook_regex", "AC3", mut(["q3", "hook_token_regex"], "")),
    ("upper_equal_not_bool", "AC3", mut(["q3", "upper_equal"], "yes")),
    ("flagged_not_bool", "AC3", mut(["q6", "flagged"], "no")),
    ("no_model_test", "AC3", mut(["q7", "model_test"], "")),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c247_"))
    shutil.copytree(REAL / "lib", root / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    (root / "src").mkdir()
    (root / "src/example.py").write_text("a\nb\nc\nd\n", encoding="utf-8")
    f = root / P.REC
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(rec), encoding="utf-8")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-26s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build(GOOD)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IBHM1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn(GOOD))
    expect(label, "IBHM1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c247_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_record", "IBHM1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
