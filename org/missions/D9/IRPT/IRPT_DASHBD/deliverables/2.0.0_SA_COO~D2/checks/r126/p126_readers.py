"""IRPT_DASHBD round 126, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-258, the SERVED-READER READ for the dim_return_method claim columns (CTO ROUND-126 ANALYSIS
@2cf3e13682 ruling 2): does any reader other than the producer and its tests take a claim column from the served `dim_return_method` row? The answer decides the branch:
NONE -> the dim contract's next version marks the six claim columns `see_manifest` (not dropped); ONE OR MORE -> the contract stays byte-identical and the ruling flips to A.
LOCAL: repo reads only (the portal submodule is read in the primary checkout); the contract edit is the one repo change.

  DB-b-258 (~211)   the record RD_CLAIM_READERS_R126.json and, on the none-branch, the contract's next version
                    DB126-2-AC1 (the read: the candidate files equal the recount, every one classed with a verified cited line, the decision follows the classes)
                    DB126-2-AC2 (the contract matches the decision, both branches)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                      the pure clauses on synthetic arms
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~211/RD_CLAIM_READERS_R126.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-258.dim-return-method-claim-columns-served-reader-read-and-contract-marking.md"
CONTRACT_REL = "org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json"
PRODUCER_REL = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
CLAIM_NAMES = ["tolerance_claim", "large_flow_share_claim", "plausibility_band_low_claim", "plausibility_band_high_claim", "comparability_max_excluded_weight_claim",
               "threshold_claims_source"]
DIM_TOKEN = "dim_return_method"
CLASSES = ("reads_claim_column", "reads_whole_row", "reads_other_dim_columns", "names_prefix_or_grant_only", "writes_dim_row", "comment_or_doc_only")
EXCLUDE_PREFIXES = ("org/", "docs/", "data/transcripts/", "projects/", "workflows/")
BASE_VERSION, NEW_VERSION = "0.6.0", "0.7.0"
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout.decode("utf-8", "replace"), r.returncode


def base_commit(root):
    out, _ = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(out.split(), "the order's first commit is not in this history")
    return out.split()[-1]


def is_test(path):
    parts = path.split("/")
    return "tests" in parts[:-1] or parts[-1].startswith("test_")


def is_excluded(path):
    return path.startswith(EXCLUDE_PREFIXES) or path.endswith(".md") or is_test(path) or path == PRODUCER_REL


# ------------------------------------------------------------------------------------------------ pure clauses
def check_record(rec, recount, line_of, contract_unchanged_needed=None):
    """rec: the worker's record; recount: sorted list of candidate files; line_of(file, n) -> text of line n (or None)."""
    exp = {"claim_names", "candidate_files", "candidates", "decision", "words"}
    need(set(rec) == exp, "record keys differ: extra %s missing %s" % (sorted(set(rec) - exp), sorted(exp - set(rec))))
    need(rec["claim_names"] == CLAIM_NAMES, "claim_names must be the six names in order")
    need(rec["candidate_files"] == recount, "candidate_files differ from the recount: extra %s missing %s" %
         (sorted(set(rec["candidate_files"]) - set(recount))[:3], sorted(set(recount) - set(rec["candidate_files"]))[:3]))
    cands = rec["candidates"]
    need(isinstance(cands, list) and sorted(c.get("file") for c in cands) == recount, "candidates must hold exactly one entry per candidate file")
    any_reader = False
    for c in cands:
        need(set(c) == {"file", "class", "line", "line_text"}, "candidate keys differ: %s" % c.get("file"))
        need(c["class"] in CLASSES, "class of %s is not one of %s" % (c["file"], CLASSES))
        need(isinstance(c["line"], int) and c["line"] >= 1, "line of %s is not a line number" % c["file"])
        need(isinstance(c["line_text"], str) and 1 <= len(c["line_text"]) <= 160, "line_text of %s must be the cited line, 1 to 160 characters" % c["file"])
        got = line_of(c["file"], c["line"])
        need(got is not None and got.strip().startswith(c["line_text"].strip()) and (len(c["line_text"].strip()) >= 12 or got.strip() == c["line_text"].strip()),
             "the bytes at %s:%s do not begin with line_text (a cited prefix of 12 characters or more, or the whole line)" % (c["file"], c["line"]))
        if c["class"] in ("reads_claim_column", "reads_whole_row"):
            any_reader = True
        if c["class"] == "reads_claim_column":
            need(any(n in c["line_text"] for n in CLAIM_NAMES), "%s is classed reads_claim_column but its cited line names no claim column" % c["file"])
    want = "grant_A" if any_reader else "see_manifest"
    need(rec["decision"] == want, "decision must be %s given the classes, got %s" % (want, rec["decision"]))
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1600, "words must be one paragraph of 80 to 1600 characters")
    need(not LONG_DIGITS.findall(rec["words"]), "words carry a run of 8 or more digits")
    return want


