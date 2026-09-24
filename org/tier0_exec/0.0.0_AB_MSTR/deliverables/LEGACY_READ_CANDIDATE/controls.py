"""LEGACY-READ waiver control suite. Runs the REAL gate as a subprocess on mutated candidates.

Every arm states what it changes and what it must produce. A PASS here means the gate produced the
required verdict for the required reason -- the reason is matched too, so an arm cannot pass because
something unrelated refused.
"""
import json
import os
import subprocess
import sys
import tempfile

WT = r"C:\Users\AndrewBerman\Desktop\mstr-naming-waiver"
SCR = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(SCR, "candidate.diff")
CARRIER_REL = "org/standards/NAMING_LEGACY_READS.json"
TARGET_REL = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
GATE = os.path.join(WT, ".tools", "naming-gate.py")
LINE = "silver/api_dims/accounts_v2/"  # match by LITERAL: a mutation that inserts a line shifts every line number


def run_gate(diff_path, env=None):
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run([sys.executable, GATE, "--diff", diff_path, "--enforce"],
                       cwd=WT, capture_output=True, text=True, env=e)
    return p.returncode, p.stdout + p.stderr


def verdict_for(out, needle=LINE):
    for ln in out.split("\n"):
        if ln.startswith("NAMING ") and needle in ln:
            return ln.split()[1]
    return "<none>"


def why_for(out, needle=LINE):
    lines = out.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("NAMING ") and needle in ln:
            return lines[i + 1].strip() if i + 1 < len(lines) else ""
    return ""


def mutate_diff(replacements):
    """Write a copy of candidate.diff with literal string replacements applied to ADDED lines."""
    src = open(CAND, encoding="utf-8", errors="replace").read()
    for a, b in replacements:
        src = src.replace(a, b)
    fd, path = tempfile.mkstemp(suffix=".diff", dir=SCR)
    os.close(fd)
    open(path, "w", encoding="utf-8", newline="\n").write(src)
    return path


def set_carrier(mutator):
    """Commit a mutated carrier at HEAD, return a restore callable."""
    orig = subprocess.run(["git", "show", "HEAD:" + CARRIER_REL], cwd=WT,
                          capture_output=True, text=True).stdout
    doc = json.loads(orig)
    mutator(doc)
    p = os.path.join(WT, *CARRIER_REL.split("/"))
    open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=2) + "\n")
    subprocess.run(["git", "add", CARRIER_REL], cwd=WT, check=True)
    subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "control: carrier mutation"],
                   cwd=WT, check=True)

    def restore():
        open(p, "w", encoding="utf-8", newline="\n").write(orig)
        subprocess.run(["git", "add", CARRIER_REL], cwd=WT, check=True)
        subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "control: carrier restored"],
                       cwd=WT, check=True)
    return restore


RESULTS = []


def arm(name, want_verdict, want_why_sub, rc_expect, diff_path=None, env=None, carrier_mut=None, needle=None):
    restore = set_carrier(carrier_mut) if carrier_mut else None
    try:
        rc, out = run_gate(diff_path or CAND, env)
        nd = needle or LINE
        v, w = verdict_for(out, nd), why_for(out, nd)
        ok = (v == want_verdict) and (want_why_sub.lower() in w.lower()) and (rc == rc_expect)
        RESULTS.append((ok, name, v, rc, w[:150]))
    finally:
        if restore:
            restore()


# ---------------------------------------------------------------- POSITIVE
arm("P1 the approved site, carrier at HEAD, in force",
    "WAIVED-READ", "positional arg 2 of _latest_date_partition", 0)

# ---------------------------------------------------------------- NEGATIVES
arm("N1 literal CHANGED in the diff (becomes NEW)",
    "REFUSE", "NEW and OUT-OF-PATTERN", 1,
    diff_path=mutate_diff([('"silver/api_dims/accounts_v2/"', '"silver/api_dims/accounts_v3/"')]),
    needle="silver/api_dims/accounts_v3/")

arm("N2a alternate read helper (_read_parquet), still a read",
    "REFUSE", "waiver NOT applied", 1,
    diff_path=mutate_diff([('_latest_date_partition(s3, bucket, "silver/api_dims/accounts_v2/"',
                            '_read_parquet(s3, bucket, "silver/api_dims/accounts_v2/"')]))

arm("N2b moved into a WRITE call",
    "REFUSE", "waiver NOT applied", 1,
    diff_path=mutate_diff([('_latest_date_partition(s3, bucket, "silver/api_dims/accounts_v2/"',
                            's3.put_object(Bucket=bucket, Key="silver/api_dims/accounts_v2/"')]))

