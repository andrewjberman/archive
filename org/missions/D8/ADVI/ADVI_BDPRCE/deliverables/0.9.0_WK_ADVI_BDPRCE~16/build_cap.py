"""Assemble CAP.json for BP-c-4 from the measured per-day counts (counts_all.jsonl, written by count_rows.py).
Read-only: reads this folder's counts_all.jsonl and writes CAP.json only. Stdlib only.
usage: python -I build_cap.py <read_at ISO UTC> <out CAP.json>"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAP_N = 500000
SECOND_WINDOW = ["2026-09-04", "2026-09-11", "2026-09-18", "2026-09-25"]

CALLS = [
    "aws s3 ls s3://opal-data-bd/forwardfill_v2/unrealized/ (tail of listing, read only)",
    "aws s3api list-objects-v2 --bucket opal-data-bd --prefix forwardfill_v2/unrealized/ --query Contents[].[Key,Size,LastModified] --output text (91 keys: 76 UNREALIZED_DAILY, 15 _complete; auto-paginated, counted client-side)",
    "aws s3 cp s3://opal-data-bd/forwardfill_v2/unrealized/UNREALIZED_DAILY_<date>.xlsx C:/dev/wk-bdprce-r3-16-data/ (76 get-object reads, one per daily key)",
    "aws lambda get-function-configuration --function-name bd-49f-runner (Timeout, MemorySize, environment key names and non-secret values only)",
    "python -I count_rows.py <76 downloaded xlsx> (local, streams sheet XML, no write to S3)",
    "python -I openpyxl read_only iter_rows on UNREALIZED_DAILY_2026-10-09.xlsx (local positive control)",
]

PAGING_CONFIG = (
    "infra/aws/lambda/bd-pipeline/bd-49f-runner/lambda_function.py:74-76 BD_REST_TABLES tuple, MAX_RETRIES and "
    "BACKOFF_BASE_S (retry knobs, no row or page limit); "
    "data/cot/scripts/bronze/cot_bronze_ingest.py:76 BD_TXN_CHUNK_DAYS (date tiling, applied to transactions only at :797); "
    ":102-103 STATUS_POLL_INTERVAL_S=5 and STATUS_POLL_TIMEOUT_S=900 (run poll timeout, not a row cap); "
    ":247-248 urlopen(req, timeout=HTTP_TIMEOUT_S) then payload = resp.read() (no size bound); "
    ":147 SNAPSHOT_TABLES includes unrealized (point-in-time snapshot); "
    ":430 the run body pops isAdhoc, isLimitSize and needsIDsForGrouping before v1/run; "
    "data/black_diamond/scripts/bronze/templates/unrealized.json:493 dateRangeType Custom, :497 isLimitSize false "
    "(stored value, removed at cot_bronze_ingest.py:430 before the run); "
    "Lambda bd-49f-runner configuration: Timeout 900, MemorySize 1024, environment keys BD_SNAPSHOT_ASOF_LAG_BDAYS, "
    "BACKOFF_BASE_S, COT_MARKET_HOLIDAYS, MAX_RETRIES, BD_TXN_CHUNK_DAYS (3); none of these is a row, page or size limit. "
    "xlsx sheet capacity is 1048576 rows, so the file format cannot be the limit at 500000. "
    "Searched runner, shared module and template for limit, page, top, maxRows, pageSize, row cap and 500000; "
    "the only limit-named setting is the isLimitSize flag above, and BD's server-side default for it is not readable from the repo."
)

PAGING_PLAN = (
    "Not run. The unrealized export is a point-in-time snapshot (cot_bronze_ingest.py:147), so the date tiling used for "
    "transactions (BD_TXN_CHUNK_DAYS, :797) cannot split it. A complete pull would need one export per slice of the qt4 "
    "template's Relationship ID filter (unrealized.json:79-83, a List-type filter under the portfolio join at :75), with the "
    "slice value set in the run body, each slice's data-row count checked below 500000 with count_rows.py, and the slices "
    "unioned before silver/unrealized is built from forwardfill_v2/unrealized. Whether BD enforces the cap per run or per "
    "account is not established from the repo."
)


def load_counts():
    recs = []
    with open(os.path.join(HERE, "counts_all.jsonl"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    per_day = {}
    for r in recs:
        d = re.search(r"(\d{4}-\d{2}-\d{2})", r["name"]).group(1)
        if d in per_day:
            raise SystemExit("duplicate date %s" % d)
        per_day[d] = int(r["data_rows"])
    return per_day


def main(read_at, out_path):
    per_day = load_counts()
    rows_per_day = {d: per_day[d] for d in sorted(per_day)}
    days_checked = len(rows_per_day)
    n500 = sum(1 for v in rows_per_day.values() if v == CAP_N)
    zero = sum(1 for v in rows_per_day.values() if v == 0)
    nonzero = {d: v for d, v in rows_per_day.items() if v > 0}
    pre = {d: v for d, v in nonzero.items() if v != CAP_N}
    cap_days = sorted(d for d, v in rows_per_day.items() if v == CAP_N)
    second_rows = [per_day[d] for d in SECOND_WINDOW]
    verdict = "CAP" if n500 > 1 else ("NOT_A_CAP" if nonzero else "NOT_DETERMINED")
    evidence = (
        "Of the %d daily keys read (2026-03-27 to 2026-10-09), %d are header-only stubs with 0 data rows and %d hold data; "
        "%d of the non-stub days read exactly %d data rows, on every such day from %s to %s (%s), "
        "while the %d non-stub days before %s vary with the book from %d (%s) to %d (%s). "
        "No setting in the runner, the shared module, the template or the Lambda configuration yields 500000 (paging_config), "
        "so the cap, if any, sits on the Black Diamond side and is inferred from the count pattern, not read from a BD setting; "
        "the 2026-10-09 export opened with openpyxl (read_only) gives 500001 rows including the header, agreeing with the sheet-XML count, "
        "and the xlsx format cannot be the limit at 500000 rows."
    ) % (
        days_checked, zero, len(nonzero), n500, CAP_N, cap_days[0], cap_days[-1],
        ", ".join(d[5:] for d in cap_days),
        len(pre), cap_days[0], min(pre.values()), min(pre, key=pre.get), max(pre.values()), max(pre, key=pre.get),
    )
    rec = {
        "order": "BP-c-4",
        "read_at": read_at,
        "claim": "measured",
        "calls": CALLS,
        "days_checked": days_checked,
        "rows_per_day": rows_per_day,
        "days_at_500000": n500,
        "paging_config": PAGING_CONFIG,
        "second_window": {"dates": SECOND_WINDOW, "rows": second_rows},
        "verdict": verdict,
        "evidence": evidence,
        "paging_plan": PAGING_PLAN if verdict == "CAP" else "n/a",
    }
    text = json.dumps(rec, indent=1, sort_keys=False) + "\n"
    text.encode("ascii")  # refuse non-ASCII output
    with open(out_path, "w", encoding="ascii", newline="\n") as fh:
        fh.write(text)
    print("built %s days=%d at_500000=%d zero=%d nonzero=%d verdict=%s" % (
        out_path, days_checked, n500, zero, len(nonzero), verdict))
    print("cap_days=%s" % ",".join(cap_days))
    print("pre_cap min=%s max=%s n=%d" % (min(pre.values()), max(pre.values()), len(pre)))
    print("second_window=%s" % list(zip(SECOND_WINDOW, second_rows)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_cap.py <read_at ISO UTC> <out CAP.json>")
    main(sys.argv[1], sys.argv[2])