def check_contract(decision, base, new):
    if decision == "grant_A":
        need(new == base, "the decision is grant_A, so the contract must be unchanged")
        return True
    need(new.get("contract_version") == NEW_VERSION and base.get("contract_version") == BASE_VERSION, "contract_version must go %s to %s" % (BASE_VERSION, NEW_VERSION))
    bcols, ncols = base["columns"], new["columns"]
    need([(c["name"], c["type"], c["nullable"]) for c in bcols] == [(c["name"], c["type"], c["nullable"]) for c in ncols], "the column names, types, nullability or order changed")
    need(new.get("schema_hash") == base.get("schema_hash"), "schema_hash must not change (no column is added or dropped)")
    marked = [c["name"] for c in ncols if c.get("carrier") == "see_manifest"]
    need(marked == [c["name"] for c in ncols if c["name"] in CLAIM_NAMES] and sorted(marked) == sorted(CLAIM_NAMES), "exactly the six claim columns carry carrier see_manifest: %s" % marked)
    for b, n in zip(bcols, ncols):
        rest = {k: v for k, v in n.items() if k != "carrier"}
        need(rest == b, "column %s changed beyond the carrier key" % b["name"])
        if b["name"] not in CLAIM_NAMES:
            need("carrier" not in n, "column %s must not carry a carrier key" % b["name"])
    for k in set(base) | set(new):
        if k not in ("contract_version", "columns", "supersedes", "carrier_note"):
            need(base.get(k) == new.get(k), "contract key %s changed" % k)
    need(isinstance(new.get("carrier_note"), str) and "manifest" in new["carrier_note"] and 40 <= len(new["carrier_note"]) <= 900, "carrier_note must say where the claims travel (the per-fire manifest), 40 to 900 characters")
    need(new["supersedes"].get("contract_version") == BASE_VERSION and new["supersedes"].get("schema_hash") == base["schema_hash"], "supersedes must name 0.6.0 and its schema hash")
    return True


# ------------------------------------------------------------------------------------------------ the live run
def main_tree(root):
    out, rc = git(root, "rev-parse", "--git-common-dir")
    p = Path(out.strip())
    if not p.is_absolute():
        p = (Path(root) / p).resolve()
    return p.parent


def recount_files(root):
    names = CLAIM_NAMES + [DIM_TOKEN]
    args = []
    for n in names:
        args += ["-e", n]
    out, _ = git(root, "grep", "-l", "-F", *args)
    files = [f for f in out.split("\n") if f.strip()]
    port = main_tree(root) / "portal"
    if (port / ".git").exists():
        pout, _ = git(port, "grep", "-l", "-F", *args)
        files += ["portal/" + f for f in pout.split("\n") if f.strip()]
    return sorted(f for f in set(files) if not is_excluded(f))


def line_reader(root):
    def line_of(rel, n):
        p = Path(root) / rel
        if rel.startswith("portal/"):
            p = main_tree(root) / rel
        if not p.is_file():
            return None
        lines = p.read_bytes().decode("utf-8", "replace").splitlines()
        return lines[n - 1] if 1 <= n <= len(lines) else None
    return line_of


def run(root, cid):
    root = Path(root)
    rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
    recount = recount_files(root)
    if cid == "DB126-2-AC1":
        want = check_record(rec, recount, line_reader(root))
        print("OK: claim-column reader read: %d candidate files (recounted, claim names and the dim token, tests, org, docs, projects, workflows, markdown and the producer excluded), every one classed with its cited line verified; decision %s" % (len(recount), want))
        return True
    if cid == "DB126-2-AC2":
        want = check_record(rec, recount, line_reader(root))
        base = json.loads(subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (base_commit(root), CONTRACT_REL)], capture_output=True).stdout.decode("utf-8"))
        new = json.loads((root / CONTRACT_REL).read_text(encoding="utf-8"))
        check_contract(want, base, new)
        print("OK: dim contract matches decision %s (%s)" % (want, "unchanged" if want == "grant_A" else "0.7.0, six claim columns carrier see_manifest, schema_hash unchanged, nothing else changed"))
        return True
    raise Fail("unknown criterion %s" % cid)


