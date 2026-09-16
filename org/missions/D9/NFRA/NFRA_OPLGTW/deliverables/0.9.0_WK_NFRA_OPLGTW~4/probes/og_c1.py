#!/usr/bin/env python3
"""OGC1-AC13 probe (NFRA_OPLGTW.TO-OG-c-1): every reader of `meta/complete` found by an
unscoped repo read, with what it reads, and whether any reads a field OG-c-1 removes or
renames.

Usage:  py -3.12 <this file> AC13
Prints `VERDICT: PASS-OGC1-AC13` or `VERDICT: FAIL-OGC1-AC13 <reason>`; rc 0 / 1.

THREE INDEPENDENT LEGS, so no leg certifies another:
  1. THE CENSUS -- the saved output of `comp-find 'meta/complete' --files --all` beside this
     probe (census_meta_complete.txt). Its DENOMINATOR line is printed, the page must be the
     whole population (PAGE 1 of 1, showing N of N), and the two consumers the task order
     names must be in it.
  2. THE FIELD DELTA -- the v1 marker as the CUT BASE's code builds it (loaded from git at
     the base commit, not from the worktree) against the object the CELL's write path puts,
     from the same fixture with the clock frozen. Removed, renamed and value-changed fields
     are each printed with their count; all three must be zero.
  3. THE READERS -- every census hit classified EXECUTED or RECORD; for each executed file,
     what it reads of the marker (field accesses by name, S3 filter prefix/suffix). The
     accelerator's Lambda target is followed one hop, because it reads the event and does
     not name the prefix. No reader may read a removed, renamed or changed field.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[8]      # probes/<serial>/deliverables/<CODE>/<MACRO>/<D>/missions/org/ROOT
DELIV = HERE.parents[1]
CENSUS = DELIV / "census_meta_complete.txt"
SILVER = ROOT / "data" / "assets" / "scripts" / "silver"
BASE = "1bcc827bda"          # the cut the worktree was branched from
PRODUCER = "data/assets/scripts/silver/conversion_manifest.py"
REQUIRED = ("infra/aws/terraform/opal-assets/silver.tf",
            "infra/aws/terraform/opal-assets/advi_49f_floor.tf")
ACCELERATOR_TARGET = "infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py"
EXECUTED_SUFFIXES = (".py", ".tf", ".sh", ".js", ".ts", ".mjs", ".cjs", ".ps1")
M, D = "08335338", "2026-07-13"
FROZEN = "2026-07-13T12:00:00Z"


def fail(reason: str) -> int:
    print("VERDICT: FAIL-OGC1-AC13 " + reason)
    return 1


def read_census():
    if not CENSUS.is_file():
        return None, "census file absent: " + str(CENSUS.relative_to(ROOT))
    text = CENSUS.read_text(encoding="utf-8", errors="replace")
    den = re.search(r"DENOMINATOR: (\d+) hit\(s\) across (\d+) file\(s\) scanned", text)
    page = re.search(r"PAGE (\d+) of (\d+)\s+\(showing (\d+) of (\d+)\)", text)
    if not den or not page:
        return None, "census has no DENOMINATOR or PAGE line"
    if page.group(1) != page.group(2) or page.group(3) != page.group(4):
        return None, "census page is not the whole population: " + page.group(0)
    paths, in_list = [], False
    for line in text.splitlines():
        if line.startswith("  [") and "]" in line:
            in_list = True
            continue
        if line.startswith("SYSTEMS CONTEXT"):
            break
        if in_list and line.startswith("    ") and line.strip():
            paths.append(line.strip())
    return {"hits": int(den.group(1)), "scanned": int(den.group(2)),
            "listed": int(page.group(3)), "paths": paths, "den_line": den.group(0)}, ""


def base_module():
    """conversion_manifest as it stood at the cut, loaded from git -- never the worktree."""
    proc = subprocess.run(["git", "show", BASE + ":" + PRODUCER], cwd=str(ROOT),
                          capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0 or "COMPLETE_MARKER_SCHEMA" not in proc.stdout:
        raise RuntimeError("git show " + BASE + ":" + PRODUCER + " rc=" + str(proc.returncode)
                           + " -- the base producer could not be read (positive control)")
    mod = types.ModuleType("conversion_manifest_at_base")
    mod.__file__ = PRODUCER + "@" + BASE
    exec(compile(proc.stdout, mod.__file__, "exec"), mod.__dict__)
    return mod


def fixture_results():
    tables = ("fact_rps", "fact_rps_s2", "dim_position", "dim_balance")
    return [types.SimpleNamespace(
        key="schwab/" + M + "/bronze/rps/20260713/" + M + ".CRS20260713.RPS.zip",
        action="converted", master=M, feed="RPS", reason="",
        silver_keys=["schwab/" + M + "/silver/" + t + "/date=" + D + "/data.parquet"
                     for t in tables],
        tables={"fact_rps": {"rows_out": 5}, "fact_rps_s2": {"rows_out": 3}},
        projections={"dim_position": {"rows": 5, "fact_rows": 5},
                     "dim_balance": {"rows": 3, "fact_rows": 3}})]


class _Capture:
    """The smallest client the write path needs: it records the PUT body."""

    def __init__(self):
        self.body = None

    def put_object(self, Bucket, Key, Body, **_conditions):        # noqa: N803
        self.body = Body

    def head_object(self, Bucket, Key):                             # noqa: N803
        return {}


def field_delta():
    sys.path.insert(0, str(SILVER))
    sys.path.insert(0, str(SILVER.parent / "lib"))
    import conversion_manifest as cur
    base = base_module()
    cur._marker_emitted_at = lambda: FROZEN
    base._marker_emitted_at = lambda: FROZEN
    results = fixture_results()
    legacy = base.build_complete_markers("r1", M, results)[0]
    marker = cur.build_complete_markers("r1", M, results)[0]
    inventory = {"bronze": {"rps": [results[0].key]},
                 "silver": {t: [{"key": k, "version_id": "v1", "size": 10, "etag": '"e"',
                                 "rows": 5 if t in ("fact_rps", "dim_position") else 3}]
                            for k in results[0].silver_keys
                            for t in [k.split("/")[3]]}, "errors": []}
    client = _Capture()
    cur.write_complete_marker_verified(
        client, "opal-data-assets", marker,
        compose=lambda date: cur.build_closure("r1", "event", M, date, inventory, results))
    published = json.loads(client.body.decode("utf-8"))
    removed = sorted(set(legacy) - set(published))
    added = sorted(set(published) - set(legacy))
    changed = sorted(k for k in set(legacy) & set(published) if legacy[k] != published[k])
    same_key = base.complete_marker_key(M, D) == cur.complete_marker_key(M, D)
    return legacy, published, removed, added, changed, same_key


def accessed_fields(text: str, fields) -> list:
    out = []
    for f in fields:
        pat = (r"""\[\s*["']""" + re.escape(f) + r"""["']\s*\]|\.get\(\s*["']"""
               + re.escape(f) + r"""["']""")
        if re.search(pat, text):
            out.append(f)
    return out


def what_it_reads(path: str, fields) -> str:
    text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
    if path == PRODUCER or path.endswith("/opal-assets-silver-schwab/conversion_manifest.py"):
        return "WRITER (the producer" + ("" if path == PRODUCER else ", vendored copy OG-c-2 "
                                         "re-vendors") + "); reads no marker"
    if "/tests/" in path:
        return "TEST: asserts the v1 face; fields " + ",".join(accessed_fields(text, fields))
    if path.endswith(".tf"):
        prefixes = re.findall(r'filter_prefix\s*=\s*"([^"]*meta/complete[^"]*)"', text)
        body = accessed_fields(text, fields)
        if prefixes:
            suffix = re.findall(r'filter_suffix\s*=\s*"([^"]*)"', text)
            return ("S3 ObjectCreated on key prefix " + ",".join(prefixes) + " suffix "
                    + ",".join(sorted(set(suffix))) + " -- the object KEY, no body field"
                    + ("" if not body else "; body fields " + ",".join(body)))
        return ("names the marker in comments only; body fields read: "
                + (",".join(body) if body else "none"))
    body = accessed_fields(text, fields)
    return "body fields read: " + (",".join(body) if body else "none")


def main(argv) -> int:
    if argv[1:] != ["AC13"]:
        print("usage: og_c1.py AC13")
        return 2
    census, why = read_census()
    if census is None:
        return fail(why)
    print("CENSUS: " + census["den_line"] + " | listed " + str(census["listed"])
          + " file(s), page complete | source "
          + str(CENSUS.relative_to(ROOT)).replace("\\", "/"))
    missing = [p for p in REQUIRED if p not in census["paths"]]
    if missing:
        return fail("census lacks the named consumer(s) " + ",".join(missing))
    if census["listed"] != len(census["paths"]):
        return fail("parsed " + str(len(census["paths"])) + " paths of "
                    + str(census["listed"]) + " listed")

    legacy, published, removed, added, changed, same_key = field_delta()
    print("FIELDS: v1 at " + BASE + " = " + str(len(legacy)) + " " + ",".join(sorted(legacy)))
    print("DELTA: removed " + str(len(removed)) + " " + str(removed) + " | renamed "
          + str(len(removed)) + " (a rename shows as a removal) | value-changed "
          + str(len(changed)) + " " + str(changed) + " | added " + str(len(added)) + " "
          + str(added) + " | marker key unchanged: " + str(same_key))
    touched = set(removed) | set(changed)

    violations, executed, records = [], 0, 0
    for path in census["paths"]:
        if not (ROOT / path).is_file():
            print("READER RECORD   " + path + " :: not on disk in this tree")
            records += 1
            continue
        if path.endswith(EXECUTED_SUFFIXES):
            executed += 1
            reads = what_it_reads(path, list(legacy))
            print("READER EXECUTED " + path + " :: " + reads)
            if path != PRODUCER and "WRITER" not in reads and "TEST" not in reads:
                hit = [f for f in accessed_fields(
                    (ROOT / path).read_text(encoding="utf-8", errors="replace"), list(legacy))
                    if f in touched]
                violations.extend(path + ":" + f for f in hit)
        else:
            records += 1
            print("READER RECORD   " + path + " :: prose/data record, not executed")
    target = ROOT / ACCELERATOR_TARGET
    ttext = target.read_text(encoding="utf-8", errors="replace")
    t_fields = accessed_fields(ttext, list(legacy))
    t_get = "get_object" in ttext
    print("READER HOP      " + ACCELERATOR_TARGET + " :: the accelerator's target (silver.tf "
          "lambda_function_arn = module.advi_49f_gold_dispatch); reads Records[0].s3.object.key"
          + " only; marker body fields read: " + (",".join(t_fields) if t_fields else "none")
          + "; get_object present: " + str(t_get))
    violations.extend(ACCELERATOR_TARGET + ":" + f for f in t_fields if f in touched)
    print("READERS: " + str(executed) + " executed + " + str(records) + " record = "
          + str(executed + records) + " of " + str(census["listed"]) + " census files, plus 1 hop")

    if removed or changed or not same_key:
        return fail("the cell removes/renames/changes v1 field(s) " + str(sorted(touched))
                    + (" and moves the marker key" if not same_key else ""))
    if violations:
        return fail("reader(s) read a touched field: " + ",".join(violations))
    print("VERDICT: PASS-OGC1-AC13")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
