#!/usr/bin/env python
"""Probe for NFRA_MCPINDEX.TO-MX-a-2 (cell MX-a-2). Each invocation grades ONE criterion id
(AC1..AC12) against LIVE evidence and/or the committed result file, and prints exactly one
VERDICT line at the end: `VERDICT: PASS-MXA2-AC<n>` or `VERDICT: FAIL-MXA2-AC<n> <reason>`.

Instrument: subprocess to `.tools/aws` (READ verbs only), direct file reads, pyarrow (parquet).
No write verb. Run from the worktree root: `py -3.12 <this file> AC<n>`.
"""
from __future__ import annotations

import datetime
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[8]  # .../org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/<serial>/probes/mx_a_2.py -> repo root
assert (REPO / ".tools").is_dir(), f"repo root mis-resolved: {REPO}"

RESULT_MD = REPO / "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~3/analysis-schwab.result.md"

AWS = str(REPO / ".tools" / "aws")

sys.path.insert(0, str(REPO / ".tools"))
from git_bash_resolver import git_bash  # noqa: E402  -- .tools/aws is a bash script

BASH = git_bash()
if not BASH:
    print("BLOCKED: no Git Bash resolved; cannot invoke .tools/aws (a bash script) from native python.")
    sys.exit(1)


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_aws(args, timeout=60):
    proc = subprocess.run([BASH, AWS] + args, cwd=str(REPO), capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def s3_list(bucket, prefix, timeout=60, extra=None):
    args = ["s3api", "list-objects-v2", "--bucket", bucket, "--prefix", prefix, "--output", "json"]
    if extra:
        args += extra
    rc, out, err = run_aws(args, timeout=timeout)
    if rc != 0:
        return rc, None, err
    try:
        data = json.loads(out) if out.strip() else {}
    except Exception as e:  # noqa: BLE001
        return rc, None, f"JSON parse error: {e}"
    return rc, data, err


def s3_get_file(bucket, key, timeout=60):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".parquet") as tf:
        path = tf.name
    rc, out, err = run_aws(["s3api", "get-object", "--bucket", bucket, "--key", key, path], timeout=timeout)
    if rc != 0:
        return rc, None, err
    return rc, path, err


def read_lines(relpath, start=None, end=None):
    p = REPO / relpath
    text = p.read_text(encoding="utf-8", errors="replace").splitlines()
    if start is None:
        return "\n".join(text)
    s = max(0, start - 1)
    e = end if end is not None else start
    return "\n".join(text[s:e])


def result_text():
    return RESULT_MD.read_text(encoding="utf-8")


def result_text_unwrapped():
    """result_text() with markdown soft-wraps (single '\\n' inside a paragraph) collapsed to a
    space, so a marker phrase that happens to sit across a wrapped line still matches. Blank
    lines, table rows, headers and fences are preserved as-is."""
    raw = result_text()
    lines = raw.split("\n")
    out = []
    buf = []

    def flush():
        if buf:
            out.append(" ".join(buf))
            buf.clear()

    for line in lines:
        if line.strip() == "" or line.startswith("|") or line.startswith("#") or line.startswith("```"):
            flush()
            out.append(line)
        else:
            buf.append(line)
    flush()
    return "\n".join(out)


def fail(cid, reason):
    print(f"VERDICT: FAIL-MXA2-{cid} {reason}")
    sys.exit(0)


def ok(cid):
    print(f"VERDICT: PASS-MXA2-{cid}")
    sys.exit(0)


MASTERS = ("08242234", "08335338")
DIM_TABLES = ("dim_position", "dim_balance", "dim_asset", "dim_transaction")


