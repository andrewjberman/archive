"""r2_checks.py -- MDPF_CANON round 2 (issuer 2.0.0_SA_COO~D1): one file, four checks, one per cell.

Usage (repo root of the checkout under test): python <this file> census|basis|publisher|builder

The round-1 analysis (ledger/ROUND_ANALYSIS.round1.md @409182ae5a) section 3, items 2-4. Each subcommand prints one line per arm and
"ROUND 2 <NAME>: <k> of <n> arms", and exits 0 only when every arm passes. Reads only; writes nothing; no AWS.

census    (CN-b-1, M1) deliverables/READER_CENSUS.md
  1 SHAPE      the file exists with a "DENOMINATOR:" line and an "INSTRUMENT:" line, and a table whose header names reader, kind,
               evidence and verdict.
  2 SURFACES   at least one row for each of the four surfaces: gold/mdpf_revamp/, portal/gold/mdpf/, the served key
               json/portfolios/aum-timeseries.json, and the old bronze mdpf/bronze/.
  3 EVIDENCE   every evidence cell of the form path:line names a tracked file with at least that many lines.
  4 PLANTED    the evidence comparator refuses a missing file and an out-of-range line.
basis     (CN-b-2, M7) deliverables/X2_GLOBAL_BASIS.md and the conformance ledger's X2 row
  1 SECTIONS   headings for the aggregation level, the minimum firm count, and why no per-firm or per-account row survives.
  2 COUNT      the minimum-firm-count section states an integer of at least 2.
  3 CITED      infra/logic/06_CONFORMANCE_LEDGER.md's X2 row cites the basis file's path.
publisher (CN-b-3, M5's capability, no switch) infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf
  1 RUNTIME    the publisher's runtime is python3.11 (the estate's existing pyarrow layer's runtime; build ladder: reuse).
  2 LAYER      the publisher declares layers referencing a data "aws_lambda_layer_version" whose layer_name is
               pandas-pyarrow-requests-layer, declared in the opal-assets stack.
  3 NO SWITCH  GOLD_BUCKET, GOLD_ROOT, SERVE_BUCKET and SERVE_ROOT are byte-identical to their base values (the read source moves in
               the publisher's own later round, LAST).
builder   (CN-b-4, W1-S1) infra/aws/terraform/mdpf-pipeline/iam.tf aws_iam_role_policy.mdpf_gold_writers
  1 NO LOCAL   no S3 ARN in that policy names ${local.mdpf_bucket}.
  2 BUILDER    every composite ARN's bucket is a module output keyed into the opal_name module's generated scope_bucket map.
  3 EQUALS     the map value used equals the bucket address("mdpf", "global", "gold", <artifact>, "date=...") returns.
"""
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
sys.path.insert(0, ROOT)
DLV = os.path.join(ROOT, "org/missions/D8/MDPF/MDPF_CANON/deliverables")
arms = []


def hcl_strings(text):
    """Every double-quoted HCL string in text, with a quote inside a ${...} interpolation kept inside the string
    (amended on row MDPF_CANON-D1-W7-S1: `"arn:aws:s3:::${module.m.scope_bucket["mdpf"]}/..."` is ONE string)."""
    out, i, n = [], 0, len(text)
    while i < n:
        if text[i] != '"':
            i += 1
            continue
        j, depth, buf = i + 1, 0, []
        while j < n:
            c = text[j]
            if depth == 0 and c == '"':
                break
            if c == "\\" and j + 1 < n:
                buf.append(text[j:j + 2])
                j += 2
                continue
            if text.startswith("${", j):
                depth += 1
                buf.append("${")
                j += 2
                continue
            if c == "}" and depth:
                depth -= 1
            buf.append(c)
            j += 1
        out.append("".join(buf))
        i = j + 1
    return out


def arm(label, fn):
    f = []
    try:
        detail = fn(f) or ""
    except Exception as e:  # noqa: BLE001 -- an arm that raises is a failed arm, said in its line
        f.append("RAISED: " + (str(e).splitlines() or [repr(e)])[0][:200])
        detail = ""
    arms.append((label, not f, detail if not f else " | ".join(f)))


