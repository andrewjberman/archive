"""Controls for naming-gate's tf_local LEGACY-READ read_context kind (laptop 1.0.0_SA_CTO msg 102531).

Loads .tools/naming-gate.py from the path given as argv[1] (default: the cto_o_tflocal worktree) and exercises
tf_local_ok, the loader's validation and waivers_for directly. The HEAD carrier read and authority_ok are stubbed,
so each arm grades exactly one condition. Prints PASS/FAIL per arm; exits 1 on any FAIL.
"""
import importlib.util
import json
import os
import sys

GATE = sys.argv[1] if len(sys.argv) > 1 else "C:/Users/Opal Bloomberg/Desktop/cto_o_tflocal/.tools/naming-gate.py"
TF_PATH = "infra/aws/terraform/opal-assets/advi_49f_floor.tf"
LIT = "gold/advi/_logs/chain_"
NAME = "advi_49f_chain_log_prefix"

spec = importlib.util.spec_from_file_location("naming_gate", GATE)
ng = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ng)

RESULTS = []


def arm(label, ok, detail):
    RESULTS.append(ok)
    print("%s  %s -- %s" % ("PASS" if ok else "FAIL", label, detail))


def entry(rc, file=TF_PATH, literal=LIT, eid="OPLGTW-LEGACY-READ-01"):
    return {"id": eid, "file": file, "literal": literal, "remediation": "ADVI_FIRMBKTS", "purpose": "control",
            "authority": {"record": "r", "pin": "0" * 40}, "as_of_cutoff": "2099-12-31", "owner": "1.0.0_SA_CTO~O",
            "read_context": rc}


TF_RC = {"kind": "tf_local", "local_name": NAME, "occurrences": 1, "reference_count": 3}


def load_with(entries):
    doc = json.dumps({"schema_version": 1, "entries": entries}).encode()
    real_git, real_auth = ng.git, ng.authority_ok
    ng.git = lambda *a: (0, doc, b"") if a[:1] == ("show",) else real_git(*a)
    ng.authority_ok = lambda auth, eid: (True, "stubbed")
    try:
        return ng.load_legacy_reads()
    finally:
        ng.git, ng.authority_ok = real_git, real_auth


def expect_ok(label, text, rc=TF_RC):
    ok, note = ng.tf_local_ok(entry(rc), text)
    arm(label, ok, note)


def expect_refuse(label, text, needle, rc=TF_RC):
    ok, note = ng.tf_local_ok(entry(rc), text)
    arm(label, (not ok) and needle in note, note)


