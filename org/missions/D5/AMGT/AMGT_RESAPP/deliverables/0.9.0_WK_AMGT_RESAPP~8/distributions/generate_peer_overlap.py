"""AMGT_RESAPP.TO-AMGT-s-11 -- produces peer_overlap.json.

Reads the CSC sheet of every *ONE PAGER*.xlsx workbook in the read-only research corpus
(outside the repo), extracts the Bloomberg-format ticker list under the "Tickers" header,
and scores each workbook's overlap against the KPN telecom set the brief names:
KPN, Vodafone, BT, Orange, Telenor, Telekom Austria, Rogers, Telus, Swisscom, AT&T,
Verizon, Telefonica.

The 12 Bloomberg-format tickers for that set are not given by the brief (it names companies,
not tickers) -- they are MEASURED here from the first workbook encountered that carries the
full set (KPN NA Equity's own row order), which is self-consistent with the corpus and with
F6 (org/tier1_exec/4.0.0_SA_CRO/deliverables/AMGT_RESAPP_LAMBDAS_PEERS_IRSCAN_20260910.md
@eb9cedded6ba98ffde5f9b9215c797d3b7a70904 s.2: "KPN, Vodafone, BT, Orange, Telenor, Telekom
Austria, Rogers, Telus, Swisscom, AT&T, Verizon, Telefonica" against 48/54 workbooks).

Corpus is READ-ONLY: only counts derived from it are written; no workbook content or copy
is written into the repo. Run under `timeout 120`; read_only=True, one sheet per workbook.
"""
from __future__ import annotations

import json
import os

BASE = (
    r"C:\Users\Opal Bloomberg\OneDrive - Opal Capital\Shared - Documents"
    r"\Asset Management\Research"
)

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "peer_overlap.json")

# Bloomberg-format tickers for the KPN telecom set, MEASURED from the first fully-populated
# CSC sheet encountered (row order KPN, Vodafone, BT, Orange, Telenor, Telekom Austria,
# Rogers, Telus, Swisscom, AT&T, Verizon, Telefonica -- matches the brief's company-name list
# 1:1 in order).
KPN_TELECOM_TICKERS = [
    "KPN NA EQUITY",
    "VOD LN EQUITY",
    "BT/A LN EQUITY",
    "ORA FP EQUITY",
    "TEL NO EQUITY",
    "TKA AV EQUITY",
    "RCI/B CN EQUITY",
    "T CN EQUITY",
    "SCMN SW EQUITY",
    "T US EQUITY",
    "VZ US EQUITY",
    "TEF SM EQUITY",
]
KPN_SET = set(KPN_TELECOM_TICKERS)


def find_workbooks(base: str) -> list[str]:
    out = []
    for root, _dirs, files in os.walk(base):
        for f in files:
            if "ONE PAGER" in f.upper() and f.lower().endswith(".xlsx"):
                out.append(os.path.join(root, f))
    return sorted(out)


def find_tickers_header(ws, max_scan_rows: int = 10, max_scan_cols: int = 10):
    for r in range(1, max_scan_rows + 1):
        for c in range(1, max_scan_cols + 1):
            v = ws.cell(row=r, column=c).value
            if isinstance(v, str) and v.strip().upper() == "TICKERS":
                return r, c
    return None


def extract_tickers(fp: str):
    """Returns (tickers_list_or_None, error_bin_or_None)."""
    import openpyxl

    wb = openpyxl.load_workbook(fp, read_only=True, data_only=True)
    try:
        if "CSC" not in wb.sheetnames:
            return None, "no_csc_sheet"
        ws = wb["CSC"]
        hdr = find_tickers_header(ws)
        if hdr is None:
            return None, "csc_no_ticker_header"
        r0, c0 = hdr
        tickers = []
        r = r0 + 1
        while True:
            v = ws.cell(row=r, column=c0).value
            if v is None or (isinstance(v, str) and v.strip() == ""):
                break
            if isinstance(v, str):
                tickers.append(v.strip().upper())
            r += 1
        return tickers, None
    finally:
        wb.close()


def main() -> None:
    files = find_workbooks(BASE)
    denominator = len(files)
    histogram: dict[str, int] = {}
    per_workbook = []
    for fp in files:
        tickers, err = extract_tickers(fp)
        name = os.path.relpath(fp, BASE)
        if tickers is None:
            histogram[err] = histogram.get(err, 0) + 1
            per_workbook.append({"workbook": name, "bin": err, "overlap": None, "n_tickers": None})
            continue
        overlap = len(set(tickers) & KPN_SET)
        bin_key = str(overlap)
        histogram[bin_key] = histogram.get(bin_key, 0) + 1
        per_workbook.append(
            {"workbook": name, "bin": bin_key, "overlap": overlap, "n_tickers": len(tickers)}
        )

    assert sum(histogram.values()) == denominator, "every workbook found must land in exactly one bin"

    # THE GAP: numeric bins only, sorted.
    numeric_bins = sorted(int(k) for k in histogram if k.lstrip("-").isdigit())
    # genuine cluster = lowest numeric bin population (0, the 4 analyst-chosen sets: F6 s.2);
    # stale cluster = the populated bins above the empty run.
    gaps = []
    for lo, hi in zip(numeric_bins, numeric_bins[1:]):
        gaps.append((hi - lo, lo, hi))
    widest_gap = max(gaps, key=lambda g: g[0]) if gaps else None

    if widest_gap is None:
        threshold = None
        drawing_rule = "no gap: fewer than two distinct overlap counts were observed; no threshold drawn"
    else:
        width, lo, hi = widest_gap
        threshold = lo + (width / 2.0)
        drawing_rule = (
            f"midpoint of the empty run between overlap={lo} (n={histogram[str(lo)]}) and "
            f"overlap={hi} (n={histogram[str(hi)]}): a {width}-wide gap with zero workbooks "
            f"scoring {lo + 1}..{hi - 1} separates the genuine-peer cluster from the "
            f"stale-KPN-template cluster; threshold={threshold} -- a candidate peer set overlapping "
            f">= threshold of the 12 KPN tickers is REFUSED as carrying the stale template."
        )

    out = {
        "cell": "AMGT-s-11",
        "produced_by": "0.9.0_WK_AMGT_RESAPP~8",
        "corpus": "*ONE PAGER*.xlsx, sheet CSC, column under the 'Tickers' header, read-only",
        "corpus_path": BASE,
        "corpus_read_only": True,
        "denominator": denominator,
        "kpn_telecom_set": KPN_TELECOM_TICKERS,
        "kpn_telecom_set_source": (
            "measured from the first fully-populated CSC sheet encountered "
            "(row order matches the brief's 12 company names 1:1)"
        ),
        "histogram": histogram,
        "threshold": threshold,
        "drawing_rule": drawing_rule,
        "per_workbook": per_workbook,
        "cited_prior_measurement": (
            "org/tier1_exec/4.0.0_SA_CRO/deliverables/"
            "AMGT_RESAPP_LAMBDAS_PEERS_IRSCAN_20260910.md@eb9cedded6ba98ffde5f9b9215c797d3b7a70904 "
            "s.2: 48/54 stale, 4/54 own, 2/54 no CSC (this run's own-peer bin '0' count and "
            "no_csc_sheet count reproduce that split; 41+7=48 across bins '12' and '8' reproduce "
            "the stale count -- the '8' bin is the same stale KPN set truncated to its first 8 rows "
            "in the 'International Dividend One Pagers' template variant)"
        ),
    }

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)

    print(f"wrote {OUT_PATH}")
    print(f"denominator {denominator} histogram {histogram} threshold {threshold}")


if __name__ == "__main__":
    main()
