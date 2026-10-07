"""TO-DB-b-41: the local release run of the reporting-gold handler (`--local`, ONE trading day, the first 20 accounts of the sample).

Usage (from the worktree root):
  python <this file> run before <day> <outdir>   the round-25 handler (git show 5ffd7b740d:<handler>) AND that commit's declaration
  python <this file> run after  <day> <outdir>   the handler and the declaration at this branch, with --class-out and --lots-out-dir
  python <this file> build <day> <before_dir> <after_dir> <out.json>

Reads S3 only; writes local files only. `run` records its wall time and peak working set beside its outputs (stats.json).
The 20 accounts are the first 20 of the 100-account sample whose record is deliverables/0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json
(the sample every later round graded: the round-23 draw, 91 graded accounts, carried through round 24).
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
SOURCES_REL = "data/assets/scripts/gold/irpt_reporting/sources.json"
BEFORE_PIN = "5ffd7b740d"
SAMPLE_RECORD = ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json"
N_ACCOUNTS = 20
TABLES = ("account_activity_daily", "account_lot_realized", "account_lot_unrealized_daily")


def accounts():
    return json.loads(SAMPLE_RECORD.read_text(encoding="utf-8"))["accounts"][:N_ACCOUNTS]


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_show(rel):
    return subprocess.run(["git", "show", "%s:%s" % (BEFORE_PIN, rel)], cwd=str(ROOT), capture_output=True, check=True).stdout


def run(side, day, outdir):
    import psutil
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    if side == "before":
        # the round-25 handler placed so that its own _ROOT (five levels up) is this worktree; its declaration is that commit's
        shim = ROOT / ".scratch" / "before" / "w" / "x" / "y"
        shim.mkdir(parents=True, exist_ok=True)
        (shim / "handler.py").write_bytes(git_show(HANDLER_REL))
        decl = ROOT / ".scratch" / "before" / "sources_5ffd7b740d.json"
        decl.write_bytes(git_show(SOURCES_REL))
        spec = importlib.util.spec_from_file_location("handler_before", str(shim / "handler.py"))
        h = importlib.util.module_from_spec(spec)
        sys.modules["handler_before"] = h
        spec.loader.exec_module(h)
        orig = h.ard.load_declaration
        h.ard.load_declaration = lambda path=decl: orig(path)
        h.local(day, out / "returns.parquet", accounts=accounts(), class_out=str(out / "class.parquet"))
    else:
        sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))
        import handler as h
        h.local(day, out / "returns.parquet", accounts=accounts(), class_out=str(out / "class.parquet"), lots_out_dir=str(out))
    mem = psutil.Process().memory_info()
    stats = {"side": side, "wall_seconds": round(time.time() - t0, 1), "peak_working_set_mb": round(mem.peak_wset / 2**20, 1)}
    (out / "stats.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
    print(json.dumps(stats))


def build(day, before, after, out_json):
    import pandas as pd
    sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
    import account_activity_lots as aal
    b, a = Path(before), Path(after)
    rows = {"account_return_daily_before": len(pd.read_parquet(b / "returns.parquet")),
            "account_return_daily_after": len(pd.read_parquet(a / "returns.parquet")),
            "account_class_daily_before": len(pd.read_parquet(b / "class.parquet")),
            "account_class_daily_after": len(pd.read_parquet(a / "class.parquet"))}
    pk = {}
    for t in TABLES:
        frame = pd.read_parquet(a / ("%s.parquet" % t))
        key = list(aal.PRIMARY_KEYS[t])
        dup = int(frame.duplicated(subset=key).sum())
        rows[t] = int(len(frame))
        pk[t] = {"primary_key": key, "rows": int(len(frame)), "distinct_keys": int(len(frame) - dup), "duplicate_keys": dup,
                 "unique": dup == 0,
                 "coverage_census": {k: int(v) for k, v in frame["coverage"].value_counts().sort_index().items()}}
        if "basis_source" in frame.columns:
            pk[t]["basis_source_census"] = {k: int(v) for k, v in frame["basis_source"].value_counts().sort_index().items()}
    sb = json.loads((b / "stats.json").read_text(encoding="utf-8"))
    sa = json.loads((a / "stats.json").read_text(encoding="utf-8"))
    rec = {
        "task_order": "IRPT_DASHBD.TO-DB-b-41", "worker": "0.9.0_WK_IRPT_DASHBD~23", "day": day, "accounts_requested": N_ACCOUNTS,
        "accounts_source": "the first %d of the `accounts` list in %s" % (N_ACCOUNTS, SAMPLE_RECORD.relative_to(ROOT).as_posix()),
        "before_side": {"handler": "git show %s:%s" % (BEFORE_PIN, HANDLER_REL), "sources_json": "git show %s:%s" % (BEFORE_PIN, SOURCES_REL)},
        "after_side": {"handler": "the extended handler at this branch", "sources_json": "the declaration at this branch (lot_source added)"},
        "returns_sha256_before": sha256_of(b / "returns.parquet"),
        "returns_sha256_after": sha256_of(a / "returns.parquet"),
        "class_sha256_before": sha256_of(b / "class.parquet"),
        "class_sha256_after": sha256_of(a / "class.parquet"),
        "rows": rows, "primary_key_uniqueness": pk,
        "wall_seconds": {"before": sb["wall_seconds"], "after": sa["wall_seconds"]},
        "peak_working_set_mb": {"before": sb["peak_working_set_mb"], "after": sa["peak_working_set_mb"]},
        "lots_parquet_sha256": {t: sha256_of(a / ("%s.parquet" % t)) for t in TABLES},
    }
    rec["returns_byte_identical"] = rec["returns_sha256_before"] == rec["returns_sha256_after"]
    rec["class_byte_identical"] = rec["class_sha256_before"] == rec["class_sha256_after"]
    Path(out_json).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("returns identical=%s class identical=%s pk unique=%s rows=%s" % (
        rec["returns_byte_identical"], rec["class_byte_identical"], {t: pk[t]["unique"] for t in TABLES}, {t: rows[t] for t in TABLES}))


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "build":
        build(*sys.argv[2:6])
    else:
        raise SystemExit("usage: run before|after <day> <outdir> | build <day> <before> <after> <out.json>")