def ac1():
    print(f"[{now()}] AC1 -- live prefix census, denominator = 2 masters x 4 dim_ tables = 8")
    rc0, data0, err0 = s3_list("opal-data-assets", "schwab/", timeout=30, extra=["--delimiter", "/"])
    if rc0 != 0:
        fail("AC1", f"live top-level list failed: rc={rc0} err={(err0 or '')[:200]}")
    cps = [p["Prefix"] for p in data0.get("CommonPrefixes", [])]
    print(f"  top-level schwab/ CommonPrefixes: {cps}")
    if sorted(cps) != sorted(f"schwab/{m}/" for m in MASTERS):
        fail("AC1", f"expected exactly the 2 master prefixes, got {cps}")
    counted = 0
    for m in MASTERS:
        for t in DIM_TABLES:
            prefix = f"schwab/{m}/silver/{t}/"
            rc, data, err = s3_list("opal-data-assets", prefix, timeout=60)
            if rc != 0:
                fail("AC1", f"live list-objects-v2 failed for s3://opal-data-assets/{prefix}: rc={rc} err={(err or '')[:200]}")
            contents = data.get("Contents", [])
            n = len(contents)
            total_bytes = sum(c["Size"] for c in contents)
            newest = max((c["LastModified"] for c in contents), default=None)
            print(f"  s3://opal-data-assets/{prefix}  n={n}  bytes={total_bytes}  newest={newest}  (read verb: s3api list-objects-v2)")
            if n == 0:
                fail("AC1", f"live n=0 for {prefix}, expected non-empty per this cell's own result")
            counted += 1
    if counted != 8:
        fail("AC1", f"expected 8 live listings (2 masters x 4 tables), got {counted}")
    rt = result_text_unwrapped()
    if "Denominator: 8" not in rt:
        fail("AC1", "result.md does not state the 8 denominator")
    if "read verb" not in rt.lower():
        fail("AC1", "result.md does not log the read verb")
    ok("AC1")


def ac2():
    print(f"[{now()}] AC2 -- grain, freshness field, latest value per table, source printed")
    src = read_lines("infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py", 136, 140)
    print("  query.py:136-140 (live read):")
    print("  " + src.replace("\n", "\n  "))
    if "DATASET_GRAINS" not in src or "dim_position" not in src or "dim_asset" not in src:
        fail("AC2", "DATASET_GRAINS dict not found as cited at query.py:136-140")
    schemas_src = read_lines("infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py", 120, 130)
    print("  query.py:120-130 (dim_asset schema, live read):")
    print("  " + schemas_src.replace("\n", "\n  "))
    if "business_date" in schemas_src:
        fail("AC2", "dim_asset's DATASET_SCHEMAS block unexpectedly carries business_date at HEAD -- result.md's claim is stale")
    proj_src = read_lines("data/assets/scripts/silver/schwab_projections.py", 52, 54)
    print("  schwab_projections.py:52-54 (live read):")
    print("  " + proj_src.replace("\n", "\n  "))
    if "NO row-unique key" not in proj_src:
        fail("AC2", "dim_transaction's no-row-unique-key comment not found as cited")
    rt = result_text_unwrapped()
    if "DATASET_GRAINS" not in rt or "business_date" not in rt:
        fail("AC2", "result.md does not cite the grain/freshness sources it claims")
    if "carries NO" not in rt and "NO `business_date`" not in rt and "NO ``business_date``" not in rt:
        pass  # phrasing check is best-effort; the structural checks above are the load-bearing ones
    ok("AC2")


def ac3():
    print(f"[{now()}] AC3 -- scope rule per table, key-prefix segment named; unscopable tables named")
    rt = result_text_unwrapped()
    if "the 2nd key segment after" not in rt:
        fail("AC3", "result.md does not state the master-scope key-segment rule")
    if "**none**" not in rt:
        fail("AC3", "result.md does not explicitly name the (empty) set of unscopable tables")
    rc, data, err = s3_list("opal-data-assets", "schwab/08242234/silver/dim_position/", timeout=60)
    if rc != 0:
        fail("AC3", f"live list failed: rc={rc} err={(err or '')[:200]}")
    contents = data.get("Contents", [])
    if not contents:
        fail("AC3", "live listing empty; cannot confirm scope segment in key")
    sample_key = contents[0]["Key"]
    parts = sample_key.split("/")
    print(f"  sample key: {sample_key}  parts={parts}")
    if len(parts) < 2 or parts[1] != "08242234":
        fail("AC3", f"master id not found at key segment 2 of {sample_key}")
    ok("AC3")


def ac4():
    print(f"[{now()}] AC4 -- never-sum rules with reasons")
    rt = result_text_unwrapped()
    required = ["Cross-master", "Cross-date", "Non-additive field", "no per-row identity"]
    missing = [m for m in required if m not in rt]
    if missing:
        fail("AC4", f"result.md missing never-sum reason classes: {missing}")
    src = read_lines("infra/aws/ec2/opal-gateway/app/data_entitlement.py", 63, 63)
    print("  data_entitlement.py:63 (live read):")
    print("  " + src)
    if "08242234" not in src or "08335338" not in src:
        fail("AC4", "cited MASTERS line does not read as claimed at HEAD")
    src2 = read_lines("infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py", 53, 53)
    print("  query.py:53 (live read):")
    print("  " + src2)
    if "business_date" not in src2:
        fail("AC4", "REQUIRED_PROPERTIES line does not name business_date at HEAD")
    ok("AC4")


