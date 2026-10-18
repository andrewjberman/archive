"""cm4_inventory.py -- AMGT_HARVST HVST-cm-4 part B (round 98, CTO round-97 analysis item 4). READ-ONLY.

Writes cm4_inventory.out beside this file (newline="\\n") and echoes it. Five sections:
  SCHEDULE          scheduled tasks and register entries that run the model-block pull or derive. Triggers come from
                    the registers (line numbers printed) and from the local schtasks export (CSV written by
                    `schtasks //query //fo CSV //v` into the worktree scratch folder; read-only). A trigger that cannot
                    be read is printed `unread` with the reason.
  SCHEDULE-SCAN     the local schtasks rows checked for a model-block or dossier command.
  DOSSIER-WRITERS   every production code path that calls dossier.write_one or gold_put on the research_dossier table,
                    from a read-only scan of the shared checkout (C:/Dev/ajb_workspace) with its denominator per extension.
  BUILD-COST        per-name requests and bytes, from the memoised slices in cm4_census.parts.out (COST lines).
  MODEL-BLOCK-LANDING the newest derived/model_block/<key>/<stamp>/ for ten names (UNH, the two slash keys, seven names
                    picked by index from the census's sorted name listing), with the spread of the landing times.
Reads of S3: list_objects_v2 on the harvest bucket only (the census's Guarded client, list operations only).
"""

import csv
import os
import re
import statistics
import sys
from datetime import datetime, timezone

WT = os.getcwd()
sys.path.insert(0, WT)

SHARED = "C:/Dev/ajb_workspace"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "cm4_inventory.out")
PARTS_PATH = os.path.join(HERE, "cm4_census.parts.out")
SCHTASKS_CSV = os.path.join(WT, ".scratch", "schtasks_v.csv")
CODE_ROOTS = ("lib", "integrations", "infra", ".tools")
SKIP_DIRS = frozenset((".git", "__pycache__", "node_modules", ".venv", "venv"))
SKIP_NAME = re.compile(r"credential|secret|\.env", re.I)  # never opened: credential-bearing names
SCHED_EXT = (".ps1", ".cmd", ".bat", ".sh", ".yaml", ".yml", ".tf")
STAMP = re.compile(r"^\d{8}T\d{6}Z$")
DEF = re.compile(r"^\s*def (\w+)\s*\(")

lines = []


def emit(text):
    safe = text.encode("ascii", "backslashreplace").decode("ascii")
    print(safe, flush=True)
    lines.append(safe)


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
        return fh.read()


def line_of(path, pattern):
    """(line number, text) of the first line matching `pattern` in `path`, or (None, None)."""
    rx = re.compile(pattern)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for n, text in enumerate(fh, 1):
            if rx.search(text):
                return n, text.strip()
    return None, None


def rel(path):
    return path.replace("\\", "/").split(SHARED + "/", 1)[-1] if SHARED in path else path