def read(rel):
    p = os.path.join(ROOT, rel)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


def block(src, kind, label):
    m = re.search(r'(?m)^%s\s+"[^"]*"\s+"%s"\s*\{|^%s\s+"%s"\s*\{' % (kind, re.escape(label), kind, re.escape(label)), src)
    if not m:
        return None
    depth, i = 1, m.end()
    while depth and i < len(src):
        depth += {"{": 1, "}": -1}.get(src[i], 0)
        i += 1
    return src[m.end():i - 1]


# ---------------------------------------------------------------- census
def evidence_fault(cell):
    m = re.fullmatch(r"`?([^`:\s]+):(\d+)`?", cell.strip())
    if not m:
        return None
    path, line = m.group(1), int(m.group(2))
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return f"EVIDENCE: {path} does not exist"
    n = sum(1 for _ in open(full, encoding="utf-8", errors="replace"))
    if line < 1 or line > n:
        return f"EVIDENCE: {path}:{line} is past its {n} lines"
    return ""


def census():
    src = read("org/missions/D8/MDPF/MDPF_CANON/deliverables/READER_CENSUS.md")
    rows = []

    def shape(f):
        if src is None:
            f.append("MISSING: deliverables/READER_CENSUS.md")
            return ""
        for tag in ("DENOMINATOR:", "INSTRUMENT:"):
            if tag not in src:
                f.append(f"no {tag} line")
        hdr = [ln for ln in src.splitlines() if ln.startswith("|") and all(w in ln.lower() for w in ("reader", "kind", "evidence", "verdict"))]
        if not hdr:
            f.append("no table header naming reader, kind, evidence and verdict")
            return ""
        cols = [c.strip().lower() for c in hdr[0].strip("|").split("|")]
        start = src.splitlines().index(hdr[0])
        for ln in src.splitlines()[start + 2:]:
            if not ln.startswith("|"):
                break
            cells = [c.strip() for c in ln.strip("|").split("|")]
            rows.append(dict(zip(cols, cells)))
        return f"{len(rows)} rows"

    def surfaces(f):
        if not rows:
            f.append("INPUT: no rows")
            return ""
        text = "\n".join(" ".join(r.values()) for r in rows)
        for s in ("gold/mdpf_revamp/", "portal/gold/mdpf/", "json/portfolios/aum-timeseries.json", "mdpf/bronze/"):
            if s not in text:
                f.append(f"no row names {s}")
        return "all four surfaces carry rows"

    def evidence(f):
        n = 0
        for r in rows:
            ev = next((v for k, v in r.items() if "evidence" in k), "")
            for cell in re.split(r"[;,]\s*", ev):
                x = evidence_fault(cell)
                if x is None:
                    continue
                n += 1
                if x:
                    f.append(x)
        if rows and n == 0:
            f.append("no evidence cell of the form path:line")
        return f"{n} path:line evidence cells resolve"

    def planted(f):
        if not evidence_fault("no/such/file.py:3"):
            f.append("a missing file was not refused")
        if not evidence_fault("lib/opal_naming.py:999999"):
            f.append("an out-of-range line was not refused")
        if evidence_fault("lib/opal_naming.py:1") != "":
            f.append("a correct cell was refused")
        return "missing file and out-of-range line refused; a correct cell passes"

    arm("SHAPE: DENOMINATOR, INSTRUMENT and the reader/kind/evidence/verdict table", shape)
    arm("SURFACES: rows for both retiring trees, the stale served key and the old bronze", surfaces)
    arm("EVIDENCE: every path:line cell resolves to a file and a line in range", evidence)
    arm("PLANTED: the evidence comparator refuses a missing file and an out-of-range line", planted)
    return "CENSUS"