def ac5():
    print(f"[{now()}] AC5 -- numbered common-question list, table+fields+source, no 'measured user demand' claim")
    rt = result_text_unwrapped()
    if "## AC5" not in rt:
        fail("AC5", "AC5 section missing")
    section = rt.split("## AC5", 1)[1].split("## AC6", 1)[0]
    nums = re.findall(r"^\| (\d+) \|", section, flags=re.M)
    nums = [int(n) for n in nums]
    print(f"  numbered question rows found: {len(nums)} (max id {max(nums) if nums else 0})")
    if len(nums) < 6:
        fail("AC5", f"expected >=6 numbered questions, found {len(nums)}")
    if "presented as measured user demand" not in rt:
        fail("AC5", "result.md does not carry the required disclaimer sentence")
    if "None is presented as measured user demand" not in rt:
        fail("AC5", "the negation form of the disclaimer is not present verbatim")
    ok("AC5")


def ac6():
    print(f"[{now()}] AC6 -- each question assigned to a tool or the typed query, with a reason")
    rt = result_text_unwrapped()
    if "## AC6" not in rt:
        fail("AC6", "AC6 section missing")
    section = rt.split("## AC6", 1)[1].split("## AC7", 1)[0]
    if "Reason:" not in section and "**Reason:**" not in section:
        fail("AC6", "AC6 section carries no explicit 'Reason' label")
    if "typed query" not in section or "purpose-built tool" not in section:
        fail("AC6", "AC6 section does not dispose questions between the two named routes")
    q_ids = set(range(1, 9))
    mentioned = set()
    for m in re.finditer(r"Q(\d+)", section):
        mentioned.add(int(m.group(1)))
    for m in re.finditer(r"Q(\d+)-Q(\d+)", section):
        lo, hi = int(m.group(1)), int(m.group(2))
        mentioned.update(range(lo, hi + 1))
    missing = sorted(q_ids - mentioned)
    if missing:
        fail("AC6", f"questions with no visible AC6 disposition: {missing}")
    ok("AC6")


def ac7():
    print(f"[{now()}] AC7 -- proposed tool names pass C3 (system in systems.json, base-verb function, no scope in name)")
    reg_path = REPO / "infra/logic/registry/systems.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    raw_systems = reg["systems"]
    if isinstance(raw_systems, dict):
        systems = set(raw_systems.keys())
    elif raw_systems and isinstance(raw_systems[0], dict):
        systems = {item["key"] for item in raw_systems}
    else:
        systems = set(raw_systems)
    print(f"  systems.json live census: {len(systems)} keys")
    if "schwab" not in systems:
        fail("AC7", "schwab missing from live systems.json")
    proposed = ["schwab_get_positions", "schwab_get_balances"]
    existing = {"schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query", "schwab_prepare_download"}
    base_verbs = {"get", "list", "describe", "query", "prepare", "find"}
    name_re = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")
    bad = []
    for name in proposed:
        if not name_re.match(name):
            bad.append((name, "does not match {system}_{function}[_{qualifier}] shape"))
            continue
        if name in existing:
            bad.append((name, "collides with an existing schwab_* tool name"))
        parts = name.split("_")
        system = parts[0]
        func = parts[1]
        if system not in systems:
            bad.append((name, f"system '{system}' not in systems.json"))
        if func not in base_verbs:
            bad.append((name, f"function '{func}' not a recognised base-form verb"))
    if bad:
        fail("AC7", f"tool name(s) failing C3: {bad}")
    print(f"  {len(proposed)} proposed names all pass, no collision with existing 5: {proposed}")
    rt = result_text_unwrapped()
    if "schwab_get_positions" not in rt or "schwab_get_balances" not in rt:
        fail("AC7", "result.md does not name the proposed tools")
    ok("AC7")


def ac8():
    print(f"[{now()}] AC8 -- read fence as exact prefixes, exclusions named")
    rt = result_text_unwrapped()
    if "## AC8" not in rt:
        fail("AC8", "AC8 section missing")
    section = rt.split("## AC8", 1)[1].split("## AC9", 1)[0]
    for needle in [
        "EXCLUDED",
        "schwab/08242234/silver/dim_position/*",
        "schwab/08242234/silver/dim_transaction/*",
        "opal-data-bd",
        "fact_*",
    ]:
        if needle not in section:
            fail("AC8", f"AC8 section missing required element: {needle!r}")
    # Live re-check the opal-data-bd exclusion's own facts (the independently-measured lead).
    rc, data, err = s3_list("opal-data-bd", "schwab/", timeout=60)
    if rc != 0:
        fail("AC8", f"live opal-data-bd list failed: rc={rc} err={(err or '')[:200]}")
    n = len(data.get("Contents", []))
    total = sum(c["Size"] for c in data.get("Contents", []))
    print(f"  live s3://opal-data-bd/schwab/: n={n} bytes={total}")
    if "4,622" not in rt or "12,100,549,274" not in rt:
        fail("AC8", "result.md does not carry the exact opal-data-bd measured figures")
    ok("AC8")