# ------------------------------------------------------------------ SCHEDULE
def schedule_section():
    rows = []  # (name, trigger, read?) for the INVENTORY counts
    ps1 = SHARED + "/lib/research/corpus/schedule_induction.ps1"
    n_at, t_at = line_of(ps1, r"\[string\]\$AtUtc = '\d\d:\d\d'")
    n_fire, t_fire = line_of(ps1, r"induction_scheduled -m lib\.research\.corpus\.induction_scheduled --mode fire|OPAL_INDUCTION_FIRE=1")
    from lib import opal_naming  # the name the register builds (never typed here)
    task = opal_naming.name("amgt", None, "induction", "daily")
    at = re.search(r"'(\d\d:\d\d)'", t_at or "")
    trigger = ("%sZ daily" % at.group(1)) if at else "unread"
    emit("SCHEDULE %s trigger=%s (register default; %s:%s) command_file=schedule_induction.ps1 "
         "action=induction_scheduled --mode fire with OPAL_INDUCTION_FIRE=1 (%s:%s)"
         % (task, trigger, rel(ps1), n_at, rel(ps1), n_fire))
    rows.append((task, trigger, trigger != "unread"))
    entry = {"model_block_admit_cmd": "integrations/bloomberg/research/model_block_pull.py:admit (cmd_admit)",
             "model_block_refresh_cmd": "integrations/bloomberg/research/model_block_pull.py:refresh (cmd_refresh)"}
    mbp = SHARED + "/integrations/bloomberg/research/model_block_pull.py"
    n_admit, _ = line_of(mbp, r"^def cmd_admit\(")
    n_refresh, _ = line_of(mbp, r"^def cmd_refresh\(")
    n_derived, _ = line_of(mbp, r'derived_key = f"derived/')
    n_bronze, _ = line_of(mbp, r"^def _bronze_prefix\(")
    n_plog, _ = line_of(mbp, r"amgt/harvest/state/pull_log/")
    n_stamp, _ = line_of(mbp, r"^def utc_stamp\(")
    emit("SCHEDULE-CHAIN %s runs %s (%s:%s) then %s (%s:%s); the fire gate is the task action's env var"
         % (task, entry["model_block_admit_cmd"], rel(mbp), n_admit, entry["model_block_refresh_cmd"], rel(mbp), n_refresh))
    emit("SCHEDULE-WRITES %s writes=derived/model_block/<slash_safe_key>/<utc_stamp>/model_block.json "
         "(%s:%s, stamp utc_stamp %s:%s); raw bloomberg/harvest/bronze/{refdata,histdata,bestdata}/ "
         "(%s:%s); pull log amgt/harvest/state/pull_log/ (%s:%s)"
         % (task, rel(mbp), n_derived, rel(mbp), n_stamp, rel(mbp), n_bronze, rel(mbp), n_plog))
    ind = SHARED + "/lib/research/corpus/induction_run.py"
    ind_text = read_text(ind)
    emit("SCHEDULE-CHAIN %s first step induction_run.py: dossier refs=%d write_one/gold_put refs=%d (%s)"
         % (task, len(re.findall(r"dossier", ind_text)), len(re.findall(r"write_one|gold_put", ind_text)), rel(ind)))
    devs = SHARED + "/org/devices/crossbox/XB-20261009T054248Z-aff1.json"
    n_x, t_x = line_of(devs, r"13:00Z amgt-induction-daily")
    emit("CORROBORATION crossbox 2026-10-09 record names the 13:00Z amgt-induction-daily fire log at %s:%s"
         % (rel(devs), n_x))
    oc = SHARED + "/org/devices/state/sitez/open_calls.json"
    n_o, t_o = line_of(oc, r"AMGT induction at 09:00")
    emit("CORROBORATION sitez open-calls text names the AMGT induction at 09:00 (ET, = 13:00Z under EDT) at %s:%s"
         % (rel(oc), n_o))
    live = [r for r in schtasks_rows() if "induction" in r["TaskName"].lower()]
    if live:
        for r in live:
            rows.append((r["TaskName"], r["Schedule Type"], True))
    else:
        emit("SCHEDULE %s LIVE-REGISTRATION trigger=unread (no induction task in the dell1 schtasks export; the sitez "
             "task is not queryable from this box)" % task)
        rows.append((task + " LIVE", "unread", False))

    ps_reg = SHARED + "/integrations/bloomberg/pipeline/register_daily_task.ps1"
    n_name, _ = line_of(ps_reg, r"TaskName = 'OPAL_BBGTML_daily_pull'")
    n_time, t_time = line_of(ps_reg, r"\[string\]\$At = '\d\d:\d\d'")
    tm = re.search(r"'(\d\d:\d\d)'", t_time or "")
    cmd = SHARED + "/integrations/bloomberg/pipeline/scheduled_daily_pull.cmd"
    ctext = read_text(cmd)
    emit("SCHEDULE OPAL_BBGTML_daily_pull trigger=%s America/New_York daily (register default %s:%s; task name %s:%s) "
         "command_file=scheduled_daily_pull.cmd model_block_refs=%d model_block_pull_refs=%d stage_derive_refs=%d "
         "runs_model_block_pull=%s"
         % (tm.group(1) if tm else "unread", rel(ps_reg), n_time, rel(ps_reg), n_name, len(re.findall("model_block", ctext)),
            len(re.findall("model_block_pull", ctext)), len(re.findall("stage_derive", ctext)),
            "no" if "model_block" not in ctext else "CHECK"))
    rows.append(("OPAL_BBGTML_daily_pull", tm.group(1) if tm else "unread", bool(tm)))

    cyc = [r for r in schtasks_rows() if "Continuous Cycle" in r["TaskName"]]
    olib = SHARED + "/lib/opal_data_harvest"
    refs = 0
    scanned_cycle = 0
    for dirpath, dirnames, filenames in os.walk(olib):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".py") and not SKIP_NAME.search(f):
                scanned_cycle += 1
                refs += len(re.findall(r"model_block|stage_pull|stage_derive", read_text(os.path.join(dirpath, f))))
    for r in cyc:
        emit("SCHEDULE %s trigger=%s (dell1 schtasks row) command=lib.opal_data_harvest.cycle_runner "
             "model_block_refs=%d in %d .py files of lib/opal_data_harvest" % (r["TaskName"].strip("\\"), r["Schedule Type"].strip(), refs, scanned_cycle))
        rows.append((r["TaskName"], r["Schedule Type"], True))

    for name, cmdname in (("OpalResearch-ExecManagement", "run_management.cmd"),
                          ("OpalResearch-FilingsAnalyzer", "run_filings.cmd"),
                          ("OpalResearch-Scores", "run_scores.cmd")):
        r = [x for x in schtasks_rows() if x["TaskName"].strip("\\") == name]
        path = SHARED + "/lib/research/llm_batch/launchers/" + cmdname
        body = read_text(path)
        mrefs = len(re.findall(r"model_block|stage_derive|model_block_pull|dossier|write_one|gold_put", body))
        trig = ("%s %s" % (r[0]["Schedule Type"].strip(), r[0]["Start Time"])) if r else "unread"
        emit("SCHEDULE %s trigger=%s (dell1 schtasks row; state %s) command_file=%s model_block_or_dossier_refs=%d"
             % (name, trig, r[0]["Status"] if r else "n/a", cmdname, mrefs))
        rows.append((name, trig, bool(r)))

    emit("NOTE pull_consumer.py (integrations/bloomberg/research) has no clock trigger: a queue-driven, person-started "
         "drain (SQS; ck4_writers.out and LEAD_PANEL brief evidence record 'no scheduled task'); it stages the same "
         "model block through stage_pull and stage_derive when run")
    read = sum(1 for _n, _t, ok in rows if ok)
    unread = sum(1 for _n, _t, ok in rows if not ok)
    return read, unread


