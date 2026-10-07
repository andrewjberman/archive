"""ETFS_RIVALS -- THE MORNING PASS (ROUND_ANALYSIS.round13.md section 3 @8e9364a2d5), one read by 2.0.0_SA_COO~RV after the
07:00 ET vehicle run. READ-ONLY: live S3 through get/list only; writes one JSON beside this file's caller-named out dir.

    python morning_pass.py <worktree root> <page day YYYY-MM-DD> <G4 date YYYY-MM-DD> <out dir>

1. The ADDENDUM 1 census: every (CUSIP/ISIN key, Bloomberg key) pair G4's `security_parsekey` gives, and for each whether the
   page day's holding_contribution and buying_trend carry the Bloomberg key and no longer the identifier key (MERGED), with the
   funds on each side and both names (a merged pair whose names disagree is the failure arm). Nebius (N97284108 ->
   NBIS_US_Equity) is the positive control.
2. `fund_sections` in the served page day's manifest.
3. C-S36's four names: the visible ticker-form strings left on the served page.
4. The PARSEKYABLE_DES points: G4 rows carrying a parsekey, and the pull-enrichment markers' `parsekey_points` / `unreachable`.
A missing input prints as ABSENT with its key; nothing is inferred from an absence."""
from __future__ import annotations

import io
import json
import pathlib
import re
import sys

ROOT, PAGE_DAY, G4_DAY, OUT = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4]).resolve()
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))

import pyarrow.parquet as pq  # noqa: E402

from rivalfunds import enrichment_bloomberg as eb  # noqa: E402
from rivalfunds import homes, revision, sinks  # noqa: E402

S = sinks.S3Sink()
C_S36 = ("8053 JP Equity", "9433 JP Equity", "RBLX US Equity", "000270 KS Equity")


def newest(table: str, day: str):
    us = [u for u in S.list(homes.address("rivalfunds", "etfs", "gold", table, f"date={day}") + "/") if u.endswith(".parquet")]
    if not us:
        return None, None, 0
    u = revision.newest(us)
    return u, pq.read_table(io.BytesIO(S.get(u))).to_pandas(), len(us)


def _nn(v) -> bool:
    return v is not None and not (isinstance(v, float) and v != v) and str(v).strip() != ""


def main() -> int:
    rec: dict = {"page_day": PAGE_DAY, "g4_day": G4_DAY}
    g4u, g4, n4 = newest("security_market", G4_DAY)
    rec["g4"] = {"object": g4u, "objects_at_date": n4, "rows": None if g4 is None else int(len(g4)),
                 "has_parsekey_column": bool(g4 is not None and "security_parsekey" in g4.columns)}
    pairs = {}
    if g4 is not None and "security_parsekey" in g4.columns:
        for sid, pk, nm in zip(g4["security_id"], g4["security_parsekey"], g4.get("security_name", [None] * len(g4))):
            if _nn(pk):
                pairs[str(sid)] = {"parsekey": str(pk), "bloomberg_key": eb.security_key(str(pk)), "g4_name": nm if _nn(nm) else None}
    rec["g4"]["parsekey_rows"] = len(pairs)

    tables = {}
    for t in ("holding_contribution", "buying_trend"):
        u, df, n = newest(t, PAGE_DAY)
        tables[t] = df
        rec[t] = {"object": u, "objects_at_date": n, "rows": None if df is None else int(len(df))}
    census = []
    for k, p in sorted(pairs.items()):
        row = {"identifier_key": k, **p}
        for t, df in tables.items():
            if df is None:
                row[t] = "ABSENT"
                continue
            sec = df[df["axis"] == "security"]
            fund = sec["fund_id"].astype(str)
            b = sec["bucket"].astype(str)
            on_id = sorted(set(fund[b == k]))
            on_bb = sorted(set(fund[b == p["bloomberg_key"]]))
            names_bb = sorted({str(x) for x in sec.loc[b == p["bloomberg_key"], "security_name"] if _nn(x)})
            row[t] = {"funds_on_identifier_key": on_id, "funds_on_bloomberg_key": on_bb, "bloomberg_key_names": names_bb,
                      "state": ("MERGED" if on_bb and not on_id else "SPLIT" if on_id and on_bb else
                                "IDENTIFIER_ONLY" if on_id else "NEITHER")}
        census.append(row)
    rec["census"] = census
    rec["census_counts"] = {t: {s: sum(1 for r in census if isinstance(r.get(t), dict) and r[t]["state"] == s)
                                for s in ("MERGED", "SPLIT", "IDENTIFIER_ONLY", "NEITHER")} for t in tables}
    neb = next((r for r in census if r["identifier_key"] == "N97284108"), None)
    rec["nebius_control"] = neb if neb else "ABSENT: no parsekey row for N97284108 in G4"

    man_u, idx_u = homes.page(PAGE_DAY, "manifest.json"), homes.page(PAGE_DAY, "index.html")
    if S.exists(man_u):
        m = json.loads(S.get(man_u))
        rec["page"] = {k: m.get(k) for k in ("batch_id", "status", "generated_at", "holding_dialogs", "fund_sections",
                                             "funds_updated", "funds_total", "index_bytes", "audit_bytes")}
    else:
        rec["page"] = f"ABSENT: {man_u}"
    if S.exists(idx_u):
        h = S.get(idx_u).decode("utf-8")
        text = re.sub(r"<[^>]+>", "\x00", h)
        rec["c_s36_ticker_form_left"] = {n: text.count(n) for n in C_S36}
        rec["page_audit_hrefs"] = h.count(f'href="/rivalfunds/{PAGE_DAY}/audit"')
    else:
        rec["c_s36_ticker_form_left"] = f"ABSENT: {idx_u}"

    marks = []
    for u in S.list(homes.address("rivalfunds", "etfs", "state", homes.state_table("pull-enrichment"), f"date={G4_DAY}") + "/"):
        try:
            d = json.loads(S.get(u))
        except Exception as e:  # noqa: BLE001
            marks.append({"marker": u.rsplit("/", 1)[-1], "unreadable": type(e).__name__})
            continue
        det = d.get("detail") if isinstance(d.get("detail"), dict) else d
        marks.append({"marker": u.rsplit("/", 1)[-1], "status": d.get("status"),
                      "parsekey_points": det.get("parsekey_points"), "parsekey_failures": det.get("parsekey_failures"),
                      "unreachable": det.get("unreachable"), "session_attempts": det.get("session_attempts")})
    rec["enrichment_markers"] = marks

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"morning_pass_{PAGE_DAY}.json").write_text(json.dumps(rec, indent=2, default=str), encoding="utf-8")
    short = {k: rec[k] for k in ("g4", "census_counts", "page", "c_s36_ticker_form_left", "enrichment_markers")}
    short["nebius_control"] = rec["nebius_control"]
    print(json.dumps(short, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
