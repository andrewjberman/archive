#!/usr/bin/env python
"""Probe for NFRA_MCPINDEX.TO-MX-a-7 (cell MX-a-7). Each invocation grades ONE criterion id
(AC1..AC11) against LIVE evidence and/or the committed result file, and prints exactly one
VERDICT line at the end: `VERDICT: PASS-MXA7-AC<n>` or `VERDICT: FAIL-MXA7-AC<n> <reason>`.

Instrument: subprocess to `.tools/aws` (READ verbs only), direct file reads, pyarrow (parquet).
No write verb. Run from the worktree root: `py -3.12 <this file> AC<n>`.
"""
from __future__ import annotations

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[8]  # .../org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/<serial>/probes/mx_a_7.py -> repo root
assert (REPO / ".tools").is_dir(), f"repo root mis-resolved: {REPO}"

RESULT_MD = REPO / "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~3/analysis-etfs.result.md"

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
    print(f"VERDICT: FAIL-MXA7-{cid} {reason}")
    sys.exit(0)


def ok(cid):
    print(f"VERDICT: PASS-MXA7-{cid}")
    sys.exit(0)


BUCKET = "opal-data-assets"
# (source, fund, table) -- the property's 8 table/fund combos (2 sources x 2 funds x 2 tables each).
COMBOS = [
    ("trueshares", "DIVZ", "fact_netassets_page"),
    ("trueshares", "IDVZ", "fact_netassets_page"),
    ("trueshares", "DIVZ", "fact_holdings"),
    ("trueshares", "IDVZ", "fact_holdings"),
    ("pathfinder", "PFDE", "fact_holdings"),
    ("pathfinder", "PFOE", "fact_holdings"),
    ("pathfinder", "PFDE", "fact_dailynav"),
    ("pathfinder", "PFOE", "fact_dailynav"),
]


def ac1():
    print(f"[{now()}] AC1 -- live prefix census, denominator = 2 sources x 2 funds x 2 tables = 8")
    rc0, data0, err0 = s3_list(BUCKET, "trueshares/", timeout=30, extra=["--delimiter", "/"])
    if rc0 != 0:
        fail("AC1", f"live trueshares/ list failed: rc={rc0} err={(err0 or '')[:200]}")
    cps_ts = sorted(p["Prefix"] for p in data0.get("CommonPrefixes", []))
    if cps_ts != ["trueshares/DIVZ/", "trueshares/IDVZ/"]:
        fail("AC1", f"expected exactly the 2 trueshares fund prefixes, got {cps_ts}")
    rc1, data1, err1 = s3_list(BUCKET, "pathfinder/", timeout=30, extra=["--delimiter", "/"])
    if rc1 != 0:
        fail("AC1", f"live pathfinder/ list failed: rc={rc1} err={(err1 or '')[:200]}")
    cps_pf = sorted(p["Prefix"] for p in data1.get("CommonPrefixes", []))
    if not {"pathfinder/PFDE/", "pathfinder/PFOE/"}.issubset(set(cps_pf)):
        fail("AC1", f"expected the 2 pathfinder fund prefixes among {cps_pf}")
    counted = 0
    empty = []
    for source, fund, table in COMBOS:
        prefix = f"{source}/{fund}/silver/{table}/"
        rc, data, err = s3_list(BUCKET, prefix, timeout=60)
        if rc != 0:
            fail("AC1", f"live list-objects-v2 failed for s3://{BUCKET}/{prefix}: rc={rc} err={(err or '')[:200]}")
        contents = data.get("Contents", [])
        n = len(contents)
        total_bytes = sum(c["Size"] for c in contents)
        newest = max((c["LastModified"] for c in contents), default=None)
        print(f"  s3://{BUCKET}/{prefix}  n={n}  bytes={total_bytes}  newest={newest}  (read verb: s3api list-objects-v2)")
        if n == 0:
            empty.append((source, fund, table))
        counted += 1
    if counted != 8:
        fail("AC1", f"expected 8 live listings (2 sources x 2 funds x 2 tables), got {counted}")
    print(f"  empty combos (0 objects): {empty}")
    if empty != [("trueshares", "DIVZ", "fact_holdings"), ("trueshares", "IDVZ", "fact_holdings")]:
        fail("AC1", f"expected exactly trueshares fact_holdings (DIVZ, IDVZ) to be the empty combos, got {empty}")
    rt = result_text_unwrapped()
    if "Denominator: 8" not in rt:
        fail("AC1", "result.md does not state the 8 denominator")
    if "read verb" not in rt.lower():
        fail("AC1", "result.md does not log the read verb")
    ok("AC1")


