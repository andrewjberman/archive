"""r3_checks.py -- MDPF_CANON round 3 (issuer 2.0.0_SA_COO~D1): one file, three checks, one per cell.

Usage (repo root of the checkout under test): python <this file> basis|writer|reader

Round-2 analysis (ledger/ROUND_ANALYSIS.round2.md @71e85b7191) section 3 items 2-4. Each subcommand prints one line per arm and
"ROUND 3 <NAME>: <k> of <n> arms", and exits 0 only when every arm passes. Reads only; writes nothing; no AWS.

basis   (CN-c-1, M7 recut) deliverables/0.9.0_WK_MDPF_CANON~8/X2_GLOBAL_BASIS.md and the conformance ledger's X2 row
  1 SHAPE     a "# ..." document with a line "AS-OF:" naming an ISO date and a line "DENOMINATOR:" naming a count, and the three
              headings: "Field families", "Single-firm entries", "Method".
  2 FAMILIES  the Field families section holds one table row for each of: headline sums, by_model, non_model_aua,
              inflection_non_model_aua; each row carries an integer minimum firm count in a cell headed "min firms".
  3 CITED     infra/logic/06_CONFORMANCE_LEDGER.md's X2 row cites this file's path.
writer  (CN-c-2, M8) data/mdpf/scripts/bronze/pull_orion_model_composition.py and infra/aws/terraform/mdpf-pipeline/iam.tf
  1 NO TYPED  the script carries no string literal (docstrings excluded) containing "mdpf/bronze" and no bucket literal
              "opal-data-mdpf", and imports the builder (opal_naming).
  2 DEST      bronze_destination("2026-10-09") returns (bucket, key_prefix) equal to address("mdpf", "inflection", "bronze",
              "orion_model_composition", "date=2026-10-09") split at the bucket; the script puts each model file at
              "<key_prefix>/model_<id>.json" and the meta at "<key_prefix>/_meta/pull_complete.json".
  3 GRANT     iam.tf carries an s3:PutObject statement whose resource is the bucket and prefix of arm 2 (a literal ARN equal to the
              builder's, or an interpolation of a module output).
reader  (CN-c-3, M4 slice 1) data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py
  1 NO TYPED  the script carries no string literal (docstrings excluded) containing "mdpf/bronze", and imports the builder
              (opal_naming). The feeder's own OUTPUT bucket literal is not this cell's and is not graded.
  2 SOURCE    bronze_partition_prefix("2026-10-09") equals the writer's bronze_destination("2026-10-09") byte for byte.
  3 ROLL      resolve_bronze_date, given a fake S3 listing whose partitions are date=2026-10-05 and date=2026-10-07 under the builder's
              parent prefix, resolves 2026-10-09 to ("2026-10-07", 2), and 2026-10-07 to ("2026-10-07", 0).
"""
import importlib.util
import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
# R3_ROOT points the files under test at a reference tree (the issuer's green control); the builder is always the repo's own.
ROOT = os.environ.get("R3_ROOT") or REPO
sys.path.insert(0, os.path.join(REPO, "lib"))
sys.path.insert(0, REPO)

BASIS = "org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~8/X2_GLOBAL_BASIS.md"
LEDGER = "infra/logic/06_CONFORMANCE_LEDGER.md"
WRITER = "data/mdpf/scripts/bronze/pull_orion_model_composition.py"
READER = "data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py"
IAM = "infra/aws/terraform/mdpf-pipeline/iam.tf"
arms = []


def arm(name, ok, line):
    arms.append((name, bool(ok), line))


def text(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def finish(label):
    for i, (n, ok, line) in enumerate(arms, 1):
        print("ARM %d %s: %s -- %s" % (i, n, "PASS" if ok else "FAIL", line))
    k = sum(1 for _, ok, _ in arms if ok)
    print("ROUND 3 %s: %d of %d arms" % (label, k, len(arms)))
    return 0 if k == len(arms) else 1


def expected_dest(date):
    from opal_naming import address
    uri = address("mdpf", "inflection", "bronze", "orion_model_composition", "date=" + date)
    bucket, key = uri[len("s3://"):].split("/", 1)
    return bucket, key


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def typed_home(src, bucket_too=True):
    """String literals (docstrings excluded) naming the old bronze home, and whether the builder is imported."""
    import ast
    tree = ast.parse(src)
    doc = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = getattr(node, "body", [])
            if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant):
                doc.add(id(b[0].value))
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in doc:
            v = node.value
            if "mdpf/bronze" in v or (bucket_too and v == "opal-data-mdpf"):
                bad.append(v)
    return bad, ("opal_naming" in src)


