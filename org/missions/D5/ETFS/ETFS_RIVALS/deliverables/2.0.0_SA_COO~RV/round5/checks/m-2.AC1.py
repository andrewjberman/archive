"""RIV-m-2 AC1 (row W5-S21) -- the Bloomberg collector's capture dedup is LINEAR in the number of captures: a bulk import of 60
captures acquired on one day reads each existing sidecar a bounded number of times, never once per later capture.

A counting `LocalSink` (a sink object passes through `sinks.get_sink`) counts `get()` calls on `*.sidecar.json`. 60 distinct
capture files (60 report dates, one acquisition date) are imported in one batch.
  - sidecar GETs <= 3 x 60 = 180 (today `_existing_by_sha` re-lists and re-reads the partition per capture: ~60*59/2 = 1770);
  - control: re-importing the same 60 files writes no new data object in the sink (run markers under state/ excluded; idempotent across batch ids)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

N = 60


def run(v):
    c.setup_path()
    from rivalfunds import collector_bloomberg as cb
    from rivalfunds import sinks

    class Counting(sinks.LocalSink):
        sidecar_gets = 0

        def get(self, uri):
            if uri.endswith(".sidecar.json"):
                Counting.sidecar_gets += 1
            return super().get(uri)

    tmp = pathlib.Path(c.tmpdir("rv_m2_"))
    days = c.weekdays_ending("2026-09-29", N)
    files = []
    for d in days:  # one acquisition date for all: the `at` is the same day
        f = c.bbg_capture_file(tmp, d)
        txt = pathlib.Path(f).read_text(encoding="utf-8").replace(f'"{d}T23:00:00-04:00"', '"2026-09-30T11:00:00-04:00"')
        pathlib.Path(f).write_text(txt, encoding="utf-8")
        files.append(f)
    s = Counting(str(tmp / "sink"))
    r = cb.handler_entry({"mode": "import", "captures": files, "batch_id": "i1", "sink": s, "date": days[-1]})
    gets = Counting.sidecar_gets
    print(f"import of {N}: status {r.get('status')}, sidecar GETs {gets}")
    v.check(r.get("status") in ("OK", "PARTIAL") and gets <= 3 * N, f"sidecar GETs {gets} <= {3 * N}")
    before = sorted(str(q) for q in (tmp / "sink").rglob("*") if q.is_file() and "state" not in q.parts)
    Counting.sidecar_gets = 0
    r2 = cb.handler_entry({"mode": "import", "captures": files, "batch_id": "i2", "sink": s, "date": days[-1]})
    after = sorted(str(q) for q in (tmp / "sink").rglob("*") if q.is_file() and "state" not in q.parts)
    print(f"re-import: status {r2.get('status')}, objects before {len(before)}, after {len(after)}, sidecar GETs {Counting.sidecar_gets}")
    v.check(len(before) > 0 and after == before, "control: the re-import writes no new object (the dedup still dedups)")

failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