def ac2():
    print(f"[{now()}] AC2 -- grain, freshness field, latest value per table, source printed")
    src = read_lines("data/assets/scripts/silver/etf_schemas.py", 113, 123)
    print("  etf_schemas.py:113-123 (NETASSETS_PAGE_COLS, live read):")
    print("  " + src.replace("\n", "\n  "))
    if "nav_as_of" not in src or "net_assets_as_of" not in src:
        fail("AC2", "NETASSETS_PAGE_COLS dict not found as cited at etf_schemas.py:113-123")
    if "business_date" in src:
        fail("AC2", "fact_netassets_page unexpectedly carries a business_date-named column at HEAD -- result.md's claim is stale")
    hold_src = read_lines("data/assets/scripts/silver/etf_schemas.py", 127, 145)
    print("  etf_schemas.py:127-145 (HOLDINGS_VENDOR/ADDITIVE, live read):")
    print("  " + hold_src.replace("\n", "\n  "))
    if "date_std" not in hold_src or '"Date"' not in hold_src:
        fail("AC2", "HOLDINGS_VENDOR/ADDITIVE dict not found as cited at etf_schemas.py:127-145")
    nav_src = read_lines("data/assets/scripts/silver/etf_schemas.py", 188, 206)
    print("  etf_schemas.py:188-206 (DAILYNAV_VENDOR/ADDITIVE, live read):")
    print("  " + nav_src.replace("\n", "\n  "))
    if "rate_date_std" not in nav_src or '"Rate Date"' not in nav_src:
        fail("AC2", "DAILYNAV_VENDOR/ADDITIVE dict not found as cited at etf_schemas.py:188-206")
    rt = result_text_unwrapped()
    for needle in ("nav_as_of", "date_std", "rate_date_std", "as_of"):
        if needle not in rt:
            fail("AC2", f"result.md does not cite the freshness source it claims ({needle!r} missing)")
    ok("AC2")


def ac3():
    print(f"[{now()}] AC3 -- scope rule per table, key-prefix segment named; unscopable tables named")
    rt = result_text_unwrapped()
    if "2nd" not in rt and "segment 2" not in rt:
        fail("AC3", "result.md does not state the fund-scope key-segment rule")
    if "**none**" not in rt:
        fail("AC3", "result.md does not explicitly name the (empty) set of unscopable tables")
    rc, data, err = s3_list(BUCKET, "trueshares/DIVZ/silver/fact_netassets_page/", timeout=60)
    if rc != 0:
        fail("AC3", f"live list failed: rc={rc} err={(err or '')[:200]}")
    contents = data.get("Contents", [])
    if not contents:
        fail("AC3", "live listing empty; cannot confirm scope segment in key")
    sample_key = contents[0]["Key"]
    parts = sample_key.split("/")
    print(f"  sample key: {sample_key}  parts={parts}")
    if len(parts) < 2 or parts[1] != "DIVZ":
        fail("AC3", f"fund id not found at key segment 2 of {sample_key}")
    ok("AC3")


def ac4():
    print(f"[{now()}] AC4 -- never-sum rules with reasons")
    rt = result_text_unwrapped()
    required = ["Cross-fund", "Cross-date", "Non-additive field"]
    missing = [m for m in required if m not in rt]
    if missing:
        fail("AC4", f"result.md missing never-sum reason classes: {missing}")
    src = read_lines("data/assets/scripts/silver/etf_schemas.py", 56, 60)
    print("  etf_schemas.py:56-60 (live read):")
    print("  " + src)
    if "TRUESHARES_SCOPES" not in src or "PATHFINDER_FUNDS" not in src:
        fail("AC4", "cited scope-tuple lines do not read as claimed at HEAD")
    if "DIVZ" not in src or "PFDE" not in src:
        fail("AC4", "cited scope tuples do not name the expected fund tickers at HEAD")
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
    for m in re.finditer(r"Q(\d+)[-–](\d+)", section):
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
    if "trueshares" not in systems or "pathfinder" not in systems:
        fail("AC7", "trueshares or pathfinder missing from live systems.json")
    proposed = ["trueshares_get_snapshot", "pathfinder_get_snapshot", "pathfinder_get_holdings"]
    base_verbs = {"get", "list", "describe", "query", "prepare", "find"}
    name_re = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")
    bad = []
    for name in proposed:
        if not name_re.match(name):
            bad.append((name, "does not match {system}_{function}[_{qualifier}] shape"))
            continue
        parts = name.split("_")
        system = parts[0]
        func = parts[1]
        if system not in systems:
            bad.append((name, f"system '{system}' not in systems.json"))
        if func not in base_verbs:
            bad.append((name, f"function '{func}' not a recognised base-form verb"))
    if bad:
        fail("AC7", f"tool name(s) failing C3: {bad}")
    print(f"  {len(proposed)} proposed names all pass: {proposed}")
    rt = result_text_unwrapped()
    for name in proposed:
        if name not in rt:
            fail("AC7", f"result.md does not name the proposed tool {name!r}")
    ok("AC7")