def basis():
    t = text(BASIS)
    if t is None:
        arm("SHAPE", False, "%s is absent" % BASIS)
        arm("FAMILIES", False, "no document")
        arm("CITED", False, "no document to cite")
        return finish("BASIS")
    asof = re.search(r"^AS-OF:\s*(\d{4}-\d{2}-\d{2})", t, re.M)
    den = re.search(r"^DENOMINATOR:\s*.*\d", t, re.M)
    heads = [h for h in ("Field families", "Single-firm entries", "Method")
             if re.search(r"^#+\s*" + re.escape(h) + r"\b", t, re.M)]
    arm("SHAPE", asof and den and len(heads) == 3,
        "as-of %s, denominator %s, headings %d of 3" % (asof.group(1) if asof else "none", "present" if den else "none", len(heads)))
    sect = re.search(r"^#+\s*Field families\b(.*?)(?=^#+\s|\Z)", t, re.M | re.S)
    body = sect.group(1) if sect else ""
    header = [ln for ln in body.splitlines() if ln.strip().startswith("|") and re.search(r"min firms", ln, re.I)]
    cols = [c.strip().lower() for c in header[0].strip().strip("|").split("|")] if header else []
    idx = cols.index("min firms") if "min firms" in cols else -1
    found = []
    for fam in ("headline sums", "by_model", "non_model_aua", "inflection_non_model_aua"):
        ok = False
        for ln in body.splitlines():
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if ln.strip().startswith("|") and cells and fam in cells[0].lower().replace("`", "") and idx >= 0 and len(cells) > idx \
                    and re.fullmatch(r"\d+", cells[idx]):
                ok = True
        found.append((fam, ok))
    arm("FAMILIES", all(ok for _, ok in found) and idx >= 0,
        "%d of 4 families carry an integer in the min firms column%s"
        % (sum(1 for _, ok in found if ok), "" if idx >= 0 else " (no 'min firms' column)"))
    led = text(LEDGER) or ""
    rows = [ln for ln in led.splitlines() if re.search(r"\bX2\b", ln)]
    arm("CITED", any(BASIS in ln for ln in rows), "%d ledger line(s) name X2; %d cite the basis path"
        % (len(rows), sum(1 for ln in rows if BASIS in ln)))
    return finish("BASIS")


def writer():
    src = text(WRITER)
    if src is None:
        arm("NO TYPED", False, "absent")
        arm("DEST", False, "absent")
        arm("GRANT", False, "absent")
        return finish("WRITER")
    bad, imp = typed_home(src)
    arm("NO TYPED", not bad and imp, "typed-home literals: %s; imports opal_naming: %s" % (bad or "none", imp))
    want_bucket, want_key = expected_dest("2026-10-09")
    ok, line = False, ""
    try:
        mod = load(WRITER, "r3_writer")
        got = mod.bronze_destination("2026-10-09")
        ok = tuple(got) == (want_bucket, want_key)
        line = "got %s, want %s" % (tuple(got), (want_bucket, want_key))
        uses = ('{key_prefix}' in src or "key_prefix" in src) and "pull_complete.json" in src
        ok = ok and uses
        line += "; put keys compose from the prefix: %s" % uses
    except Exception as e:  # a missing function is the base state
        line = "%s: %s" % (type(e).__name__, str(e)[:120])
    arm("DEST", ok, line)
    iam = text(IAM) or ""
    hit = False
    # line-wise, not quote-wise: an interpolation holds quotes (scope_bucket["mdpf"]) -- the round-2 W7-S1 defect
    for m in re.finditer(r"arn:aws:s3:::[^\n]*orion_model_composition[^\n]*", iam):
        s = m.group(0)
        if "${" in s and "module." in s:
            hit = True
        elif s.startswith("arn:aws:s3:::" + want_bucket + "/" + want_key.rsplit("/", 1)[0]):
            hit = True
    put = "s3:PutObject" in iam
    arm("GRANT", hit and put, "an orion_model_composition ARN on the builder's bucket and prefix: %s; s3:PutObject present: %s"
        % (hit, put))
    return finish("WRITER")


def reader():
    src = text(READER)
    if src is None:
        arm("NO TYPED", False, "absent")
        arm("SOURCE", False, "absent")
        arm("ROLL", False, "absent")
        return finish("READER")
    bad, imp = typed_home(src, bucket_too=False)
    arm("NO TYPED", not bad and imp, "old bronze path literals: %s; imports opal_naming: %s" % (bad or "none", imp))
    want = expected_dest("2026-10-09")
    mod, line, ok = None, "", False
    try:
        mod = load(READER, "r3_reader")
        got = tuple(mod.bronze_partition_prefix("2026-10-09"))
        ok = got == want
        line = "got %s, want %s" % (got, want)
    except Exception as e:
        line = "%s: %s" % (type(e).__name__, str(e)[:120])
    arm("SOURCE", ok, line)
    ok2, line2 = False, ""
    try:
        bucket, key = want
        parent = key.rsplit("/", 1)[0] + "/"

        class Pager:
            def paginate(self, **kw):
                assert kw["Bucket"] == bucket, "listed bucket %r" % kw["Bucket"]
                pfx = kw["Prefix"]
                assert parent.startswith(pfx) or pfx.startswith(parent), "listed prefix %r not the parent %r" % (pfx, parent)
                return [{"CommonPrefixes": [{"Prefix": parent + "date=2026-10-05/"}, {"Prefix": parent + "date=2026-10-07/"}]}]

        class S3:
            def get_paginator(self, _):
                return Pager()

        mod._s3 = lambda: S3()
        a = tuple(mod.resolve_bronze_date("2026-10-09"))
        b = tuple(mod.resolve_bronze_date("2026-10-07"))
        ok2 = a == ("2026-10-07", 2) and b == ("2026-10-07", 0)
        line2 = "2026-10-09 -> %s, 2026-10-07 -> %s" % (a, b)
    except Exception as e:
        line2 = "%s: %s" % (type(e).__name__, str(e)[:160])
    arm("ROLL", ok2, line2)
    return finish("READER")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"basis": basis, "writer": writer, "reader": reader}.get(cmd)
    if not fn:
        print("usage: r3_checks.py basis|writer|reader")
        sys.exit(2)
    sys.exit(fn())