# ---------------------------------------------------------------- basis
def basis():
    src = read("org/missions/D8/MDPF/MDPF_CANON/deliverables/X2_GLOBAL_BASIS.md")
    led = read("infra/logic/06_CONFORMANCE_LEDGER.md") or ""
    heads = [ln.lower() for ln in (src or "").splitlines() if ln.startswith("#")]

    def sections(f):
        if src is None:
            f.append("MISSING: deliverables/X2_GLOBAL_BASIS.md")
            return ""
        for want in ("aggregation level", "minimum firm count", "per-firm or per-account"):
            if not any(want in h for h in heads):
                f.append(f"no heading naming '{want}'")
        return f"{len(heads)} headings"

    def count(f):
        if src is None:
            f.append("INPUT: no file")
            return ""
        lines = src.splitlines()
        i = next((k for k, ln in enumerate(lines) if ln.startswith("#") and "minimum firm count" in ln.lower()), None)
        if i is None:
            f.append("INPUT: no minimum-firm-count heading")
            return ""
        body = []
        for ln in lines[i + 1:]:
            if ln.startswith("#"):
                break
            body.append(ln)
        nums = [int(x) for x in re.findall(r"\b(\d+)\b", "\n".join(body))]
        if not any(n >= 2 for n in nums):
            f.append("the section states no integer of at least 2")
        return f"integers stated: {sorted(set(nums))[:6]}"

    def cited(f):
        path = "org/missions/D8/MDPF/MDPF_CANON/deliverables/X2_GLOBAL_BASIS.md"
        rows = [ln for ln in led.splitlines() if ln.startswith("|") and re.search(r"\|\s*\**X2\**\s*\|", ln)]
        if not rows:
            f.append("no X2 row in infra/logic/06_CONFORMANCE_LEDGER.md")
        elif not any(path in r for r in rows):
            f.append("the X2 row does not cite " + path)
        return "the ledger's X2 row cites the basis"

    arm("SECTIONS: aggregation level, minimum firm count, why no per-firm or per-account row survives", sections)
    arm("COUNT: the minimum firm count is an integer of at least 2", count)
    arm("CITED: the conformance ledger's X2 row cites the basis file", cited)
    return "BASIS"


# ---------------------------------------------------------------- publisher
BASE_ENV = {"GOLD_BUCKET": "local.monolith_bucket", "GOLD_ROOT": '"portal/gold/mdpf"', "SERVE_BUCKET": "local.platinum_bucket",
            "SERVE_ROOT": '"platinum/mdpf"'}


def publisher():
    tf = read("infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf") or ""
    stack = "".join(open(os.path.join(ROOT, "infra/aws/terraform/opal-assets", n), encoding="utf-8").read()
                    for n in sorted(os.listdir(os.path.join(ROOT, "infra/aws/terraform/opal-assets"))) if n.endswith(".tf"))
    m = re.search(r'(?m)^module\s+"([^"]*publisher[^"]*)"\s*\{', tf)
    body = ""
    if m:
        depth, i = 1, m.end()
        while depth and i < len(tf):
            depth += {"{": 1, "}": -1}.get(tf[i], 0)
            i += 1
        body = tf[m.end():i - 1]

    def runtime(f):
        if not body:
            f.append("no publisher module block in mdpf_portal_publisher.tf")
            return ""
        r = re.search(r'(?m)^\s*runtime\s*=\s*"([^"]+)"', body)
        if not r or r.group(1) != "python3.11":
            f.append(f"runtime is {r.group(1) if r else None!r} (want python3.11, the existing layer's runtime)")
        return "runtime python3.11"

    def layer(f):
        lay = re.search(r'(?m)^\s*layers\s*=\s*\[([^\]]*)\]', body or "")
        if not lay:
            f.append("the publisher declares no layers")
            return ""
        refs = re.findall(r'data\.aws_lambda_layer_version\.([a-z0-9_]+)', lay.group(1))
        ok = False
        for ref in refs:
            d = block(stack, "data", ref)
            if d and re.search(r'layer_name\s*=\s*"pandas-pyarrow-requests-layer"', d):
                ok = True
        if not ok:
            f.append("no layer reference resolves to a data source named pandas-pyarrow-requests-layer in the opal-assets stack")
        return "the layer is the estate's pandas-pyarrow-requests-layer"

    def no_switch(f):
        for k, v in BASE_ENV.items():
            mm = re.search(r'(?m)^\s*%s\s*=\s*(\S+)' % k, body or "")
            if not mm or mm.group(1) != v:
                f.append(f"{k} = {mm.group(1) if mm else None} (want {v} -- the read source does not move this round)")
        return "the four read/serve settings unchanged"

    arm("RUNTIME: the publisher runs python3.11, the estate's pyarrow layer's runtime", runtime)
    arm("LAYER: the publisher carries pandas-pyarrow-requests-layer from the opal-assets stack", layer)
    arm("NO SWITCH: GOLD_BUCKET/GOLD_ROOT/SERVE_BUCKET/SERVE_ROOT unchanged", no_switch)
    return "PUBLISHER"