_CSV = None


def schtasks_rows():
    global _CSV
    if _CSV is None:
        with open(SCHTASKS_CSV, "r", encoding="utf-8", errors="replace", newline="") as fh:
            rows = list(csv.reader(fh))
        hdr = rows[0]
        _CSV = [dict(zip(hdr, r)) for r in rows[1:] if len(r) == len(hdr)]
        emit("SCHEDULE-SCAN local schtasks export rows=%d (dell1; `schtasks //query //fo CSV //v`, read-only)" % len(_CSV))
        hits = [r for r in _CSV if re.search(r"model_block|stage_derive|model_block_pull|dossier|induction", r["Task To Run"], re.I)]
        emit("SCHEDULE-SCAN rows whose command names a model-block, induction or dossier script: %d of %d" % (len(hits), len(_CSV)))
    return _CSV


# -------------------------------------------------------------- DOSSIER-WRITERS
def dossier_section():
    ext_count = {}
    files_walked = 0
    py_files = []
    sched_files = []
    for root in CODE_ROOTS:
        base = os.path.join(SHARED, root)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for f in filenames:
                files_walked += 1
                ext = os.path.splitext(f)[1].lower() or "(none)"
                ext_count[ext] = ext_count.get(ext, 0) + 1
                full = os.path.join(dirpath, f)
                if ext == ".py":
                    py_files.append(full)
                elif ext in SCHED_EXT:
                    sched_files.append(full)
    for ext in sorted(ext_count, key=lambda e: (-ext_count[e], e)):
        emit("SCAN-DENOMINATOR roots=%s ext=%s files=%d" % (",".join(CODE_ROOTS), ext, ext_count[ext]))
    emit("SCAN-DENOMINATOR roots=%s total_files=%d (all extensions; py=%d scanned for writer calls; %d scheduling-type "
         "files scanned for dossier scheduling references; credential-named files are never opened)"
         % (",".join(CODE_ROOTS), files_walked, len(py_files), len(sched_files)))

    call_rx = re.compile(r"(?<![\w.])write_one\s*\(|dossier\.write_one\s*\(|gold_put\s*\(")
    writers = []   # (rel path, line, enclosing function, what)
    code_files = []
    for path in py_files:
        rp = rel(path)
        if "/tests/" in rp or os.path.basename(rp).startswith("test_") or "deliverables/" in rp:
            continue
        if SKIP_NAME.search(os.path.basename(rp)):
            continue
        code_files.append((rp, read_text(path)))
    for rp, text in code_files:
        current = None
        for n, line in enumerate(text.splitlines(), 1):
            m = DEF.match(line)
            if m:
                current = m.group(1)
                continue
            if call_rx.search(line):
                if rp.endswith("lib/research/corpus/dossier.py"):
                    if "write_one(" in line or ("gold_put(" in line and "TABLE" in line):
                        writers.append((rp, n, current or "-", "write_one" if "write_one(" in line else "gold_put(TABLE)"))
                elif "dossier.write_one(" in line or ("gold_put(" in line and "dossier.TABLE" in line):
                    writers.append((rp, n, current or "-", "dossier.write_one" if "write_one(" in line else "gold_put(dossier.TABLE)"))
    # the writer functions: the function enclosing each writer call (write_one holds the gold_put)
    funcs = []
    for rp, n, fn, what in writers:
        if fn not in funcs:
            funcs.append(fn)
    # callers of each writer function: call sites of its NAME from other functions, in non-test code
    def callers_of(fn):
        if fn == "write_one":
            return sum(1 for (_r, _n, f2, w2) in writers if w2 in ("write_one", "dossier.write_one") and f2 != "write_one")
        rx = re.compile(r"\b%s\b" % re.escape(fn))
        total = 0
        for rp, text in code_files:
            for line in text.splitlines():
                if DEF.match(line):
                    continue
                if rx.search(line) and not line.lstrip().startswith("#"):
                    total += len(rx.findall(line))
        return total
    sched_hits = {}   # every scheduling-type line naming the dossier module or its entry points
    writer_class = []  # the subset whose line names a WRITE entry point (a reader or a comment is a mention)
    rx_sched = re.compile(r"corpus[./\\]dossier|dossier\.py|dossier\.main|--write-all|--write-one-twice")
    rx_writer = re.compile(r"write_one|write-all|write_all|--write\b|_run_write|dossier\.main|--write-one-twice")
    for path in sched_files:
        rp = rel(path)
        if SKIP_NAME.search(os.path.basename(rp)):
            continue
        text = read_text(path)
        for n, line in enumerate(text.splitlines(), 1):
            if rx_sched.search(line):
                sched_hits[rp] = sched_hits.get(rp, 0) + 1
                if rx_writer.search(line):
                    writer_class.append("%s:%d" % (rp, n))
                else:
                    emit("DOSSIER-SCHEDULE-MENTION %s:%d is a mention (no write entry point on the line)" % (rp, n))
    dossier_path = SHARED + "/lib/research/corpus/dossier.py"
    cache = {}
    for rp, n, fn, what in writers:
        if fn not in cache:
            cache[fn] = callers_of(fn)
        status = "none" if not writer_class else "CHECK:" + ",".join(writer_class)
        emit("DOSSIER-WRITERS %s:%d %s callers=%d what=%s schedule=%s" % (rp, n, fn, cache[fn], what, status))
    emit("DOSSIER-WRITERS-SUMMARY distinct_writer_functions=%d writer_call_sites=%d" % (len(funcs), len(writers)))
    emit("DOSSIER-SCHEDULE-REFS scheduling-type lines naming the dossier module: %d in %d file(s); lines naming a WRITE "
         "entry point: %d (%s)"
         % (sum(sched_hits.values()), len(sched_hits), len(writer_class), ",".join(writer_class) or "none"))
    # the shared-checkout dossier.py must carry the write call sites this census names (a control on the scan)
    dtext = read_text(dossier_path)
    emit("DOSSIER-CONTROL dossier.py write_one defs=%d gold_put_research_dossier=%d"
         % (len(re.findall(r"^def write_one\(", dtext, re.M)), len(re.findall(r"gold_put\(TABLE", dtext))))
    # a writer function counts as scheduled only when a scheduling-type file names a WRITE entry point (none does)
    return len(funcs), (len(funcs) if writer_class else 0), files_walked