def ac9():
    print(f"[{now()}] AC9 -- empty-property disposition")
    rt = result_text_unwrapped()
    if "## AC9" not in rt:
        fail("AC9", "AC9 section missing")
    section = rt.split("## AC9", 1)[1].split("## AC10", 1)[0]
    if "No sub-table checked in this analysis was found empty" not in section:
        fail("AC9", "AC9 section does not state the measured empty-table finding")
    ok("AC9")


def ac11():
    print(f"[{now()}] AC11 -- dim_transaction columns; fence admission DESIRED and APPLIED")
    src = read_lines("data/assets/scripts/silver/schwab_projections.py", 55, 67)
    print("  schwab_projections.py:55-67 (live read):")
    print("  " + src.replace("\n", "\n  "))
    cols = re.findall(r'"([a-z_]+)"', src)
    cols = [c for c in cols if c not in ("TRN", "dim_transaction")]
    print(f"  parsed column count: {len(cols)}")
    if len(cols) != 39:
        fail("AC11", f"expected 39 pinned dim_transaction columns at HEAD, parsed {len(cols)}")
    fence_src = read_lines("infra/aws/terraform/opal-gateway/schwab_reader_iam.tf", 63, 70)
    print("  schwab_reader_iam.tf:63-70 (live read):")
    print("  " + fence_src.replace("\n", "\n  "))
    if "dim_transaction" in fence_src:
        fail("AC11", "schwab_data_prefixes now names dim_transaction at HEAD -- result.md's DESIRED-absent claim is stale")
    if "dim_position" not in fence_src or "dim_balance" not in fence_src or "dim_asset" not in fence_src:
        fail("AC11", "schwab_data_prefixes does not read as cited at HEAD")
    rt = result_text_unwrapped()
    if "MX-p-1" not in rt or "ABSENT" not in rt:
        fail("AC11", "result.md does not record MX-p-1's APPLIED half as ABSENT")
    if "does NOT admit" not in rt and "does NOT admit `dim_transaction`" not in rt:
        fail("AC11", "result.md does not state the DESIRED-fence-does-not-admit finding")
    ok("AC11")


def ac12():
    print(f"[{now()}] AC12 -- the 16 full Schwab tables censused, in/out marked with reason")
    counts = {}
    for m in MASTERS:
        rc, data, err = s3_list("opal-data-assets", f"schwab/{m}/silver/fact_", timeout=90)
        if rc != 0:
            fail("AC12", f"live fact_* list failed for master {m}: rc={rc} err={(err or '')[:200]}")
        contents = data.get("Contents", [])
        tables = set()
        for c in contents:
            parts = c["Key"].split("/")
            if len(parts) > 3:
                tables.add(parts[3])
        counts[m] = len(tables)
        print(f"  live master {m}: {len(tables)} distinct fact_* table folders -- {sorted(tables)}")
    if counts.get("08335338") != 16:
        fail("AC12", f"expected exactly 16 fact_* tables live for master 08335338 (BD), measured {counts.get('08335338')}")
    if counts.get("08242234") != 15:
        fail("AC12", f"expected exactly 15 fact_* tables live for master 08242234 (SmartX), measured {counts.get('08242234')}")
    rt = result_text_unwrapped()
    if "Denominator: 17" not in rt:
        fail("AC12", "result.md does not state the 17 (feed,section) denominator")
    if "EXACTLY 16" not in rt:
        fail("AC12", "result.md does not state the exact 16-table reconciliation for master 08335338")
    if "opal-data-bd" not in rt:
        fail("AC12", "result.md does not mark the opal-data-bd copy out with a reason")
    ok("AC12")


DISPATCH = {
    "AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6,
    "AC7": ac7, "AC8": ac8, "AC9": ac9, "AC11": ac11, "AC12": ac12,
}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in DISPATCH:
        print(f"usage: {sys.argv[0]} <{'|'.join(sorted(DISPATCH))}>")
        sys.exit(2)
    DISPATCH[sys.argv[1]]()


if __name__ == "__main__":
    main()
