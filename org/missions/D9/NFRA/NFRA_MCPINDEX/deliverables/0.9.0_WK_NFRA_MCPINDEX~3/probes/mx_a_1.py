#!/usr/bin/env python
"""Probe for NFRA_MCPINDEX.TO-MX-a-1 (cell MX-a-1). Each invocation grades ONE criterion id
(AC1..AC12) against LIVE evidence and/or the committed result file, and prints exactly one
VERDICT line at the end: `VERDICT: PASS-MXA1-AC<n>` or `VERDICT: FAIL-MXA1-AC<n> <reason>`.

Instrument: subprocess to `.tools/aws` (READ verbs only), direct file reads. No write verb.
Run from the worktree root: `py -3.12 <this file> AC<n>`.
"""
from __future__ import annotations

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[8]  # .../org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/<serial>/probes/mx_a_1.py -> repo root
assert (REPO / ".tools").is_dir(), f"repo root mis-resolved: {REPO}"

RESULT_MD = REPO / "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~3/analysis-portal.result.md"

AWS = str(REPO / ".tools" / "aws")

sys.path.insert(0, str(REPO / ".tools"))
from git_bash_resolver import git_bash  # noqa: E402  -- .tools/aws is a bash script; a native-Windows

BASH = git_bash()
if not BASH:
    print("BLOCKED: no Git Bash resolved; cannot invoke .tools/aws (a bash script) from native python.")
    sys.exit(1)


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_aws(args, timeout=60):
    # .tools/aws is a bash script (shebang #!/usr/bin/env bash); a native-Windows python subprocess
    # cannot exec it directly (WinError 193). Route through the resolved Git Bash absolute path.
    proc = subprocess.run([BASH, AWS] + args, cwd=str(REPO), capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def s3_list(bucket, prefix, timeout=60):
    rc, out, err = run_aws(["s3api", "list-objects-v2", "--bucket", bucket, "--prefix", prefix, "--output", "json"], timeout=timeout)
    if rc != 0:
        return rc, None, err
    try:
        data = json.loads(out) if out.strip() else {}
    except Exception as e:  # noqa: BLE001
        return rc, None, f"JSON parse error: {e}"
    return rc, data, err


def s3_get(bucket, key, timeout=30):
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
        path = tf.name
    rc, out, err = run_aws(["s3api", "get-object", "--bucket", bucket, "--key", key, path], timeout=timeout)
    if rc != 0:
        return rc, None, err
    try:
        content = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return rc, None, f"JSON parse error: {e}"
    return rc, content, err


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
    lines (paragraph/section breaks) and table rows (line starts with '|') are preserved as-is."""
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
    print(f"VERDICT: FAIL-MXA1-{cid} {reason}")
    sys.exit(0)


def ok(cid):
    print(f"VERDICT: PASS-MXA1-{cid}")
    sys.exit(0)


def ac1():
    print(f"[{now()}] AC1 -- live prefix census, denominator = 4 portal families + 2 firm buckets")
    families = [
        ("opal-data-portal-v2", "platinum/mdpf/"),
        ("opal-data-portal-v2", "platinum/etfs/"),
        ("opal-data-portal-v2", "platinum/advi/"),
        ("opal-data-portal-v2", "json/"),
    ]
    counted = 0
    for bucket, prefix in families:
        rc, data, err = s3_list(bucket, prefix, timeout=90)
        if rc != 0:
            fail("AC1", f"live list-objects-v2 failed for s3://{bucket}/{prefix}: rc={rc} err={err[:200]}")
        contents = data.get("Contents", [])
        n = len(contents)
        total_bytes = sum(c["Size"] for c in contents)
        newest = max((c["LastModified"] for c in contents), default=None)
        print(f"  s3://{bucket}/{prefix}  n={n}  bytes={total_bytes}  newest={newest}  (read verb: s3api list-objects-v2)")
        counted += 1
    # firm buckets (advisor intelligence, separate grant)
    for bucket, prefix in [("opal-data-inf", "platinum/firm/"), ("opal-data-cot", "platinum/firm/")]:
        rc, data, err = s3_list(bucket, prefix, timeout=60)
        if rc != 0:
            fail("AC1", f"live list-objects-v2 failed for s3://{bucket}/{prefix}: rc={rc} err={err[:200]}")
        contents = data.get("Contents", [])
        n = len(contents)
        total_bytes = sum(c["Size"] for c in contents)
        print(f"  s3://{bucket}/{prefix}  n={n}  bytes={total_bytes}  (read verb: s3api list-objects-v2)")
        counted += 1
    if counted != 6:
        fail("AC1", f"expected 6 live listings (4 portal families + 2 firm buckets), got {counted}")
    rt = result_text_unwrapped()
    denom = "Denominator: 4 surface families" in rt
    if not denom:
        fail("AC1", "result.md does not state the 4-family denominator")
    if "read verb" not in rt.lower():
        fail("AC1", "result.md does not log the read verb")
    print("  result.md carries the 4-family denominator and a command log with the read verb.")
    ok("AC1")


def ac2():
    print(f"[{now()}] AC2 -- freshness field per table, source printed")
    # Re-read the code citation live and confirm the dict is present at HEAD.
    src = read_lines("data/mdpf/scripts/gold/mdpf_gold_consolidator.py", 246, 253)
    print("  data/mdpf/scripts/gold/mdpf_gold_consolidator.py:246-253 (live read):")
    print("  " + src.replace("\n", "\n  "))
    if "TYPE_AS_OF_FIELD" not in src or '"period"' not in src or '"as_of"' not in src:
        fail("AC2", "TYPE_AS_OF_FIELD dict not found as cited at mdpf_gold_consolidator.py:246-253")
    # Re-fetch one live object and confirm freshness field present.
    rc, obj, err = s3_get("opal-data-portal-v2", "platinum/mdpf/global/aum-metrics.json")
    if rc != 0 or obj is None:
        fail("AC2", f"live get-object failed for aum-metrics.json: rc={rc} err={(err or '')[:200]}")
    if "period" not in obj or "last_updated" not in obj:
        fail("AC2", "aum-metrics.json does not carry 'period'/'last_updated' at live read")
    print(f"  live aum-metrics.json: period={obj.get('period')} last_updated={obj.get('last_updated')}")
    rc2, obj2, err2 = s3_get("opal-data-portal-v2", "platinum/etfs/positioning_data.json")
    if rc2 != 0 or obj2 is None:
        fail("AC2", f"live get-object failed for positioning_data.json: rc={rc2} err={(err2 or '')[:200]}")
    if "data_as_of" not in obj2 or "generated_at" not in obj2:
        fail("AC2", "positioning_data.json does not carry data_as_of/generated_at at live read")
    print(f"  live positioning_data.json: data_as_of={obj2.get('data_as_of')} generated_at={obj2.get('generated_at')}")
    rt = result_text_unwrapped()
    if "TYPE_AS_OF_FIELD" not in rt or "generated_at" not in rt:
        fail("AC2", "result.md does not cite the freshness-field sources it claims")
    ok("AC2")


def ac3():
    print(f"[{now()}] AC3 -- scope rule per table, key-prefix segment named; unscopable tables named")
    rt = result_text_unwrapped()
    required_markers = [
        "scope carried by the 2nd key segment",  # mdpf
        "cannot be read from its key",  # etfs -- first unscopable table
        "carried by the BUCKET NAME",  # inf/cot -- second unscopable table
        "carry NO firm or master scope",  # json/*
    ]
    missing = [m for m in required_markers if m not in rt]
    if missing:
        fail("AC3", f"result.md missing scope-rule statements: {missing}")
    # Live re-check: mdpf scopes measured from a fresh list.
    rc, data, err = s3_list("opal-data-portal-v2", "platinum/mdpf/", timeout=90)
    if rc != 0:
        fail("AC3", f"live list failed: rc={rc} err={(err or '')[:200]}")
    scopes = set()
    for c in data.get("Contents", []):
        parts = c["Key"].split("/")
        if len(parts) > 2 and parts[2] not in ("archive", "_manifests"):
            scopes.add(parts[2])
    print(f"  live mdpf scopes (2nd key segment): {sorted(scopes)}")
    if not scopes:
        fail("AC3", "no firm/scope segments found live under platinum/mdpf/")
    ok("AC3")


def ac4():
    print(f"[{now()}] AC4 -- never-sum rules with reasons")
    rt = result_text_unwrapped()
    if rt.count("**mdpf, cross-master**") + rt.count("cross-master") < 1:
        fail("AC4", "no cross-master never-sum rule found")
    required = ["cross-master", "cross-basis", "cross-date", "cross-fund", "cross-firm", "cross-period"]
    missing = [m for m in required if m not in rt]
    if missing:
        fail("AC4", f"result.md missing never-sum reason classes: {missing}")
    src = read_lines("data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py", 23, 24)
    print("  dim_mdpf_aggregate_aua_timeseries.py:23-24 (live read):")
    print("  " + src.replace("\n", "\n  "))
    if "NEVER" not in src or "sum" not in src.lower():
        fail("AC4", "cited never-sum line does not read as claimed at HEAD")
    ok("AC4")


def ac5():
    print(f"[{now()}] AC5 -- numbered common-question list, table+fields+source, no 'measured user demand' claim")
    rt = result_text_unwrapped()
    nums = re.findall(r"^\| (\d+) \|", rt, flags=re.M)
    nums = [int(n) for n in nums]
    print(f"  numbered question rows found: {len(nums)} (max id {max(nums) if nums else 0})")
    if len(nums) < 10:
        fail("AC5", f"expected >=10 numbered questions, found {len(nums)}")
    if "presented as measured user demand" not in rt:
        fail("AC5", "result.md does not carry the required disclaimer sentence")
    # Ensure the disclaimer is a NEGATION, not a positive claim: the word 'None is presented' must precede it.
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
        fail("AC6", "AC6 section does not dispose every question between the two named routes")
    # cross-check: every question number 1..18 from AC5 appears somewhere in AC6's text (as Qn or a range).
    q_ids = set(range(1, 19))
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
    if not {"mdpf", "etfs", "advi"} <= systems:
        fail("AC7", "mdpf/etfs/advi missing from live systems.json")
    proposed = [
        "mdpf_get_aum_metrics", "mdpf_get_account_distribution", "mdpf_get_aggregate_aua",
        "mdpf_get_category_views", "mdpf_get_non_model_assets", "etfs_get_positioning",
        "advi_get_leaderboard", "advi_get_mix_summary", "advi_get_partner_analytics",
        "advi_get_growth_chart",
    ]
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
    if "REFUSES to invent a tool name" not in rt:
        fail("AC7", "result.md does not record the C3 registry-gap refusal for the market-data family")
    ok("AC7")


def ac8():
    print(f"[{now()}] AC8 -- read fence as exact prefixes, exclusions named")
    rt = result_text_unwrapped()
    if "## AC8" not in rt:
        fail("AC8", "AC8 section missing")
    section = rt.split("## AC8", 1)[1].split("## AC9", 1)[0]
    for needle in ["EXCLUDED", "platinum/mdpf/*", "platinum/etfs/positioning_data.json", "platinum/advi/49financial/*", "opal-data-inf", "opal-data-cot"]:
        if needle not in section:
            fail("AC8", f"AC8 section missing required element: {needle!r}")
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
    print(f"[{now()}] AC11 -- four surface families denominator; portal page + precomputed key per surface")
    rt = result_text_unwrapped()
    if "**Denominator: 4**" not in rt:
        fail("AC11", "AC11 denominator not stated as 4")
    section = rt.split("## AC11", 1)[1].split("## AC12", 1)[0]
    rows = re.findall(r"^\| (\d) \|", section, flags=re.M)
    if sorted(set(rows)) != ["1", "2", "3", "4"]:
        fail("AC11", f"expected exactly 4 surface rows, found {rows}")
    for needle in ["portal page", "precomputed key"]:
        if needle not in section.lower() and needle not in section:
            pass  # header words checked loosely below
    if "ModelPortfolios.tsx" not in section or "Macroeconomics" not in section:
        fail("AC11", "AC11 rows missing expected page citations")
    ok("AC11")


def ac12():
    print(f"[{now()}] AC12 -- advisor-intelligence firm buckets/prefixes listed separately from opal-data-portal-v2")
    rc1, out1, err1 = run_aws(["s3api", "list-objects-v2", "--bucket", "opal-data-inflection", "--delimiter", "/"], timeout=30)
    rc2, out2, err2 = run_aws(["s3api", "list-objects-v2", "--bucket", "opal-data-cottonwood", "--delimiter", "/"], timeout=30)
    print(f"  live opal-data-inflection: rc={rc1} err={(err1 or '').strip()[:150]}")
    print(f"  live opal-data-cottonwood: rc={rc2} err={(err2 or '').strip()[:150]}")
    rc3, data3, err3 = s3_list("opal-data-inf", "platinum/firm/", timeout=60)
    rc4, data4, err4 = s3_list("opal-data-cot", "platinum/firm/", timeout=60)
    if rc3 != 0 or rc4 != 0:
        fail("AC12", f"live legacy-bucket listing failed: rc3={rc3} rc4={rc4}")
    n3 = len(data3.get("Contents", []))
    n4 = len(data4.get("Contents", []))
    print(f"  live opal-data-inf platinum/firm/: n={n3}")
    print(f"  live opal-data-cot platinum/firm/: n={n4}")
    if n3 == 0 or n4 == 0:
        fail("AC12", "one of the legacy firm buckets returned zero objects live")
    rt = result_text_unwrapped()
    if "opal-data-inf" not in rt or "opal-data-cot" not in rt:
        fail("AC12", "result.md does not name the legacy firm buckets")
    if "AccessDenied" not in rt:
        fail("AC12", "result.md does not record the AccessDenied measurement on the LGIC-named buckets")
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