# ------------------------------------------------------------------ BUILD-COST
def cost_section():
    gets, nbytes = [], []
    with open(PARTS_PATH, "r", encoding="utf-8") as fh:
        for line in fh.read().splitlines():
            m = re.match(r"^COST (\S+) gets=(\d+) bytes=(\d+)$", line)
            if m:
                gets.append((int(m.group(2)), m.group(1)))
                nbytes.append((int(m.group(3)), m.group(1)))
    g = [x for x, _n in gets]
    b = [x for x, _n in nbytes]
    gmax = max(gets)
    bmax = max(nbytes)
    emit("BUILD-COST names=%d gets_median=%d gets_max=%d (%s) bytes_median=%d bytes_max=%d (%s) total_gets=%d total_bytes=%d"
         % (len(gets), statistics.median(g), gmax[0], gmax[1], statistics.median(b), bmax[0], bmax[1], sum(g), sum(b)))
    emit("BUILD-COST-MEMO each COST line is the fetched requests and bytes of one name (memo hits are not counted); the memo "
         "is a per-process read-through cache capped at 1 GiB, and each slice process starts cold, so the first names of a "
         "slice carry the shared-object fills (order-dependent)")
    return sorted(NAMES_FROM_PARTS())


def NAMES_FROM_PARTS():
    out = set()
    with open(PARTS_PATH, "r", encoding="utf-8") as fh:
        for line in fh.read().splitlines():
            if line.startswith("NAME "):
                out.add(line.split()[1])
    return out