arm("N2c KEYWORD form instead of the approved positional",
    "REFUSE", "KEYWORD argument", 1,
    diff_path=mutate_diff([('_latest_date_partition(s3, bucket, "silver/api_dims/accounts_v2/"',
                            '_latest_date_partition(s3, bucket, prefix="silver/api_dims/accounts_v2/"')]))

arm("N3 DUPLICATE occurrence added elsewhere",
    "REFUSE", "occurs 2 time(s)", 1,
    diff_path=mutate_diff([('+    acc_date = _latest_date_partition',
                            '+    _dup = "silver/api_dims/accounts_v2/"; acc_date = _latest_date_partition')]))

arm("N4 carrier points at a DIFFERENT remediation",
    "REFUSE", "written against remediation", 1,
    carrier_mut=lambda d: d["entries"][0].__setitem__("remediation", "SOME_OTHER_REMEDIATION"))

arm("N5 EXPIRED: cutoff one day in the past",
    "REFUSE", "expired: cutoff", 1,
    carrier_mut=lambda d: d["entries"][0].__setitem__("as_of_cutoff", "2026-09-21"))

arm("N6 helper hash NOT the reviewed text",
    "REFUSE", "not the REVIEWED text", 1,
    carrier_mut=lambda d: d["entries"][0]["read_context"].__setitem__("helper_body_sha256", "0" * 64))

arm("N7 authority pin does not resolve",
    "REFUSE", "does not resolve to a commit", 1,
    carrier_mut=lambda d: d["entries"][0]["authority"].__setitem__("pin", "0" * 40))

arm("N8 authority pin resolves but record lacks the ruling id",
    "REFUSE", "does not contain the ruling id", 1,
    carrier_mut=lambda d: d["entries"][0].__setitem__("id", "IRPT-M-LEGACY-READ-99"))

arm("N9 DUPLICATE entries for the same file+literal (ambiguous)",
    "REFUSE", "duplicate authority", 1,
    carrier_mut=lambda d: d["entries"].append(json.loads(json.dumps(d["entries"][0]))))

arm("N10 malformed entry (unknown field)",
    "REFUSE", "malformed", 1,
    carrier_mut=lambda d: d["entries"][0].__setitem__("extra_field", True))

arm("N11 bucket rebound a second time in the enclosing function",
    "REFUSE", "bound 2 time(s)", 1,
    diff_path=mutate_diff([('+    acc_date = _latest_date_partition',
                            '+    bucket = "opal-data-49financial"; acc_date = _latest_date_partition')]))

# ---------------------------------------------------------------- VACUITY
arm("V1 carrier EMPTY at HEAD -> stock behaviour",
    "REFUSE", "REFUSE unless the diff removes it", 1,
    carrier_mut=lambda d: d.__setitem__("entries", []))


def carrier_absent_at_head():
    """Remove the carrier from HEAD entirely; restore it afterwards."""
    orig = subprocess.run(["git", "show", "HEAD:" + CARRIER_REL], cwd=WT,
                          capture_output=True, text=True).stdout
    subprocess.run(["git", "rm", "-q", CARRIER_REL], cwd=WT, check=True)
    subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "control: carrier absent"],
                   cwd=WT, check=True)

    def restore():
        p = os.path.join(WT, *CARRIER_REL.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write(orig)
        subprocess.run(["git", "add", CARRIER_REL], cwd=WT, check=True)
        subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "control: carrier restored"],
                       cwd=WT, check=True)
    return restore


def _selfgrant(mode):
    """Put a VALID entry somewhere that is NOT committed HEAD, and prove it does not grant."""
    orig = subprocess.run(["git", "show", "HEAD:" + CARRIER_REL], cwd=WT,
                          capture_output=True, text=True).stdout
    p = os.path.join(WT, *CARRIER_REL.split("/"))
    # first make HEAD carry NO entries, so only the uncommitted copy could possibly authorize
    doc = json.loads(orig)
    empty = json.loads(orig)
    empty["entries"] = []
    open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(empty, indent=2) + "\n")
    subprocess.run(["git", "add", CARRIER_REL], cwd=WT, check=True)
    subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "control: HEAD carrier emptied"],
                   cwd=WT, check=True)
    # now place the full entry per the mode
    open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=2) + "\n")
    if mode in ("staged", "same-commit"):
        subprocess.run(["git", "add", CARRIER_REL], cwd=WT, check=True)

    def restore():
        open(p, "w", encoding="utf-8", newline="\n").write(orig)
        subprocess.run(["git", "add", CARRIER_REL], cwd=WT, check=True)
        subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "control: carrier restored"],
                       cwd=WT, check=True)
    return restore