def ac8():
    print(f"[{now()}] AC8 -- read fence as exact prefixes, exclusions named")
    rt = result_text_unwrapped()
    if "## AC8" not in rt:
        fail("AC8", "AC8 section missing")
    section = rt.split("## AC8", 1)[1].split("## AC9", 1)[0]
    for needle in [
        "EXCLUDED",
        "trueshares/DIVZ/silver/fact_netassets_page/*",
        "pathfinder/PFDE/silver/fact_holdings/*",
        "bronze",
        "msn/",
    ]:
        if needle not in section:
            fail("AC8", f"AC8 section missing required element: {needle!r}")
    # Live re-check the msn/ struck-tier exclusion (measured empty, per etf_conversion.py's own census).
    rc, data, err = s3_list(BUCKET, "msn/", timeout=30, extra=["--delimiter", "/"])
    if rc != 0:
        fail("AC8", f"live msn/ list failed: rc={rc} err={(err or '')[:200]}")
    if data.get("Contents") or data.get("CommonPrefixes"):
        fail("AC8", f"msn/ is no longer empty at HEAD -- result.md's struck-tier claim is stale: {data}")
    print("  live s3://opal-data-assets/msn/: measured empty (struck tier, matches result.md)")
    ok("AC8")


def ac9():
    print(f"[{now()}] AC9 -- empty-property / empty-table disposition, no tool proposed for an empty combo")
    rt = result_text_unwrapped()
    if "## AC9" not in rt:
        fail("AC9", "AC9 section missing")
    section = rt.split("## AC9", 1)[1].split("## AC10", 1)[0]
    if "trueshares" not in section or "fact_holdings" not in section:
        fail("AC9", "AC9 section does not name the empty trueshares fact_holdings combo")
    if "no tool" not in section.lower() and "NO TOOL" not in section:
        fail("AC9", "AC9 section does not state that no tool is proposed for the empty combo")
    rc, data, err = s3_list(BUCKET, "trueshares/DIVZ/silver/fact_holdings/", timeout=60)
    if rc != 0:
        fail("AC9", f"live list failed: rc={rc} err={(err or '')[:200]}")
    if data.get("Contents"):
        fail("AC9", "trueshares/DIVZ/silver/fact_holdings/ is no longer empty at HEAD -- result.md's claim is stale")
    ok("AC9")


def ac11():
    print(f"[{now()}] AC11 -- every question class answered per fund; a fund with no data for a date named")
    rt = result_text_unwrapped()
    if "## AC11" not in rt:
        fail("AC11", "AC11 section missing")
    section = rt.split("## AC11", 1)[1]
    for fund in ("DIVZ", "IDVZ", "PFDE", "PFOE"):
        if fund not in section:
            fail("AC11", f"AC11 section does not name fund {fund}")
    if "2026-08-29" not in section or "2026-08-30" not in section:
        fail("AC11", "AC11 section does not name the measured fact_dailynav gap dates (2026-08-29, 2026-08-30)")
    # Live re-check: fact_dailynav is missing exactly the two weekend dates fact_netassets_page carries.
    rc_na, data_na, err_na = s3_list(BUCKET, "trueshares/DIVZ/silver/fact_netassets_page/", timeout=60)
    rc_nav, data_nav, err_nav = s3_list(BUCKET, "pathfinder/PFDE/silver/fact_dailynav/", timeout=60)
    if rc_na != 0 or rc_nav != 0:
        fail("AC11", f"live list failed: na_rc={rc_na} nav_rc={rc_nav}")
    def dates_of(data):
        out = set()
        for c in data.get("Contents", []):
            m = re.search(r"date=([\d-]+)", c["Key"])
            if m:
                out.add(m.group(1))
        return out
    d_na = dates_of(data_na)
    d_nav = dates_of(data_nav)
    gap = sorted(d_na - d_nav)
    print(f"  fact_netassets_page dates: {len(d_na)}  fact_dailynav dates: {len(d_nav)}  gap: {gap}")
    if gap != ["2026-08-29", "2026-08-30"]:
        fail("AC11", f"live gap no longer matches result.md's claimed (2026-08-29, 2026-08-30): {gap}")
    ok("AC11")


DISPATCH = {
    "AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6,
    "AC7": ac7, "AC8": ac8, "AC9": ac9, "AC11": ac11,
}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in DISPATCH:
        print(f"usage: {sys.argv[0]} <{'|'.join(sorted(DISPATCH))}>")
        sys.exit(2)
    DISPATCH[sys.argv[1]]()


if __name__ == "__main__":
    main()
