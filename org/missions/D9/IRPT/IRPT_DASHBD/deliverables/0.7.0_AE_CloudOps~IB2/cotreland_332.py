"""IRPT_DASHBD TO-DB-b-332 (applier 0.7.0_AE_CloudOps~IB2): the Cottonwood RE-LAND pair, eight gold days: the reads and the dry runs.

  python cotreland_332.py gates | before | dry

Reuses the read helpers of cotgold_329.py (same bucket, gold and published prefixes, same functions). Every event is ONE synchronous
invoke, never retried here. Account ids are never printed or written. Counts, hashes and words only.
"""
import datetime as dt
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cotgold_329 as g  # noqa: E402
import fill328 as f  # noqa: E402

STATE = HERE / "state332"
ROOT = g.ROOT
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
PACKET = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_RELAND_PAIR.md"
COO_HALF = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_RELAND_PAIR_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_RELAND_PAIR_CTO_HALF.md"
PACKET_SHA = "37ce1e48bb2abd4e1cb150dd8cb672bea86534ec3ac6c206e4b06fc5e0938e23"
SLUG = "irpt-dashbd-cottonwood-reland-pair-20261017"
RELANDED = ["2026-07-22", "2026-07-27", "2026-07-29", "2026-08-03"]
DAYS = ["2026-07-22", "2026-07-23", "2026-07-27", "2026-07-28", "2026-07-29", "2026-07-30", "2026-08-03", "2026-08-04"]
FULL_DAY = "2026-07-21"
# packet section 2: gold before (rows / versions / NOT_MEASURABLE)
PACKET_GOLD = {"2026-07-22": (157, 2, 12), "2026-07-23": (879, 2, 734), "2026-07-27": (3, 2, 3), "2026-07-28": (881, 2, 878),
               "2026-07-29": (1, 2, 0), "2026-07-30": (881, 2, 880), "2026-08-03": (159, 2, 12), "2026-08-04": (888, 2, 740)}
GOLD_FN, PUB_FN = g.GOLD_FN, g.PUB_FN


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def not_measurable(key, vid=None):
    import pyarrow.parquet as pq
    kw = {"Bucket": g.BUCKET, "Key": key}
    if vid:
        kw["VersionId"] = vid
    t = pq.read_table(io.BytesIO(g.s3.get_object(**kw)["Body"].read()), columns=["day_quality"])
    vals = t.column("day_quality").to_pylist()
    return len(vals), sum(1 for v in vals if v == "NOT_MEASURABLE"), sorted({str(v) for v in vals})


def day_facts(day):
    objs = g.day_object(day)
    if len(objs) != 1:
        return {"objects": len(objs)}
    vs = g.day_versions(objs[0])
    rows, nm, kinds = not_measurable(objs[0])
    return {"objects": 1, "key": objs[0], "rows": rows, "versions": len(vs), "version_ids": [v["VersionId"] for v in vs], "not_measurable": nm, "quality_values": kinds}


def window_ok():
    t = dt.datetime.now(dt.timezone.utc)
    return not (t.weekday() < 5 and dt.time(11, 30) <= t.time() < dt.time(14, 15))


def cmd_gates():
    sha = hashlib.sha256((ROOT / PACKET).read_bytes()).hexdigest()
    coo, cto = (ROOT / COO_HALF).read_text(encoding="utf-8"), (ROOT / CTO_HALF).read_text(encoding="utf-8")
    coo_ok, cto_ok = "SIGNED" in coo and PACKET_SHA in coo, "SIGNED" in cto and PACKET_SHA[:8] in cto
    f.SURFACE, f.SLUG = g.SURFACE, SLUG
    nw, nfiles, found = f.open_legs_on_surface()
    gc, pc = g.lam_cfg.get_function_configuration(FunctionName=GOLD_FN), g.lam_cfg.get_function_configuration(FunctionName=PUB_FN)
    sc = g.scheds()
    facts = {d: day_facts(d) for d in DAYS}
    full = g.day_object(FULL_DAY)
    mism = [d for d in DAYS if (facts[d].get("rows"), facts[d].get("versions"), facts[d].get("not_measurable")) != PACKET_GOLD[d]]
    full_rows = g.parquet_rows(full[0]) if full else None
    live_ok = (gc["CodeSha256"] == g.GOLD_CODE and pc["CodeSha256"] == g.PUB_CODE and sc == {"account_return_daily": "ENABLED", "publish_daily": "DISABLED"}
               and not mism and full_rows == 879 and gc.get("MemorySize") == 1024 and pc.get("MemorySize") == 1024
               and not (gc.get("Environment") or {}).get("Variables") and not (pc.get("Environment") or {}).get("Variables"))
    print("GATES packet_sha_ok=%s coo=%s cto=%s window_ok=%s" % (sha == PACKET_SHA, coo_ok, cto_ok, window_ok()))
    print("GATES worktrees_read=%d marker_files_read=%d open_legs_on_this_surface=%d %s" % (nw, nfiles, len(found), found))
    print("GATES live: gold_code_ok=%s pub_code_ok=%s schedules=%s days_matching_packet=%d/8 mismatched=%s full_day_rows=%s no_env=%s -> live_matches_packet=%s" % (
        gc["CodeSha256"] == g.GOLD_CODE, pc["CodeSha256"] == g.PUB_CODE, sc, 8 - len(mism), mism, full_rows,
        not (gc.get("Environment") or {}).get("Variables") and not (pc.get("Environment") or {}).get("Variables"), live_ok))
    print("GATES quality values seen: %s" % sorted({v for d in DAYS for v in facts[d].get("quality_values", [])}))
    save("gates.json", {"packet_sha256": sha, "coo_half_signed": coo_ok, "cto_half_signed": cto_ok,
                        "one_change_at_a_time": {"worktrees_read": nw, "open_markers_naming_this_surface": len(found)}, "live_matches_packet": bool(live_ok)})
    save("gates_days.json", {d: {k: v for k, v in facts[d].items() if k != "key"} for d in DAYS})
    return 0 if (sha == PACKET_SHA and coo_ok and cto_ok and not found and live_ok and window_ok()) else 3