def frozen_candidate():
    """The OG-m-2b candidate REBUILT from its frozen pin: base 8340c65376 + the committed patch (sha256 600a4b6da9e7).

    The worker worktree no longer holds the 2b lines (OG-m-2a removed them from its working tree), so the pin is the
    only authoritative source of the bytes the entry binds.
    """
    import subprocess
    import tempfile
    here = os.path.dirname(os.path.abspath(__file__))
    patch = os.path.join(here, "OG-m-2b_candidate_vs_8340c65376.patch")
    repo = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=here, capture_output=True,
                          text=True).stdout.strip()
    tmp = tempfile.mkdtemp()
    target = os.path.join(tmp, *TF_PATH.split("/"))
    os.makedirs(os.path.dirname(target))
    base_bytes = subprocess.run(["git", "show", "8340c65376:%s" % TF_PATH], cwd=repo, capture_output=True).stdout
    open(target, "wb").write(base_bytes)
    r = subprocess.run(["git", "apply", "--include=%s" % TF_PATH, patch], cwd=tmp, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("could not rebuild the frozen candidate: %s" % r.stderr)
    return open(target, encoding="utf-8").read()


base = frozen_candidate()
if os.environ.get("SHOW"):
    print(base[:200])

# POSITIVE: the real OG-m-2b candidate.
expect_ok("POSITIVE real candidate (occurrences 1, reference_count 3)", base)

# NEGATIVES on tf_local_ok, each for its own printed reason.
dup = base + '\n# a second inline copy\nresource "x" "y" {\n  k = "%s"\n}\n' % LIT
expect_refuse("NEG literal duplicated inline elsewhere", dup, "occurs 2 time(s)")
twice = base.replace('  %s = "%s"' % (NAME, LIT), '  %s = "%s"\n  %s = "x"' % (NAME, LIT, NAME), 1)
expect_refuse("NEG local assigned twice", twice, "assigned again")
expect_refuse("NEG reference_count 2", base, "referenced 3 time(s), approved 2", dict(TF_RC, reference_count=2))
expect_refuse("NEG reference_count 4", base, "referenced 3 time(s), approved 4", dict(TF_RC, reference_count=4))
outside = ('variable "v" {\n  %s = "%s"\n}\nx = local.%s\ny = local.%s\nz = local.%s\n'
           % (NAME, LIT, NAME, NAME, NAME))
expect_refuse("NEG assignment outside a locals block", outside, "not a direct entry of a top-level locals block")
unbal = 'locals {\n  %s = "%s"\n' % (NAME, LIT)
expect_refuse("NEG unparseable (unbalanced braces)", unbal, "unparseable")

# waivers_for suffix routing (the loader stubbed to return the entry as good).
real_load = ng.load_legacy_reads
try:
    py_entry = entry({"helper": "h", "helper_body_sha256": "0", "arg_index": 0, "enclosing_function": "f",
                      "bucket_arg": {"name": "b", "value": "v"}, "occurrences": 1})
    ng.load_legacy_reads = lambda: ([py_entry], [])
    w = ng.waivers_for(TF_PATH, base)
    note = w.get("__denied__", {}).get(LIT, "")
    arm("NEG kind-less (Python) entry on a .tf", LIT not in w and "needs read_context kind tf_local" in note, note)
    py_path = "infra/aws/lambda/x.py"
    ng.load_legacy_reads = lambda: ([entry(TF_RC, file=py_path)], [])
    w = ng.waivers_for(py_path, "x = 1\n")
    note = w.get("__denied__", {}).get(LIT, "")
    arm("NEG tf_local entry on a .py", LIT not in w and "authorizes a .tf file only" in note, note)
    ng.load_legacy_reads = lambda: ([entry(TF_RC)], [])
    w = ng.waivers_for(TF_PATH, base)
    arm("POSITIVE waivers_for routes the .tf to tf_local_ok", LIT in w, str(w.get(LIT, ("", w))[1]))
finally:
    ng.load_legacy_reads = real_load

# Loader validation of malformed tf_local read_contexts.
for label, rc, needle in [
    ("NEG malformed: extra field", dict(TF_RC, extra=1), "is not exactly"),
    ("NEG malformed: occurrences True", dict(TF_RC, occurrences=True), "tf_local read_context is malformed"),
    ("NEG malformed: reference_count 0", dict(TF_RC, reference_count=0), "tf_local read_context is malformed"),
    ("NEG malformed: unknown kind", dict(TF_RC, kind="hcl"), "is not exactly"),
]:
    good, bad = load_with([entry(rc)])
    reason = bad[0][1] if bad else ""
    arm(label, not good and needle in reason, reason or "accepted")
good, bad = load_with([entry(TF_RC)])
arm("POSITIVE loader accepts a well-formed tf_local entry", len(good) == 1 and not bad, "good=%d bad=%d" % (len(good), len(bad)))
good, bad = load_with([py_entry])
arm("POSITIVE loader still accepts a kind-less Python entry", len(good) == 1 and not bad, "good=%d bad=%d" % (len(good), len(bad)))

n_fail = RESULTS.count(False)
print("TALLY: %d PASS / %d FAIL (denominator %d arms)" % (RESULTS.count(True), n_fail, len(RESULTS)))
sys.exit(1 if n_fail else 0)