# ------------------------------------------------------------------------------------------------ the self-test
def selftest():
    import copy

    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)

    files = ["a/x.py", "b/y.json"]
    text = {("a/x.py", 3): "df = read(dim_return_method)", ("b/y.json", 7): '"tolerance_claim": "measured"'}

    def line_of(f, n):
        return text.get((f, n))
    rec = {"claim_names": list(CLAIM_NAMES), "candidate_files": list(files),
           "candidates": [{"file": "a/x.py", "class": "names_prefix_or_grant_only", "line": 3, "line_text": "df = read(dim_return_method)"},
                          {"file": "b/y.json", "class": "comment_or_doc_only", "line": 7, "line_text": '"tolerance_claim": "measured"'}],
           "decision": "see_manifest", "words": "w" * 120}
    assert check_record(rec, files, line_of) == "see_manifest"
    r2 = copy.deepcopy(rec)
    r2["candidates"][1]["class"] = "reads_claim_column"
    r2["decision"] = "grant_A"
    assert check_record(r2, files, line_of) == "grant_A"
    arms = (("missing file", lambda r: r["candidate_files"].pop()), ("extra file", lambda r: r["candidate_files"].append("c.py")),
            ("bad class", lambda r: r["candidates"][0].update({"class": "unknown"})), ("wrong line", lambda r: r["candidates"][0].update({"line": 4})),
            ("wrong text", lambda r: r["candidates"][0].update({"line_text": "other"})),
            ("decision ignores reader", lambda r: (r["candidates"][1].update({"class": "reads_claim_column"}))),
            ("decision A without reader", lambda r: r.update({"decision": "grant_A"})),
            ("reader cites no claim name", lambda r: (r["candidates"][0].update({"class": "reads_claim_column"}), r.update({"decision": "grant_A"}))),
            ("whole row ignored", lambda r: r["candidates"][1].update({"class": "reads_whole_row"})),
            ("short words", lambda r: r.update({"words": "x"})), ("extra key", lambda r: r.update({"x": 1})),
            ("claim names", lambda r: r.update({"claim_names": ["a"]})), ("digits", lambda r: r.update({"words": "w" * 100 + " 123456789"})))
    for label, fn in arms:
        r3 = copy.deepcopy(rec)
        fn(r3)
        red(lambda: check_record(r3, files, line_of), label)
    base = {"contract_version": BASE_VERSION, "schema_hash": "h", "supersedes": {"contract_version": "0.5.0", "schema_hash": "g"},
            "columns": [{"name": n, "type": "string", "nullable": False, "meaning": "m"} for n in CLAIM_NAMES + ["method_version"]]}
    new = copy.deepcopy(base)
    new["contract_version"] = NEW_VERSION
    new["supersedes"] = {"contract_version": BASE_VERSION, "schema_hash": "h"}
    new["carrier_note"] = "the claims travel in the per-fire manifest thresholds object, not in this dimension row; columns kept for the history"
    for c in new["columns"]:
        if c["name"] in CLAIM_NAMES:
            c["carrier"] = "see_manifest"
    assert check_contract("see_manifest", base, new)
    assert check_contract("grant_A", base, base)
    red(lambda: check_contract("grant_A", base, new), "grant_A but changed")
    red(lambda: check_contract("see_manifest", base, base), "see_manifest but unchanged")
    for label, fn in (("version", lambda n: n.update({"contract_version": "0.8.0"})), ("hash", lambda n: n.update({"schema_hash": "x"})),
                      ("column dropped", lambda n: n["columns"].pop()), ("unmarked", lambda n: n["columns"][0].pop("carrier")),
                      ("extra marked", lambda n: n["columns"][-1].update({"carrier": "see_manifest"})),
                      ("meaning edited", lambda n: n["columns"][0].update({"meaning": "z"})),
                      ("note missing", lambda n: n.pop("carrier_note")), ("other key", lambda n: n.update({"table": "t"})),
                      ("supersedes", lambda n: n["supersedes"].update({"schema_hash": "q"}))):
        n2 = copy.deepcopy(new)
        fn(n2)
        red(lambda: check_contract("see_manifest", base, n2), label)
    assert is_excluded("a/tests/x.py") and is_excluded("a/test_x.py") and is_excluded("org/x") and is_excluded("projects/a.json") and is_excluded("n/readme.md") and is_excluded(PRODUCER_REL) and not is_excluded("infra/a.tf")
    print("selftest: record (12 red arms), contract (both branches, 11 red arms) and exclusion clauses behave")
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except (Fail, OSError, ValueError, KeyError, TypeError, IndexError) as e:
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