def cmd_before():
    facts = {d: day_facts(d) for d in DAYS}
    full = g.day_object(FULL_DAY)
    nobj, nver, total = g.gold_totals()
    prefixes, sobj, sver, _ = g.series_counts()
    objs = g.gold_objects()
    parts = {k.split("/")[-2] for k in objs}
    out = {"day_rows": {d: facts[d]["rows"] for d in DAYS}, "day_versions": {d: facts[d]["versions"] for d in DAYS},
           "full_day_rows": g.parquet_rows(full[0]) if full else None, "gold_total_rows": total, "partitions": len(parts),
           "series_prefixes": prefixes, "series_objects": sobj, "series_versions": sver,
           "gold_code_sha256": g.lam_cfg.get_function_configuration(FunctionName=GOLD_FN)["CodeSha256"],
           "publish_code_sha256": g.lam_cfg.get_function_configuration(FunctionName=PUB_FN)["CodeSha256"], "schedules": g.scheds()}
    save("before.json", out)
    save("before_not_measurable.json", {d: facts[d]["not_measurable"] for d in DAYS})
    save("before_day_version_ids.json", {d: facts[d]["version_ids"] for d in DAYS})
    save("before_gold_layout.json", {"gold_objects": nobj, "gold_versions": nver, "per_partition_versions": {k.split("/")[-2]: v for k, v in objs.items()}})
    sil = subprocess.run([sys.executable, "-I", str(ROOT / D / "2.0.0_SA_COO~D2/reads/cot_relanding_state_read.py"), "--out", str(STATE / "silver_counts.json")],
                         capture_output=True, text=True, cwd=str(ROOT), timeout=600)
    print("BEFORE", json.dumps(out, sort_keys=True), "| gold parquet objects %d versions %d (denominator printed)" % (nobj, nver))
    print("BEFORE not_measurable", json.dumps(load("before_not_measurable.json"), sort_keys=True))
    print("BEFORE silver read rc=%d" % sil.returncode, (sil.stdout or sil.stderr).strip().splitlines()[-1][:200] if (sil.stdout or sil.stderr) else "")
    return 0


def cmd_dry():
    if (STATE / "dry.json").exists():
        print("REFUSED: the dry runs are already recorded")
        return 2
    if not window_ok():
        print("STOP: inside the weekday 11:30Z to 14:15Z band")
        return 3
    go0 = g.gold_objects()
    events, problems = {}, []
    for day in DAYS:
        body, rep, fl = g.invoke(GOLD_FN, {"rewrite": {"start": day, "end": day}, "dry_run": True})
        res = (body.get("results") or {}).get(day)
        rows = res.get("rows") if isinstance(res, dict) and isinstance(res.get("rows"), int) else None
        ev = {"ok": body.get("ok"), "days": body.get("days"), "held": body.get("held"), "rows": rows, "report": rep,
              "flags": {k: v for k, v in fl.items() if k in ("timed_out", "access_denied", "function_error")}, "result_shape": g.shape(res) if res is not None else None, "invoked_utc": fl["invoked_utc"]}
        events[day] = ev
        why = []
        if fl["timed_out"] or fl["access_denied"] or fl["function_error"] or (rep["max_memory_mb"] or 0) > 819 or (rep["duration_s"] or 0) > 600:
            why.append("timeout/AccessDenied/error/memory above 819 MB/duration above 600 s")
        if ev["held"] != 0 or ev["days"] != [day] or ev["ok"] is not True or rows is None or not 840 <= rows <= 960:
            why.append("held/days/ok/rows outside 840-960")
        print("DRY %s ok=%s days=%s held=%s rows=%s report=%s -> %s" % (day, ev["ok"], ev["days"], ev["held"], rows, rep, why or "ok"))
        if why:
            problems.append((day, why))
            break  # a STOP line stops the pair
    go1 = g.gold_objects()
    moved = len(go0) != len(go1) or sum(go0.values()) != sum(go1.values())
    rec = {"ok": not problems and len(events) == 8, "days": list(events), "held": sum((e["held"] or 0) for e in events.values()),
           "rows": {d: e["rows"] for d, e in events.items()}, "gold_objects_before": len(go0), "gold_objects_after": len(go1),
           "gold_versions_before": sum(go0.values()), "gold_versions_after": sum(go1.values())}
    save("dry_events.json", {"events": events, "problems": problems})
    print("DRY record=%s moved=%s problems=%s" % (json.dumps(rec, sort_keys=True), moved, problems or "none"))
    if not problems and not moved and len(events) == 8:
        save("dry.json", rec)
        return 0
    return 3


if __name__ == "__main__":
    sys.exit({"gates": cmd_gates, "before": cmd_before, "dry": cmd_dry}[sys.argv[1]]())