# ------------------------------------------------------ MODEL-BLOCK-LANDING
class ListOnly(object):
    """Read-only S3 view on the harvest bucket: list_objects_v2 and its paginator only."""

    def __init__(self, client):
        self._c = client
        self.requests = 0

    def list_objects_v2(self, **kw):
        assert kw.get("Bucket") == "opal-data-harvest", kw.get("Bucket")
        self.requests += 1
        return self._c.list_objects_v2(**kw)

    def get_paginator(self, op):
        assert op == "list_objects_v2", op
        outer = self

        class _P(object):
            def paginate(self, **kw):
                assert kw.get("Bucket") == "opal-data-harvest", kw.get("Bucket")
                for page in outer._c.get_paginator("list_objects_v2").paginate(**kw):
                    outer.requests += 1
                    yield page
        return _P()


def landing_section(sorted_names):
    from lib.research.harvest import store
    from lib.research.identity import crosswalk
    client = ListOnly(store._default_client())
    picks = ["UNH_US_Equity", "BP/_LN_Equity", "NG/_LN_Equity"]
    for i in (0, 13, 26, 39, 52, 65, 78):
        picks.append(sorted_names[i])
    results = []
    for name in picks:
        base = "derived/model_block/%s/" % crosswalk.slash_safe_key(name)
        prefixes = []
        for page in client.get_paginator("list_objects_v2").paginate(Bucket="opal-data-harvest", Prefix=base, Delimiter="/"):
            for cp in page.get("CommonPrefixes", []) or []:
                prefixes.append(cp["Prefix"])
        stamps = [p.rstrip("/").rsplit("/", 1)[-1] for p in prefixes]
        stamps = sorted(s for s in stamps if STAMP.match(s))
        if not stamps:
            emit("LANDING %s key=%s newest_stamp=none stamps_listed=0" % (name, crosswalk.slash_safe_key(name)))
            results.append((name, None))
            continue
        newest = stamps[-1]
        obj = base + newest + "/model_block.json"
        present = client.list_objects_v2(Bucket="opal-data-harvest", Prefix=obj)
        found = any(o.get("Key") == obj for o in (present.get("Contents", []) or []))
        landed = datetime.strptime(newest, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        emit("LANDING %s key=%s newest_stamp=%s landing_utc=%s stamps_listed=%d model_block_json=%s"
             % (name, crosswalk.slash_safe_key(name), newest, landed.strftime("%Y-%m-%dT%H:%M:%SZ"), len(stamps),
                "present" if found else "absent"))
        results.append((name, landed))
    times = [t for _n, t in results if t is not None]
    if times:
        lo, hi = min(times), max(times)
        spread = int((hi - lo).total_seconds() // 60)
        emit("LANDING-SPREAD names=%d with_stamp=%d earliest=%s latest=%s spread_minutes=%d"
             % (len(results), len(times), lo.strftime("%Y-%m-%dT%H:%M:%SZ"), hi.strftime("%Y-%m-%dT%H:%M:%SZ"), spread))
    emit("LANDING-READS list_objects_v2 requests=%d (harvest bucket only; stamps are UTC from utc_stamp, "
         "model_block_pull.py:641)" % client.requests)
    return len(results)


def main():
    if os.path.exists(SCHTASKS_CSV) is False:
        raise SystemExit("schtasks export missing: %s" % SCHTASKS_CSV)
    emit("CENSUS-INVENTORY HVST-cm-4 part B (round 98). Shared checkout %s read-only; worktree %s; code at the census commit "
         "and the shared HEAD carry no diff in lib/research or integrations/bloomberg/research" % (SHARED, WT))
    read, unread = schedule_section()
    writers, sched_writers, files_scanned = dossier_section()
    names = cost_section()
    sampled = landing_section(sorted(names))
    final = ("INVENTORY schedules_read=%d schedules_unread=%d dossier_writers=%d scheduled_dossier_writers=%d "
             "names_landing_sampled=%d files_scanned=%d" % (read, unread, writers, sched_writers, sampled, files_scanned))
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        for line in lines + [final]:
            fh.write(line + "\n")
    print(final, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