# ---------------------------------------------------------------- builder
def builder():
    iam = read("infra/aws/terraform/mdpf-pipeline/iam.tf") or ""
    gen = read("infra/aws/terraform/modules/opal_name/generated_locals.tf") or ""
    body = block(iam, "resource", "mdpf_gold_writers") or ""
    arns = [s for s in hcl_strings(body) if s.startswith("arn:aws:s3:::")]
    comp = [a for a in arns if "/mdpf/global/gold/" in a or not a.split(":::", 1)[1].count("/")]

    def no_local(f):
        if not body:
            f.append("no aws_iam_role_policy.mdpf_gold_writers")
            return ""
        bad = [a for a in arns if "${local.mdpf_bucket}" in a]
        if bad:
            f.append(f"{len(bad)} ARN(s) still name ${{local.mdpf_bucket}}")
        return f"{len(arns)} S3 ARNs, none on local.mdpf_bucket"

    keys = []

    def builder_out(f):
        for a in comp:
            m = re.match(r'arn:aws:s3:::\$\{module\.([a-z0-9_]+)\.scope_bucket\["([a-z0-9]+)"\]\}', a)
            if not m:
                f.append(f"not builder output: {a}")
            else:
                keys.append(m.group(2))
        if not comp:
            f.append("no composite ARN found")
        return f"{len(comp)} composite ARN(s) on module scope_bucket[...]"

    def equals(f):
        from lib.opal_naming import address
        want = address("mdpf", "global", "gold", "aum_metrics", "date=2026-10-08").split("/")[2]
        mp = dict(re.findall(r'"([a-z0-9]+)"\s*=\s*"(opal-data-[a-z0-9-]+)"', gen.split("scope_bucket", 1)[1].split("}", 1)[0])) if "scope_bucket" in gen else {}
        if not keys:
            f.append("INPUT: arm 2 resolved no key")
        for k in set(keys):
            if mp.get(k) != want:
                f.append(f'scope_bucket["{k}"] = {mp.get(k)!r}, address() composite bucket = {want!r}')
        return f"the key resolves to {want}"

    arm("NO LOCAL: the gold writers' policy names no ${local.mdpf_bucket}", no_local)
    arm('BUILDER: every composite ARN takes its bucket from module.<opal_name>.scope_bucket["<key>"]', builder_out)
    arm("EQUALS: that map value equals address()'s composite gold bucket", equals)
    return "BUILDER"


which = (sys.argv[1:] or [""])[0]
name = {"census": census, "basis": basis, "publisher": publisher, "builder": builder}.get(which)
if not name:
    print("usage: r2_checks.py census|basis|publisher|builder")
    sys.exit(2)
title = name()
ok = 0
for label, passed, detail in arms:
    ok += passed
    print(f"{'ARM PASS' if passed else 'ARM FAIL'} {label} :: {detail}")
print(f"ROUND 2 {title}: {ok} of {len(arms)} arms")
sys.exit(0 if ok == len(arms) else 1)
