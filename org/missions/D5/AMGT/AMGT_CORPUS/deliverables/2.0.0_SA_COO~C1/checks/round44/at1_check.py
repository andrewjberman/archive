"""AMGT_CORPUS round 44, CRPS-at-1 (FWD-12, PRD v0.9 ADDENDUM D at PRD:433-456) -- the team-sheet reader. Issuer's file. READ-ONLY
S3 reads of the stored workbooks (bronze research-report objects); nothing written; no library access (the library is site-Z only).

  PYTHONPATH=. python at1_check.py

The build under test is `lib.research.corpus.team_sheet` with:
  rows_for(security_key, client)  -> {"class": "own_new"|"own_model"|"master"|"master_absent", "workbook_key": <s3 key or None>,
                                      "sheet": <"Model NEW VERSION"|"Model"|None>, "rows": [<label>, ...],
                                      "model_rows_beside": [<label>, ...] or None, "reason": <str or None>}
  census(client)                  -> {security_key: rows_for(...)} over the served names (continuation._resolved_security_keys)

The check holds its OWN implementation of the rules (round 40's ap9 instruments, ap9_row_compare.labels_of and
ap9_sheet_census.sheet_counts), so the reader is graded against an independent derivation, not against itself:
  - a sheet CARRIES FIGURES when >= 10 rows have a label in their first 4 cells and two or more numbers (rows 1-400, cols 1-60);
  - a workbook is FIGURE-CARRYING when `Model NEW VERSION` or `Model` carries figures; the team sheet is `Model NEW VERSION` when it
    carries figures, else `Model`;
  - a row's label is the first non-empty string in its first 4 cells, kept when the row has two or more numbers; labels compared after
    whitespace collapse and lower-casing;
  - of two or more figure-carrying workbooks in one name's partition, the one with the newest stored modified date is read (the
    object's `x-amz-meta` source mtime when the ingest stored one, else its S3 LastModified);
  - a name with no figure-carrying workbook takes the master `FactSet Based ONE PAGER TEMPLATE 2026 03 09_v2.xlsx` by the same sheet
    rule; when the store holds no such file the class is `master_absent` with a reason (the round-44 cut found it absent).

Prints per class counts and `at1 build <b>/2 control <c>/1`:
  b1  classes sum to the served names, and EVERY workbook holding both sheets with figures carries a non-empty model_rows_beside
  b2  rows_for(k)["rows"] equals the check's own derivation on every served name with an own workbook (count printed)
  control  a name with an own workbook in the store (BABA_US_Equity) reads own_new/own_model, and a served name with no workbook
           reads master/master_absent
"""
import io
import re
import sys
import types

sys.modules.setdefault("fitz", types.ModuleType("fitz"))

import openpyxl  # noqa: E402

from lib.research.corpus import continuation, extract  # noqa: E402
from lib.research.harvest import store  # noqa: E402

SHEETS = ("Model NEW VERSION", "Model")
MIN_FIGURE_ROWS = 10
MASTER = "FactSet Based ONE PAGER TEMPLATE 2026 03 09_v2.xlsx"


def norm(text):
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def _rows(ws):
    out = []
    for row in ws.iter_rows(min_row=1, max_row=400, max_col=60, values_only=True):
        label = next((v for v in row[:4] if isinstance(v, str) and v.strip()), None)
        nums = sum(1 for v in row if isinstance(v, (int, float)) and not isinstance(v, bool))
        if label is not None and nums >= 2:
            out.append(norm(label))
    return out


def _derive(client, keys):
    """The check's own class and rows for one partition's workbook keys."""
    best = None
    for key in keys:
        head = client.head_object(Bucket=store.HARVEST_BUCKET, Key=key)
        meta = head.get("Metadata") or {}
        stamp = meta.get("source-mtime") or meta.get("mtime") or head["LastModified"].isoformat()
        body = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
        try:
            wb = openpyxl.load_workbook(io.BytesIO(body), read_only=True, data_only=True)
        except Exception:  # noqa: BLE001 -- an unreadable workbook is not figure-carrying
            continue
        try:
            per = {s: _rows(wb[s]) for s in SHEETS if s in wb.sheetnames}
        finally:
            wb.close()
        carrying = {s: r for s, r in per.items() if len(r) >= MIN_FIGURE_ROWS}
        if not carrying:
            continue
        sheet = "Model NEW VERSION" if "Model NEW VERSION" in carrying else "Model"
        both = len(carrying) == 2
        cand = (stamp, key, sheet, carrying[sheet], both)
        if best is None or cand[0] > best[0]:
            best = cand
    return best


def main():
    client = store._default_client()
    prefix = store.table_prefix(extract.SOURCE, "bronze", extract.BRONZE_REQUEST)
    served = continuation._resolved_security_keys(client=client)
    by_part = {}
    for k in extract._list_keys(client, prefix):
        if k.lower().endswith((".xlsx", ".xlsm")):
            by_part.setdefault(k[len(prefix):].split("/")[0].split("=", 1)[-1], []).append(k)
    try:
        from lib.research.corpus import team_sheet
    except ImportError:
        print("at1 team_sheet reader absent (lib.research.corpus.team_sheet not importable)")
        print("at1 served %d names; partitions with a workbook %d" % (len(served), sum(1 for k in served if k in by_part)))
        print("at1 build 0/2 control 0/1")
        return 1
    got = team_sheet.census(client)
    classes = {}
    for k in served:
        c = (got.get(k) or {}).get("class")
        classes[c] = classes.get(c, 0) + 1
    print("at1 classes %s sum %d served %d" % (sorted(classes.items(), key=lambda kv: str(kv[0])), sum(classes.values()), len(served)))
    beside_missing, rows_ok, rows_n = [], 0, 0
    for k in served:
        if k not in by_part:
            continue
        mine = _derive(client, by_part[k])
        g = got.get(k) or {}
        if mine is None:
            continue
        rows_n += 1
        if [norm(r) for r in (g.get("rows") or [])] == mine[3] and g.get("sheet") == mine[2]:
            rows_ok += 1
        else:
            print("ROWS-DIFFER %s sheet %s/%s rows %d/%d" % (k, g.get("sheet"), mine[2], len(g.get("rows") or []), len(mine[3])))
        if mine[4] and not g.get("model_rows_beside"):
            beside_missing.append(k)
    for k in beside_missing:
        print("BESIDE-MISSING %s" % k)
    b1 = int(sum(classes.values()) == len(served) and None not in classes and not beside_missing)
    b2 = int(rows_n > 0 and rows_ok == rows_n)
    print("at1 rows match %d of %d own-workbook names" % (rows_ok, rows_n))
    ctl = 0
    t = got.get("BABA_US_Equity") or {}
    no_wb = next((k for k in served if k not in by_part), None)
    if t.get("class") in ("own_new", "own_model") and no_wb and (got.get(no_wb) or {}).get("class") in ("master", "master_absent"):
        ctl = 1
    print("at1 build %d/2 control %d/1" % (b1 + b2, ctl))
    return 0 if b1 + b2 == 2 and ctl else 1


if __name__ == "__main__":
    sys.exit(main())
