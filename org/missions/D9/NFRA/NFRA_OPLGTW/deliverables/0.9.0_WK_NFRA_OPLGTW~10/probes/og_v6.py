"""NFRA_OPLGTW OG-v-6 probe. Usage: og_v6.py AC1|AC2|AC3.
Prints its measurement with its denominator, then exactly one line:
  VERDICT: PASS-OGV6-AC<n>   or   VERDICT: FAIL-OGV6-AC<n> <reason>
Never prints a customer value: only counts, names, hashes, VersionIds, dates and booleans.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import og_v6_common as C  # noqa: E402

PROTOCOL = os.path.join(C.REPO_ROOT, "infra", "aws", "ec2", "opal-gateway", "tests", "acceptance", "WALKTHROUGH_PROTOCOL.md")
INVESTIGATION = os.path.join(C.REPO_ROOT, "org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "surprise-channel",
                             "investigations", "INVESTIGATION_v1.md")
GD_PATH = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/CONTROLLED_WALKTHROUGH_RECORD.md"
C3_REASONS = {"duplicate_source_grain", "paging_refused_no_unique_grain"}


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def git(*args):
    r = subprocess.run(["git", "-C", C.REPO_ROOT] + list(args), capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def verdict(n, ok, reason=""):
    print(f"VERDICT: PASS-OGV6-AC{n}" if ok else f"VERDICT: FAIL-OGV6-AC{n} {reason}")
    sys.exit(0 if ok else 1)


def ssm_values(sealed):
    prefix = sealed["ssm_copy_of_record"]["prefix"]
    out = {}
    for name in sealed["ssm_copy_of_record"]["names"]:
        raw = json.loads(C.aws(["ssm", "get-parameter", "--name", prefix + name, "--with-decryption",
                                "--query", "Parameter.[Type,Value]", "--output", "json"]))
        out[name] = (raw[0], raw[1])
    return out


# ------------------------------------------------------------------ AC1
def ac1():
    import pyarrow.parquet as pq
    g = load(C.GRAIN_PATH)
    snaps = g["snapshots"]
    combos = {(s["dataset"], s["master"], s["date"]) for s in snaps}
    expect = {(d, m, dt) for d in C.DATASETS for m in C.MASTERS for dt in (g["dates"]["D_PREV"], g["dates"]["D_NEW"])}
    print(f"snapshots in file: {len(snaps)}; distinct dataset x master x date: {len(combos)}; "
          f"expected 3x2x2={len(expect)}; coverage equal: {combos == expect}")
    tmp = tempfile.mkdtemp(prefix="ogv6_ac1_")
    matched, bad = 0, []
    try:
        for i, s in enumerate(snaps):
            grain = C.DECLARED_GRAIN[s["dataset"]]
            if list(grain) != s["declared_grain"]:
                bad.append((i, "declared_grain"))
                continue
            local = os.path.join(tmp, f"s{i}.parquet")
            meta = json.loads(C.aws(["s3api", "get-object", "--bucket", C.BUCKET, "--key", s["key"],
                                     "--version-id", s["version_id"], local]))
            if meta.get("VersionId") != s["version_id"]:
                bad.append((i, "version_id"))
                continue
            t = pq.read_table(local, columns=list(grain))
            cnt = Counter(zip(*[t.column(c).to_pylist() for c in grain]))
            coll = [k for k, v in cnt.items() if v > 1]
            got = {"rows": t.num_rows, "colliding_keys": len(coll),
                   "extra_rows": sum(cnt[k] - 1 for k in coll),
                   "status": "HOLDS" if not coll else "COLLIDES"}
            same = all(got[k] == s[k] for k in got)
            os.remove(local)
            if same:
                matched += 1
            else:
                bad.append((i, "counts"))
            print(f"  {s['dataset']} {s['master']} {s['date']}: rows={got['rows']} colliding_keys={got['colliding_keys']} "
                  f"extra_rows={got['extra_rows']} {got['status']} equals_file={same}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"denominator: {matched} of {len(snaps)} snapshots re-read by VersionId and equal to the file (of 12 required)")
    verdict(1, len(snaps) == 12 and combos == expect and matched == 12 and not bad, f"matched={matched}/12 bad={bad}")


# ------------------------------------------------------------------ AC2
def protocol_rows():
    with open(PROTOCOL, "r", encoding="utf-8") as fh:
        text = fh.read()
    sec = text[text.index("## 4. Real-data questions"):text.index("## 5. Record templates")]
    rows = []
    for line in sec.splitlines():
        if line.startswith("| RQ"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            rows.append({"id": c[0], "kind": c[1], "masters": [m.strip() for m in c[2].split(",")],
                         "dates": c[3], "dataset": c[4]})
    return rows


def ac2():
    sealed = load(C.SEALED_PATH)
    g = load(C.GRAIN_PATH)
    rows = protocol_rows()
    qs = sealed["questions"]
    ids_t, ids_s = [r["id"] for r in rows], [q["id"] for q in qs]
    print(f"protocol section 4 rows: {len(ids_t)}; sealed questions: {len(ids_s)}; id sets equal: {set(ids_t) == set(ids_s)} "
          f"(no duplicates: {len(set(ids_t)) == len(ids_t)})")
    fails = []
    if set(ids_t) != set(ids_s) or len(set(ids_t)) != len(ids_t):
        fails.append("ids")
    d_new, d_prev = sealed["dates"]["D_NEW"], sealed["dates"]["D_PREV"]
    by_t = {r["id"]: r for r in rows}
    for q in qs:
        r = by_t.get(q["id"])
        if not r:
            continue
        if r["kind"] != q["kind"] or r["dataset"] != q["dataset"] or r["masters"] != q["masters"]:
            fails.append(f"{q['id']} columns differ")
        if not all(d in r["dates"] for d in q["dates"]):
            fails.append(f"{q['id']} dates not literal in the table")
    kinds = Counter(q["kind"] for q in qs)
    print("count per kind: " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
    if kinds["units"] < 1 or kinds["between_masters"] < 1:
        fails.append("kinds")
    vals = ssm_values(sealed)
    marker_ok = {(m["master"], m["date"]): m["closure_status"] == "qualified" for m in sealed["markers"]}
    for m in C.MASTERS:
        bd = [q for q in qs if q["kind"] == "between_dates" and q["masters"] == [m]]
        ok = bool(bd)
        for q in bd:
            ans = vals[q["id"]][1]
            ok = ok and q["dates"] == [d_prev, d_new] and marker_ok[(m, d_prev)] and marker_ok[(m, d_new)] \
                and "NONE_QUALIFIED" not in ans
        print(f"between_dates for {m} on D_PREV={d_prev} and D_NEW={d_new}, both markers qualified, no NONE_QUALIFIED answer: {ok}")
        if not ok:
            fails.append(f"between_dates {m}")
    status = {(s["master"], s["date"], s["dataset"]): s["status"] for s in g["snapshots"]}
    collides_total = refused_ok = 0
    for q in qs:
        touched = [status[(m, d, q["dataset"])] for m in q["masters"] for d in q["dates"]]
        if "COLLIDES" in touched:
            collides_total += 1
            ans = json.loads(vals[q["id"]][1])
            if q["expected_class"] == "C3_REFUSAL" and ans.get("outcome") == "UNAVAILABLE" and ans.get("reason") in C3_REASONS:
                refused_ok += 1
            else:
                fails.append(f"{q['id']} collides but is not a C3 refusal")
    print(f"questions whose dataset COLLIDES on their date: {collides_total}; sealed with a C3 refusal: {refused_ok} "
          f"(of {len(qs)} questions)")
    verdict(2, not fails, "; ".join(fails))


# ------------------------------------------------------------------ AC3
def leaf_strings(x, out):
    if isinstance(x, dict):
        for v in x.values():
            leaf_strings(v, out)
    elif isinstance(x, list):
        for v in x:
            leaf_strings(v, out)
    elif isinstance(x, str):
        out.append(x)


def scan_files():
    files = []
    root = os.path.join(C.REPO_ROOT, "org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables",
                        "0.9.0_WK_NFRA_OPLGTW~10")
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for f in fn:
            if not f.endswith(".pyc"):
                files.append(os.path.join(dp, f))
    files += [p for p in (PROTOCOL, INVESTIGATION) if os.path.exists(p)]
    return files


def ac3():
    import hashlib
    sealed = load(C.SEALED_PATH)
    fails = []
    pre = sealed["preseal_absence_check"]
    commit = pre["commit"]
    gd = [c for c in pre["checks"] if c["record"] == "G-D"][0]
    print(f"pre-seal record: commit={commit[:10]} G-D recorded rc={gd['rc']} result={gd['result']} path={gd['path'] == GD_PATH}")
    if gd["result"] != "ABSENT" or gd["rc"] == 0 or gd["path"] != GD_PATH:
        fails.append("G-D not ABSENT in the record")
    rc, seal_commit = git("log", "--diff-filter=A", "--format=%H", "-1", "--", os.path.relpath(C.SEALED_PATH, C.REPO_ROOT).replace("\\", "/"))
    if rc != 0 or not seal_commit:
        fails.append("seal not committed yet")
        print("seal commit: NONE")
    else:
        anc = git("merge-base", "--is-ancestor", commit, seal_commit)[0] == 0
        print(f"seal commit={seal_commit[:10]}; pre-seal commit is an ancestor of it: {anc}")
        if not anc or commit == seal_commit:
            fails.append("pre-seal commit not an ancestor of the seal commit")
    rc_gd = git("cat-file", "-e", f"{commit}:{GD_PATH}")[0]
    rc_ctl = git("cat-file", "-e", f"{commit}:{pre['positive_control']['path']}")[0]
    print(f"re-derived at the pre-seal commit: G-D rc={rc_gd} (ABSENT if non-zero), positive control rc={rc_ctl} (PRESENT if 0)")
    if rc_gd == 0 or rc_ctl != 0:
        fails.append("re-derived absence read failed")

    vals = ssm_values(sealed)
    if any(t != "SecureString" for t, _ in vals.values()):
        fails.append("not SecureString")
    salt = vals["SALT"][1]
    ok_n = 0
    qs = sealed["questions"]
    for q in qs:
        ans = vals[q["id"]][1]
        dig = "sha256:" + hashlib.sha256((salt + ans).encode("ascii")).hexdigest()
        if dig == q["expected_answer_hash"]:
            ok_n += 1
        else:
            fails.append(f"{q['id']} digest")
    print(f"digests re-derived from the SSM salt and answers: {ok_n} of {len(qs)}")

    needles = []
    skipped = 0
    for q in qs:
        ans = vals[q["id"]][1]
        needles.append(ans)
        ls = []
        leaf_strings(json.loads(ans), ls)
        for s in ls:
            if re.fullmatch(r"-?\d+\.\d+", s):
                if len(s) >= 6:
                    needles.append(s)
                else:
                    skipped += 1
    needles = sorted(set(needles))
    files = scan_files()
    hits = 0
    for f in files:
        with open(f, "rb") as fh:
            blob = fh.read().decode("utf-8", errors="ignore")
        for n in needles:
            if n in blob:
                hits += 1
                print(f"  HIT in {os.path.relpath(f, C.REPO_ROOT)}")
    print(f"scan: {len(files)} files against {len(needles)} SSM-held answer values (whole answers plus decimal leaves of "
          f"6+ characters; {skipped} shorter decimal leaves not scanned): {hits} values found")
    if hits:
        fails.append("value found in a committed file")
    verdict(3, not fails, "; ".join(fails))


if __name__ == "__main__":
    which = (sys.argv[1] if len(sys.argv) > 1 else "").upper()
    fn = {"AC1": ac1, "AC2": ac2, "AC3": ac3}.get(which)
    if fn is None:
        print("VERDICT: FAIL-OGV6-AC0 usage: og_v6.py AC1|AC2|AC3")
        sys.exit(2)
    try:
        fn()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"VERDICT: FAIL-OGV6-{which} probe error {type(exc).__name__}: {str(exc)[:200]}")
        sys.exit(1)