def arm_raw(name, want_verdict, want_why_sub, rc_expect, setup, diff_path=None, needle=None):
    restore = setup()
    try:
        rc, out = run_gate(diff_path or CAND)
        nd = needle or LINE
        v, w = verdict_for(out, nd), why_for(out, nd)
        ok = (v == want_verdict) and (want_why_sub.lower() in w.lower()) and (rc == rc_expect)
        RESULTS.append((ok, name, v, rc, w[:150]))
    finally:
        restore()


arm_raw("V2 carrier ABSENT from HEAD -> stock behaviour",
        "REFUSE", "REFUSE unless the diff removes it", 1, carrier_absent_at_head)

# SELF-GRANT: a valid entry that is not in committed HEAD must never authorize.
arm_raw("S1 self-grant, entry UNSTAGED in the worktree only",
        "REFUSE", "REFUSE unless the diff removes it", 1, lambda: _selfgrant("unstaged"))
arm_raw("S2 self-grant, entry STAGED but not committed",
        "REFUSE", "REFUSE unless the diff removes it", 1, lambda: _selfgrant("staged"))
arm_raw("S3 self-grant, entry staged in the SAME commit being graded",
        "REFUSE", "REFUSE unless the diff removes it", 1, lambda: _selfgrant("same-commit"))

# LR-01: 1.0.0_SA_CTO's three defeats of the first recognizer, as permanent arms.
arm("LR-01a helper locally REBOUND inside build_inf",
    "REFUSE", "bound 2 time(s) in this module", 1,
    diff_path=mutate_diff([('+    acc_date = _latest_date_partition',
                            '+    _latest_date_partition = _latest_date_partition; acc_date = _latest_date_partition')]))
arm("LR-01b bucket REBOUND by a comprehension target (no Assign)",
    "REFUSE", "comprehension", 1,
    diff_path=mutate_diff([('+    acc_date = _latest_date_partition',
                            '+    [None for bucket in ["opal-data-49financial"]]; acc_date = _latest_date_partition')]))
arm("LR-02a valid entry, MALFORMED twin SECOND (ambiguous)",
    "REFUSE", "duplicate authority", 1,
    carrier_mut=lambda d: d["entries"].append({k: v for k, v in
                                               json.loads(json.dumps(d["entries"][0])).items() if k != "purpose"}))
arm("LR-02b MALFORMED twin FIRST, valid entry second (order must not matter)",
    "REFUSE", "duplicate authority", 1,
    carrier_mut=lambda d: d.__setitem__("entries", [
        {k: v for k, v in json.loads(json.dumps(d["entries"][0])).items() if k != "purpose"},
        json.loads(json.dumps(d["entries"][0]))]))

# ---------------------------------------------------------------- ALIAS AND MIXED USE
arm("A1 helper reached through a local ALIAS",
    "REFUSE", "call(s) match the approved site", 1,
    diff_path=mutate_diff([('+    acc_date = _latest_date_partition(s3, bucket, "silver/api_dims/accounts_v2/"',
                            '+    _lp = _latest_date_partition; acc_date = _lp(s3, bucket, "silver/api_dims/accounts_v2/"')]))

arm("A2 literal held in a VARIABLE, then passed to the approved helper",
    "REFUSE", "waiver NOT applied", 1,
    diff_path=mutate_diff([('+    acc_date = _latest_date_partition(s3, bucket, "silver/api_dims/accounts_v2/"',
                            '+    _k = "silver/api_dims/accounts_v2/"; acc_date = _latest_date_partition(s3, bucket, _k')]))

arm("A3 MIXED use: same variable feeds the approved read AND a write",
    "REFUSE", "waiver NOT applied", 1,
    diff_path=mutate_diff([('+    acc_date = _latest_date_partition(s3, bucket, "silver/api_dims/accounts_v2/"',
                            '+    _k = "silver/api_dims/accounts_v2/"; s3.put_object(Bucket=bucket, Key=_k);'
                            ' acc_date = _latest_date_partition(s3, bucket, _k')]))

arm("A4 approved read KEPT, a second write of the same literal ADDED",
    "REFUSE", "occurs 2 time(s)", 1,
    diff_path=mutate_diff([('+    acc_date = _latest_date_partition(s3, bucket, "silver/api_dims/accounts_v2/"',
                            '+    s3.put_object(Bucket=bucket, Key="silver/api_dims/accounts_v2/");'
                            ' acc_date = _latest_date_partition(s3, bucket, "silver/api_dims/accounts_v2/"')]))

print("%-4s %-58s %-13s %-4s %s" % ("OK", "ARM", "VERDICT", "rc", "why (truncated)"))
for ok, name, v, rc, w in RESULTS:
    print("%-4s %-58s %-13s %-4s %s" % ("PASS" if ok else "FAIL", name, v, rc, w))
print("\n%d of %d arms PASS" % (sum(1 for r in RESULTS if r[0]), len(RESULTS)))
